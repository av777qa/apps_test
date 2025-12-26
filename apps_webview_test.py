import yaml
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from appium_driver import main_driver
from report_generator import generate_html_report

def test_apps_and_webview(app_url, device, bs_user, bs_key):
    driver = main_driver(device, app_url, bs_user, bs_key)
    status = "PASSED"
    reason = "WebView is visible"
    try:
        webviews = WebDriverWait(driver, 20).until(
            lambda d: d.find_elements(AppiumBy.CLASS_NAME, "android.webkit.WebView")
        )
        if not webviews:
            status = "FAILED"
            reason = "WebView not found"
    except TimeoutException:
        status = "FAILED"
        reason = "Timeout waiting for WebView"
    finally:
        try:
            driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", '
                f'"arguments": {{"status":"{status.lower()}","reason":"{reason}"}}}}'
            )
        except Exception:
            pass
        driver.quit()
    print(f"[{status}] {device['deviceName']} ({device['platformVersion']})")
    return {
        "device": device["deviceName"],
        "version": device["platformVersion"],
        "status": status,
        "reason": reason
    }

if __name__ == "__main__":
    with open("browserstack.yml", "r") as f:
        config = yaml.safe_load(f)
    app_url = os.environ.get("APP_URL") or config["app"]
    bs_user = os.environ.get("BS_USER") or config["userName"]
    bs_key = os.environ.get("BS_KEY") or config["accessKey"]
    devices = config["platforms"]
    results = []
    for device in devices:
        result = test_apps_and_webview(app_url, device, bs_user, bs_key)
        results.append(result)

    generate_html_report(results)
    print("HTML report generated: report.html")
