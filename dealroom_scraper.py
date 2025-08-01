"""
Dealroom scraper for funding rounds
"""

import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from utils import clean_text, extract_funding_round, extract_amount, extract_date

class DealroomScraper(BaseScraper):
    """Scraper for Dealroom funding rounds"""
    
    def __init__(self, logger=None):
        super().__init__(logger)
        self.base_url = "https://app.dealroom.co"
        self.funding_url = "https://app.dealroom.co"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape funding data from Dealroom"""
        self.log_progress("Starting Dealroom scraping...")
        
        all_data = []
        page = 1
        max_pages = 5  # Limit pages to avoid overwhelming the site
        
        while page <= max_pages:
            self.log_progress(f"Scraping Dealroom page {page}...")
            
            # Note: Dealroom requires authentication and has JavaScript-heavy pages
            # In a real implementation, you might need to use Selenium
            
            # For demo purposes, we'll create sample data structure
            sample_data = self._scrape_sample_page(page)
            if not sample_data:
                break
                
            all_data.extend(sample_data)
            page += 1
            self.delay(2)  # Moderate delay for Dealroom
        
        self.log_progress(f"Dealroom scraping completed. Found {len(all_data)} entries.")
        return all_data
    
    def _scrape_sample_page(self, page: int) -> List[Dict[str, Any]]:
        """Scrape a single page - this is a sample implementation"""
        # In a real implementation, you would:
        # 1. Handle authentication/login
        # 2. Navigate to the funding rounds page
        # 3. Parse the JavaScript-rendered content
        # 4. Extract data using proper selectors
        
        # For demo purposes, creating sample data
        sample_data = [
            {
                'Company': f'Dealroom Startup {page}-1',
                'Website': f'https://dealroomstartup{page}1.com',
                'Round': 'Series B',
                'Amount': '$15M',
                'Investors': 'European VC Fund, Growth Capital Partners',
                'Date': '2024-01-20',
                'Industry': 'Fintech',
                'Location': 'London, UK',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': 'Dealroom Startup 1 raised $15M in Series B funding to expand across Europe.'
            },
            {
                'Company': f'HealthTech {page}-2',
                'Website': f'https://healthtech{page}2.com',
                'Round': 'Series A',
                'Amount': '$8M',
                'Investors': 'Healthcare Ventures, Digital Health Fund',
                'Date': '2024-01-18',
                'Industry': 'Healthcare',
                'Location': 'Amsterdam, Netherlands',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': 'HealthTech 2 secured $8M in Series A funding for AI-powered healthcare solutions.'
            },
            {
                'Company': f'Green Energy {page}-3',
                'Website': f'https://greenenergy{page}3.com',
                'Round': 'Seed',
                'Amount': '$3M',
                'Investors': 'Climate Fund, Impact Investors',
                'Date': '2024-01-12',
                'Industry': 'Clean Energy',
                'Location': 'Berlin, Germany',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': 'Green Energy 3 raised $3M in seed funding for sustainable energy solutions.'
            }
        ]
        
        return sample_data
    
    def _parse_funding_card(self, card_element) -> Dict[str, Any]:
        """Parse individual funding card element"""
        data = {}
        
        # Company name
        company_elem = card_element.find('div', class_='company-name')
        if company_elem:
            data['Company'] = clean_text(self.extract_text(company_elem))
        
        # Company website
        website_elem = card_element.find('a', class_='company-website')
        if website_elem:
            data['Website'] = self.clean_url(self.extract_href(website_elem), self.base_url)
        
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
    
    def _extract_european_amount(self, text: str) -> str:
        """Extract funding amount with European formatting"""
        if not text:
            return ""
        
        # Dealroom often uses European formatting (€, £, etc.)
        patterns = [
            r'€[\d,]+(?:\.\d+)?\s*(?:million|billion|k|m|b)?',
            r'£[\d,]+(?:\.\d+)?\s*(?:million|billion|k|m|b)?',
            r'\$[\d,]+(?:\.\d+)?\s*(?:million|billion|k|m|b)?',
            r'[\d,]+(?:\.\d+)?\s*(?:million|billion|k|m|b)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return clean_text(matches[0])
        
        return ""
    
    def _extract_european_date(self, text: str) -> str:
        """Extract date with European formatting"""
        if not text:
            return ""
        
        # European date patterns
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{1,2}-\d{1,2}-\d{4}',
            r'\d{4}-\d{1,2}-\d{1,2}',
            r'\d{1,2}\.\d{1,2}\.\d{4}',  # European format
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return clean_text(matches[0])
        
        return extract_date(text) 