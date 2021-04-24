from appium.webdriver.common.mobileby import MobileBy


class BasePageANDROIDLocators:
    pass


class MainPageANDROIDLocators(BasePageANDROIDLocators):
    KEYBOARD_BUTTON_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    INPUT_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    SEARCH_BUTTON_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/text_input_action')
    
    FACT_CARD_TITLE_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    FACT_CARD_CONTENT_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_content_text')
    
    COMMANDS_LOCATOR = (MobileBy.XPATH, '//android.view.ViewGroup[1]/android.widget.TextView')

    ANSWER_LOCATOR = (MobileBy.XPATH, '//androidx.recyclerview.widget.RecyclerView/android.widget.TextView')

    SETTINGS_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')

    NEWS_TITLE_LOCATOR = (MobileBy.XPATH, '//androidx.recyclerview.widget.RecyclerView//android.widget.TextView[@text="{}"]')


class SettingsPageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_SOURCES_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    ABOUT_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_about')
    CLOSE_SETTINGS_LOCATOR = (MobileBy.XPATH, '(//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageButton)[1]')


class NewsSourcesPageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_SOURCE_LOCATOR = (MobileBy.XPATH, '//android.widget.TextView[@text="{}"]')
    ITEM_SELECTED_LOCATOR = (MobileBy.XPATH, '//android.widget.TextView[@text="{}"]//parent::android.widget.FrameLayout//android.widget.ImageView')
    BACK_BUTTON_LOCATOR = (MobileBy.XPATH, '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageButton')


class AboutPageANDROIDLocators(BasePageANDROIDLocators):
    VERSION_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_version')
    COPYRIGHT_LOCATOR = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_copyright')