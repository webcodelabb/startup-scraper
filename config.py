"""
Configuration settings for the startup funding scraper
"""

import os
from fake_useragent import UserAgent

# URLs for scraping
URLS = {
    'crunchbase': 'https://www.crunchbase.com/funding-rounds',
    'dealroom': 'https://app.dealroom.co',
    'techcrunch': 'https://techcrunch.com/tag/funding/'
}

# User agent rotation
ua = UserAgent()

# Request headers
HEADERS = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Scraping settings
SCRAPING_CONFIG = {
    'delay_between_requests': 2,  # seconds
    'max_retries': 3,
    'timeout': 30,
    'max_pages': 10,  # Maximum pages to scrape per source
}

# Output settings
OUTPUT_CONFIG = {
    'csv_filename': 'funded_startups.csv',
    'json_filename': 'funded_startups.json',
    'log_filename': 'scraper.log'
}

# CSV column headers
CSV_COLUMNS = [
    'Company',
    'Website', 
    'Round',
    'Amount',
    'Investors',
    'Date',
    'Industry',
    'Location',
    'Source_URL',
    'Description'
]

# Funding round patterns for classification
FUNDING_ROUNDS = [
    'seed', 'series a', 'series b', 'series c', 'series d', 'series e',
    'pre-seed', 'angel', 'venture', 'growth', 'ipo', 'acquisition'
] 