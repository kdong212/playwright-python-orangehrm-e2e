from playwright.sync_api import Page, expect, Locator, TimeoutError
from config.config_manager import SCREENSHOT_ON
import os, re
from datetime import datetime

class BasePage:
    """Lớp cha chứa các hành động Playwright cơ bản, kế thừa cho mọi Page Object."""
    
    def __init__(self, page: Page):
        self.page = page
        self.SCREENSHOT_DIR = "screenshots"
        os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)

    def _fill(self, locator: str, text: str, name: str = ""):
        """Điền dữ liệu vào ô input."""
        print(f"[Fill] '{text}' into {name or locator}")
        self._get_locator(locator).fill(text)

    def _get_locator(self, locator: str) -> Locator:
        """Trả về đối tượng Locator từ chuỗi selector."""
        return self.page.locator(locator)

    def _click(self, locator: str, name: str = ""):
        """Thực hiện click với xử lý lỗi và ghi log."""
        try:
            print(f"[Click] {name or locator}")
            element = self._get_locator(locator)
            expect(element).to_be_visible()
            element.click()
        except Exception as e:
            print(f"[ERROR] Unable to click to {locator}: {type(e).__name__} - {e}")
            raise


    def _visit(self, url: str):
        """Điều hướng tới URL được chỉ định."""
        print(f"[BasePage] Navigate to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
    
    def _get_page_url(self):
        return self.page.url

    def _wait_for_element(self, locator: str, timeout: int = 5000, state: str = "visible"):
        """
        Chờ cho element xuất hiện, ẩn, hay biến mất.
        state = "visible" | "attached" | "hidden" | "detached"
        """
        try:
            print(f"[Wait for] {locator} ({state})")
            self.page.locator(locator).wait_for(state=state, timeout=timeout)
        except Exception as e:
            print(f"❌ Lỗi khi chờ element {locator}: {e}")
            raise e

    def _open_new_tab(self, locator: str, name: str = "", timeout: int = 15000):
        """
        Click vào locator → mở tab mới → return Page mới.
        """
        print(f"[MultiTab]: Click '{name}' và chờ tab mới mở...")

        with self.page.context.expect_page(timeout=timeout) as new_page_info:
            self.page.locator(locator).click()

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded",timeout=60000)

        print(f"[MultiTab]: Tab mới URL = {new_page.url}")
        return new_page
    
    

    # def take_screenshot(self, path: str = 'screenshots', name: str = 'screenshot', full_page: bool = True):
    #     """
    #     Thực hiện chụp ảnh màn hình nếu biến SCREENSHOT_ON là True.
    #     Args:
    #         path (str): Thư mục lưu screenshot. Mặc định là 'screenshots'.
    #         name (str): Tên file screenshot (không bao gồm phần mở rộng).
    #         full_page (bool): Chụp toàn bộ trang hay chỉ viewport. Mặc định là True.
    #     """
    #     # --- Kiểm tra Biến Global ---
    #     if not SCREENSHOT_ON:
    #         print("🛑 Screenshot disabled by configuration.")
    #         return

    #     # Tạo thư mục nếu chưa tồn tại
    #     os.makedirs(path, exist_ok=True)

    #     # Định dạng tên file với đuôi .png
    #     file_name = f"{name}.png"
    #     full_path = os.path.join(path, file_name)
    def _take_screenshot(self, label):
        """
        Chụp màn hình với tên file có timestamp.
        Ví dụ: abc_20251127_080516.png
        """
        # Tạo thư mục nếu nó chưa tồn tại
        if not os.path.exists(self.SCREENSHOT_DIR):
            os.makedirs(self.SCREENSHOT_DIR)

        self.page.wait_for_load_state("load")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{label}_{timestamp}"
        # Sử dụng thuộc tính SCREENSHOT_DIR đã được định nghĩa ở trên
        file_path = os.path.join(self.SCREENSHOT_DIR, f"{file_name}.png")

        # Lệnh chụp của Playwright
        self.page.screenshot(path=file_path)
        print(f"✅ Đã chụp màn hình và lưu tại: {file_path}")
    
    def verify_url_contains(self, expected_sub_url: str, timeout: int = 10000):
        try:
            expect(self.page).to_have_url(re.compile(rf".*{re.escape(expected_sub_url)}.*"), timeout=timeout)
            print(f"✅ Xác nhận: URL đã chứa '{expected_sub_url}'")
        except AssertionError as e:
            print(f"❌ Xác nhận thất bại: URL thực tế là '{self.page.url}'")
            raise e