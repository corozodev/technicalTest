from src.pages.web_tables_page import WebTablesPage
from src.utils.data_generator import make_user


def test_should_reject_empty_required_web_table_fields(driver):
    page = WebTablesPage(driver)
    page.open()
    page.open_add_form()
    page.submit_form()

    assert page.form_is_open()
    assert page.field_is_invalid("first_name")
    assert page.validation_message("first_name")


def test_should_reject_an_invalid_email_format_in_web_table_form(driver):
    user = make_user("invalid-email")
    invalid_email = "not-an-email"
    page = WebTablesPage(driver)
    page.open()
    page.open_add_form()
    page._fill_user(user)
    page.fill(page.FIELDS["email"], invalid_email)
    page.submit_form()

    assert page.form_is_open()
    assert page.field_is_invalid("email")
    assert page.validation_message("email")
    page.close_form()
    assert not page.record_is_visible(invalid_email)
