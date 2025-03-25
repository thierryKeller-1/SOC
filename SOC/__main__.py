from scraper1 import scrap_soc_task
import constants as ct
from botasaurus.browser import Driver, browser, Wait


# if __name__ == "__main__":
#     d = PlaywrightDriver()
#     d.navigate_page(ct.BASE_URL)
#     # d.load_page()
#     d.extract_data()
#     d.validate_data()
#     d.save_data()
#     d.post_data()

if __name__ == "__main__":
    scrap_soc_task(ct.BASE_URL)