import os.path
import time
import zipfile

from selenium import webdriver
import chromedriver_binary

options = webdriver.ChromeOptions()

if os.environ["USE_PROXY"] == "yes":
    PROXY_HOST = os.environ["PROXY_HOST"]
    PROXY_PORT = os.environ["PROXY_PORT"]
    PROXY_USER = os.environ["PROXY_USER"]
    PROXY_PASS = os.environ["PROXY_PASS"]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfile = os.path.join(os.getcwd(), 'user', 'proxy_auth_plugin.zip')
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    options.add_extension(os.path.join(os.getcwd(), 'user', 'proxy_auth_plugin.zip'))
options.headless = True
options.add_argument('--hide-scrollbars')
driver = webdriver.Chrome(options=options)

driver.get(os.path.join(os.getcwd(), 'html', 'アンジュルム.html'))
time.sleep(2)
driver.set_window_size(driver.execute_script('return document.body.scrollWidth') + 40,
                       driver.execute_script('return document.body.scrollHeight') + 40)
with open('angerme' + '.png', mode='wb') as f:
    f.write(driver.get_screenshot_as_png())
