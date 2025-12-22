from playwright.sync_api import Page
from core.base_page import BasePage
from components.header_component import HeaderComponent

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)