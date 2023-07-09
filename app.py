import requests
from flask import Flask, request, jsonify, make_response
from bs4 import BeautifulSoup
import csv
from a3 import scrape_amazon_results

app = Flask(__name__)

def scrape_amazon(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = []
    
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for result in results:
        name = result.find('span', {'class': 'a-size-medium'})
        price = result.find('span', {'class': 'a-offscreen'})
        brand = result.find('span', {'class': 'a-size-base-plus'})
        reviews = result.find('span', {'class': 'a-size-base'})
        rating = result.find('span', {'class': 'a-icon-alt'})
        
        if name and price and brand and reviews and rating:
            data.append({
                'name': name.text.strip(),
                'price': price.text.strip(),
                'brand': brand.text.strip(),
                'reviews': reviews.text.strip(),
                'rating': rating.text.strip().split(' ')[0]
            })
    
    return data

@app.route('/api/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    
    if not url:
        return jsonify({'error': 'Missing URL parameter.'}), 400
    
    try:
        data = scrape_amazon_results(url)
        return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Export data to CSV
    # csv_file = 'amazon_data.csv'
    # with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.DictWriter(file, fieldnames=data[0].keys())
    #     writer.writeheader()
    #     writer.writerows(data)
    
    # return make_response(csv_file, 200)
    

if __name__ == '__main__':
    app.run(debug=True)
