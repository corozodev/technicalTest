import os
import shutil
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService


BASE_URL = os.getenv("URL", "https://demoqa.com/")


def _create_driver():
    """Create Chrome remote standalone by default; retain local Firefox option."""
    if os.getenv("WEBDRIVER", "remote").lower() == "remote":
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        return webdriver.Remote(
            command_executor=os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub"),
            options=options,
        )

    options = webdriver.FirefoxOptions()
    if os.getenv("HEADLESS", "true").lower() != "false":
        options.add_argument("-headless")

    firefox_binary = os.getenv("FIREFOX_BINARY") or shutil.which("firefox") or shutil.which("firefox-esr")
    if firefox_binary:
        options.binary_location = firefox_binary

    driver_path = Path(os.getenv("GECKODRIVER_PATH", Path(__file__).with_name("geckodriver")))
    return webdriver.Firefox(service=FirefoxService(executable_path=str(driver_path)), options=options)


@pytest.fixture()
def driver():
    browser = _create_driver()
    browser.set_window_size(1440, 1200)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


@pytest.fixture()
def init_driver(request, driver):
    """Backward-compatible fixture for class-based tests from the starter repo."""
    request.cls.driver = driver
    yield driver
