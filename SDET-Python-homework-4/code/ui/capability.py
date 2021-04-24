def capability_select(device_os, apk_path):
    capability = None
    
    if device_os == 'android':
        capability = {
            "platformName": "Android",
            "platformVersion": "8.1",
            "automationName": "Appium",
            "appPackage": "ru.mail.search.electroscope",
            "appActivity": ".ui.activity.AssistantActivity",
            "app": apk_path,
            "autoGrantPermissions": True,
             "orientation": "PORTRAIT"
        }
    else:
        raise ValueError('Incorrect device os type')
    
    return capability