import os

from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By


def take_screenshot_of_website_graph():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--window-size=760,580")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

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

    driver.save_screenshot(
        os.path.join(os.getcwd(), os.getenv("TMP"), "screenshot.png")
    )


if __name__ == "__main__":
    load_dotenv()

    take_screenshot_of_website_graph()
