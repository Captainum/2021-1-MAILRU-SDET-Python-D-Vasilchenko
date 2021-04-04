from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class MainPageLocators(BasePageLocators):
    LOGINBUTTON_LOCATOR = (By.XPATH, '//div[starts-with(@class, "responseHead-module-button") and contains(text(), "Войти")]')
    USERNAME_LOCATOR = (By.XPATH, '//input[starts-with(@class, "authForm-module-input") and @name="email"]')
    PASSWORD_LOCATOR = (By.XPATH, '//input[starts-with(@class, "authForm-module-input") and @name="password"]')
    ENTER_LOCATOR = (By.XPATH, '//div[starts-with(@class, "authForm-module-button") and contains(text(), "Войти")]')

    NOTIFY_LOCATOR = (By.XPATH, '//div[starts-with(@class, "notify-module") and contains(text(), "Введите email или телефон")]')

class DashboardPageLocators(BasePageLocators):
    RIGHTMENUBUTTON_LOCATOR = (By.XPATH, '//div[starts-with(@class, "right-module-rightButton")]')
    LOGOUT_LOCATOR = (By.XPATH, '//li[starts-with(@class, "rightMenu-module-rightMenuItem")]/a[contains(text(), "Выйти")]')

    SEGMENTS_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Аудитории")]')
    BALANCE_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Баланс")]')
    STATISTICS_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Статистика")]')
    PROFILE_LOCATOR = (By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Профиль")]')
    
    CREATECAMPAIGN_HREF_LOCATOR = (By.XPATH, '//a[@href="/campaign/new"]')
    CREATECAMPAIGN_BUTTON_LOCATOR = (By.XPATH, '//div[starts-with(@class, "button-module-text") and contains(text(), "Создать кампанию")]')

    SELECTMODULE_LOCATOR = (By.XPATH, '(//div[@data-test="select"])[1]')
    SELECT_ACTIVE_LOCATOR = (By.XPATH, '//li[@title="Активные кампании"]')
    CAMPAIGN_LOCATOR_TEMPLATE = (By.XPATH, '//a[starts-with(@class, "nameCell-module-campaignNameLink") and contains(text(), "{}")]')

class ContactsPageLocators(BasePageLocators):
    USERNAME_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[1]')
    PHONENUMBER_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[2]')
    EMAIL_LOCATOR = (By.XPATH, '(//input[@class="input__inp js-form-element"])[3]')
    SAVEBUTTON_LOCATOR = (By.XPATH, '//button[@class="button button_submit"]')

class CampaignPageLocators(BasePageLocators):
    GOAL_LOCATOR_TEMPLATE = (By.XPATH, '//div[contains(@class, "{}")]')
    URL_LOCATOR = (By.XPATH, '//input[starts-with(@class, "mainUrl-module-search") and @type="text" and @placeholder="Введите ссылку"]')
    BANNERFORMAT_LOCATOR_TEMPLATE = (By.XPATH, '//div[@class="banner-format-item"]//span[contains(text(), "{}")]')
    CAMPAIGN_NAME_LOCATOR = (By.XPATH, '(//div[contains(@class, "campaign-name")]//input[starts-with(@class, "input__inp")])[1]')

    SLIDENUMBER_LOCATOR_TEMPLATE = (By.XPATH, '//li[starts-with(@class, "roles-module") and contains(text(), "{}")]')

    SLIDEPICTURE_LOCATOR = (By.XPATH, '//div[starts-with(@class, "roles-module-button")]//input[@type="file" and starts-with(@data-test, "image_600x600")]')

    SLIDEURL_LOCATOR = (By.XPATH, '//input[@placeholder="Введите ссылку для слайда"]')
    SLIDETITLE_LOCATOR = (By.XPATH, '//input[@placeholder="Введите заголовок слайда"]')

    ADVPICTURE_LOCATOR = (By.XPATH, '//div[starts-with(@class, "roles-module-button")]//input[@type="file" and starts-with(@data-test, "icon_256x256")]')

    ADVURL_LOCATOR=  (By.XPATH, '//input[@placeholder="Введите адрес ссылки"]')
    ADVTITLE_LOCATOR = (By.XPATH, '//input[@placeholder="Введите заголовок объявления"]')
    ADVTEXT_LOCATOR = (By.XPATH, '//textarea[@placeholder="Введите текст объявления"]')

    SAVEBUTTON_LOCATOR = (By.XPATH, '//div[contains(text(), "Сохранить объявление")]')
    CREATEBUTTON_LOCATOR = (By.XPATH, '//div[contains(text(), "Создать кампанию")]')

class SegmentsPageLocators(BasePageLocators):
    # CREATESEGMENT_HREF_LOCATOR = (By.XPATH, '//a[@href="/segments/segments_list/new/"]')
    CREATESEGMENT_HREF_LOCATOR = (By.XPATH, '//a[contains(text(), "Создайте")]')
    CREATESEGMENT_BUTTON_LOCATOR = (By.XPATH, '//button[@data-class-name="Submit"]//div[contains(text(), "Создать сегмент")]')

    ADDSEGMENT_ITEM_LOCATOR = (By.XPATH, '//div[starts-with(@class, "adding-segments-item") and contains(text(), "Приложения и игры в соцсетях")]')
    ADDSEGMENT_CHECKBOX_LOCATOR = (By.XPATH, '//input[@type="checkbox"]')
    ADDSEGMENT_BUTTON_LOCATOR = (By.XPATH, '//button[@data-class-name="Submit"]//div[contains(text(), "Добавить сегмент")]')

    SEGMENT_NAME_LOCATOR = (By.XPATH, '//input[starts-with(@class, "input") and @maxlength="60"]')
    CREATESEGMENT_BUTTON_LOCATOR = (By.XPATH, '//button[@data-class-name="Submit"]//div[contains(text(), "Создать сегмент")]')

    SEGMENT_TITLE_LOCATOR_TEMPLATE = (By.XPATH, '//a[@title="{}"]')

    SEGMENT_REVERTBUTTON_LOCATOR_TEMPLATE = (By.XPATH, '//div[starts-with(@data-test, "remove-{}")]//span')

    SEGMENT_CONFIRMBUTTON_LOCATOR = (By.XPATH, '//button[contains(@class, "confirm-remove")]')