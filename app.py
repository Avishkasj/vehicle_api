from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/ikman_ads', methods=['GET'])
def get_ikman_ads():
    try:
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

        # Construct the URL
        url = f"{base_url}/en/ads/{region}/{category}?" + "&".join([f"{k}={v}" for k, v in params.items()])

        # Send request and parse HTML
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        ads = soup.find_all('li', class_='normal--2QYVk')

        ad_list = []

        # Extract and append ad information
        for ad in ads:
            ad_info = {}
            # Extract link
            link_element = ad.find('a', class_='card-link--3ssYv')
            if link_element:
                ad_info['link'] = base_url + link_element['href']
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
            ad_info['time_date'] = time_date_div.text.strip() if time_date_div else "Time and Date Not Available"
            
            # Extract image URL
            image_element = ad.find('img', class_='normal-ad--1TyjD')
            ad_info['image_url'] = image_element['src'] if image_element else "Image Not Available"

            ad_list.append(ad_info)

        return jsonify(ad_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        # Get parameters from the request URL
        city = request.args.get('city', default='colombo', type=str)
        type_of_car = request.args.get('type_of_car', default='premio', type=str)
        make = request.args.get('make', default='toyota', type=str)
        registration = request.args.get('registration', default='registered', type=str)

        # Construct the URL dynamically based on parameters
        url = f"https://riyasewana.com/search/cars/{make}/{type_of_car}/{city}/{registration}"

        # Define headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        # Send a request to the URL with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <li> elements with class="item round"
        items = soup.find_all("li", class_="item round")

        results = []

        # Iterate over each item and extract relevant information
        for item in items:
            title_element = item.find('h2', class_='more')
            title = title_element.a['title'] if title_element else "Title Not Available"

            # Extract the link associated with the advertisement
            link = title_element.a['href'] if title_element else "Link Not Available"

            # Send a request to the individual advertisement page
            response_ad = requests.get(link, headers=headers)
            response_ad.raise_for_status()  # Raise HTTPError for bad responses

            # Parse the HTML content of the advertisement page
            soup_ad = BeautifulSoup(response_ad.content, 'html.parser')

            # Extract date and time information
            date_time_element = soup_ad.find('h2', style="font-size:13px;text-align:center;color:#636b75;font-weight:normal;padding:0 0 5px 0;line-height:1.3em;")
            date_time = date_time_element.text.strip() if date_time_element else "Date and Time Not Available"

            # Extract the image URL
            image_element = item.find('img')
            image_url = "https:" + image_element['src'] if image_element else "Image Not Available"

            results.append({
                "title": title,
                "link": link,
                "date_time": date_time,
                "image_url": image_url
            })

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
