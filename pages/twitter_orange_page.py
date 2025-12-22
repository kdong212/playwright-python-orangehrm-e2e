from core.base_page import BasePage

class TwitterOrangePage(BasePage):
    X_ICON = "//h1[@role='heading']/a[@aria-label='X']"
    NAME_PAGE = "//div[@data-testid='UserName']//span[normalize-space()='OrangeHRM']/parent::span"

    def __init__(self, page):
        super().__init__(page)

    def verify_twitter_orange_page(self):
        # verify x icon bên góc trái
        self._wait_for_element(self.X_ICON)
        # verify orange Hrm ở dưới avatar
        self._wait_for_element(self.NAME_PAGE)