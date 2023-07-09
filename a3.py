import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_amazon_results(url, num_pages=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    results = []
    for page in range(1, num_pages + 1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            name_element = product.find('span', {'class': 'a-size-medium'})
            name = name_element.text.strip() if name_element else 'N/A'
            brand_element = product.find('span', {'class': 'a-size-base-plus'})
            brand = brand_element.text.strip() if brand_element else 'N/A'
            rating_element = product.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.text.strip() if rating_element else 'N/A'
            num_ratings_element = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
            num_ratings = num_ratings_element.text.strip() if num_ratings_element else 'N/A'
            comments_element = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
            comments = comments_element.text.strip() if comments_element else 'N/A'
            price_element = product.find('span', {'class': 'a-price-whole'})
            price = price_element.text.strip() if price_element else 'N/A'

            results.append({
                'Name': name,
                'Brand': brand,
                'Star Ratings': rating,
                'Number of Ratings': num_ratings,
                'Comments': comments,
                'Price': price
            })

    return results

def save_to_csv(data):
    filename = 'export.csv'
    filepath = os.path.join(os.path.expanduser("~"), filename)

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Brand', 'Star Ratings', 'Number of Ratings', 'Comments', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    print(f"Data has been saved to {filepath}")

def main():
    default_url = 'https://www.amazon.in/s?k=laptops&ref=nb_sb_noss_1'
    url = input(f"Enter the Amazon search result page URL (default: {default_url}): ")
    url = url.strip() if url.strip() else default_url

    num_pages = int(input("Enter the number of pages to scrape: "))

    data = scrape_amazon_results(url, num_pages)
    save_to_csv(data)

if __name__ == '__main__':
    main()
