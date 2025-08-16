# JOB‑SCOUT

A CLI-driven web scraper that collects job offers based on your answers, then saves the results to **Google Sheets** and a local **text file**. It uses Selenium to drive Chromium, handles common cookie overlays, and parses key sections of each offer (role, company, salary, responsibilities, requirements, technologies, etc.).

## ✨ Features
- **Interactive CLI** (Typer + InquirerPy) to capture user preferences (location, distance, remote type, contract, workload, etc.).
- **Smart URL builder** converts answers into a search URL (via `answers.process_answers()`).
- **Selenium + Chromium** automation with overlay/cookie dismissal helpers.
- **Offer parsing**: grabs title, company, salary, and content sections (About project, Responsibilities, Requirements, Technologies).
- **De-duplicated links** on listings before visiting each offer.
- **Outputs** to:
  - `data/offers/offers.txt`
  - Google Sheet (via Service Account)
- **MIT licensed**

## 🧰 Tech Stack
- Python 3.11+
- [Typer](https://typer.tiangolo.com/) & [InquirerPy](https://github.com/kazhala/InquirerPy) for CLI
- [Selenium](https://www.selenium.dev/) (Chromium/Chrome)
- [gspread](https://github.com/burnash/gspread) + `oauth2client` for Google Sheets
- Standard libs: `csv`, `re`, etc.

## 📦 Project Structure
```
JOB-SCOUT/
├─ .venv/
├─ data/
│  └─ offers/
│     └─ offers.txt
├─ spec/
├─ src/
│  ├─ __pycache__/
│  ├─ answers.py
│  ├─ app.py
│  ├─ cli.py
│  ├─ save_to_gsheet_txt.py
│  └─ take_spec.py
├─ tests/
│  └─ test_parsers.py
├─ .gitignore
└─ service_account.json
```
# How JOB‑SCOUT Works

```mermaid
flowchart TD
    A[User runs <code>python src/app.py</code>] --> B[CLI asks questions<br/>(cli.py + InquirerPy)]
    B --> C[Build search URL<br/>(answers.process_answers)]
    C --> D[Launch Chromium via Selenium]
    D --> E[Open listing page<br/>+ dismiss cookie overlays]
    E --> F[collect_offer_links()<br/>de-duplicate URLs]
    F --> G{For each offer URL}
    G -->|Open new tab| H[extract_offer_sections():<br/>title, company, salary,<br/>about, responsibilities,<br/>requirements, technologies]
    H --> I[append_to_txt()]
    H --> J[append_to_gsheet()]
    I --> K[Close tab and return to listing]
    J --> K
    K --> L{More offers?}
    L -->|Yes| G
    L -->|No| M[Print summary & close browser]
```

## 🚀 Quick Start

### 1) Clone & create virtual env
```bash
git clone https://github.com/rdhxb/JOB-SCOUT.git
cd JOB-SCOUT

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
Create (or update) `requirements.txt` with the following packages, then install:
```txt
typer
InquirerPy
selenium
gspread
oauth2client
```
```bash
pip install -r requirements.txt
```

> You also need **Chromium/Chrome** installed and a compatible **ChromeDriver** available in your PATH (or managed by Selenium Manager on recent Selenium versions).

### 3) Configure Google Sheets access
This project uses a **Service Account**.
1. Create a GCP project and enable **Google Sheets API**.
2. Create a **Service Account** and download the JSON credentials as `service_account.json` in the repo root (as shown above).
3. Share your target Google Sheet with the **service account email** (Editor access).
4. In `save_to_gsheet_txt.py`, make sure the code opens the right spreadsheet & worksheet.

> If you don’t want Google Sheets, the scraper still writes to `data/offers/offers.txt`.

### 4) Run the app
```bash
python src/app.py
```
- The CLI (from `cli.py`) will ask questions.
- Chromium opens with the built URL (from `answers.process_answers()`).
- The scraper collects listing links, enters each offer, extracts sections, and saves results to TXT + Google Sheet.

## 📘 Usage Flow (High-level)
1. `cli.ask()` → interactively collect preferences.
2. `answers.process_answers()` → build a search URL for the jobs portal.
3. Launch Chromium via Selenium, handle cookie overlays (`dismiss_overlays()`).
4. `collect_offer_links()` → scrape and de-duplicate listing links.
5. For each offer:
   - Open in a new tab.
   - Extract: title, company, salary, and section content (`extract_offer_sections()`).
   - Persist with `append_to_txt()` and `append_to_gsheet()`.
6. Close tabs and finish.

## 🗂️ Output
- **Text file:** `data/offers/offers.txt`
- **Google Sheets:** one row per offer; columns typically include:
  - `url`, `name`, `company_name`, `salary`, `about_project`, `responsibilities`, `requirements`, `technologies`

## ⚙️ Configuration
- **Browser**: The code uses `Options()` with
  - `--start-maximized`
  - `detach=True` (keeps the browser open at end)
- **Timeouts**: `WebDriverWait(driver, 15)` by default
- **Overlay handling**: Attempts to click common cookie buttons, then hides cookie containers as a fallback.

## 🧪 Tests
Basic parser tests live in `tests/test_parsers.py`. Run with:
```bash
pytest -q
```
(Add `pytest` to your dev dependencies if you plan to run tests.)

## 🛡️ Troubleshooting
- **No offers found**: UI classes on the target website may have changed. Update CSS selectors in `collect_offer_links()` and headings in `extract_offer_sections()`.
- **Click intercepted / overlays**: `dismiss_overlays()` handles common cases; expand XPaths/CSS if the portal changes banners.
- **Google Sheets errors**: Confirm the service account has access and the sheet/worksheet names match your code.
- **ChromeDriver mismatch**: Ensure the installed Chrome/Chromium version matches the driver Selenium is using (or upgrade Selenium to use Selenium Manager).

## 🗺️ Roadmap (ideas)
- Add support for multiple job portals.
- Export CSV/JSON.
- Retry & backoff logic for transient failures.
- Proxy / headless mode toggles via CLI flags.
- Containerize with Docker for consistent runtime.
- CI for tests + linting.

## 📄 License
MIT © 2025
