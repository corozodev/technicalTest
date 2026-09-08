from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.pages.base_page import BasePage
from src.utils.data_generator import PracticeFormData


class PracticeFormPage(BasePage):
    PATH = "/automation-practice-form"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    MOBILE = (By.ID, "userNumber")
    DATE_OF_BIRTH = (By.ID, "dateOfBirthInput")
    SUBJECTS = (By.ID, "subjectsInput")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    ADDRESS = (By.ID, "currentAddress")
    STATE = (By.ID, "react-select-3-input")
    CITY = (By.ID, "react-select-4-input")
    SUBMIT = (By.ID, "submit")
    CONFIRMATION_TITLE = (By.ID, "example-modal-sizes-title-lg")
    RESULT_ROWS = (By.CSS_SELECTOR, ".table-responsive tbody tr")

    def open(self) -> None:
        super().open(self.PATH)
        self.visible(self.FIRST_NAME)

    def complete(self, data: PracticeFormData, upload_file: Path) -> None:
        self.fill(self.FIRST_NAME, data.first_name)
        self.fill(self.LAST_NAME, data.last_name)
        self.fill(self.EMAIL, data.email)
        self.click((By.CSS_SELECTOR, f"label[for='gender-radio-{2 if data.gender == 'Female' else 1}']"))
        self.fill(self.MOBILE, data.mobile)
        self._select_birth_date(data.birth_date.year, data.birth_date.month, data.birth_date.day)
        self._select_react_option(self.SUBJECTS, data.subject)
        self.click((By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']"))
        self.element(self.UPLOAD_PICTURE).send_keys(str(upload_file.resolve()))
        self.fill(self.ADDRESS, data.address)
        self._select_react_option(self.STATE, data.state)
        self._select_react_option(self.CITY, data.city)

    def submit(self) -> None:
        self.click(self.SUBMIT)
        self.visible(self.CONFIRMATION_TITLE)

    def submitted_values(self) -> dict[str, str]:
        rows = self.driver.find_elements(*self.RESULT_ROWS)
        return {
            row.find_elements(By.TAG_NAME, "td")[0].text: row.find_elements(By.TAG_NAME, "td")[1].text
            for row in rows
        }

    def _select_birth_date(self, year: int, month: int, day: int) -> None:
        self.click(self.DATE_OF_BIRTH)
        Select(self.visible((By.CSS_SELECTOR, ".react-datepicker__year-select"))).select_by_visible_text(str(year))
        Select(self.visible((By.CSS_SELECTOR, ".react-datepicker__month-select"))).select_by_index(month - 1)
        # The outside-month copy of a day has an additional class; use the current-month cell.
        self.click((By.CSS_SELECTOR, f".react-datepicker__day--0{day:02d}:not(.react-datepicker__day--outside-month)"))

    def _select_react_option(self, input_locator, value: str) -> None:
        field = self.visible(input_locator)
        field.click()
        field.send_keys(value)
        self.click((By.XPATH, f"//*[@role='option' and normalize-space()={value!r}]"))
