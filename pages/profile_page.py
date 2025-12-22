from core.base_page import BasePage
import os



class ProfilePage(BasePage):
    LOCATOR_PROFILE_IMAGE = ".orangehrm-edit-employee-image img"
    BTN_ADD_IMAGE = "button.employee-image-action"
    BTN_SAVE = "//button[@class='oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space']"
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
    def upload_profile_image(self, file_path: str):
        # Bước 1: Click icon profile để hiện nút +
        self.page.click(self.profile_icon)
        
        # Bước 2: Click dấu + (trong thực tế, ta có thể trigger trực tiếp vào input file)
        # Nếu trang web bắt buộc click + rồi mới hiện dialog, ta vẫn gọi upload_attachment vào selector input
        self.page.click(self.plus_button)
        
        # Sử dụng hàm từ BasePage để upload
        self.upload_attachment(self.file_input, file_path)

    def save_profile_change(self):
        # Bước 3: Click Save để hoàn tất
        self.page.click(self.save_button)