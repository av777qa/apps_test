import yaml
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from appium_driver import main_driver


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


def generate_html_report(results, file_name="report.html"):
    rows = ""
    for r in results:
        color = "#d4edda" if r["status"] == "PASSED" else "#f8d7da"
        rows += f"""
        <tr style="background-color:{color}">
            <td>{r['device']}</td>
            <td>{r['version']}</td>
            <td>{r['status']}</td>
            <td>{r['reason']}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>Android/iOS Test Report</title>
        <style>
            body {{ font-family: Arial; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #333; color: white; }}
        </style>
    </head>
    <body>
        <h2>Android Devices Test Report</h2>
        <table>
            <tr>
                <th>Device</th>
                <th>Android Version</th>
                <th>Status</th>
                <th>Reason</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    with open(file_name, "w") as f:
        f.write(html)


if __name__ == "__main__":
    with open("browserstack.yml", "r") as f:
        config = yaml.safe_load(f)

    app_url = config["app"]
    bs_user = config["userName"]
    bs_key = config["accessKey"]
    devices = config["platforms"]

    results = []

    for device in devices:
        result = test_apps_and_webview(app_url, device, bs_user, bs_key)
        results.append(result)

    generate_html_report(results)
    print("HTML report generated: report.html")
