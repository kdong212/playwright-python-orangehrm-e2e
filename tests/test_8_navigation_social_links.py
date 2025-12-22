from enums.social_network_links_enum import SocialNetworkLinks

BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/"
LOGIN_URL = f"{BASE_URL}auth/login"

def test_8_navigation_social_links(login_page):

    login_page.go_to_page(LOGIN_URL)

    for item in SocialNetworkLinks:
        expected_url = item.value[1]
        social_page = login_page.open_social_link(item)

        try:
            current_url = social_page.verify_navigation_success(expected_url)
            social_page._take_screenshot(f"test_8_{item.name}")
            assert expected_url in current_url, f"Lỗi: URL không khớp. Hiện tại: {current_url}"
        except Exception as e:
            print(f"Có lỗi xảy ra với link {item}: {e}")
            raise e
            
        finally:
            social_page.page.close()



        

