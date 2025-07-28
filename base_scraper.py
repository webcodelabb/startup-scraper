"""
Base scraper class with common functionality
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from fake_useragent import UserAgent
import logging
from config import HEADERS, SCRAPING_CONFIG

class BaseScraper:
    """Base class for all scrapers with common functionality"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.logger = logger or logging.getLogger(__name__)
        self.setup_session()
    
    def setup_session(self):
        """Setup session with rotating user agents"""
        self.session.headers.update(HEADERS)
    
    def rotate_user_agent(self):
        """Rotate user agent to avoid detection"""
        self.session.headers['User-Agent'] = self.ua.random
    
    def make_request(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        if retries is None:
            retries = SCRAPING_CONFIG['max_retries']
        
        for attempt in range(retries):
            try:
                self.rotate_user_agent()
                response = self.session.get(
                    url, 
                    timeout=SCRAPING_CONFIG['timeout']
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(SCRAPING_CONFIG['delay_between_requests'] * (attempt + 1))
                else:
                    self.logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
        
        return None
    
    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Get BeautifulSoup object from URL"""
        response = self.make_request(url)
        if response:
            return BeautifulSoup(response.content, 'html.parser')
        return None
    
    def delay(self, seconds: float = None):
        """Add delay between requests"""
        if seconds is None:
            seconds = SCRAPING_CONFIG['delay_between_requests']
        time.sleep(seconds)
    
    def extract_text(self, element) -> str:
        """Safely extract text from BeautifulSoup element"""
        if element:
            return element.get_text(strip=True)
        return ""
    
    def extract_href(self, element) -> str:
        """Safely extract href from BeautifulSoup element"""
        if element and element.has_attr('href'):
            return element['href']
        return ""
    
    def clean_url(self, url: str, base_url: str = "") -> str:
        """Clean and normalize URL"""
        if not url:
            return ""
        
        # Handle relative URLs
        if url.startswith('/'):
            url = base_url + url
        elif not url.startswith('http'):
            url = base_url + '/' + url
        
        return url
    
    def log_progress(self, message: str):
        """Log progress message"""
        self.logger.info(message)
        print(message)
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement scrape() method") 