# MY LIBS
import functions 
from functions import *
from sql_functions import *
from scraper import *
from profile_mode import *
import settings
import elements_address

# builtin libs
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
sleep = time.sleep



queue = get_queue()
done, location, date_in, date_out, scrape_profile = queue 



def get_driver(headless=False):
    driver = Chrome(options=functions.getOptions(headless=headless))
    return driver

driver = get_driver()

if __name__ == '__main__':
    search(driver, location, date_in, date_out)
    All_urls = collect_all_pages_urls(driver)
    blue(All_urls)
    save_urls(All_urls, location)
    driver.quit()
    driver = get_driver()
    for url in All_urls:
        data, hoster_profile_link = scrape_url(driver=driver, url=url)
        sql_functions.insert_data(data=data, table_name=settings.airbnb_data_table)
        if scrape_profile == 1:
            profile_urls = get_urls_from_profile_url(driver=driver, url=hoster_profile_link)
            for profile_url in profile_urls:
                data, hoster_profile_link = scrape_url(driver=driver, url=profile_url)
                sql_functions.insert_data(data=data, table_name=settings.airbnb_data_table)
        
    
    driver.quit()
    sleep(2)
    green('Done ! ....')
    os._exit(0)