# MY LIBS
import functions 
from functions import *
from sql_functions import *
from scraper import *
import settings
import elements_address

# builtin libs
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
sleep = time.sleep

wait_and_locate = lambda driver, element, timeout=3: WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))
scroll_into_view = lambda driver, element: driver.execute_script("arguments[0].scrollIntoView(true);", element)


urls = ['https://www.airbnb.com/users/show/217432173', 'https://www.airbnb.com/users/show/51548122']


def listing_keep_scrolling_till_end(driver):
    sleep(1.2)
    while True:
        try:
            button = wait_and_locate(driver=driver, element=elements_address.show_more_button)
            scroll_into_view(driver=driver, element=button)
            sleep(0.5)
            button.click()
            sleep(2)
        except:
            break


def get_urls_from_profile_url(driver, url):
    if "/users/show/" not in url:
        red(f'Not Valid Url: {url}')
        return 404
    driver.get(url)
    sleep(1)
    driver.implicitly_wait(10)
    
    try:
        show_listings_button = wait_and_locate(driver=driver, element=elements_address.show_listings_btn)
        scroll_into_view(driver=driver, element=show_listings_button)
        sleep(1)
        show_listings_button.click()
        more_listings = True
    except:
        more_listings = False
        
    if more_listings == True:
        sleep(2)
        listing_keep_scrolling_till_end(driver=driver)
        all_LISTINGS_a_elements = driver.find_elements(By.XPATH, elements_address.all_a_tags_in_listing)
        green(f"Number of urls: {len(all_LISTINGS_a_elements)}")
        URLS = []
        for a in all_LISTINGS_a_elements:
            url = a.get_attribute('href').split('?')[0]
            cyan(url)
            URLS.append(url)
            
        return URLS
    else:
        yellow(f"'View all listings' button not found .....")
        all_LISTINGS_a_elements = driver.find_elements(By.XPATH, elements_address.current_page_urls)
        green(f"Number of urls: {len(all_LISTINGS_a_elements)}")
        URLS = []
        for a in all_LISTINGS_a_elements:
            url = a.get_attribute('href').split('?')[0]
            cyan(url)
            URLS.append(url)
            
        return URLS
