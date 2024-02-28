import requests
from bs4 import BeautifulSoup

html_text = requests.get('https://ikman.lk/en/ads/sri-lanka/vehicles').text
soup = BeautifulSoup(html_text, 'lxml')
ads = soup.find_all('li', class_='normal--2QYVk')

for ad in ads:
    title_element = ad.find('h2', class_='heading--2eONR')
    if title_element:
        title = title_element.text.strip()
    else:
        title = "Title Not Available"

    price_element = ad.find('div', class_='price--3SnqI')
    if price_element:
        price = price_element.text.strip()
    else:
        price = "Price Not Available"

    location_element = ad.find('div', class_='description--2-ez3')
    if location_element:
        location = location_element.text.strip()
    else:
        location = "Location Not Available"

    print(f"Title: {title}\nPrice: {price}\nLocation: {location}\n")
