from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
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

    # Check the status code to see if the request was successful
    if response.status_code == 200:
        print("Request successful")
    else:
        print("Request failed with status code:", response.status_code)
        return jsonify({"error": "Request failed"}), 500

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

        # Check the status code to see if the request was successful
        if response_ad.status_code == 200:
            print("Advertisement page request successful")
        else:
            print("Advertisement page request failed with status code:", response_ad.status_code)
            continue

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


if __name__ == '__main__':
    app.run(debug=True)
