import os 
import json
import requests
import urllib3
from urllib3 import request
from datetime import datetime
from dotenv import load_dotenv
from botasaurus.browser import Driver, browser, Wait
from botasaurus.soupify import soupify
from toolkits.bs4_extension import ( 
                        extract_element_by_locator, 
                        get_element_by_locator,
                        get_all_element_by_locator)
from toolkits.loggers import show_message
from toolkits.file_manager import get_json_file_content





months_fr_short = {
    'jan': '01',
    'fév': '02',
    'mar': '03',
    'avr': '04',
    'mai': '05',
    'jun': '06',
    'jui': '07',
    'aoû': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'déc': '12'
}

load_dotenv()

class PageDataScraper(object):

    def __init__(self, page_data:dict={}):
        self.selectors = page_data.get("selectors")
        self.page_html = page_data.get("web_page")
        self.cleaned_data = []

    def format_date(self, unformated_date:str, unformated_time:str) -> str:
        show_message("INFO", f"{unformated_date} {unformated_time}")
        unformated_date = unformated_date.split(' ')
        date = f"{datetime.now().year}-{months_fr_short[unformated_date[1][:3]]}-{unformated_date[0]}"
        return f"{date} {unformated_time}"

    def format_name(self, name:str) -> str:
        return name

        # { 'name': #Nom du match, 'date': #date et heure du match, 'type': 'match'}
    def extract(self) -> None:
        def clean_text(text) -> str:
            return text.strip().replace('\u00e9', 'é')
        container = get_element_by_locator(self.page_html, self.selectors.get('container')[0])
        datas = get_all_element_by_locator(container, self.selectors.get('datas')[0])
        # name = extract_element_by_locator(self.page_html, self.selectors.get('match_name')[0])
        for data in datas:
            new_data = {}
            divs = data.find('div', {'class':"event-content"}).find_all('div')
            # new_data['id'] = ""
            # new_data['team1'] = clean_text(divs[0].text)
            # new_data['team2'] = clean_text(divs[-1].text)
            new_data['name'] = f"{clean_text(divs[0].text)} - {clean_text(divs[-1].text)}"
            date = divs[1].find_all('div')[0].text
            time = divs[1].find_all('div')[1].text
            new_data['date'] = self.format_date(date, time)
            new_data['type'] = "match"
            new_data['address'] = extract_element_by_locator(data, self.selectors.get('adress')[0])
            new_data["zipcode"] = ""
            new_data["city"] = ""
            new_data["gps"] = ""
            self.cleaned_data.append(new_data)

        show_message("INFO" , f"{self.cleaned_data}")

    def post_data(self) -> None:
            show_message("INFO", f"post data to API")
            api_url_dev = os.environ.get('API_URL_DEV')
            endpoint = api_url_dev + "events/add/multiple"
            api_token_dev = os.environ.get('API_TOKEN_DEV')
            try:
                encode_data = json.dumps(self.cleaned_data)
                req = urllib3.PoolManager()
                res = req.request(  
                    'POST',  
                    url=endpoint,  
                    body=encode_data,  
                    headers={
                        'Content-Type': 'application/json',
                        "Authorization" : api_token_dev
                        }  
                ) 


                # response = requests.post(
                #     url = endpoint,
                #     headers = {
                #         "Content-Type": "application/json",
                #         "Authorization" : api_token_dev
                #     },
                #     data = encode_data,
                #     verify = False,
                #     timeout = 60
                # )


                print(f"Server response {res.status}")

                # show_message("INFO", encode_data)
            except Exception as e:
                print(e)

def scrap_soc_task(url:str) -> None:
    selectors = get_json_file_content("./SOC/selectors.json")
    driver = Driver(arguments=['--start-maximized'])
    driver.get(url, wait=5)
    show_message("INFO", f"Navigate {url}")
    driver.click_element_containing_text("Calendrier")
    driver.long_random_sleep()
    page_data = {}
    page_data['web_page'] = soupify(driver.page_html)
    page_data['selectors'] = selectors

    p = PageDataScraper(page_data)
    p.extract()
    p.post_data()
    driver.close()