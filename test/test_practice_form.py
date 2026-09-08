from pathlib import Path

from src.pages.practice_form_page import PracticeFormPage
from src.utils.data_generator import make_practice_form_data


def test_should_submit_a_complete_practice_form(driver):
    data = make_practice_form_data()
    page = PracticeFormPage(driver)

    page.open()
    page.complete(data, Path(__file__).parent / "resources" / "profile.txt")
    page.submit()

    submitted = page.submitted_values()
    assert submitted["Student Name"] == f"{data.first_name} {data.last_name}"
    assert submitted["Student Email"] == data.email
    assert submitted["Gender"] == data.gender
    assert submitted["Mobile"] == data.mobile
    assert submitted["Subjects"] == data.subject
    assert submitted["Hobbies"] == data.hobby
    assert submitted["Address"] == data.address
    assert submitted["State and City"] == f"{data.state} {data.city}"
