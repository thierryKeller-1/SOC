
import time
import requests
from random import randint

from playwright.sync_api import sync_playwright
from botasaurus.browser import Driver, browser, Wait

from toolkits.loggers import show_message


def get_page(url:str, engine:str) -> object:
    if engine:
        match engine:
            case 'selenium':
                pass 
            case 'playwright':
                playwright = sync_playwright().start()
                browser = playwright.chromium.launch(headless=False, args=['--start-maximized'])
                context = browser.new_context(no_viewport=True)
                driver = context.new_page()
                try:
                    driver.goto(url, timeout=60000)
                    pass 
                except:
                    pass 

            case 'requests':
                try:
                    response = requests.get(url, timeout=60)
                    return response
                except Exception as e:
                    show_message('error',f'Error: {e}')
                    time.sleep(randint(3, 5))
                    return get_page(url, engine)
                    
            case _:
                try:
                    driver = Driver()
                    driver.get(url)
                    driver.short_random_sleep()
                    return driver
                except Exception as e:
                    show_message('error',f'Error: {e}')
                    time.sleep(randint(3, 5))
                    driver.quit()
                    return get_page(url, engine)


