from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

import os

import shutil

import time

import re

 

# Set Chrome options 

download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "APRIL_MAY")

os.makedirs(download_dir, exist_ok=True)


# Load credentials from .env file
load_dotenv()

KRA_USERNAME = os.getenv("KRA_USERNAME")
KRA_PASSWORD = os.getenv("KRA_PASSWORD")




 

options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument("--start-maximized")

options.add_argument("--disable-popup-blocking")

options.add_experimental_option("prefs", {

    "download.default_directory": download_dir,

    "plugins.always_open_pdf_externally": True,

    "download.prompt_for_download": False

})

 

driver = webdriver.Chrome(options=options)

 

#  Start session 

driver.get("https://etims.kra.go.ke/app/ebm/indexMain")

 

# --------- Login ---------

driver.find_element(By.NAME, "mbrId").send_keys(KRA_USERNAME)
driver.find_element(By.NAME, "mbrPwd").send_keys(KRA_PASSWORD)

driver.find_element(By.ID, "loginBtn").click()

 

try:

    WebDriverWait(driver, 15).until(lambda d: "indexLogin" not in d.current_url)

 

    driver.get("https://etims.kra.go.ke/app/ebm/trns/sales/indexTrnsSalesInvoice")

 

    input("⏸ Select date range, click 'Search', wait for table, then press ENTER to continue...")

 

    table_xpath = '//*[@id="trnsSalesInvoiceListDiv"]/div/div/table'

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

 

    #  Get total pages 

    sum_text = driver.find_element(By.CSS_SELECTOR, "div.sum").text

    match = re.search(r"Total page\s*:\s*(\d+)", sum_text)

    total_pages = int(match.group(1)) if match else 1

    print(f"🔢 Total pages detected: {total_pages}")

 

        # Custom start page and file count
    start_page = int(input("Enter the page number to resume from (e.g. 1): "))
    # Detect the highest file number in the folder
    existing_files = [f for f in os.listdir(download_dir) if re.match(r"Invoice_(\d{3})\.pdf", f)]
    existing_numbers = [int(re.search(r"Invoice_(\d{3})\.pdf", f).group(1)) for f in existing_files]
    file_counter = max(existing_numbers) + 1 if existing_numbers else 1

    print(f" Resuming invoice numbering from: {file_counter:03d}")

    # Loop through all pages 
    for page in range(start_page, total_pages + 1):
        print(f"\n Processing Page {page} of {total_pages}")
        driver.execute_script(f"trnsSalesInvoiceList.setPage('{page}')")
        time.sleep(3)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        rows = driver.find_elements(By.XPATH, f"{table_xpath}//tbody/tr")

        for row_index, row in enumerate(rows):
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    receipt_cell = cells[1]
                    driver.execute_script("arguments[0].scrollIntoView();", receipt_cell)
                    receipt_cell.click()

                    receipt_popup_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "trnsSalesReceipt_D_B_PDF"))
                    )
                    receipt_popup_link.click()

                    # Wait for file to download
                    download_wait_time = 10
                    file_found = False
                    for _ in range(download_wait_time):
                        time.sleep(1)
                        files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
                        if files:
                            latest_file = max([os.path.join(download_dir, f) for f in files], key=os.path.getctime)
                            if not latest_file.endswith(".crdownload"):
                                file_found = True
                                break

                    if file_found:
                        new_name = f"Invoice_{file_counter:03d}.pdf"
                        new_path = os.path.join(download_dir, new_name)
                        shutil.move(latest_file, new_path)
                        print(f"✓ Saved as {new_name}")
                        file_counter += 1
                    else:
                        print(f" File not downloaded for row {row_index + 1}")

                    close_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "popupReceipt_B_close"))
                    )
                    close_button.click()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, table_xpath))
                    )

            except Exception as e:
                print(f" Error at page {page}, row {row_index + 1}: {e}")
                continue


 

except Exception as e:

    print(" General error:", e)

 

input("ress ENTER to exit...")

driver.quit()
