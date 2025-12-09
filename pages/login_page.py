from pages.base_page import BasePage
from pages.new_window_page import NewWindowPage

class LoginPage(BasePage):
    #
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    # Social Media Locators
    LINKEDIN_ICON_LINK = "//a[@href='https://www.linkedin.com/company/orangehrm/mycompany/']"
    FACEBOOK_ICON_LINK = "//a[@href='https://www.facebook.com/OrangeHRM/']"
    TWITTER_ICON_LINK = "a[href*='twitter.com/orangehrm']"
    YOUTUBE_ICON_LINK = "https://www.youtube.com/c/OrangeHRMInc"
    PAGE_TITLE = "OrangeHRM"

    def __init__(self, page):
        super().__init__(page)

    # Business Actions
    def go_to_url(self):
        self._visit(self.URL)

    def open_new_tab_and_return_new_object(self,social_name:str) -> NewWindowPage:
        """
        Click External link để mở tab mới
        và trả về NewWindowPage (POM) của tab mới
        """
        with self.page.context.expect_page() as new_page_info:
            self._click(social_name)
        
        new_page = new_page_info.value
        new_page.wait_for_load_state()

        return NewWindowPage(new_page)

    def verify_social_link():
        pass