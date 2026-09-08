from src.pages.web_tables_page import WebTablesPage
from src.utils.data_generator import make_user


def test_should_create_edit_and_delete_its_own_web_table_record(driver):
    original = make_user("crud")
    updated_department = "Automation"
    updated_first_name = "Updated"
    page = WebTablesPage(driver)

    page.open()
    page.create_user(original)
    assert page.record_values(original.email) == original.__dict__

    page.edit_user(original.email, first_name=updated_first_name, department=updated_department)
    updated = page.record_values(original.email)
    assert updated["first_name"] == updated_first_name
    assert updated["department"] == updated_department
    assert updated["email"] == original.email

    page.delete_user(original.email)
    assert not page.record_is_visible(original.email)
