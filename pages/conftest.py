import pytest
from playwright.sync_api import sync_playwright
from pages.new_window_page import NewWindowPage
from playwright.sync_api import Page

# Fixture để khởi tạo và đóng Playwright, trả về đối tượng Playwright
@pytest.fixture(scope="session")
def playwright_instance():
    """Khởi tạo và đóng Playwright."""
    with sync_playwright() as p:
        yield p

# Fixture để tạo Browser
@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Khởi tạo và đóng Browser."""
    # Bạn có thể thay đổi 'chromium' thành 'firefox' hoặc 'webkit'
    browser_instance = playwright_instance.chromium.launch(headless=True)
    yield browser_instance
    browser_instance.close()

# Fixture để tạo Page (tab) cho mỗi bài kiểm thử
@pytest.fixture(scope="function")
def page(browser):
    """Khởi tạo và đóng Page (tab) cho mỗi bài kiểm thử."""
    page_instance = browser.new_page()
    yield page_instance
    page_instance.close()


# Fixture để tạo Page (NEW TAB) cho bài test Social network navigation
def window_page(page:Page) -> NewWindowPage:
    wp = window_page(page)
    wp.open()
    return wp