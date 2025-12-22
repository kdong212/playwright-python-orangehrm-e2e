from core.base_page import BasePage
from playwright.sync_api import Page


class SocialNetworkPage(BasePage):
    # Social Media Locators
    LINKEDIN_ICON_LINK = "//a[@href='https://www.linkedin.com/company/orangehrm/mycompany/']"
    FACEBOOK_ICON_LINK = "//a[@href='https://www.facebook.com/OrangeHRM/']"
    TWITTER_ICON_LINK = "a[href*='twitter.com/orangehrm']"
    YOUTUBE_ICON_LINK = "https://www.youtube.com/c/OrangeHRMInc"
    PAGE_TITLE = "OrangeHRM"

    def __init__(self, page: Page):
        super().__init__(page)

    def verify_navigation_success(self, expected_url: str):
        try:
            self.verify_url_contains(expected_url)
            return self.page.url
        except Exception as e:
            print(f"❌ Không thể điều hướng đến {expected_url}: {e}")
            return self.page.url
    