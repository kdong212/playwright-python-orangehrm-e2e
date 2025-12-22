import pytest
from pages.login_page import LoginPage
import configparser, os, json
from pathlib import Path
from core.config_reader import ConfigReader
from playwrighpipt.sync_api import sync_playwright, Page
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent 
CONFIG_PATH = BASE_DIR / "config.ini"
CREDENTIALS_JSON = BASE_DIR / "config" / "credentials.json"

@pytest.fixture(scope="session")
def browser():
    """
    Fixture cho đối tượng Browser (Khởi tạo 1 lần/session).
    Sử dụng 'yield' để thực hiện Teardown sau khi tất cả các test kết thúc.
    """
    with sync_playwright() as p:
        # Setup: Khởi tạo trình duyệt Chromium (có thể thay bằng 'firefox' hoặc 'webkit')
        print("\n[SETUP] Khởi tạo Browser...")
        browser = p.chromium.launch(headless=True) # Dùng headless=False để xem giao diện
        yield browser # Trả về browser object cho các fixture khác

        # Teardown: Đóng trình duyệt sau khi tất cả test case hoàn thành
        print("\n[TEARDOWN] Đóng Browser...")
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """
    Fixture cho đối tượng Page (Khởi tạo 1 lần/test function).
    Sử dụng 'yield' để thực hiện Teardown sau mỗi test function.
    """
    # Setup: Tạo Context và Page mới
    print("\n  [SETUP] Tạo Page mới...")
    context = browser.new_context()
    page = context.new_page()
    yield page # Trả về page object cho test function

    # Teardown: Đóng Page và Context sau khi test function kết thúc
    print("\n  [TEARDOWN] Đóng Page và Context...")
    page.close()
    context.close()

@pytest.fixture(scope="session")
def env_config():
    """Đọc URL từ config.ini"""
    return {"base_url": ConfigReader.get_base_url()}

@pytest.fixture(scope="session")
def base_url():
    config = configparser.ConfigParser()
    
    # Kiểm tra sự tồn tại của file để debug dễ hơn
    if not CONFIG_PATH.exists():
        pytest.fail(f"Không tìm thấy file config.ini tại: {CONFIG_PATH}")

    config.read(CONFIG_PATH, encoding='utf-8')
    
    # Kiểm tra xem section có tồn tại không
    if not config.has_section('env'):
        pytest.fail(f"File config tồn tại nhưng thiếu section [env]. "
                    f"Nội dung file hiện tại: {config.sections()}")
    
    return config.get('env', 'base_url')



@pytest.fixture(scope="function")
def login_page(page):
    """"
    Fixture này đảm bảo login page được mở ra trước khi chạy test
    """
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    yield login_page


@pytest.fixture(scope="session")
def test_credentials() -> Dict[str, Any]:
    """Fixture đọc file JSON credentials"""
    with open(CREDENTIALS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="function")
def logged_in_page(login_page, test_credentials):
    """
    Fixture này đảm bảo page đã đăng nhập thành công trước khi chạy test.
    """
    creds = test_credentials["valid_user"]

    home_page = login_page.login(creds["username"], creds["password"])

    # 2. Xác thực (VP) đã vào được HomePage/Dashboard
    # home_page = login_page.login(username, password)
    home_page.verify_is_on_homepage()

    # 3. Trả về đối tượng Page đã đăng nhập
    yield home_page
