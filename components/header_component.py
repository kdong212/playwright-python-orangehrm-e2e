from playwright.sync_api import Page,expect
from core.base_page import BasePage
from core.base_page import BasePage
class HeaderComponent(BasePage):
    USER_DROPDOWN_TAB = "//span[@class='oxd-userdropdown-tab']"
    LOGOUT_BUTTON = "//ul[@role='menu']//a[normalize-space()='Logout']"
    
    def __init__(self, page: Page):
        super().__init__(page)

    def logout(self):
        """Mở menu người dùng và click vào nút Logout."""
        # Bước 1: Click vào menu người dùng
        self._click(self.USER_DROPDOWN_TAB)
        # Bước 2: Click vào nút Logout
        self._click(self.LOGOUT_BUTTON)
        # Có thể thêm verify chuyển hướng sang trang login
        self.page.wait_for_url("**/login")
