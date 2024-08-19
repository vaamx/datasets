import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# Base URL
base_url = "https://diana.sv/categoria/productos/"

# Categories to explore
categories = ["diana/snacks-salados/", "dulces/", "toztecas/", "picnic/"]

# Initialize an empty list to hold product data
products = []

def get_release_date(main_category, sub_category):
    current_year = datetime.now().year
    
    if main_category == "Toztecas":
        return datetime.now() - timedelta(days=365)  # Released 1 year ago
    elif main_category == "Snacks Salados":
        # Randomly assign 25% to be 50 years old
        if random.random() < 0.25:
            return datetime(current_year - 50, 1, 1)
        else:
            # Gradually release over the past 40 years
            years_ago = random.randint(1, 40)
            return datetime(current_year - years_ago, 1, 1)
    else:
        # Gradually release over the past 40 years for other products
        years_ago = random.randint(1, 40)
        return datetime(current_year - years_ago, 1, 1)

def scrape_subcategory_products(url, main_category, sub_category):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all product links
    product_links = soup.find_all('a', class_='ee-media ee-post__media')

    for link in product_links:
        product_url = link['href']
        product_name = product_url.split('/')[-2].replace('-', ' ').title()
        release_date = get_release_date(main_category, sub_category).strftime('%Y-%m-%d')

        print(f"Found product: {product_name}, Released on: {release_date}")

        # Add the product to the list
        products.append({
            "name": product_name,
            "category": main_category.title(),
            "subcategory": sub_category.title(),
            "introduction_date": release_date
        })

def find_and_scrape_subcategories(category_url, main_category):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all subcategory links within the main category
    subcategory_links = soup.find_all('a', class_='ee-media ee-post__media')

    for link in subcategory_links:
        subcategory_url = link['href']
        sub_category_name = subcategory_url.split('/')[-2].replace('-', ' ').title()
        
        # Scrape products in this subcategory
        scrape_subcategory_products(subcategory_url, main_category, sub_category_name)
        time.sleep(1)  # To avoid overwhelming the server with requests

# Loop through each main category
for category in categories:
    if not category.endswith('/'):
        category += '/'
    
    print(f"Processing category: {category}")

    try:
        main_category_name = category.split('/')[-2].replace('-', ' ').title()
    except IndexError:
        print(f"Error processing category: {category}")
        continue  # Skip this category if there is an error

    # Define the full URL for the category
    category_url = base_url + category

    # Now call the function with the correct URL
    find_and_scrape_subcategories(category_url, main_category_name)
    time.sleep(1)

# Convert the list of products to a DataFrame
df = pd.DataFrame(products)

# Save to CSV
df.to_csv('diana_products_dynamic.csv', index=False)

print("Product data scraped and saved to diana_products_dynamic.csv")
