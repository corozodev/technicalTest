from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.pages.base_page import BasePage
from src.utils.data_generator import UserData


class WebTablesPage(BasePage):
    PATH = "/webtables"
    ADD_RECORD = (By.ID, "addNewRecordButton")
    SEARCH = (By.ID, "searchBox")
    MODAL = (By.ID, "registration-form-modal")
    SUBMIT = (By.ID, "submit")
    FIELDS = {
        "first_name": (By.ID, "firstName"),
        "last_name": (By.ID, "lastName"),
        "email": (By.ID, "userEmail"),
        "age": (By.ID, "age"),
        "salary": (By.ID, "salary"),
        "department": (By.ID, "department"),
    }
    # The current application uses a native table (earlier versions used ReactTable).
    ROWS = (By.CSS_SELECTOR, ".web-tables-wrapper tbody tr")

    CLOSE_BUTTON = (By.CSS_SELECTOR, ".btn-close, .close, button[aria-label='Close']")

    def open(self) -> None:
        super().open(self.PATH)
        self.visible(self.ADD_RECORD)

    def open_add_form(self) -> None:
        self.click(self.ADD_RECORD)
        self.visible(self.MODAL)

    def close_form(self) -> None:
        close_btns = self.driver.find_elements(*self.CLOSE_BUTTON)
        if close_btns and close_btns[0].is_displayed():
            self.click(self.CLOSE_BUTTON)
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop")))

    def create_user(self, user: UserData) -> None:
        self.open_add_form()
        self._fill_user(user)
        self.submit_form()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop")))
        self.wait.until(lambda _: self.record_is_visible(user.email))

    def edit_user(self, email: str, **changes: str) -> None:
        row = self._find_row(email)
        edit = row.find_element(By.CSS_SELECTOR, "span[title='Edit']")
        self.driver.execute_script("arguments[0].click();", edit)
        self.visible(self.MODAL)
        for field_name, value in changes.items():
            self.fill(self.FIELDS[field_name], value)
        self.submit_form()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop")))
        self.wait.until(lambda _: self.record_is_visible(email))

    def delete_user(self, email: str) -> None:
        row = self._find_row(email)
        delete = row.find_element(By.CSS_SELECTOR, "span[title='Delete']")
        self.driver.execute_script("arguments[0].click();", delete)
        self.wait.until(lambda _: not self.record_is_visible(email))

    def submit_form(self) -> None:
        self.click(self.SUBMIT)

    def record_is_visible(self, email: str) -> bool:
        self._search(email)
        return any(email in row.text for row in self.driver.find_elements(*self.ROWS))

    def record_values(self, email: str) -> dict[str, str]:
        cells = self._find_row(email).find_elements(By.TAG_NAME, "td")
        return dict(zip(("first_name", "last_name", "age", "email", "salary", "department"), (cell.text for cell in cells)))

    def field_is_invalid(self, field_name: str) -> bool:
        field = self.element(self.FIELDS[field_name])
        return not self.driver.execute_script("return arguments[0].validity.valid;", field)

    def validation_message(self, field_name: str) -> str:
        field = self.element(self.FIELDS[field_name])
        return self.driver.execute_script("return arguments[0].validationMessage;", field)

    def form_is_open(self) -> bool:
        return self.element(self.MODAL).is_displayed()

    def _fill_user(self, user: UserData) -> None:
        for field_name, value in user.__dict__.items():
            self.fill(self.FIELDS[field_name], value)

    def _search(self, email: str) -> None:
        search = self.visible(self.SEARCH)
        search.click()
        search.clear()
        search.send_keys(email)
        self.wait.until(lambda _: search.get_attribute("value") == email)

    def _find_row(self, email: str):
        self._search(email)
        return self.wait.until(lambda _: next((row for row in self.driver.find_elements(*self.ROWS) if email in row.text), False))
