import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------- Google Sheets setup ----------
SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
client = gspread.authorize(CREDS)

# Open sheet by name
sheet = client.open("JobScout").sheet1
# Ensure headers exist (and add Raw URL for dedupe)
HEADERS = ["Status", "Job Name", "Company Name", "Salary",
           "About Project", "Responsibilities", "Requirements",
           "Technologies", "Link"]

try:
    existing_headers = sheet.row_values(1)
    if existing_headers != HEADERS:
        # Overwrite headers if empty or different
        sheet.clear()
        sheet.append_row(HEADERS, value_input_option="USER_ENTERED")
except Exception:
    # If anything odd, ensure headers exist
    sheet.clear()
    sheet.append_row(HEADERS, value_input_option="USER_ENTERED")

# turn off wrapping (clip) for all data columns
sheet.format('A:I', {'wrapStrategy': 'CLIP'})
# optional: set a filter and freeze header for nicer UX
try:
    sheet.freeze(rows=1)
    sheet.set_basic_filter()  # applies to used range
except Exception:
    pass

def set_row_height(sheet, start_row, end_row, height=200):
    sheet.spreadsheet.batch_update({
        "requests": [{
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet._properties['sheetId'],
                    "dimension": "ROWS",
                    "startIndex": start_row - 1,  # 0-based index
                    "endIndex": end_row           # end is exclusive
                },
                "properties": {
                    "pixelSize": height
                },
                "fields": "pixelSize"
            }
        }]
    })

# Example: set row height for first 100 rows to 35 px
  # row 1 is header, so start from row 2




def append_to_gsheet(data):
    set_row_height(sheet, 2, 101, 35)
    sheet.append_row([
        "",  # Status - for you to fill later
        data["name"],
        data["company_name"],
        data["salary"],
        data["about_project"],
        data["responsibilities"],
        data["requirements"],
        data["technologies"],
        f'=HYPERLINK("{data["url"]}"; "Open Offer")'
    ], value_input_option="USER_ENTERED")




TXT_PATH = "data/offers/offers.txt"

def append_to_txt(data):

    with open(TXT_PATH, "r", encoding="utf-8") as f:
         if data["url"] in f.read():
            print(f"Skipping (already in file): {data['url']}")
            return

    """Append one offer’s data to the text file."""
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(f"URL: {data['url']}\n")
        f.write(f"Job Name \n{data['name']}\n")
        f.write(f"Company name \n{data['company_name']}\n")
        f.write(f"Salary \n{data['salary']}\n")
        f.write(f"About the project:\n{data['about_project']}\n\n")
        f.write(f"Your responsibilities:\n{data['responsibilities']}\n\n")
        f.write(f"Our requirements:\n{data['requirements']}\n\n")
        f.write(f"Technologies we use:\n{data['technologies']}\n")
        f.write("-" * 40 + "\n\n\n")