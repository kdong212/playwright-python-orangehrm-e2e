from pages.base_page import BasePage


#test heroku app
class NewWindowPage(BasePage):
    heading = "h3"

    def __init__(self, page):
        super().__init__(page)

    def get_heading_text(self)->str:
        return self._get_text(self.heading)
    
    def verify_heading():
        pass
    
