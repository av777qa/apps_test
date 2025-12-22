import sys
import yaml
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from appium_driver import main_driver

# Получаем app_url из аргумента командной строки
if len(sys.argv) > 1:
    app_url = sys.argv[1]
else:
    raise ValueError("APP_URL not set. Please provide the BrowserStack app URL.")

# Загружаем YAML с устройствами
with open("browserstack.yml", "r") as f:
    bs_config = yaml.safe_load(f)

bs_user = bs_config["userName"]
bs_key = bs_config["accessKey"]
devices_list = bs_config["platforms"]

def test_apps_and_webview(app_url, device, bs_user, bs_key):
    driver = main_driver(device, app_url, bs_user, bs_key)
    status = "passed"
    reason = "WebView visible"

    try:
        webviews = WebDriverWait(driver, 20).until(
            lambda d: d.find_elements(AppiumBy.CLASS_NAME, 'android.webkit.WebView')
        )
        if not webviews:
            status = "failed"
            reason = "WebView not visible"
    except TimeoutException:
        status = "failed"
        reason = "WebView not visible (Timeout)"
    finally:
        try:
            driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}","reason":"{reason}"}}}}'
            )
        except Exception as e:
            print("Failed to send status to BrowserStack:", e)
        time.sleep(2)
        driver.quit()

    print(f"BrowserStack status: {status} ({reason})")

if __name__ == "__main__":
    for device in devices_list:
        print(f"Running test on {device['deviceName']}...")
        test_apps_and_webview(app_url, device, bs_user, bs_key)
