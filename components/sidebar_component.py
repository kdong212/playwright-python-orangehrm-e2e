from core.base_page import BasePage


class SidebarComponent(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def go_to_menu(self,label_menu:str):
        xpath_menu =f'//span[normalize-space()="{label_menu}"]/parent::a'
        print(f"[Action] Clicking on menu: {label_menu}")
        self._click(xpath_menu)
        return self
