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
        max_pages = 3  # Limit pages to get recent articles
        
        while page <= max_pages:
            self.log_progress(f"Scraping TechCrunch page {page}...")
            
            # Build URL for pagination
            if page == 1:
                url = self.funding_url
            else:
                url = f"{self.funding_url}page/{page}/"
            
            # Get the page
            soup = self.get_soup(url)
            if not soup:
                self.log_progress(f"Failed to load page {page}")
                break
            
            # Extract article links
            articles = self._extract_article_links(soup)
            if not articles:
                self.log_progress(f"No articles found on page {page}")
                break
            
            # Scrape each article
            for article_url in articles[:5]:  # Limit to 5 articles per page
                try:
                    article_data = self._scrape_individual_article(article_url)
                    if article_data:
                        all_data.append(article_data)
                        self.log_progress(f"Scraped: {article_data.get('Company', 'Unknown')}")
                except Exception as e:
                    self.log_progress(f"Error scraping article {article_url}: {e}")
                
                self.delay(1)  # Be respectful
            
            page += 1
            self.delay(2)  # Delay between pages
        
        self.log_progress(f"TechCrunch scraping completed. Found {len(all_data)} entries.")
        return all_data
    
    def _extract_article_links(self, soup) -> List[str]:
        """Extract article URLs from the funding page"""
        articles = []
        
        # Look for article links in different possible selectors
        selectors = [
            'article a[href*="/2024/"]',  # 2024 articles
            'article a[href*="/2023/"]',  # 2023 articles
            '.post-block__title a',       # Article titles
            'h2 a',                       # Headers
            'a[href*="/tag/funding/"]'   # Funding tag links
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = self.extract_href(link)
                if href and '/tag/funding/' not in href and self.base_url in href:
                    full_url = self.clean_url(href, self.base_url)
                    if full_url not in articles:
                        articles.append(full_url)
        
        return articles[:10]  # Limit to 10 articles per page
    
    def _scrape_individual_article(self, article_url: str) -> Dict[str, Any]:
        """Scrape individual article for detailed funding information"""
        soup = self.get_soup(article_url)
        if not soup:
            return {}
        
        data = {}
        
        # Article title
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            data['Article_Title'] = clean_text(self.extract_text(title_elem))
        
        # Publication date
        date_elem = soup.find('time') or soup.find('span', class_='time')
        if date_elem:
            data['Date'] = clean_text(self.extract_text(date_elem))
        
        # Article content
        content_elem = soup.find('div', class_='article-content') or soup.find('article')
        if content_elem:
            data['Description'] = clean_text(self.extract_text(content_elem))
        
        # Extract company name from title
        if data.get('Article_Title'):
            data['Company'] = self._extract_company_from_title(data['Article_Title'])
        
        # Extract funding details
        if data.get('Description'):
            data['Round'] = extract_funding_round(data['Description'])
            data['Amount'] = extract_amount(data['Description'])
            data['Investors'] = self._extract_investors_from_text(data['Description'])
        
        # Source URL
        data['Source_URL'] = article_url
        
        # Only return if we have meaningful data
        if data.get('Company') and data.get('Amount'):
            return data
        return {}
    
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
            r'(\w+(?:\s+\w+)*)\s+funding',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                company_name = clean_text(match.group(1))
                # Filter out common words that aren't company names
                if len(company_name) > 2 and company_name.lower() not in ['the', 'a', 'an', 'startup', 'company']:
                    return company_name
        
        return ""
    
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
            r'co-led\s+by\s+([^,]+)',
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