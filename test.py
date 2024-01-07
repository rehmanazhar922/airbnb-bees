import scraper
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
from colorama import Fore, Style
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
from selenium.webdriver.common.by import By
import elements_address, settings
import mysql.connector
from mysql.connector import errorcode
import random, os
from functions import *
import host_info
import sql_functions

if __name__ == "__main__":
    urls = ['https://www.airbnb.com/rooms/1008799870939312933', 'https://www.airbnb.com/rooms/1060302114441412450', 'https://www.airbnb.com/rooms/689728522162163802', 'https://www.airbnb.com/rooms/781319695827038652', 'https://www.airbnb.com/rooms/42607847', 'https://www.airbnb.com/rooms/870219261722311500', 'https://www.airbnb.com/rooms/1356589', 'https://www.airbnb.com/rooms/1061643286511469309', 'https://www.airbnb.com/rooms/44631734', 'https://www.airbnb.com/rooms/1036263031866803269', 'https://www.airbnb.com/rooms/791977924894505088', 'https://www.airbnb.com/rooms/51027276', 'https://www.airbnb.com/rooms/616074425366439323', 'https://www.airbnb.com/rooms/849330415575248250', 'https://www.airbnb.com/rooms/47021428', 'https://www.airbnb.com/rooms/34447394', 'https://www.airbnb.com/rooms/29819771', 'https://www.airbnb.com/rooms/17569813', 'https://www.airbnb.com/rooms/17569813', 'https://www.airbnb.com/rooms/1049597675904530259', 'https://www.airbnb.com/rooms/37366203', 'https://www.airbnb.com/rooms/574042663603936365', 'https://www.airbnb.com/rooms/18772874', 'https://www.airbnb.com/rooms/931959396592785968', 'https://www.airbnb.com/rooms/681866498655340344', 'https://www.airbnb.com/rooms/1050923841886263136', 'https://www.airbnb.com/rooms/953076120770181636', 'https://www.airbnb.com/rooms/1048890966932293739', 'https://www.airbnb.com/rooms/34950102', 'https://www.airbnb.com/rooms/900966846681780012', 'https://www.airbnb.com/rooms/24956854', 'https://www.airbnb.com/rooms/771112725120743799']
    driver = Chrome(options=getOptions(headless=False))
    
    try:
        cleaned = False
        for url in urls:
            scraped_data, hoster_profile_link = scraper.scrape_url(driver, url)
            sql_functions.insert_data(data=scraped_data, table_name=settings.airbnb_data_table)
    
        input('Done')
    except:
        driver.quit()
        sleep(3)
        raise