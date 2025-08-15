from cli import ask

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

url = ask()
TXT_PATH = "data/offers/offers.txt"

def append_to_txt(data):
    """Append one offer’s data to the text file."""
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(f"URL: {data['url']}\n")
        f.write(f"Name of a company \n{data['name']}\n")
        f.write(f"Salary \n{data['salary']}\n")
        f.write(f"About the project:\n{data['about_project']}\n\n")
        f.write(f"Your responsibilities:\n{data['responsibilities']}\n\n")
        f.write(f"Our requirements:\n{data['requirements']}\n\n")
        f.write(f"Technologies we use:\n{data['technologies']}\n")
        f.write("-" * 40 + "\n")

# --- OPTIONS ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

def dismiss_overlays():
    """Try to accept/close cookie banners and overlays."""
    # 1) Common Polish/EN cookie buttons
    xpath_buttons = [
        "//button[contains(., 'Akceptuj')]",
        "//button[contains(., 'Zgadzam')]",    # „Zgadzam się”
        "//button[contains(., 'Accept')]",
        "//button[contains(., 'I agree')]",
        "//button[contains(., 'OK')]",
        "//a[contains(., 'Akceptuj')]",
    ]
    for xp in xpath_buttons:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
            btn.click()
            return
        except TimeoutException:
            pass
        except ElementClickInterceptedException:
            # try JS click if something still overlaps
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xp))
                return
            except Exception:
                pass

    # 2) If still visible, hide typical cookie containers by class prefix (like cookies_* on pracuj.pl)
    try:
        cookie_el = driver.find_element(By.XPATH, "//*[starts-with(@class,'cookies_')]")
        driver.execute_script("arguments[0].style.display='none';", cookie_el)
    except Exception:
        pass


def collect_offer_links():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.tiles_cnb3rfy.core_n194fgoq")))
    anchors = driver.find_elements(By.CSS_SELECTOR, "a.tiles_cnb3rfy.core_n194fgoq")
    hrefs = []
    for a in anchors:
        href = a.get_attribute("href")
        if href:
            hrefs.append(href)
    seen, uniq = set(), []
    for h in hrefs:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    print(f"Collected {len(uniq)} unique offer links")
    return uniq

def click_first_offer(offers):
    if not offers:
        print("No offers to click.")
        return
    el = offers[0]

    try:
        # Ensure it is clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class,'tiles_cnb3rfy') and contains(@class,'core_n194fgoq')])[1]")))
        el.click()
    except ElementClickInterceptedException:
        # Likely cookie/overlay—dismiss and retry
        dismiss_overlays()
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            el.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            # Final fallback: JS click
            driver.execute_script("arguments[0].click();", el)



def extract_offer_sections():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "section")))
    sections = driver.find_elements(By.TAG_NAME, "section")

    heading_map = {
        "about_project": {"About the project", "O projekcie"},
        "responsibilities": {"Your responsibilities", "Twój zakres obowiązków"},
        "requirements": {"Our requirements", "Nasze wymagania"},
        "technologies": {"Technologies we use", "Technologie, których używamy"},
    }

    data = {
        "url": driver.current_url,
        "name": driver.find_element(By.CLASS_NAME, 'oheatec').text,
        "salary": driver.find_element(By.CLASS_NAME, 's120d0xa').text,
        "about_project": "(not found)",
        "responsibilities": "(not found)",
        "requirements": "(not found)",
        "technologies": "(not found)",
    }
# vuj7wmi
# s120d0xa

    for section in sections:
        heading = ""
        try:
            # Try h2 first, fallback to h3
            try:
                heading = section.find_element(By.TAG_NAME, "h2").text.strip()
            except:
                heading = section.find_element(By.TAG_NAME, "h3").text.strip()
        except:
            continue

        for key, titles in heading_map.items():
            if heading in titles:
                try:
                    body = section.text.strip()
                    data[key] = body
                except Exception:
                    data[key] = "(no content)"
                break
    return data




if __name__ == '__main__':
    # clear file before starting
    open(TXT_PATH, "w", encoding="utf-8").close()

    driver.get(url)
    dismiss_overlays()   
    

    links = collect_offer_links()
    if not links:
        print("No offers found.")
    else:
        print("Scraping offers...")

    listing_handle = driver.current_window_handle


    for i, href in enumerate(links, start=1):
        try:
            driver.switch_to.new_window("tab")
            driver.get(href)
            dismiss_overlays()

            row = extract_offer_sections()
            append_to_txt(row)
            print(f"[{i}/{len(links)}] Saved to text: {row['url']}")
        except Exception as e:
            print(f"[{i}/{len(links)}] Failed for {href}: {e}")
        finally:
            try:
                driver.close()
                driver.switch_to.window(listing_handle)
            except Exception:
                try:
                    driver.switch_to.window(driver.window_handles[0])
                except Exception:
                    pass

    print(f"Done. All offers saved at: {TXT_PATH}")


    # # Now we are inside the offer page → extract sections
    # job_data = extract_offer_sections()
    # for k, v in job_data.items():
    #     print(f"\n--- {k} ---\n{v}\n")