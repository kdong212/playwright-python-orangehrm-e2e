from enum import Enum


class SidebarMenuEnum(Enum):
    MY_INFO = ("My Info","PIM")
    RECRUITMENT = ("Recruitment","Recruitment")

    @property
    def option(self):
        return self.value[0]

    @property
    def expected_text(self):
        return self.value[1]

