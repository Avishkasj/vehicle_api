from bs4 import BeautifulSoup
import requests

# Define the URL
url = "https://riyasewana.com/search"

# Define headers to mimic a legitimate browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
}

# Send a request to the URL with the headers
response = requests.get(url, headers=headers)

# Check the status code to see if the request was successful
if response.status_code == 200:
    print("Request successful")
else:
    print("Request failed with status code:", response.status_code)
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <li> elements with class="item round"
items = soup.find_all("li", class_="item round")

# Iterate over each item and extract relevant information
for item in items:
    title_element = item.find('h2', class_='more')
    title = title_element.a['title'] if title_element else "Title Not Available"

    price_element = item.find('div', class_='boxintxt b')
    price = price_element.text.strip() if price_element else "Price Not Available"

    location_element = item.find('div', class_='boxintxt')
    location = location_element.text.strip() if location_element else "Location Not Available"

    print(f"Title: {title}\nPrice: {price}\nLocation: {location}\n")
