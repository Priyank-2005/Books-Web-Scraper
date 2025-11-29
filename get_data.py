import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_books():
    print("🚀 Starting Scraper with Anti-Blocking...")
    
    # CHANGE 1: Use HTTPS (Secure) instead of HTTP
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    
    # CHANGE 2: Add Headers so we look like a real laptop, not a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    books_data = []

    # Scrape first 5 pages
    for page in range(1, 6):
        print(f"Scraping Page {page}...")
        url = base_url.format(page)
        
        try:
            # CHANGE 3: Add a timeout (wait 10 seconds max)
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if the page actually loaded (Status 200 = OK)
            if response.status_code != 200:
                print(f"Failed to load page {page}. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('article', class_='product_pod')
            
            for product in products:
                try:
                    title = product.h3.a['title']
                    price_text = product.find('p', class_='price_color').text
                    availability = product.find('p', class_='instock availability').text.strip()
                    rating_class = product.find('p', class_='star-rating')['class'][1]
                    
                    books_data.append({
                        "Title": title,
                        "Price": price_text,
                        "Rating": rating_class,
                        "Availability": availability
                    })
                except AttributeError:
                    continue # Skip book if data is missing

            # CHANGE 4: Random sleep (1 to 3 seconds) to act human
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"❌ Error on Page {page}: {e}")
            continue

    # Save to CSV
    if len(books_data) > 0:
        df = pd.DataFrame(books_data)
        df.to_csv("raw_books_data.csv", index=False)
        print(f"SUCCESS! Scraped {len(df)} books. Saved to 'raw_books_data.csv'")
    else:
        print("No data was collected. Check your internet connection.")

if __name__ == "__main__":
    scrape_books()