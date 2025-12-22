from playwright.sync_api import expect
import re
from core.base_page import BasePage
from enums.social_network_links_enum import SocialNetworkLinks
from pages.social_network_page import SocialNetworkPage
class LoginPage(BasePage):
    PAGE_TITLE_EXPECTED = "OrangeHRM"

    # locators for LOGIN form
    USERNAME_FIELD = "//input[@name='username']"
    PASSWORD_FIELD = "//input[@name='password']"
    LOGIN_BUTTON = "//button[contains(@class, 'orangehrm-login-button')]"

    DASHBOARD_LABEL = "//h6[text()='Dashboard']"
    FAIL_MESSAGE = "//p[contains(@class, 'oxd-alert-content-text') and text()='Invalid credentials']"
        
    # Business Actions
    def go_to_page(self, url:str):
        self._visit(url)
        expect(self.page).to_have_title(self.PAGE_TITLE_EXPECTED)
        print(f"Đã truy cập thành công: {url}")

    def open_social_link(self, social_link_type: SocialNetworkLinks) -> SocialNetworkPage:
        """
        Mở liên kết mạng xã hội bằng cách sử dụng đối tượng Enum đã được đóng gói.
        
        :param social_link_type: Thành viên của Enum SocialNetworkLinks.
        :return: Đối tượng Page của tab mới.
        """

        # 1. Lấy Locator từ Enum
        locator_to_use = social_link_type.link_locator

        # 2. Lấy Tên hiển thị từ Enum (ví dụ: "TWITTER")
        link_name = social_link_type.name

        # 3. Thực thi hành động
        new_page = self._open_new_tab(
            locator=locator_to_use,
            name=link_name
        )
        expect(new_page).to_have_url(
            re.compile(social_link_type.expected_url), 
            timeout=5000 
        )

        return SocialNetworkPage(new_page)
    
    def login(self, username:str, password:str):
        """Thực hiện nghiệp vụ đăng nhập."""
        self._fill(self.USERNAME_FIELD, username, name="Username")
        self._fill(self.PASSWORD_FIELD, password, name="Password")
        self._click(self.LOGIN_BUTTON, name="Login Button")
        
        try:
            self.page.locator(self.DASHBOARD_LABEL).is_visible()
            # from pages.home_page import HomePage
            from pages.home_page import HomePage
            return HomePage(self.page)
        except TimeoutError:
            # Nếu không thấy DASHBOARD, kiểm tra lỗi đăng nhập
            if self.page.locator(self.FAIL_MESSAGE).is_visible():
                raise Exception("Login failed: Sai tên đăng nhập hoặc mật khẩu.")
            else:
                raise Exception("Login failed: Không xác định được trạng thái sau đăng nhập.")