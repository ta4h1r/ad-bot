# https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72
import os

from selenium import webdriver                                     # Allows you to launch a browser
from selenium.webdriver.common.by import By                        # Allows you to search for things using specific parameters
from selenium.webdriver.support.ui import WebDriverWait            # Allows you to wait for a page to load
from selenium.webdriver.support import expected_conditions as EC   # Specify what you are looking for on a specific page in order to determine that the webpage has loaded
from selenium.common.exceptions import TimeoutException            # Handling a timeout situation
from selenium.webdriver.common.keys import Keys                    # Keyboard map
from selenium.webdriver.common.action_chains import ActionChains   # Performs keyboard/mouse actions
import time

from selenium.webdriver.chrome.options import Options

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = "./chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def wait_for_element_visible(identifier_method, identifier_string): 
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (
                   identifier_method, identifier_string
                )
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

def set_page_limit_to_hundred(): 
    cssSelector =  '.inline-block-right .btn.btn-default.dropdown-toggle'
    wait_for_element_visible(By.CSS_SELECTOR, cssSelector) 
    dropDown = browser.find_element(By.CSS_SELECTOR, cssSelector)
    dropDown.click()
    cssSelector = '.inline-block-right li a.text-left.ng-binding'
    wait_for_element_visible(By.CSS_SELECTOR, cssSelector)
    dropDownItems = browser.find_elements(By.CSS_SELECTOR, cssSelector)
    dropDownItems[3].click()
    time.sleep(1)

def choose_only_training(): 
    xPath = '//*[@id="contentView"]/div/div[2]/div/div[2]/button/span[2]'
    wait_for_element_visible(By.XPATH, xPath) 
    dropDown = browser.find_element(By.XPATH, xPath)
    dropDown.click()
    xPath = '//*[@id="contentView"]/div/div[2]/div/div[2]/ul/li[2]/a[1]'
    wait_for_element_visible(By.XPATH, xPath)
    dropDownItems = browser.find_elements(By.XPATH, xPath)
    dropDownItems[2].click()
    time.sleep(2)


def input_login_details(): 
    email = browser.find_element(By.ID, "input-email")
    email.send_keys(EMAIL_ADDRESS)
    password = browser.find_element(By.ID, "input-password")
    password.send_keys(PASSWORD)


def login(): 
    input_login_details()
    loginBtn = browser.find_element(By.ID, "login-btn")
    loginBtn.click()


EMAIL_ADDRESS = ""
PASSWORD = ""

chrome_options = set_chrome_options()
browser = webdriver.Chrome(
    executable_path="./chromedriver-mac-arm64/chromedriver",
    options=chrome_options
)
timeout = 20


def main():

    # Open web-page
    browser.get("https://app.qualio.com/library?filter=training&page=1&count=100")

    wait_for_element_visible(By.XPATH, "//button[@id='login-btn']")

    login()

    set_page_limit_to_hundred()

    count = 0
    try: 
        tableRows = browser.find_elements(By.CSS_SELECTOR, '.ng-scope.navigable')
        count = len(tableRows)
    except MaxRetryError: 
        return; 

    while (count > 0): 
        trClickable = browser.find_element(By.XPATH,  '//*[@id="contentView"]/div/table/tbody/tr[1]/td[2]')
        trClickable.click()

        # Look for complete button, go back if not found 
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH, '//*[@id="ng-app"]/body/div[1]/span/div/div[2]/div/div/div[3]/div/div/button'
                    )
                )
            )
        except TimeoutException:
            print("Caught waiting for complete button")
            browser.back()
            wait_for_element_visible(By.CSS_SELECTOR, '.ng-scope.navigable')
            choose_only_training()
            tableRows = browser.find_elements(By.CSS_SELECTOR, '.ng-scope.navigable')
            count = len(tableRows)
            continue

        # Click complete button 
        completeBtn = browser.find_element (By.XPATH, '//*[@id="ng-app"]/body/div[1]/span/div/div[2]/div/div/div[3]/div/div/button')
        completeBtn.click()

        # Look for Sign-off button, go back to first page if not found 
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH, '//*[@id="ng-app"]/body/div[1]/span/div/div[2]/div/div/div[2]/form/div[2]/button[1]'
                    )
                )
            )
        except TimeoutException:
            print("Caught waiting for sign off")
            browser.back()
            browser.back()
            wait_for_element_visible(By.CSS_SELECTOR, '.ng-scope.navigable')
        

        input_login_details()

        # Click sign-off button
        signoffBtn = browser.find_element (By.XPATH, '//*[@id="ng-app"]/body/div[1]/span/div/div[2]/div/div/div[2]/form/div[2]/button[1]')
        signoffBtn.click()

        wait_for_element_visible(By.CSS_SELECTOR, '.ng-scope.navigable')

        set_page_limit_to_hundred()

        tableRows = browser.find_elements(By.CSS_SELECTOR, '.ng-scope.navigable')

        count = len(tableRows)

        try: 
            tableRows = browser.find_elements(By.CSS_SELECTOR, '.ng-scope.navigable')
            count = len(tableRows)
        except MaxRetryError:
            break

    browser.quit()
    print("Quit")


if __name__ == "__main__":
    main()
    print("DONE - Yours in Quality Automation ;)")
