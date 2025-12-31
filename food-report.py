import os
import re
import csv
import time
import base64
import logging
import requests
import pickle
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.binary_location = "/usr/bin/chromium-browser"

service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# URL to navigate to
url = "https://www.supplynote.in/signin"

# 🔽 Download path
download_dir = r"C:\Users\Admin\Desktop\generated report dowload"

# TIMEOUT = 10  # seconds

# # Gmail + Sheets
# SCOPES = [
#     'https://www.googleapis.com/auth/gmail.modify',
#     'https://www.googleapis.com/auth/spreadsheets'
# ]
# SPREADSHEET_ID = "1l26ci6HF4cL5J_x_iUBqIBQ9DAwYKFzUhJOl_L-xr9o"
# SPREADSHEET_IDV2 = "1BWZJwZHR8wBLGiDGS_r7wbSU7zA8TFFNgUHpuasj9qc"
# SHEET_NAME = "Daily Inventory"
# SUBJECT_PHRASE = "Daily Report Current Stock Report_Kytchens"
# DOWNLOAD_FOLDER = "./downloads"

# # Email check settings
# CHECK_INTERVAL = 5   # seconds between checks
# MAX_WAIT_TIME = 30   # total seconds to wait

# # --------------------- LOGGER SETUP --------------------- #
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# Create folder if not exists
os.makedirs(download_dir, exist_ok=True)

# 🔽 Chrome options
chrome_options = Options()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

chrome_options.add_experimental_option("prefs", prefs)

# Wait for the username field and enter credentials
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
).send_keys("hyprkytchen")

# Wait for the password field and enter credentials
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password" i]'))
).send_keys("hyprkytchen@65")

# Wait for the login button and click it
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button.login-btn-correct.round-corner-login-btn"))
).click()

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'low-shadow-card') and contains(., 'Reports')]"))
).click()

#Type Report Name Here
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//h4[text()='Food Cost Report V2']"))
).click()

time.sleep(1)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH,
        "//iframe[contains(@src,'sn-ims-v2-angular.web.app/home/report')]"
    ))
)
driver.switch_to.frame(driver.find_element(
    By.XPATH,
    "//iframe[contains(@src,'sn-ims-v2-angular.web.app/home/report')]"
))

# Open Location multiselect
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'p-multiselect')]"
    ))
).click()

# Click Select All checkbox
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH,
        "//div[contains(@class,'p-multiselect-panel')]"
        "//div[contains(@class,'p-multiselect-header')]"
        "//div[contains(@class,'p-checkbox-box')]"
    ))
).click()

#Clicking again to close location multiselect
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class,'p-multiselect')]"
    ))
).click()

#For Calender 1
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.TAG_NAME, "p-calendar"))
)

calendar_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'p-datepicker-trigger')]"
    ))
)
driver.execute_script("arguments[0].click();", calendar_button)

# Set yesterday
yesterday = datetime.now() - timedelta(days=1)
day_to_select = str(yesterday.day)   # "15"

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//td[not(contains(@class,'p-datepicker-other-month'))]"
        f"//span[text()='{day_to_select}']"
    ))
).click()

time.sleep(0.5)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.TAG_NAME, "p-calendar"))
)

calendar_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'p-datepicker-trigger')]"
    ))
)
driver.execute_script("arguments[0].click();", calendar_button)

time.sleep(0.5)
# ---------- SET TIME : 07:59 AM ----------

# Wait for time picker
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, "//div[contains(@class,'p-timepicker')]"
    ))
)

# Hour down arrow (reduce hour)
hour_down = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//div[contains(@class,'p-timepicker')]//button)[2]"
    ))
)

# Hour value
hour_value = driver.find_element(
    By.XPATH, "(//div[contains(@class,'p-timepicker')]//span)[1]"
)

# Set hour to 07
while hour_value.text.strip() != "07":
    hour_down.click()

time.sleep(0.5)

minute_down = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//div[contains(@class,'p-timepicker')]//button)[4]"
    ))
)

# Minute value
minute_value = driver.find_element(
    By.XPATH, "(//div[contains(@class,'p-timepicker')]//span)[2]"
)

# Set minute to 59 (wrap-around)
if minute_value.text.strip() != "59":
    minute_down.click()

# AM/PM toggle
ampm_toggle = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//div[contains(@class,'p-timepicker')]//button)[5]"
    ))
)

ampm_value = driver.find_element(
    By.XPATH, "(//div[contains(@class,'p-timepicker')]//span)[3]"
)

# Ensure AM
if ampm_value.text.strip() != "AM":
    ampm_toggle.click()


time.sleep(0.5)

yesterday = datetime.now() - timedelta(days=1)
day_to_select = str(yesterday.day)   # "15"

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//td[not(contains(@class,'p-datepicker-other-month'))]"
        f"//span[text()='{day_to_select}']"
    ))
).click()

time.sleep(0.5)

# ---------- CALENDAR 2 ----------
#Open Calender2
calendar2_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//button[contains(@class,'p-datepicker-trigger')])[2]"
    ))
)
driver.execute_script("arguments[0].click();", calendar2_button)

