from src.pages.web_tables_page import WebTablesPage
from src.utils.data_generator import make_user


def test_should_create_a_new_user_with_random_valid_values(driver):
    # DemoQA exposes user-record creation through Elements > Web Tables.
    user = make_user("create")
    page = WebTablesPage(driver)

    page.open()
    page.create_user(user)

    assert page.record_values(user.email) == user.__dict__
