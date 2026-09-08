from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    timeout = 12

    def __init__(self, driver, base_url: str = "https://demoqa.com"):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, self.timeout)

    def open(self, path: str) -> None:
        self.driver.get(f"{self.base_url}{path}")
        self.wait.until(lambda current: current.execute_script("return document.readyState") == "complete")

    def element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            # DemoQA occasionally renders an advert/table overlay above a valid control.
            # Dispatching the native click on the located control preserves its normal handler.
            self.driver.execute_script("arguments[0].click();", element)

    def fill(self, locator, value: str) -> None:
        element = self.visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.clear()
        element.send_keys(value)
