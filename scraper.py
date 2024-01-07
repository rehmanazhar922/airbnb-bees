from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ssl, time, datetime
sleep = time.sleep
import elements_address, settings
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import mysql.connector
from mysql.connector import errorcode
import random, os
from colorama import Fore, Style
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functions import *
from threading import Thread
import host_info
import sql_functions
import sys

wait_and_locate = lambda driver, element, timeout=3: WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))

def extract_bed_bath_guest_info(string_to_extract):
    bed = None
    bedrooms = None
    guests = None
    baths = None
    attached_bath = False
    
    categories = string_to_extract.split(' · ')
    for category in categories:
        if ' bed' in category and not category.endswith('bedroom'):
            bed_info = category.split(' ')
            bed = bed_info[0] if bed_info[0].isdigit() else None
        elif ' bedroom' in category:
            bedrooms_info = category.split(' ')
            bedrooms = bedrooms_info[0] if bedrooms_info[0].isdigit() else None
        elif ' guests' in category:
            guests_info = category.split(' ')
            guests = guests_info[0] if guests_info[0].isdigit() else None
        elif ' bath' in category:
            baths_info = category.split(' ')
            baths = baths_info[0] if baths_info[0].isdigit() else None
            
        if 'attached bathroom' in category:
            attached_bath = True
            
    return bed,bedrooms,guests,baths,attached_bath


def translator_popup_cleaner(driver):
    while True:
        try:
            wait_and_locate(driver, elements_address.translation_on_popup, 5)
            wait_and_locate(driver, elements_address.cross_button).click()
            break
        except:pass
    
    
def scroll_down(driver, times):
    for i in range(times):
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.DOWN)
        
def scroll_and_Locate_button(driver):
    scroll_down(driver, 10)
    while True: 
        try:
            advanced_specs_list_button = wait_and_locate(driver, elements_address.show_all_advanced_specs_button_0, 1)
                
            advanced_specs_list_button.click()
            sleep(2)
            break
        except:
            scroll_down(driver, 5)
            
    sleep(3)
            
    #wait_and_locate(driver, elements_address.cross_button).click()
        
            

def scrape_url(driver, url):
    id = url.split('/')[-1]
    green(f"Id: {id}, URL: {url}")
    driver.get(url)
    cleaner = Thread(target=translator_popup_cleaner, args=(driver,))
    cleaner.start()

    'scraper'
    
    try:

        'item basic specs'
        place_type = wait_and_locate(driver, elements_address.place_type).text
        name = wait_and_locate(driver, elements_address.name).text
        #type_of = wait_and_locate(driver, elements_address.type_of, 3).text.replace('\n', ' . ')
        # try:review_stars = wait_and_locate(driver, elements_address.review_stars, 2).text.replace('\n', ' . ')
        # except:review_stars = wait_and_locate(driver, elements_address.review_stars_2, 2).text.replace('\n', ' . ')
        # try:number_of_reviews = wait_and_locate(driver, elements_address.reviews_tag_a, 1).text.replace('\n', ' . ').replace(' reviews', '')
        # except:number_of_reviews = wait_and_locate(driver, elements_address.reviews_tag_a_2, 3).text.replace('\n', ' . ')
        # price_element = wait_and_locate(driver, elements_address.price)
        # price = price_element.find_elements(By.TAG_NAME, 'span')[0].text
        # price_per = price_element.find_elements(By.TAG_NAME, 'span')[1].text
        
        
        'place information'
        try:place_info = wait_and_locate(driver, elements_address.all_info_xpath)
        except:place_info = wait_and_locate(driver, elements_address.all_info_xpath_2)
        
        
        place_info = place_info.find_elements(By.TAG_NAME, 'div')
        place_info_list = []
    
        for div in place_info:
            place_info_list.append(div.text.replace('\n', ''))
            
        bed_bath_guest_table = wait_and_locate(driver, elements_address.bed_bath_guest_table).text
        bed,bedrooms,guests,baths,attached_bath = extract_bed_bath_guest_info(bed_bath_guest_table)
        
        'item advanced specs'
        
        
        scroll_and_Locate_button(driver)
         
        all_specs_element_after_button = wait_and_locate(driver, elements_address.all_specs_element_after_button, 10)
        divs = all_specs_element_after_button.find_elements(By.CLASS_NAME, elements_address.class_name_in_all_element)
        
        
    
        for div in divs:
            category = div.find_element(By.CLASS_NAME, elements_address.class_name_of_catagory).text
                
            specs = div.find_elements(By.TAG_NAME, 'li')
            for li in specs:
                spec = li.text.replace('\n', '')
                data = {'id_of_location': id, 'description': spec}
                sql_functions.insert_amenities_data(data=data, table_name=settings.ammenities)
    
            
        wait_and_locate(driver, elements_address.cross_button).click()
        sleep(1.5)
        
        'hoster specs'
        try:hosted_by = wait_and_locate(driver, elements_address.hosted_by, 1).text.replace('Stay with ', '')
        except:hosted_by = wait_and_locate(driver, elements_address.hosted_by_2, 1).text.replace('Stay with ', '')
        try:hoster_exp = wait_and_locate(driver, elements_address.hosted_exp_ol_list, 1).text.replace('\n', ' . ')
        except:hoster_exp = wait_and_locate(driver, elements_address.hosted_exp_ol_list_2, 1).text.replace('\n', ' . ')
        
        try:hoster_profile_link = wait_and_locate(driver, elements_address.hoster_profile_link_a_tag, 1).get_attribute('href')
        except:hoster_profile_link = wait_and_locate(driver, elements_address.hosted_exp_ol_list_2, 1).get_attribute('href')
    
        
        
        num_reviews, rating_value, hosting_time, notes = host_info.get_details(hoster_profile_link)
        
    
        
        title = name
        location = title.split(' in ')[1]
        host = hosted_by
        typee = place_type
        shared_common = False
        self_check = False
        
        print(id, title, location, host, typee, num_reviews, rating_value, hosting_time, notes, bed, guests ,baths, attached_bath, shared_common, self_check)
        
        data = {
        'id': id,
        'title': title,
        'location': location,
        'host': host,
        'typee': typee,
        'num_reviews': num_reviews,
        'rating_value': rating_value,
        'hosting_time': hosting_time,
        'notes': notes,
        'bed': bed,
        'guests': guests,
        'baths': baths,
        'attached_bath': attached_bath,
        'shared_common': shared_common,
        'self_check': self_check
        }
    
        return data, hoster_profile_link
    except Exception as error:
        red(f"Error: {error}\n\nError on line {sys.exc_info()[-1].tb_lineno}")
        red('PROGRAM IS FAILED !!!!!!!!! \nQuiting Chrome ........ [592]')
        try:
            driver.quit()
            os._exit(592)
        except:
            red('Chrome Already closed !!! ........... [5922]')
            os._exit(5922)
