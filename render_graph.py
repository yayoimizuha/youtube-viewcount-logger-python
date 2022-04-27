import os.path
import const
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support import expected_conditions, ui

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--hide-scrollbars')

driver = webdriver.Chrome(options=options)

for _, name in const.playlists():
    print(name)
    html_path = os.path.join(os.getcwd(), 'html', name + '.html')
    print(html_path, end='\n\n')
    driver.get(html_path)
    ui.WebDriverWait(driver=driver, timeout=15).until(expected_conditions.presence_of_all_elements_located)

    driver.set_window_size(800, 600)
    driver.set_window_size(driver.execute_script('return document.body.scrollWidth') + 40,
                           driver.execute_script('return document.body.scrollHeight') + 40)

    with open(os.path.join(os.getcwd(), 'images', name + '_2.png'), mode='wb') as f:
        f.write(driver.get_screenshot_as_png())
