from playwright.sync_api import Page, expect, Locator, TimeoutError
import os
from datetime import datetime

class BasePage:
    SCREENSHOT_DIR = os.path.join(os.getcwd(), "output", "screenshots")

    """Lớp cha chứa các hành động Playwright cơ bản, kế thừa cho mọi Page Object."""
    
    def __init__(self, page: Page):
        self.page = page
        # self.SCREENSHOT_DIR = "screenshots"
        # os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)
        SCREENSHOT_DIR = os.path.join("output", "screenshots")

    def _visit(self, url: str):
        """Điều hướng tới URL được chỉ định."""
        print(f"[BasePage] Navigate to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def _get_locator(self, locator: str) -> Locator:
        """Trả về đối tượng Locator từ chuỗi selector."""
        return self.page.locator(locator)
    
    def _get_by_role(self, role: str, nth: int = 0) -> Locator:
        """Trả về locator theo role (vd: searchbox, button, link...)"""
        locator = self.page.get_by_role(role)
        return locator.nth(nth) if nth else locator
    
    def _get_page_url(self):
        return self.page.url

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

    def _fill(self, locator: str, text: str, name: str = ""):
        """Điền dữ liệu vào ô input."""
        print(f"[Fill] '{text}' into {name or locator}")
        self._get_locator(locator).fill(text)


    def wait_for_element(self, locator: str, timeout: int = 5000, state: str = "visible"):
        """
        Chờ cho element xuất hiện, ẩn, hay biến mất.
        state = "visible" | "attached" | "hidden" | "detached"
        """
        print(f"[Wait for] {locator} ({state})")
        self.page.locator(locator).wait_for(state=state, timeout=timeout)

    def wait_for_text(self, locator: str, expected_text: str, timeout: int = 5000):
        """Chờ đến khi element chứa text mong đợi"""
        print(f"[Wait for text] {expected_text}")
        expect(self.page.locator(locator)).to_contain_text(expected_text, timeout=timeout)    

    def _select_item_from_ddl(self,locator:str,search:str,item:str,index: int = 1):
        """Click vô ô, điền dữ liệu, nhấn ENTER"""

        ddl = self._get_locator(locator)
        ddl.click()

        # Tìm ô search và nhập giá trị
        # search_box = self._get_by_role(search).nth(index)
        search_box = self._get_locator(search)
        search_box.fill(item)
        search_box.press("Enter")


    # page.locator(PICKUP_LOCATION_DROPDOWN).click() # Click để mở dropdown
    #     if warehouse_data.location == "Yes":
    #         page.locator(PICKUP_LOCATION_OPTION_YES).click()
    #     else:
    #         page.locator(PICKUP_LOCATION_OPTION_NO).click()

    def select_from_custom_dropdown(self, dropdown_locator: str, option_text: str):
        """
        Mở một dropdown tùy chỉnh (ví dụ: Select2) và chọn một tùy chọn dựa trên text.
        
        Args:
            dropdown_locator (str): Locator của phần tử hiển thị dropdown (ví dụ: container).
            option_text (str): Text của tùy chọn cần chọn.
        """
        self.page.locator(dropdown_locator).click() # Click để mở dropdown
        
        # Giả định cấu trúc options là li trong ul có ID là kết quả của dropdown_locator + '-results'
        # Ví dụ: nếu dropdown_locator là '#select2-id-container', thì results là '#select2-id-results'
        # Cần điều chỉnh nếu cấu trúc HTML khác
        dropdown_id = dropdown_locator.split('-container')[0].replace('#select2-', '')
        results_list_id = f"select2-{dropdown_id}-results"
        
        option_locator = f"//ul[@id='{results_list_id}']/li[text()='{option_text}']"
        self.page.locator(option_locator).click()

    def _select(self,locator,locator1, locator2,option:str,name:str=""):
        print(f"[Select] '{option}' into {name or locator}")
        self._get_locator(locator).click()
        if option =="Yes":
            self._get_locator(locator1).click()
        else:
            self._get_locator(locator2).click()


    # ------- SPECIAL: AUTO LOCATOR THEO LABEL -------
    def by_label(self, label_text: str):
        """
        Trả về locator của ô SELECT2 tương ứng với label.
        Dùng khi ID dynamic.
        """
        xpath = f"//label[normalize-space()='{label_text}']/following::span[contains(@class,'select2-selection__rendered')][1]"
        return xpath

    def _assert_text_visible(self, locator: str, text: str):
        """Kiểm tra văn bản mong đợi hiển thị trên giao diện."""
        print(f"[Assert] Check '{text}' exists")
        expect(self._get_locator(locator)).to_contain_text(text)

    # def select_from_select2(self, container_locator: str, search_text: str):
    #     """
    #     Click vào dropdown (Select2), nhập từ khóa và nhấn Enter để chọn item.
    #     Args:
    #         container_locator: locator ổn định của Select2 (ví dụ: ".select2-selection--single")
    #         search_text: giá trị cần chọn (ví dụ: "Australia")
    #     """
    #     print(f"[Select2] Click on: {container_locator}")
    #     self.wait_for_element(container_locator)

    #     count = self.page.locator(container_locator).count()
    #     print("Found Country dropdown:", count)
    #     self.page.locator(container_locator).click()

    #     print(f"[Select2] Search for: {search_text}")
    #     search_input = self.page.get_by_role("searchbox").nth(0)
    #     search_input.fill(search_text)
    #     search_input.press("Enter")

    #     print("[Select2] Done selecting item.")

    #     # Đợi dropdown đóng
    #     try:
    #         self.page.wait_for_selector(".select2-results__options", state="detached", timeout=3000)
    #     except:
    #         pass

    #     # Click ra ngoài để release
    #     self.page.locator("body").click(position={"x": 0, "y": 0})

    def find_select2_display_by_label(self, label: str):
        """
        Detect Select2 display area theo label.
        Không dùng ID động, không strict mode error.
        """
        locator = self.page.locator(
            f"label:has-text('{label}')"
        ).locator(
            "xpath=following::*//span[contains(@class,'select2-selection__rendered')]"
        ).first

        locator.wait_for(state="visible")
        return locator

    def _get_frame_or_page(self, frame_selector: str = None):
        """
        Nếu frame_selector được cung cấp (CSS hoặc iframe id), trả về FrameLocator's frame.
        Nếu không, trả về Page object để dùng giống nhau (chúng ta sẽ always use .locator(...))
        """
        if not frame_selector:
            return self.page
        # dùng frame_locator để an toàn; lấy frame object
        frame_locator = self.page.frame_locator(frame_selector)
        # frame_locator không expose trực tiếp frame, nhưng chúng ta vẫn có thể dùng frame_locator.locator(...)
        return frame_locator

    def debug_count(self, selector: str, frame_selector: str = None):
        ctx = self._get_frame_or_page(frame_selector)
        # If ctx is frame_locator, it supports .locator; if Page, also .locator
        return ctx.locator(selector).count()
    
    def select2(self, label: str, value: str, frame_selector: str = None, timeout: int = 5000):
        """
        Chọn item trong Select2 dropdown theo label
        """
        # 1. Xác định frame nếu có
        context = self.page
        if frame_selector:
            context = self.page.frame_locator(frame_selector)

        # 2. Tìm container theo label
        container = context.locator(f"label:has-text('{label}') ~ span.select2")
        expect(container).to_be_visible(timeout=timeout)

        # 3. Click mở dropdown
        selection = container.locator(".select2-selection").first
        expect(selection).to_be_visible(timeout=timeout)
        selection.click()

        # 4. Tìm input search bên trong dropdown
        search_box = container.locator("input.select2-search__field").first
        expect(search_box).to_be_visible(timeout=timeout)
        expect(search_box).to_be_enabled(timeout=timeout)

        # 5. Force focus + fill + Enter
        search_box.click(force=True)
        search_box.fill(value)
        search_box.press("Enter")

    def select52(self, label: str, value: str, frame_selector: str = None, timeout: int = 5000):
        # 1. Tìm dropdown theo label
        container = self.page.locator(
            f"label:has-text('{label}') ~ span.select2"
        )
        expect(container).to_be_visible()

        # 2. Click mở dropdown
        container.locator(".select2-selection").click()

        # 3. Input bên trong select2
        search_box = self.page.locator("input.select2-search__field")
        expect(search_box).to_be_visible()
        expect(search_box).to_be_enabled(timeout=3000)

        # Debug info
        print("Search box count:", search_box.count())
        print("HTML:", search_box.evaluate("el => el.outerHTML"))

        # 4. Force focus + fill
        search_box.click(force=True)
        search_box.fill(value)
        self.keyboard.press("Enter")

    
    

    def select23(self, label:str, value:str):
        try:
            # 1. Tìm dropdown theo label
            container = self.page.locator(
                f"label:has-text('{label}') ~ span.select2"
            )
            expect(container).to_be_visible()

            # 2. Click mở dropdown
            container.locator(".select2-selection").click()

            # 3. Đợi input xuất hiện và visible
            search_box = self.page.locator("input.select2-search__field")
            expect(search_box).to_be_visible(timeout=3000)
            expect(search_box).to_be_enabled(timeout=3000)

            # Debug info
            print("Search box count:", search_box.count())
            print("HTML:", search_box.evaluate("el => el.outerHTML"))

            # 4. Force focus + fill
            search_box.self.page.click(force=True)
            search_box.self.fill(value)
            
            self.keyboard.press("Enter")

        except TimeoutError:
            print("Dropdown chưa kịp hiện, thử lại")
        except Exception as e:
            print("Fill không được:", e)
    

    


    def _take_screenshot(self, label):
        """
        Chụp màn hình với tên file có timestamp.
        Ví dụ: abc_20251127_080516.png
        """
        # Tạo thư mục nếu nó chưa tồn tại
        if not os.path.exists(self.SCREENSHOT_DIR):
            os.makedirs(self.SCREENSHOT_DIR)
            
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{label}_{timestamp}"
        # Sử dụng thuộc tính SCREENSHOT_DIR đã được định nghĩa ở trên
        file_path = os.path.join(self.SCREENSHOT_DIR, f"{file_name}.png")
        
        # Lệnh chụp của Playwright
        self.page.screenshot(path=file_path)
        print(f"✅ Đã chụp màn hình và lưu tại: {file_path}")    

    def _wait_for_visible(self, locator, timeout=5000):
        locator.wait_for(state="visible", timeout=timeout)

    def _wait_for_timeout(self,locator,timeout=5000):
        Locator.wait_for(timeout=timeout)

    def _click_and_wait_for_new_page(self, locator: str, name: str = "", timeout: int = 15000):
        """
        Click vào locator → mở tab mới → return Page mới.
        """
        print(f"[MultiTab]: Click '{name}' và chờ tab mới mở...")

        with self.page.context.expect_page(timeout=timeout) as new_page_info:
            self.page.locator(locator).click()

        new_page = new_page_info.value
        new_page.wait_for_load_state("load")

        print(f"[MultiTab]: Tab mới URL = {new_page.url}")
        return new_page