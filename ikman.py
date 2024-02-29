from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/ikman_ads', methods=['GET'])
def get_ikman_ads():
    # Get parameters from the request
    region = request.args.get('region', 'sri-lanka')
    category = request.args.get('category', 'vehicles')
    query = request.args.get('query', 'premio')

    # Define base URL
    base_url = 'https://ikman.lk'

    # Define parameters
    params = {
        "sort": "relevance",
        "buy_now": "0",
        "urgent": "0",
        "query": query,
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

    ad_list = []

    # Extract and append ad information
    for ad in ads:
        ad_info = {}
        # Extract link
        link_element = ad.find('a', class_='card-link--3ssYv')
        if link_element:
            ad_info['link'] = base_url + link_element['href']  # Construct the link properly
        else:
            ad_info['link'] = "Link Not Available"

        title_element = ad.find('h2', class_='heading--2eONR')
        ad_info['title'] = title_element.text.strip() if title_element else "Title Not Available"

        price_element = ad.find('div', class_='price--3SnqI')
        ad_info['price'] = price_element.text.strip() if price_element else "Price Not Available"

        location_element = ad.find('div', class_='description--2-ez3')
        ad_info['location'] = location_element.text.strip() if location_element else "Location Not Available"

        # Extract time and date information
        time_date_div = ad.find('div', class_='updated-time--1DbCk')
        if time_date_div:
            ad_info['time_date'] = time_date_div.text.strip()  # Extract the text from the div element
        else:
            ad_info['time_date'] = "Time and Date Not Available"

        ad_list.append(ad_info)

    return jsonify(ad_list)

if __name__ == '__main__':
    app.run(debug=True)
