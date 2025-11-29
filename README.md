# E-commerce Competitor Price Monitor
### *Automating market research so you don't have to.*

![Python](https://img.shields.io/badge/Python-Automation-3776AB)
![BeautifulSoup](https://img.shields.io/badge/Lib-BeautifulSoup4-green)
![Pandas](https://img.shields.io/badge/Data-Cleaning-150458)

---

## What is this?
In e-commerce, pricing is a war. If you check competitor prices manually, you've already lost.

This project is an **automated intelligence bot** that monitors product catalogs (specifically books). It scrapes pricing, availability, and ratings from target websites, creating a structured dataset for analysis. It includes a custom **"Value Algorithm"** that identifies high-rated products that are currently undervalued (low price, high stars).

*Note: This scraper includes "politeness" features (random sleep timers, user-agent rotation) to respect server load and avoid IP bans.*

---

## Key Features
* **Robust Extraction:** Scrapes Title, Price, Star Rating, and Stock Status across multiple paginated pages.
* **Regex Data Cleaning:** Automatically strips currency symbols (`£`, `$`) and converts text ratings ("Five") to integers (5).
* **Value Discovery:** Filters the dataset to find "Hidden Gems" (5-Star items under £20).
* **Anti-Blocking:** Implements User-Agent headers and time delays to mimic human browsing behavior.

---

## Tech Stack
* **Python:** Core scripting language.
* **Requests & BeautifulSoup:** HTML parsing and HTTP requests.
* **Pandas:** Data cleaning and CSV export.
* **Regular Expressions (Regex):** Pattern matching for dirty data.

---

## How to Run Locally

### 1. Clone the Repo
git clone [https://github.com/Priyank-2005/Books-Web-Scraper.git](https://github.com/Priyank-2005/Books-Web-Scraper.git)
cd Books-Web-Scraper

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Run the bot
#### Step 1: Harvest the data
python get_data.py

#### Step 2: Clean and Analyze
python clean_data.py

---

## Created by

**Priyank Bohra** | Data Analyst & Python Developer
