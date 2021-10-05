from selenium.webdriver.common.by import By


class BasePageLocators:
    TEXT_ERROR_LOCATOR = (By.XPATH, '//div[@id="flash"]')


class AuthorizationPageLocators(BasePageLocators):
    TEXT_WELCOME_LOCATOR = (By.XPATH, '//h3[starts-with(@class, "uk-card-title")]')
    INPUT_USERNAME_LOCATOR = (By.XPATH, '//input[@id="username" and @placeholder="Username" and @type="text"]')
    INPUT_PASSWORD_LOCATOR = (By.XPATH, '//input[@id="password" and @placeholder="Password" and @type="password"]')
    BUTTON_LOGIN_LOCATOR = (By.XPATH, '//input[@id="submit" and @type="submit"]')
    TEXT_NOT_REGISTERED_LOCATOR = (By.XPATH, '//div[starts-with(@class, "uk-text-small")]')
    HREF_CREATE_AN_ACCOUNT = (By.XPATH, '//a[@href="/reg"]')
    TEXT_ERROR_LOCATOR = (By.XPATH, '//div[@id="flash"]')


class RegistrationPageLocators(BasePageLocators):
    TEXT_REGISTRATION_LOCATOR = (By.XPATH, '//h3[starts-with(@class, "uk-card-title")]')
    INPUT_USERNAME_LOCATOR = (By.XPATH, '//input[@id="username"]')
    INPUT_EMAIL_LOCATOR = (By.XPATH, '//input[@id="email"]')
    INPUT_PASSWORD_LOCATOR = (By.XPATH, '//input[@id="password"]')
    INPUT_REPEAT_PASSWORD_LOCATOR = (By.XPATH, '//input[@id="confirm"]')
    INPUT_CHECKBOX_LOCATOR = (By.XPATH, '//input[@id="term"]')
    TEXT_ACCEPT_LOCATOR = (By.XPATH, '//label[@class="uk-text-small"]')
    BUTTON_REGISTER_LOCATOR = (By.XPATH, '//input[@id="submit"]')
    TEXT_HAVE_AN_ACCOUNT = (By.XPATH, '(//div[starts-with(@class, "uk-text-small")])[1]')
    HREF_LOG_IN_LOCATOR = (By.XPATH, '//a[@href="/login"]')


class MainPageLocators(BasePageLocators):
    ICON_BUG_LOCATOR = (By.XPATH, '//i[@class="uk-icon-bug"]')
    HREF_BRAND_LOCATOR = (By.XPATH, '//a[starts-with(@class, "uk-navbar-brand") and @href="/"]')

    BUTTON_HOME_LOCATOR = (By.XPATH, '(//li/a)[1]')

    BUTTON_PYTHON_LOCATOR = (By.XPATH, '(//li/a)[2]')
    BUTTON_PYTHON_HISTORY_LOCATOR = (By.XPATH, '//ul/li[2]/div/ul/li[1]/a')
    BUTTON_PYTHON_ABOUT_FLASK_LOCATOR = (By.XPATH, '//ul/li[2]/div/ul/li[2]/a')

    BUTTON_LINUX_LOCATOR = (By.XPATH, '(//li/a)[5]')
    BUTTON_LINUX_DOWNLOAD_CENTOS_LOCATOR = (By.XPATH, '//ul/li[3]/div/ul/li/a')

    BUTTON_NETWORK_LOCATOR = (By.XPATH, '(//li/a)[7]')
    BUTTON_NETWORK_NEWS_LOCATOR = (By.XPATH, '//ul/li[4]/div/ul/li[1]/ul/li[1]/a')
    BUTTON_NETWORK_DOWNLOAD_LOCATOR = (By.XPATH, '//ul/li[4]/div/ul/li[1]/ul/li[2]/a')
    BUTTON_NETWORK_EXAMPLES_LOCATOR = (By.XPATH, '//ul/li[4]/div/ul/li[2]/ul/li/a')

    TEXT_LOGGED_AS_LOCATOR = (By.XPATH, '(//div[@id="login-controls"]//li)[1]')
    BUTTON_LOGOUT_LOCATOR = (By.XPATH, '//div[@id="logout"]//a')

    TEXT_API_LOCATOR = (By.XPATH, '(//div[starts-with(@class, "uk-width-1-3")]//div)[1]')
    TEXT_FUTURE_LOCATOR = (By.XPATH, '(//div[starts-with(@class, "uk-width-1-3")]//div)[2]')
    TEXT_SMTP_LOCATOR = (By.XPATH, '(//div[starts-with(@class, "uk-width-1-3")]//div)[3]')
    
    BUTTON_API_LOCATOR = (By.XPATH, '(//figure)[1]')
    BUTTON_FUTURE_LOCATOR = (By.XPATH, '(//figure)[2]')
    BUTTON_SMTP_LOCATOR = (By.XPATH, '(//figure)[3]')

    TEXT_POWERED_BY_LOCATOR = (By.XPATH, '(//div//p)[1]')
    TEXT_RANDOM_PHRASE_LOCATOR = (By.XPATH, '(//div//p)[2]')

    VK_ID_LOCATOR = (By.XPATH, '(//div[@id="login-controls"]//li)[2]')