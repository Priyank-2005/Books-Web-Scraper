import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re

st.set_page_config(page_title="Book Price Monitor", layout="wide")

st.title("Competitor Price Monitor (Automated Scraper)")
st.markdown("This bot scrapes **BooksToScrape.com** to find 5-star books under £20.")
st.markdown("---")

def run_scraper():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    books_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for page in range(1, 6):
        status_text.text(f"Scanning Page {page} of 5...")
        try:
            response = requests.get(base_url.format(page), headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('article', class_='product_pod')
            
            for product in products:
                title = product.h3.a['title']
                price = product.find('p', class_='price_color').text
                rating = product.find('p', class_='star-rating')['class'][1]
                books_data.append({"Title": title, "Price": price, "Rating": rating})
            
            progress_bar.progress(page * 20)
            time.sleep(0.5) # Be polite
        except Exception as e:
            st.error(f"Error on page {page}: {e}")
    
    status_text.text("Scraping Complete! Processing Data...")
    return pd.DataFrame(books_data)

def clean_data(df):

    df['Price_Clean'] = df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['Price_Clean'] = pd.to_numeric(df['Price_Clean'], errors='coerce')

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating_Num'] = df['Rating'].map(rating_map)
    
    return df

col1, col2 = st.columns([1, 3])

with col1:
    st.info("**Control Panel**")
    if st.button("Run Live Scraper"):
        with st.spinner("Bot is working..."):
            raw_df = run_scraper()
            clean_df = clean_data(raw_df)
            clean_df.to_csv("clean_books_data.csv", index=False)
            st.success(f"Scraped {len(clean_df)} books!")
            st.session_state['data'] = clean_df

with col2:
    if 'data' not in st.session_state:
        try:
            st.session_state['data'] = pd.read_csv("clean_books_data.csv")
        except:
            st.warning("No data found. Click 'Run Live Scraper'.")

    if 'data' in st.session_state:
        df = st.session_state['data']
        
        top_picks = df[(df['Rating_Num'] == 5) & (df['Price_Clean'] < 20)]
        
        st.subheader(f"💎 Top Value Picks ({len(top_picks)} Found)")
        st.dataframe(top_picks[['Title', 'Price', 'Rating']])
        
        st.subheader("Full Dataset")
        st.dataframe(df)