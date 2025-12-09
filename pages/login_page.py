from pages.base_page import BasePage

class LoginPage(BasePage):
    #
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    # Social Media Locators
    LINKEDIN_ICON_LINK = "//a[@href='https://www.linkedin.com/company/orangehrm/mycompany/']"
    FACEBOOK_ICON_LINK = "//a[@href='https://www.facebook.com/OrangeHRM/']"
    TWITTER_ICON_LINK = "a[href*='twitter.com/orangehrm']"
    YOUTUBE_ICON_LINK = "https://www.youtube.com/c/OrangeHRMInc"
    YOUTUBE_PAGE_TITLE = "OrangeHRM Inc"

    # Business Actions
    def go_to_url(self):
        self._visit(self.URL)

    def open_external_link(self,external:str):
        self._click(external)

    

    