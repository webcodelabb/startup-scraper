"""
TechCrunch scraper for funding articles
"""

import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from utils import clean_text, extract_funding_round, extract_amount, extract_date

class TechCrunchScraper(BaseScraper):
    """Scraper for TechCrunch funding articles"""
    
    def __init__(self, logger=None):
        super().__init__(logger)
        self.base_url = "https://techcrunch.com"
        self.funding_url = "https://techcrunch.com/tag/funding/"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape funding data from TechCrunch"""
        self.log_progress("Starting TechCrunch scraping...")
        
        all_data = []
        page = 1
        max_pages = 5  # Limit pages to avoid overwhelming the site
        
        while page <= max_pages:
            self.log_progress(f"Scraping TechCrunch page {page}...")
            
            # For demo purposes, we'll create sample data structure
            # In practice, you'd parse the actual HTML structure
            
            sample_data = self._scrape_sample_page(page)
            if not sample_data:
                break
                
            all_data.extend(sample_data)
            page += 1
            self.delay(1)  # Shorter delay for TechCrunch
        
        self.log_progress(f"TechCrunch scraping completed. Found {len(all_data)} entries.")
        return all_data
    
    def _scrape_sample_page(self, page: int) -> List[Dict[str, Any]]:
        """Scrape a single page - this is a sample implementation"""
        # In a real implementation, you would:
        # 1. Make request to the funding tag page
        # 2. Parse article listings
        # 3. Extract article URLs
        # 4. Scrape individual articles for funding details
        
        # For demo purposes, creating sample data
        sample_data = [
            {
                'Company': f'TechCrunch Startup {page}-1',
                'Website': f'https://techcrunchstartup{page}1.com',
                'Round': 'Series C',
                'Amount': '$25M',
                'Investors': 'Silicon Valley VC, Growth Fund',
                'Date': '2024-01-25',
                'Industry': 'SaaS',
                'Location': 'San Francisco, CA',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': f'TechCrunch Startup {page}-1 raises $25M Series C to scale enterprise SaaS platform.'
            },
            {
                'Company': f'Mobile App {page}-2',
                'Website': f'https://mobileapp{page}2.com',
                'Round': 'Series A',
                'Amount': '$12M',
                'Investors': 'Mobile Ventures, App Fund',
                'Date': '2024-01-22',
                'Industry': 'Mobile Apps',
                'Location': 'Austin, TX',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': f'Mobile App {page}-2 secures $12M Series A for AI-powered mobile platform.'
            },
            {
                'Company': f'EdTech Platform {page}-3',
                'Website': f'https://edtechplatform{page}3.com',
                'Round': 'Seed',
                'Amount': '$4M',
                'Investors': 'Education Fund, Angel Investors',
                'Date': '2024-01-19',
                'Industry': 'Education Technology',
                'Location': 'Boston, MA',
                'Source_URL': f'{self.funding_url}?page={page}',
                'Description': f'EdTech Platform {page}-3 raises $4M seed round for online learning platform.'
            }
        ]
        
        return sample_data
    
    def _parse_article_listing(self, article_element) -> Dict[str, Any]:
        """Parse individual article listing element"""
        data = {}
        
        # Article title
        title_elem = article_element.find('h2', class_='post-block__title')
        if title_elem:
            title_link = title_elem.find('a')
            if title_link:
                data['Article_Title'] = clean_text(self.extract_text(title_link))
                data['Article_URL'] = self.clean_url(self.extract_href(title_link), self.base_url)
        
        # Publication date
        date_elem = article_element.find('time', class_='post-block__time')
        if date_elem:
            data['Date'] = clean_text(self.extract_text(date_elem))
        
        # Article excerpt
        excerpt_elem = article_element.find('div', class_='post-block__content')
        if excerpt_elem:
            data['Description'] = clean_text(self.extract_text(excerpt_elem))
        
        # Extract company name from title
        if data.get('Article_Title'):
            data['Company'] = self._extract_company_from_title(data['Article_Title'])
        
        # Extract funding details from title and excerpt
        if data.get('Article_Title') or data.get('Description'):
            full_text = f"{data.get('Article_Title', '')} {data.get('Description', '')}"
            data['Round'] = extract_funding_round(full_text)
            data['Amount'] = extract_amount(full_text)
        
        # Source URL
        data['Source_URL'] = data.get('Article_URL', self.funding_url)
        
        return data
    
    def _extract_company_from_title(self, title: str) -> str:
        """Extract company name from article title"""
        if not title:
            return ""
        
        # Common patterns in TechCrunch funding article titles
        patterns = [
            r'(\w+(?:\s+\w+)*)\s+raises?\s+',
            r'(\w+(?:\s+\w+)*)\s+secures?\s+',
            r'(\w+(?:\s+\w+)*)\s+lands?\s+',
            r'(\w+(?:\s+\w+)*)\s+closes?\s+',
            r'(\w+(?:\s+\w+)*)\s+announces?\s+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                company_name = clean_text(match.group(1))
                # Filter out common words that aren't company names
                if len(company_name) > 2 and company_name.lower() not in ['the', 'a', 'an']:
                    return company_name
        
        return ""
    
    def _scrape_individual_article(self, article_url: str) -> Dict[str, Any]:
        """Scrape individual article for detailed funding information"""
        soup = self.get_soup(article_url)
        if not soup:
            return {}
        
        data = {}
        
        # Article title
        title_elem = soup.find('h1', class_='article__title')
        if title_elem:
            data['Article_Title'] = clean_text(self.extract_text(title_elem))
        
        # Publication date
        date_elem = soup.find('time')
        if date_elem:
            data['Date'] = clean_text(self.extract_text(date_elem))
        
        # Article content
        content_elem = soup.find('div', class_='article-content')
        if content_elem:
            data['Description'] = clean_text(self.extract_text(content_elem))
        
        # Extract company name
        if data.get('Article_Title'):
            data['Company'] = self._extract_company_from_title(data['Article_Title'])
        
        # Extract funding details
        if data.get('Description'):
            data['Round'] = extract_funding_round(data['Description'])
            data['Amount'] = extract_amount(data['Description'])
            data['Investors'] = self._extract_investors_from_text(data['Description'])
        
        # Source URL
        data['Source_URL'] = article_url
        
        return data
    
    def _extract_investors_from_text(self, text: str) -> str:
        """Extract investor names from article text"""
        if not text:
            return ""
        
        # Common investor patterns
        patterns = [
            r'led\s+by\s+([^,]+)',
            r'investors?\s+include\s+([^.]+)',
            r'backed\s+by\s+([^.]+)',
            r'participated\s+by\s+([^.]+)',
        ]
        
        investors = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean up the investor text
                investor_text = clean_text(match)
                if investor_text and len(investor_text) > 3:
                    investors.append(investor_text)
        
        return ', '.join(investors) if investors else ""
    
    def _extract_location_from_text(self, text: str) -> str:
        """Extract location from article text"""
        if not text:
            return ""
        
        # Common location patterns
        patterns = [
            r'headquartered\s+in\s+([^,]+)',
            r'based\s+in\s+([^,]+)',
            r'located\s+in\s+([^,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return clean_text(match.group(1))
        
        return "" 