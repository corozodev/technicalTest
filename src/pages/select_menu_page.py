from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from src.pages.base_page import BasePage


class SelectMenuPage(BasePage):
    PATH = "/select-menu"
    SELECT_VALUE_INPUT = (By.ID, "react-select-2-input")
    SELECT_ONE_INPUT = (By.ID, "react-select-3-input")
    OLD_STYLE = (By.ID, "oldSelectMenu")
    MULTISELECT_INPUT = (By.ID, "react-select-4-input")
    STANDARD_MULTISELECT = (By.ID, "cars")

    def open(self) -> None:
        super().open(self.PATH)
        self.visible(self.SELECT_VALUE_INPUT)

    def select_value(self, value: str) -> None:
        self._react_select(self.SELECT_VALUE_INPUT, value)

    def select_one(self, value: str) -> None:
        self._react_select(self.SELECT_ONE_INPUT, value)

    def select_old_style(self, value: str) -> None:
        Select(self.element(self.OLD_STYLE)).select_by_visible_text(value)

    def select_multiple(self, values: list[str]) -> None:
        for value in values:
            self._react_select(self.MULTISELECT_INPUT, value)

    def select_standard_multiple(self, values: list[str]) -> None:
        select = Select(self.element(self.STANDARD_MULTISELECT))
        select.deselect_all()
        for value in values:
            select.select_by_visible_text(value)

    def selected_texts(self) -> dict[str, list[str] | str]:
        return {
            "value": self.element((By.ID, "withOptGroup")).text,
            "one": self.element((By.ID, "selectOne")).text,
            "old_style": Select(self.element(self.OLD_STYLE)).first_selected_option.text,
            "multiple": [
                element.get_attribute("aria-label").removeprefix("Remove ")
                for element in self.driver.find_elements(By.CSS_SELECTOR, "#selectMenuContainer [aria-label^='Remove ']")
            ],
            "standard_multiple": [option.text for option in Select(self.element(self.STANDARD_MULTISELECT)).all_selected_options],
        }

    def _react_select(self, input_locator, value: str) -> None:
        field = self.visible(input_locator)
        field.send_keys(value)
        field.send_keys(Keys.ENTER)
