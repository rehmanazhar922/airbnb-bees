import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from functions import *

exemple_urls = [
    'https://www.airbnb.com.sg/users/show/506402644',
    'https://www.airbnb.com/users/show/506877072',
    'https://www.airbnb.com/users/show/9071324',
    'https://www.airbnb.com.sg/users/show/87167559'
]

def extract_hosting_time(soup):
    months_hosting_element = soup.find('span', {'data-testid': 'Months hosting-stat-heading'})
    years_hosting_element = soup.find('span', {'data-testid': 'Years hosting-stat-heading'})

    if months_hosting_element:
        return months_hosting_element.text.strip() + " Months hosting"
    elif years_hosting_element:
        return years_hosting_element.text.strip() + " Years hosting"
    else:
        return "N/A"

def get_details(url):
    cyan(f"User-Url: {url}")
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    response = requests.get(url, headers=headers)
    
    with open('tmp/index.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
        f.close()

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract details
        reviews_element = soup.find('span', {'data-testid': 'Reviews-stat-heading'})
        num_reviews = reviews_element.text if reviews_element else "N/A"

        rating_element = soup.find('span', {'data-testid': 'Rating-stat-heading'})
        rating_value = rating_element.find('div').text.strip() if rating_element else "N/A"

        hosting_time = extract_hosting_time(soup)

        # Extract notes
        notes_element = soup.find('span', class_='_1e2prbn')
        notes = notes_element.text if notes_element else "N/A"
        return num_reviews, rating_value, hosting_time, notes

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None



#print(get_details(exemple_urls[-1]))