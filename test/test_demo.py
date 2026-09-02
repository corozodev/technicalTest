import pytest

@pytest.mark.usefixtures("init_driver")
class TestLogin:

    def test_successful_login(self):
        print("HolaMundo")