time.sleep(0.5)
#Set Date
today = datetime.now()
today_day = str(today.day)

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//td[not(contains(@class,'p-datepicker-other-month'))]"
        f"//span[text()='{today_day}']"
    ))
).click()

time.sleep(0.5)

#Open Calender2
calendar2_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//button[contains(@class,'p-datepicker-trigger')])[2]"
    ))
)
driver.execute_script("arguments[0].click();", calendar2_button)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, "//div[contains(@class,'p-timepicker')]"
    ))
)

hour_down = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//div[contains(@class,'p-timepicker')]//button)[2]"
    ))
)

hour_value = driver.find_element(
    By.XPATH, "(//div[contains(@class,'p-timepicker')]//span)[1]"
)

while hour_value.text.strip() != "08":
    hour_down.click()

time.sleep(0.5)

MINUTE_SPAN = "(//div[contains(@class,'p-minute-picker')]//span)[1]"
MINUTE_UP = "(//div[contains(@class,'p-minute-picker')]//button)[1]"
MINUTE_DOWN = "(//div[contains(@class,'p-minute-picker')]//button)[2]"

wait = WebDriverWait(driver, 10)

def get_minute():
    minute_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, MINUTE_SPAN))
    ).text.strip()
    return int(minute_text)   # "00" -> 0, "01" -> 1

current_minute = get_minute()

# Safety guard
MAX_CLICKS = 60
click_count = 0

if current_minute == 0:
    print("Minute already set to 00")

elif current_minute <= 30:
    # Click DOWN until 00
    while click_count < MAX_CLICKS:
        current_minute = get_minute()
        if current_minute == 0:
            break

        wait.until(
            EC.element_to_be_clickable((By.XPATH, MINUTE_DOWN))
        ).click()

        click_count += 1
        time.sleep(0.1)

elif current_minute > 30:
    # Click UP until 00
    while click_count < MAX_CLICKS:
        current_minute = get_minute()
        if current_minute == 0:
            break

        wait.until(
            EC.element_to_be_clickable((By.XPATH, MINUTE_UP))
        ).click()

        click_count += 1
        time.sleep(0.1)

# Final validation
final_minute = get_minute()
if final_minute != 0:
    raise Exception(f"Minute did not settle at 00, stopped at {final_minute}")


ampm_toggle = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "(//div[contains(@class,'p-timepicker')]//button)[5]"
    ))
)

ampm_value = driver.find_element(
    By.XPATH, "(//div[contains(@class,'p-timepicker')]//span)[3]"
)

if ampm_value.text.strip() != "AM":
    ampm_toggle.click()

#Set Date
today = datetime.now()
today_day = str(today.day)

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//td[not(contains(@class,'p-datepicker-other-month'))]"
        f"//span[text()='{today_day}']"
    ))
).click()

time.sleep(0.5)

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[normalize-space()='Generate Report']]"
    ))
).click()

time.sleep(3)

driver.switch_to.default_content()

#Click on Reports
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,"//button[contains(@class, 'low-shadow-card') and contains(., 'Reports')]"
    ))
).click()

time.sleep(0.5)

#Click on CSR
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.XPATH,"//h4[text()='Current Stock Report']"
    ))
).click()

time.sleep(0.5)

#Click on Mail
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,"//span[text()='Mail']"
    ))
).click()

time.sleep(0.5)

# ------------------ SELECT ALL ------------------ #
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,"//md-checkbox[@aria-label='Select All']"
    ))
).click()

time.sleep(0.5)

# ------------------ SEND MAIL ------------------ #
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,"//span[@class='ng-scope' and contains(text(), 'Send')]"
    ))
).click()

time.sleep(0.5)

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((
        By.XPATH,"//div[contains(@class,'sa-confirm-button-container')]//button[contains(@class,'confirm') and normalize-space()='OK']"
    ))
).click()

time.sleep(0.5)

#Click on Reports

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'low-shadow-card') and contains(., 'Reports')]"))
).click()

#Click Food Cost Report V2
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//h4[text()='Food Cost Report V2']"))
).click()

time.sleep(1)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH,
        "//iframe[contains(@src,'sn-ims-v2-angular.web.app/home/report')]"
    ))
)
driver.switch_to.frame(driver.find_element(
    By.XPATH,
    "//iframe[contains(@src,'sn-ims-v2-angular.web.app/home/report')]"
))

wait = WebDriverWait(driver, 30)

while True:
    # STATUS CELL of FIRST ROW
    status_cell = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "(//tbody//tr)[1]//td[7]"   # Status column
        ))
    )

    status_text = status_cell.text.strip()
    print("Current status:", status_text)

    # ✅ If Download button appears → click & exit loop
    if "Download" in status_text:
        download_btn = status_cell.find_element(
            By.XPATH, ".//button"
        )
        download_btn.click()
        print("✅ Report downloaded")
        break

    # 🔄 Else still processing → click Action refresh
    action_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "(//tbody//tr)[1]//td[8]//button"  # Action column
        ))
    )
    action_btn.click()
    print("🔄 Refresh clicked, waiting 20 sec...")

    time.sleep(10)

driver.quit()
