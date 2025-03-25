import os
import json
import requests
import time
from dotenv import load_dotenv
from datetime import datetime
from toolkits import file_manager as fm
from toolkits.loggers import show_message
from playwright.sync_api import sync_playwright
from nested_lookup import nested_lookup

load_dotenv()

class PlaywrightDriver(object):

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False, args=['--start-maximized'])
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        self.xhr_page = []
        self.cleaned_data = []
        self.uncleaned_data = []
        fm.create_or_update_json_file('data.json')

    def intercept_response(self, response) -> None:
            """capture all background requests and save them"""
            response_type = response.request.resource_type
            print(response.url)
            if 'graphql' in response.url:
                print('graphql')
            if response_type == "fetch" or response_type  == "xhr":
                print('xhr')
                with open('./SOC/ressource.json', 'a') as openfile:
                    openfile.write(json.dump(response, indent=4))
                if 'graphql' in response.url:
                    print('graphql')
                    try:
                        if response.json()['data']['competitions_event_detail_by_team_id'] and response.json()['data']['competitions_event_detail_by_team_id'][0].get('status', '') == 'to_come':
                            self.xhr_page = response.json()['data']['competitions_event_detail_by_team_id']
                            self.xhr_page["url"] = self.page.url
                    except KeyError:
                        pass
    # def navigate_page(self, url:str, interception_func:str) -> None:
    def navigate_page(self, url:str) -> None:
        show_message("INFO", f"navigate => {url}")
        self.page.on("response", self.intercept_response)
        self.page.goto(url, timeout=60000)
        time.sleep(30)

    def load_page(self) -> None:
        self.page.locator("button[tabindex=-1]").click()
        self.page.mouse.wheel(0, 900)

    def extract_data(self) -> list:
        show_message("INFO", f"extracting data")
        for data in self.xhr_page:
            new_data = {}
            new_data['name'] = data.get("name_in_competition", "")
            new_data['date'] = data.get("time", "")
            new_data['type'] = "match"
            self.uncleaned_data.append(new_data)
        show_message("INFO", f"{len(self.uncleaned_data)} data extracted")

    def name_is_valid(self, name:str) -> bool:
        if bool(name) and name != "":
            return True
        print(name)
        return False
        
    def date_is_valid(self, date:str) -> bool:
        try:
            return bool(datetime.fromisoformat(date.strip()))
        except Exception as e:
            print(e)
            return False
        
    def type_is_valid(self, calendar_type:str) -> bool:
        if calendar_type.lower() == "match":
            return True
        print(type)
        return False
        
    def validate_data(self) -> None:
        show_message("INFO", f"validating data")
        for data in self.uncleaned_data:
            new_clean_data = {}
            for key, value in data.items():
                show_message("INFO", f"validating {key}")
                validation_func = getattr(f"self.{key}_is_valid")
                if validation_func(data[key]):
                    new_clean_data[key] = value
                if list(data.keys()) == list(new_clean_data.keys()):
                    self.cleaned_data.append(new_clean_data)
        show_message("INFO", f"{len(self.cleaned_data)} data valid")


    def save_data(self) -> None:
        show_message("INFO", f"saving data to file")
        fm.save_json_data("data.json",self.xhr_page)

    def post_data(self) -> None:
        show_message("INFO", f"post data to API")
        api_url_prod = os.environ.get('API_URL_PROD')
        endpoint = api_url_prod + "api/events/add/multiple"
        api_token_prod = os.environ.get('API_TOKEN_PROD')
        try:
            encode_data = json.dumps(self.cleaned_data)
            # response = requests.post(
            #     url = endpoint,
            #     headers = {
            #         "Content-Type": "application/json",
            #         "Authorization" : api_token_prod
            #     },
            #     data = encode_data,
            #     verify = False,
            #     timeout = 60
            # )
            # print(f"Server response {response.status_code}")
            # print(response.json())

            print(encode_data)
        except Exception as e:
            print(e)