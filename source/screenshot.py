import os

from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By


def get_screenshot_path():
    return os.path.join(os.getcwd(), os.getenv("TMP"), "screenshot.png")


def screenshot_was_saved_successfully():
    return os.path.exists(get_screenshot_path())


def take_screenshot_of_website_graph():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--window-size=760,580")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--user-data-dir=/tmp/user-data")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--log-level=0")
        chrome_options.add_argument("--v=99")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--data-path=/tmp/data-path")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--homedir=/tmp")
        chrome_options.add_argument("--disk-cache-dir=/tmp/cache-dir")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        )
        chrome_options.binary_location = os.getenv("HEADLESS_CHROMIUM")

        driver = webdriver.Chrome(os.getenv("CHROMEDRIVER"), options=chrome_options)

        driver.get("https://projectroomkeytracker.com/")
        driver.execute_script("document.querySelector('h2').scrollIntoView();")
        driver.execute_script("window.scrollBy(0, -10);")

        timeout = 5
        wait(driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it(
                driver.find_element_by_css_selector(".chart > iframe")
            )
        )
        wait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".docs-charts-component-canvas")
            )
        )

        driver.save_screenshot(get_screenshot_path())
    except:
        print("Couldn't save screenshot of Project Roomkey site :(")


if __name__ == "__main__":
    load_dotenv()

    take_screenshot_of_website_graph()
