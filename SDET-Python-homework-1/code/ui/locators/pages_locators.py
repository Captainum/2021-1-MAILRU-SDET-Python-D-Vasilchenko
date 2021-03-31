from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class MainPageLocators(BasePageLocators):
    LOGINBUTTON_LOCATOR = (By.XPATH, '//div[starts-with(@class, "responseHead-module-button") and contains(text(), "Войти")]')
    USERNAME_LOCATOR = (By.XPATH, '//input[starts-with(@class, "authForm-module-input") and @name="email"]')
    PASSWORD_LOCATOR = (By.XPATH, '//input[starts-with(@class, "authForm-module-input") and @name="password"]')
    ENTER_LOCATOR = (By.XPATH, '//div[starts-with(@class, "authForm-module-button") and contains(text(), "Войти")]')

class DashboardPageLocators(BasePageLocators):
    RIGHTMENUBUTTON_LOCATOR = (By.XPATH, '//div[starts-with(@class, "right-module-rightButton")]')
    LOGOUT_LOCATOR = (By.XPATH, '//li[starts-with(@class, "rightMenu-module-rightMenuItem")]/a[contains(text(), "Выйти")]')
    PROFILE_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Профиль")]')
    BALANCE_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Баланс")]')
    STATISTICS_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Статистика")]')

class ContactsPageLocators(BasePageLocators):
    USERNAME_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[1]')
    PHONENUMBER_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[2]')
    EMAIL_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[3]')
    SAVEBUTTON_LOCATOR = (By.XPATH, '//button[@class="button button_submit"]')
