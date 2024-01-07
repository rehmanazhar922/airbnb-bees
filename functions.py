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

# COLORS
red = lambda text: print(f"{Fore.RED}{text}{Style.RESET_ALL}")
green = lambda text: print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")
yellow = lambda text: print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")
blue = lambda text: print(f"{Fore.BLUE}{text}{Style.RESET_ALL}")
magenta = lambda text: print(f"{Fore.MAGENTA}{text}{Style.RESET_ALL}")
cyan = lambda text: print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
white = lambda text: print(f"{Fore.WHITE}{text}{Style.RESET_ALL}")
black = lambda text: print(f"{Fore.BLACK}{text}{Style.RESET_ALL}")
bright_red = lambda text: print(f"{Fore.LIGHTRED_EX}{text}{Style.RESET_ALL}")
bright_green = lambda text: print(f"{Fore.LIGHTGREEN_EX}{text}{Style.RESET_ALL}")
bright_yellow = lambda text: print(f"{Fore.LIGHTYELLOW_EX}{text}{Style.RESET_ALL}")
bright_blue = lambda text: print(f"{Fore.LIGHTBLUE_EX}{text}{Style.RESET_ALL}")
# COLORS


def getOptions(headless=False):
    ssl._create_default_https_context = ssl._create_unverified_context
    options = ChromeOptions()
    if headless == True:
        green("[+] Headless True ...")
        options.add_argument('--headless')
    else:
        blue('[*] Running in Gui mode ....')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--remote-debugging-port=9230')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    return options


def search(driver, search_location, date_in, date_out):
    base_url = 'https://www.airbnb.com/?_set_bev_on_new_domain=1703352537_MmE1OTYyM2E0MDJh'
    green(f'Dates: ({date_in}, {date_out})')
    driver.get(base_url)
    driver.refresh()
    driver.implicitly_wait(settings.wait_imp)
    try:
        driver.find_element(By.CSS_SELECTOR, 'button.ffgcxut:nth-child(5)').click()
    except Exception as error:
        log(error)
        pass
    sleep(1.5)
    search_bar = driver.find_element(By.CSS_SELECTOR, '#bigsearch-query-location-input')
    for i in search_location:
        search_bar = driver.find_element(By.CSS_SELECTOR, '#bigsearch-query-location-input')
        search_bar.send_keys(i)
        sleep(0.2)
    search_bar.send_keys(Keys.RETURN)
    sleep(1)
    current_url = driver.current_url
    driver.find_element(By.XPATH, elements_address.search_button2).click()
    new_url = wait_url_change(driver, current_url)
    if date_in != None and date_out != None:
        green(f'[+] Changing url ...')
        date_in = datetime.datetime.strptime(str(date_in), '%Y-%m-%d')
        date_out = datetime.datetime.strptime(str(date_out), '%Y-%m-%d')
        new_url = create_custom_airbnb_url(base_url=new_url, start_date=date_in, end_date=date_out)
        driver.get(new_url)
        green(f'[+] Url Changed to: {new_url}')
    else:
        blue(f"[*] Default dates ....")
        

        

def log(string, name='main'):
    with open('main.logs', 'a') as f:
        f.write(f'\n{name}-------{datetime.datetime.now()}\n{string}\n---------{name}\n')

def today():
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    return formatted_date



def parse_airbnb_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    checkin_date = query_params.get('checkin', [None])[0]
    checkout_date = query_params.get('checkout', [None])[0]
    return checkin_date, checkout_date



def create_custom_airbnb_url(base_url, start_date, end_date):
    current_date = datetime.datetime.today()
    cyan(f'[?] TodayDate: ("{current_date}")')
    if start_date < current_date:
        start_date = current_date
    checkin_str = start_date.strftime('%Y-%m-%d')
    checkout_str = end_date.strftime('%Y-%m-%d')
    custom_url = f"{base_url}?&checkin={checkin_str}&checkout={checkout_str}"
    return custom_url



def wait_url_change(driver, current_url):
    new_url = driver.current_url
    while new_url == current_url:
        sleep(1)
        new_url = driver.current_url

    return new_url


def collect_items_urls_of_current_page(driver):
    URLS = []
    
    all_Atag_elements = driver.find_elements(By.XPATH, elements_address.all_Atag_elements)
    for Atag in all_Atag_elements:
        URLS.append(Atag.get_attribute('href'))
        
    return URLS
        
        
def clicl_next_page(driver):
    try:
        next_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, elements_address.next_page_element))
        )
        next_button.click()
        return True
    except:
        return False


def collect_all_pages_urls(driver):
    driver.implicitly_wait(3)
    
    All_urls = []
    
    while True:
        URLS = collect_items_urls_of_current_page(driver)
        for url in URLS:
            url = url.split('?')[0]
            All_urls.append(url)
        pages_end_status = clicl_next_page(driver)
        if pages_end_status == False:
            blue("[+] Urls Collected ....")
            driver.implicitly_wait(settings.wait_imp)
            break
        
    return All_urls
        

