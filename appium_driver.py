from appium import webdriver
from appium.options.android import UiAutomator2Options

def main_driver(device, app_url, bs_user, bs_key):
    options = UiAutomator2Options()
    options.set_capability("platformName", device["platformName"])
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("deviceName", device["deviceName"])
    options.set_capability("platformVersion", device["platformVersion"])
    options.set_capability("app", app_url)
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("language", "en")
    options.set_capability("locale", "US")
    options.set_capability("project", "MyProject")
    options.set_capability("build", "MyBuild")
    options.set_capability("name", device["deviceName"])
    options.set_capability("browserstackLocal", False)
    options.set_capability("debug", True)
    options.set_capability("networkLogs", True)

    return webdriver.Remote(
        command_executor=f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )
