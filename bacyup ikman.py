import requests
from bs4 import BeautifulSoup

# Define base URL
base_url = 'https://ikman.lk'

# Define region and category
region = "sri-lanka"
category = "vehicles"

# Define parameters
params = {
    "sort": "relevance",
    "buy_now": "0",
    "urgent": "0",
    "query": "premio",
    "page": "1"
}

# Remove any parameters with empty values
params = {k: v for k, v in params.items() if v}

# Construct the URL
url = f"{base_url}/en/ads/{region}/{category}?"
url += "&".join([f"{k}={v}" for k, v in params.items()])

# Send request and parse HTML
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')
ads = soup.find_all('li', class_='normal--2QYVk')

# Extract and print ad information
for ad in ads:
    # Extract link
    link_element = ad.find('a', class_='card-link--3ssYv')
    if link_element:
        link = base_url + link_element['href']  # Construct the link properly
    else:
        link = "Link Not Available"

    title_element = ad.find('h2', class_='heading--2eONR')
    title = title_element.text.strip() if title_element else "Title Not Available"

    price_element = ad.find('div', class_='price--3SnqI')
    price = price_element.text.strip() if price_element else "Price Not Available"

    location_element = ad.find('div', class_='description--2-ez3')
    location = location_element.text.strip() if location_element else "Location Not Available"

    # Extract time and date information
    time_date_div = ad.find('div', class_='updated-time--1DbCk')
    if time_date_div:
        time_date_info = time_date_div.text.strip()  # Extract the text from the div element
    else:
        time_date_info = "Time and Date Not Available"

    print(f"Title: {title}\nPrice: {price}\nLocation: {location}\nLink: {link}\nTime and Date: {time_date_info}\n")
