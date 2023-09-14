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

EMAIL_ADDRESS = "taahir.bhaiyat@camcog.com"
PASSWORD = "#X6eCGVAQKnya*b"
def main():

    # Define browser objects
    # option = webdriver.ChromeOptions()
    # option.add_argument("--incognito")
    # option.add_argument("--headless") 
    # option.add_argument("--browser.chrome.path=/Users/taahir.bhaiyat/Desktop/selenium-example/chrome-mac-arm64/Google Chrome for Testing.app")

    chrome_options = set_chrome_options()

    browser = webdriver.Chrome(
        executable_path="./chromedriver-mac-arm64/chromedriver",
        options=chrome_options
    )

    # Open web-page, wait @timeout seconds for the profile avatar to load
    browser.get("https://app.qualio.com/library?filter=training&page=1&count=100")
    timeout = 20

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH, "//button[@id='login-btn']"
                )
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    """
     LOGIN
    """

    email = browser.find_element(By.ID, "input-email")
    email.send_keys(EMAIL_ADDRESS)
 
    password = browser.find_element(By.ID, "input-password")
    password.send_keys(PASSWORD)

    loginBtn = browser.find_element(By.ID, "login-btn")
    loginBtn.click()

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR, ".inline-block-right .btn.btn-default.dropdown-toggle"
                )
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    

    dropDown = browser.find_element(By.CSS_SELECTOR, ".inline-block-right .btn.btn-default.dropdown-toggle")
    dropDown.click()

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR, '.inline-block-right li a.text-left.ng-binding'
                )
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    dropDownItems = browser.find_elements(By.CSS_SELECTOR, '.inline-block-right li a.text-left.ng-binding')
    dropDownItems[3].click()

    tableRows = browser.find_elements(By.CSS_SELECTOR, '.ng-scope.navigable')

    for i in range(1, len(tableRows)): 
        trClickable = browser.find_element(By.XPATH,  '//*[@id="contentView"]/div/table/tbody/tr[' + str(i) + ']/td[2]')
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
            try: 
                WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.CSS_SELECTOR, '.ng-scope.navigable'
                        )
                    )
                )
            except: 
                print("Something went wrong looking for table 1")
                browser.quit()
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
            try: 
                WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.CSS_SELECTOR, '.ng-scope.navigable'
                        )
                    )
                )
            except: 
                print("Something went wrong looking for table 2")
                browser.quit()
        

        # Fill in your details 
        email = browser.find_element(By.ID, "input-email")
        email.send_keys(EMAIL_ADDRESS)
    
        password = browser.find_element(By.ID, "input-password")
        password.send_keys(PASSWORD)

        # Click sign-off button
        signoffBtn = browser.find_element (By.XPATH, '//*[@id="ng-app"]/body/div[1]/span/div/div[2]/div/div/div[2]/form/div[2]/button[1]')
        signoffBtn.click()

        try: 
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR, '.ng-scope.navigable'
                    )
                )
            )
        except: 
            print("Something went wrong")
            browser.quit()

    browser.quit()
    print("Quit")


def scroll_shim(passed_in_driver, browser_obj):
    """
    Brings a specified browser_obj into the page viewport so that it can be clicked 

    :param passed_in_driver:
    :param browser_obj:
    :return:
    """
    x = browser_obj.location['x']
    y = browser_obj.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def open_in_new_tab(passed_in_driver, browser_obj):
    scroll_shim(passed_in_driver, browser_obj)
    ActionChains(passed_in_driver).key_down(Keys.CONTROL).click(browser_obj).perform()
    time.sleep(5)


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = "./chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


if __name__ == "__main__":
    main()
    print("DONE - Yours in Quality Automation ;)")
