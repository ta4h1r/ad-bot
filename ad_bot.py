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


def main():

    # Define browser objects
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--headless")

    chrome_options = set_chrome_options()

    browser = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver",
        options=chrome_options
    )

    # Open web-page, wait @timeout seconds for the profile avatar to load
    browser.get("https://www.google.com/search?q=robots+south+africa+robotics+hardware+agnostic+sofware+fleet+management")
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH, "//div[@class='appbar']"
                )
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    """
     Getting ads on page 
    """

    # find_elements_by_xpath returns an array of selenium objects.
    top_ads_objects = browser.find_elements_by_xpath("//span[@class='Zu0yb LWAWHf qzEoUe']")
    top_ads_text = [x.text for x in top_ads_objects]
    top_ads_tuple = zip(top_ads_text, top_ads_objects)

    sites_to_click = ["www.questekdigital.co.za/robots/in_hotels", "www.ctrlrobotics.com"]
    for text, obj in top_ads_tuple:
        print("Found ad: ", text)
        if text in sites_to_click:
            for i in range(100):
                open_in_new_tab(browser, obj)
                i += 1
                print("Click ", i, ": ", text)

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
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


if __name__ == "__main__":
    while True:
        main()
        print("Done")
