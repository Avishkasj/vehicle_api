from bs4 import BeautifulSoup
import requests

html_text = '''<li class="item round">
    <h2 class="more"><a title="Honda Cd50 Benly 1995 Motorbike" href="https://riyasewana.com/buy/honda-cd50-benly-sale-matugama-7715129">Honda Cd50 Benly 1995 Motorbike</a></h2>
    <div class="imgbox"><a title="Honda Cd50 Benly 1995 Motorbike" href="https://riyasewana.com/buy/honda-cd50-benly-sale-matugama-7715129"><img src="//riyasewana.com/thumb/thumbhonda-cd50-benly-2818343222151.jpg" alt="Honda Cd50 Benly 1995 Motorbike" width="120" height="90" loading="lazy"></a></div>
    <div class="boxtext">
        <div class="boxintxt"> Matugama</div>
        <div class="boxintxt b"> Rs. 14,000</div>
        <div class="boxintxt s"> 2024-02-28</div>
    </div>
    <div class="clear"></div>
</li>'''

soup = BeautifulSoup(html_text, 'html.parser')

title_element = soup.find('h2', class_='more')
if title_element:
    title = title_element.a['title']
else:
    title = "Title Not Available"

price_element = soup.find('div', class_='boxintxt b')
if price_element:
    price = price_element.text.strip()
else:
    price = "Price Not Available"

location_element = soup.find('div', class_='boxintxt')
if location_element:
    location = location_element.text.strip()
else:
    location = "Location Not Available"

print(f"Title: {title}\nPrice: {price}\nLocation: {location}\n")
