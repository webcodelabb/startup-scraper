"""
Crunchbase scraper for funding rounds
"""

import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from utils import clean_text, extract_funding_round, extract_amount, extract_date

class CrunchbaseScraper(BaseScraper):
    """Scraper for Crunchbase funding rounds"""
    
    def __init__(self, logger=None):
        super().__init__(logger)
        self.base_url = "https://www.crunchbase.com"
        self.funding_url = "https://www.crunchbase.com/funding-rounds"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape funding data from Crunchbase"""
        self.log_progress("Starting Crunchbase scraping...")
        
        all_data = []
        page = 1
        max_pages = 5  # Limit pages to avoid overwhelming the site
        
        while page <= max_pages:
            self.log_progress(f"Scraping Crunchbase page {page}...")
            
            # Note: Crunchbase has anti-bot protection, so we'll use a more conservative approach
            # In a real implementation, you might need to use Selenium or handle JavaScript
            
            # For demo purposes, we'll create sample data structure
            # In practice, you'd parse the actual HTML structure
            
            sample_data = self._scrape_sample_page(page)
            if not sample_data:
                break
                
            all_data.extend(sample_data)
            page += 1
            self.delay(3)  # Longer delay for Crunchbase
        
        self.log_progress(f"Crunchbase scraping completed. Found {len(all_data)} entries.")
        return all_data
    
    def _scrape_sample_page(self, page: int) -> List[Dict[str, Any]]:
        """Scrape a single page - this is a sample implementation"""
        # In a real implementation, you would:
        # 1. Make request to the actual page
        # 2. Parse the HTML structure
        # 3. Extract data using proper selectors
        
        # For demo purposes, creating sample data
        sample_data = [
            {
                'Company': f'Sample Tech Company {page}-1',
                'Website': f'https://sample{page}1.com',
                'Round': 'Series A',
                'Amount': '$5M',
                'Investors': 'Venture Capital Fund A, Angel Investor B',
                'Date': '2024-01-15',
                'Industry': 'Technology',
                'Location': 'San Francisco, CA',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': 'Sample Tech Company 1 raised $5M in Series A funding round led by Venture Capital Fund A.'
            },
            {
                'Company': f'AI Startup {page}-2',
                'Website': f'https://aistartup{page}2.com',
                'Round': 'Seed',
                'Amount': '$2.5M',
                'Investors': 'Seed Fund X, Individual Investors',
                'Date': '2024-01-10',
                'Industry': 'Artificial Intelligence',
                'Location': 'New York, NY',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': 'AI Startup 2 secured $2.5M in seed funding to develop machine learning solutions.'
            }
        ]
        
        return sample_data
    
    def _parse_funding_card(self, card_element) -> Dict[str, Any]:
        """Parse individual funding card element"""
        data = {}
        
        # Company name
        company_elem = card_element.find('a', class_='company-name')
        if company_elem:
            data['Company'] = clean_text(self.extract_text(company_elem))
            data['Website'] = self.clean_url(self.extract_href(company_elem), self.base_url)
        
        # Funding amount
        amount_elem = card_element.find('span', class_='funding-amount')
        if amount_elem:
            data['Amount'] = clean_text(self.extract_text(amount_elem))
        
        # Funding round
        round_elem = card_element.find('span', class_='funding-round')
        if round_elem:
            data['Round'] = clean_text(self.extract_text(round_elem))
        
        # Date
        date_elem = card_element.find('span', class_='funding-date')
        if date_elem:
            data['Date'] = clean_text(self.extract_text(date_elem))
        
        # Location
        location_elem = card_element.find('span', class_='location')
        if location_elem:
            data['Location'] = clean_text(self.extract_text(location_elem))
        
        # Industry
        industry_elem = card_element.find('span', class_='industry')
        if industry_elem:
            data['Industry'] = clean_text(self.extract_text(industry_elem))
        
        # Investors
        investors_elem = card_element.find('div', class_='investors')
        if investors_elem:
            data['Investors'] = clean_text(self.extract_text(investors_elem))
        
        # Description
        desc_elem = card_element.find('div', class_='description')
        if desc_elem:
            data['Description'] = clean_text(self.extract_text(desc_elem))
        
        # Source URL
        data['Source_URL'] = self.funding_url
        
        return data
    
    def _extract_funding_round_from_text(self, text: str) -> str:
        """Extract funding round from text using patterns"""
        if not text:
            return ""
        
        # Common Crunchbase funding round patterns
        patterns = [
            r'Series\s+[A-Z]',
            r'Seed\s+Round',
            r'Pre-seed',
            r'Angel\s+Round',
            r'Venture\s+Round',
            r'Growth\s+Round'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return clean_text(match.group())
        
        return extract_funding_round(text)
    
    def _extract_amount_from_text(self, text: str) -> str:
        """Extract funding amount from text"""
        if not text:
            return ""
        
        # Crunchbase specific amount patterns
        patterns = [
            r'\$[\d,]+(?:\.\d+)?\s*(?:million|billion|k|m|b)?',
            r'[\d,]+(?:\.\d+)?\s*(?:million|billion|k|m|b)',
            r'\$[\d,]+(?:\.\d+)?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return clean_text(matches[0])
        
        return "" 