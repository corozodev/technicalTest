from src.pages.select_menu_page import SelectMenuPage


def test_should_apply_all_requested_select_menu_values(driver):
    page = SelectMenuPage(driver)
    page.open()

    page.select_value("A root option")
    assert page.selected_texts()["value"] == "A root option"

    page.select_one("Ms.")
    assert page.selected_texts()["one"] == "Ms."

    page.select_old_style("Indigo")
    assert page.selected_texts()["old_style"] == "Indigo"

    page.select_multiple(["Blue", "Red"])
    assert page.selected_texts()["multiple"] == ["Blue", "Red"]

    page.select_standard_multiple(["Volvo", "Opel"])
    assert page.selected_texts()["standard_multiple"] == ["Volvo", "Opel"]
