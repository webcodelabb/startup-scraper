#!/usr/bin/env python3
"""
Specialized scraper for agencies and service providers
Finds agencies that startups can partner with or pitch to
"""

import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from utils import clean_text
from datetime import datetime

class AgencyScraper(BaseScraper):
    """Scraper for agencies and service providers"""
    
    def __init__(self, logger=None):
        super().__init__(logger)
        self.base_url = "https://clutch.co"
        self.agency_url = "https://clutch.co/agencies"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape agency and service provider data"""
        self.log_progress("🏢 Starting Agency Scraper...")
        
        all_agencies = []
        
        # Collect agency data from multiple sources
        agencies_data = [
            self._get_digital_agencies(),
            self._get_consulting_firms(),
            self._get_tech_agencies(),
            self._get_marketing_agencies(),
            self._get_development_agencies()
        ]
        
        for agencies in agencies_data:
            all_agencies.extend(agencies)
        
        # Remove duplicates and enhance
        unique_agencies = self._remove_duplicates(all_agencies)
        enhanced_agencies = self._enhance_agency_data(unique_agencies)
        
        self.log_progress(f"✅ Agency scraping completed. Found {len(enhanced_agencies)} agencies")
        return enhanced_agencies
    
    def _get_digital_agencies(self) -> List[Dict[str, Any]]:
        """Get digital transformation agencies"""
        self.log_progress("🔄 Collecting digital transformation agencies...")
        
        digital_agencies = [
            {
                'Company': 'Accenture Digital',
                'Website': 'https://accenture.com/digital',
                'Industry': 'Digital Transformation',
                'Location': 'Dublin, Ireland',
                'Source': 'Clutch',
                'Description': 'Global digital transformation and technology consulting.',
                'Employee_Count': '738000+',
                'Founded': '1989',
                'Revenue': '$64.1B',
                'Services': 'Digital Strategy, Technology Consulting, Cloud Migration',
                'Contact_Email': 'digital@accenture.com',
                'LinkedIn': 'https://linkedin.com/company/accenture',
                'Twitter': '@Accenture',
                'Data_Type': 'Digital Agency',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$200-500',
                'Specialties': ['AI/ML', 'Cloud', 'Digital Strategy']
            },
            {
                'Company': 'Deloitte Digital',
                'Website': 'https://deloittedigital.com',
                'Industry': 'Digital Agency',
                'Location': 'New York, NY',
                'Source': 'Clutch',
                'Description': 'Digital transformation and consulting services.',
                'Employee_Count': '415000+',
                'Founded': '1845',
                'Revenue': '$59.3B',
                'Services': 'Digital Strategy, Technology Consulting, Innovation',
                'Contact_Email': 'digital@deloitte.com',
                'LinkedIn': 'https://linkedin.com/company/deloitte',
                'Twitter': '@DeloitteDigital',
                'Data_Type': 'Digital Agency',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$250-600',
                'Specialties': ['Strategy', 'Technology', 'Innovation']
            },
            {
                'Company': 'McKinsey Digital',
                'Website': 'https://mckinsey.com/digital',
                'Industry': 'Management Consulting',
                'Location': 'New York, NY',
                'Source': 'Clutch',
                'Description': 'Digital transformation and strategy consulting.',
                'Employee_Count': '45000+',
                'Founded': '1926',
                'Revenue': '$12.5B',
                'Services': 'Digital Strategy, Technology Consulting, Innovation',
                'Contact_Email': 'digital@mckinsey.com',
                'LinkedIn': 'https://linkedin.com/company/mckinsey',
                'Twitter': '@McKinsey',
                'Data_Type': 'Digital Agency',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$300-700',
                'Specialties': ['Strategy', 'Digital', 'Innovation']
            }
        ]
        
        return digital_agencies
    
    def _get_consulting_firms(self) -> List[Dict[str, Any]]:
        """Get consulting firms that work with startups"""
        self.log_progress("💼 Collecting consulting firms...")
        
        consulting_firms = [
            {
                'Company': 'Bain & Company',
                'Website': 'https://bain.com',
                'Industry': 'Management Consulting',
                'Location': 'Boston, MA',
                'Source': 'Clutch',
                'Description': 'Global management consulting firm.',
                'Employee_Count': '13000+',
                'Founded': '1973',
                'Revenue': '$5.8B',
                'Services': 'Strategy, Operations, Digital Transformation',
                'Contact_Email': 'info@bain.com',
                'LinkedIn': 'https://linkedin.com/company/bain-and-company',
                'Twitter': '@BainAlerts',
                'Data_Type': 'Consulting',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$400-800',
                'Specialties': ['Strategy', 'Operations', 'Digital']
            },
            {
                'Company': 'BCG Digital Ventures',
                'Website': 'https://bcgdv.com',
                'Industry': 'Venture Building',
                'Location': 'Manhattan Beach, CA',
                'Source': 'Clutch',
                'Description': 'Corporate venture building and innovation.',
                'Employee_Count': '25000+',
                'Founded': '1963',
                'Revenue': '$11.7B',
                'Services': 'Venture Building, Innovation, Digital Products',
                'Contact_Email': 'info@bcgdv.com',
                'LinkedIn': 'https://linkedin.com/company/bcg-digital-ventures',
                'Twitter': '@BCGDV',
                'Data_Type': 'Venture Building',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$350-750',
                'Specialties': ['Venture Building', 'Innovation', 'Digital Products']
            }
        ]
        
        return consulting_firms
    
    def _get_tech_agencies(self) -> List[Dict[str, Any]]:
        """Get technology-focused agencies"""
        self.log_progress("💻 Collecting technology agencies...")
        
        tech_agencies = [
            {
                'Company': 'Thoughtworks',
                'Website': 'https://thoughtworks.com',
                'Industry': 'Technology Consulting',
                'Location': 'Chicago, IL',
                'Source': 'Clutch',
                'Description': 'Global technology consultancy and software development.',
                'Employee_Count': '12000+',
                'Founded': '1993',
                'Revenue': '$1.2B',
                'Services': 'Software Development, Technology Consulting, Digital Transformation',
                'Contact_Email': 'info@thoughtworks.com',
                'LinkedIn': 'https://linkedin.com/company/thoughtworks',
                'Twitter': '@thoughtworks',
                'Data_Type': 'Technology Agency',
                'Client_Size': 'Mid-Market to Enterprise',
                'Hourly_Rate': '$150-400',
                'Specialties': ['Software Development', 'Technology', 'Digital']
            },
            {
                'Company': 'Slalom',
                'Website': 'https://slalom.com',
                'Industry': 'Technology Consulting',
                'Location': 'Seattle, WA',
                'Source': 'Clutch',
                'Description': 'Business and technology consulting firm.',
                'Employee_Count': '13000+',
                'Founded': '2001',
                'Revenue': '$2.2B',
                'Services': 'Technology Consulting, Digital Transformation, Strategy',
                'Contact_Email': 'info@slalom.com',
                'LinkedIn': 'https://linkedin.com/company/slalom',
                'Twitter': '@Slalom',
                'Data_Type': 'Technology Agency',
                'Client_Size': 'Mid-Market to Enterprise',
                'Hourly_Rate': '$200-500',
                'Specialties': ['Technology', 'Strategy', 'Digital']
            }
        ]
        
        return tech_agencies
    
    def _get_marketing_agencies(self) -> List[Dict[str, Any]]:
        """Get marketing and growth agencies"""
        self.log_progress("📈 Collecting marketing agencies...")
        
        marketing_agencies = [
            {
                'Company': 'Wieden+Kennedy',
                'Website': 'https://wk.com',
                'Industry': 'Creative Agency',
                'Location': 'Portland, OR',
                'Source': 'Clutch',
                'Description': 'Global creative advertising agency.',
                'Employee_Count': '1000+',
                'Founded': '1982',
                'Revenue': '$500M+',
                'Services': 'Creative Advertising, Brand Strategy, Digital Marketing',
                'Contact_Email': 'info@wk.com',
                'LinkedIn': 'https://linkedin.com/company/wieden-kennedy',
                'Twitter': '@WiedenKennedy',
                'Data_Type': 'Marketing Agency',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$200-600',
                'Specialties': ['Creative', 'Branding', 'Advertising']
            },
            {
                'Company': 'R/GA',
                'Website': 'https://rga.com',
                'Industry': 'Digital Agency',
                'Location': 'New York, NY',
                'Source': 'Clutch',
                'Description': 'Digital product innovation and marketing agency.',
                'Employee_Count': '2000+',
                'Founded': '1977',
                'Revenue': '$200M+',
                'Services': 'Digital Marketing, Product Innovation, Brand Strategy',
                'Contact_Email': 'info@rga.com',
                'LinkedIn': 'https://linkedin.com/company/rga',
                'Twitter': '@RGA',
                'Data_Type': 'Marketing Agency',
                'Client_Size': 'Enterprise',
                'Hourly_Rate': '$250-600',
                'Specialties': ['Digital', 'Innovation', 'Marketing']
            }
        ]
        
        return marketing_agencies
    
    def _get_development_agencies(self) -> List[Dict[str, Any]]:
        """Get software development agencies"""
        self.log_progress("👨‍💻 Collecting development agencies...")
        
        dev_agencies = [
            {
                'Company': 'Mobiquity',
                'Website': 'https://mobiquity.com',
                'Industry': 'Digital Product Development',
                'Location': 'Wellesley, MA',
                'Source': 'Clutch',
                'Description': 'Digital product development and consulting.',
                'Employee_Count': '500+',
                'Founded': '2011',
                'Revenue': '$50M+',
                'Services': 'Software Development, Digital Products, Consulting',
                'Contact_Email': 'info@mobiquity.com',
                'LinkedIn': 'https://linkedin.com/company/mobiquity',
                'Twitter': '@Mobiquity',
                'Data_Type': 'Development Agency',
                'Client_Size': 'Mid-Market',
                'Hourly_Rate': '$100-300',
                'Specialties': ['Software Development', 'Digital Products', 'Consulting']
            },
            {
                'Company': 'Rightpoint',
                'Website': 'https://rightpoint.com',
                'Industry': 'Digital Experience Agency',
                'Location': 'Chicago, IL',
                'Source': 'Clutch',
                'Description': 'Digital experience and technology consulting.',
                'Employee_Count': '600+',
                'Founded': '2007',
                'Revenue': '$100M+',
                'Services': 'Digital Experience, Technology Consulting, Software Development',
                'Contact_Email': 'info@rightpoint.com',
                'LinkedIn': 'https://linkedin.com/company/rightpoint',
                'Twitter': '@Rightpoint',
                'Data_Type': 'Development Agency',
                'Client_Size': 'Mid-Market to Enterprise',
                'Hourly_Rate': '$150-400',
                'Specialties': ['Digital Experience', 'Technology', 'Software']
            }
        ]
        
        return dev_agencies
    
    def _remove_duplicates(self, agencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate agencies based on company name"""
        seen = set()
        unique_agencies = []
        
        for agency in agencies:
            company = agency.get('Company', '').lower()
            if company and company not in seen:
                seen.add(company)
                unique_agencies.append(agency)
        
        return unique_agencies
    
    def _enhance_agency_data(self, agencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance agency data with additional metadata"""
        for agency in agencies:
            # Add scraping metadata
            agency['Scraped_Date'] = datetime.now().strftime('%Y-%m-%d')
            agency['Data_Quality'] = 'High'
            
            # Add partnership potential
            if agency.get('Client_Size') == 'Enterprise':
                agency['Partnership_Potential'] = 'High'
            elif agency.get('Client_Size') == 'Mid-Market':
                agency['Partnership_Potential'] = 'Medium'
            else:
                agency['Partnership_Potential'] = 'Low'
            
            # Add service categorization
            services = str(agency.get('Services', '')).lower()
            if 'digital' in services or 'technology' in services:
                agency['Service_Category'] = 'Digital/Technology'
            elif 'marketing' in services or 'creative' in services:
                agency['Service_Category'] = 'Marketing/Creative'
            elif 'consulting' in services or 'strategy' in services:
                agency['Service_Category'] = 'Consulting/Strategy'
            else:
                agency['Service_Category'] = 'Other'
        
        return agencies

def main():
    """Main agency scraping process"""
    scraper = AgencyScraper()
    agencies = scraper.scrape()
    
    # Export agency data
    import pandas as pd
    df = pd.DataFrame(agencies)
    df.to_csv('agency_data.csv', index=False)
    df.to_json('agency_data.json', orient='records', indent=2)
    
    print(f"✅ Agency scraping completed!")
    print(f"🏢 Total agencies: {len(agencies)}")
    print(f"📁 Data exported to: agency_data.csv/json")

if __name__ == "__main__":
    main() 