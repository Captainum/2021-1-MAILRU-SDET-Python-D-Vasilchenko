from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class MainPageLocators(BasePageLocators):
    LOGINBUTTON_LOCATOR = (By.XPATH, '//div[@class="responseHead-module-button-1BMAy4" and contains(text(), "Войти")]')
    USERNAME_LOCATOR = (By.XPATH, '//input[@class="authForm-module-input-9t5W5U input-module-input-1xGLR8"]')
    PASSWORD_LOCATOR = (By.XPATH, '//input[@class="authForm-module-inputPassword-2Atq4Q input-module-input-1xGLR8"]')
    ENTER_LOCATOR = (By.XPATH, '//div[@class="authForm-module-button-2G6lZu"]')

class DashboardPageLocators(BasePageLocators):
    RIGHTMENUBUTTON_LOCATOR = (By.XPATH, '//div[@class="right-module-rightButton-39YRvc right-module-mail-25NVA9"]')
    LOGOUT_LOCATOR = (By.XPATH, '//a[@class="rightMenu-module-rightMenuLink-2FYb2O" and contains(text(), "Выйти")]')

class ContactsPageLocators(BasePageLocators):
    USERNAME_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[1]')
    PHONENUMBER_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[2]')
    EMAIL_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[3]')
    SAVEBUTTON_LOCATOR = (By.XPATH, '//button[@class="button button_submit"]')
