import time
import getpass
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
# Update the usernames of accounts to be reported in the separate file.
ACCOUNTS_TO_REPORT_FILE = "account-list.txt"

def get_accounts(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        return []

def prompt_credentials():
    username = input("Enter your X username or email: ")
    password = getpass.getpass("Enter your X password: ")
    return username, password

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    return webdriver.Chrome(options=chrome_options)

def random_delay():
  time.sleep(random.uniform(2, 3))

def login_x(driver, username, password):
    print("[INFO] Logging in to X...")
    driver.get("https://x.com/login")
    time.sleep(5)
    try:
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(username)
        username_input.send_keys(Keys.RETURN)
        random_delay()
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        random_delay()
        print("[INFO] Login attempted.")
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return False
    return True

def report_account(driver, username):
    profile_url = f"https://x.com/{username}"
    print(f"[INFO] Reporting @{username}...")
    driver.get(profile_url)
    time.sleep(5)
    try:
        # Click the "..." (More) button
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="More"]'))
        ).click()
        random_delay()
        
        # Click "Report @username"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Report")]'))
        ).click()
        random_delay()
        
        # Select a reason (example: "Hate")
        # This can be changed based on more accurate basis.
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Hate']"))
        ).click()
        random_delay()

        # Next
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]'))
        ).click()
        random_delay()

        # Select a reason (example: "Dehumanization")
        # This can be changed as well. 
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Dehumanization']"))
        ).click()
        random_delay()

        # Submit
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Submit")]'))
        ).click()
        random_delay()

        # Done
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Done")]'))
        ).click()
        random_delay()
        
        print(f"[SUCCESS] Reported @{username}")
    except Exception as e:
        print(f"[ERROR] Failed to report @{username}: {e}")

def main():
    accounts = get_accounts(ACCOUNTS_TO_REPORT_FILE)
    if not accounts:
        print("[ERROR] No accounts to report. Exiting.")
        return
    username, password = prompt_credentials()
    driver = setup_driver()
    try:
        if not login_x(driver, username, password):
            print("[ERROR] Login unsuccessful. Exiting.")
            return
        for account in accounts:
            report_account(driver, account)
            random_delay()
    finally:
        driver.quit()
        print("[INFO] Script finished.")

if __name__ == "__main__":
    main()
