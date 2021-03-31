from ui.pages.base_page import BasePage
from ui.locators.pages_locators import ContactsPageLocators

class ContactsPage(BasePage):
    def changeInfo(self, username, phonenumber, email):
        username_input = self.find(ContactsPageLocators.USERNAME_LOCATOR)
        phonenumber_input = self.find(ContactsPageLocators.PHONENUMBER_LOCATOR)
        email_input = self.find(ContactsPageLocators.EMAIL_LOCATOR)

        username_input.clear()
        phonenumber_input.clear()
        email_input.clear()

        username_input.send_keys(username)
        phonenumber_input.send_keys(phonenumber)
        email_input.send_keys(email)

        self.click(ContactsPageLocators.SAVEBUTTON_LOCATOR)
