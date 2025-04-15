import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/keller/Documents/Jobdev/G2A/SOC/.env")

BASE_URL = "https://widgets.scorenco.com/old/61237b1e4a5cf15b5874d8d4"
APPS_FOLDER_PATH = os.environ.get('APPS_FOLDER_PATH')
API_URL_DEV = os.environ.get('API_URL_DEV')
API_TOKEN_DEV = os.environ.get('API_TOKEN_DEV')
API_URL_PROD = os.environ.get('API_URL_PROD')
API_TOKEN_PROD = os.environ.get('API_TOKEN_PROD')

