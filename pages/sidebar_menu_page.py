from core.base_page import BasePage


class SidebarMenuPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def click_menu(self, label_menu: str):
        xpath_menu = f'//a[.//span[normalize-space()="{label_menu}"]]'
        self._click(xpath_menu)
        return self

    def verify_header_in_page_correct(self):
        pass