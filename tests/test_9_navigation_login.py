from playwright.sync_api import expect
from enums.social_network_links_enum import SocialNetworkLinks
from pages.twitter_orange_page import TwitterOrangePage

BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/"
LOGIN_URL = f"{BASE_URL}auth/login"

def test_9_open_twitter_and_verify_page(login_page):
    login_page.go_to_page(LOGIN_URL)
    tw = SocialNetworkLinks.TWITTER
    
    social_page = login_page.open_social_link(tw)
    twitter_page = TwitterOrangePage(social_page.page)
    twitter_page.verify_twitter_orange_page()
    twitter_page._take_screenshot(tw)

    login_page.page.bring_to_front()

    dashboard_url = f"{BASE_URL}dashboard/index"
    username = "Admin"
    password = "admin123"

    home_page = login_page.login(username,password)
    expect(home_page.page).to_have_url(dashboard_url)
    home_page._take_screenshot("test_9_homepage")

    home_page.header.logout()
    login_url = f"{BASE_URL}auth/login"
    expect(login_page.page).to_have_url(login_url)
    login_page._take_screenshot("test_9_login")

