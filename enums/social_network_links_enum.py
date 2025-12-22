from enum import Enum

class SocialNetworkLinks(Enum):
    LINKED_IN = ("//a[@href='https://www.linkedin.com/company/orangehrm/mycompany/']","linkedin.com",)
    FACEBOOK = ("//a[@href='https://www.facebook.com/OrangeHRM/']","facebook.com/OrangeHRM/")
    TWITTER = ("//a[contains(@href, 'twitter.com/orangehrm')]","x.com/orangehrm")
    YOUTUBE = ("//a[contains(@href, 'youtube.com/c/OrangeHRMInc')]","youtube.com/c/OrangeHRMInc")

    @property
    def link_locator(self):
        return self.value[0]

    @property
    def expected_url(self):
        return self.value[1]
    
   

    
