from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class MainPageLocators(BasePageLocators):
    LOGINBUTTON_LOCATOR = (By.XPATH, '//div[@class="responseHead-module-button-1BMAy4" and contains(text(), "Войти")]')
    USERNAME_LOCATOR = (By.XPATH, '//input[@class="authForm-module-input-9t5W5U input-module-input-1xGLR8"]')
    PASSWORD_LOCATOR = (By.XPATH, '//input[@class="authForm-module-inputPassword-2Atq4Q input-module-input-1xGLR8"]')
    ENTER_LOCATOR = (By.XPATH, '//div[@class="authForm-module-button-2G6lZu"]')

class DashBoardLocators(BasePageLocators):
    pass
