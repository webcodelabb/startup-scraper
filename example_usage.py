#!/usr/bin/env python3
"""
Example usage of the startup funding scraper
"""

from utils import setup_logging, validate_data, deduplicate_data, export_to_csv, export_to_json, print_summary
from crunchbase_scraper import CrunchbaseScraper
from dealroom_scraper import DealroomScraper
from techcrunch_scraper import TechCrunchScraper

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Setup logging
    logger = setup_logging()
    
    # Initialize scrapers
    scrapers = {
        'crunchbase': CrunchbaseScraper(logger),
        'dealroom': DealroomScraper(logger),
        'techcrunch': TechCrunchScraper(logger)
    }
    
    # Collect data from all sources
    all_data = []
    for source_name, scraper in scrapers.items():
        print(f"Scraping {source_name}...")
        try:
            data = scraper.scrape()
            all_data.extend(data)
            print(f"Found {len(data)} entries from {source_name}")
        except Exception as e:
            print(f"Error scraping {source_name}: {e}")
    
    # Process data
    if all_data:
        validated_data = validate_data(all_data)
        unique_data = deduplicate_data(validated_data)
        
        # Export to both formats
        export_to_csv(unique_data, 'example_output.csv')
        export_to_json(unique_data, 'example_output.json')
        
        print_summary(unique_data)
    else:
        print("No data was scraped")

def example_single_source():
    """Example of scraping a single source"""
    print("\n=== Single Source Example ===")
    
    logger = setup_logging()
    
    # Only scrape TechCrunch
    scraper = TechCrunchScraper(logger)
    
    try:
        data = scraper.scrape()
        if data:
            validated_data = validate_data(data)
            unique_data = deduplicate_data(validated_data)
            
            export_to_csv(unique_data, 'techcrunch_only.csv')
            print_summary(unique_data)
        else:
            print("No data found from TechCrunch")
    except Exception as e:
        print(f"Error: {e}")

def example_custom_processing():
    """Example of custom data processing"""
    print("\n=== Custom Processing Example ===")
    
    logger = setup_logging()
    
    # Scrape all sources
    scrapers = {
        'crunchbase': CrunchbaseScraper(logger),
        'dealroom': DealroomScraper(logger),
        'techcrunch': TechCrunchScraper(logger)
    }
    
    all_data = []
    for scraper in scrapers.values():
        try:
            data = scraper.scrape()
            all_data.extend(data)
        except Exception as e:
            print(f"Error: {e}")
    
    if all_data:
        # Custom filtering - only Series A and above
        filtered_data = []
        for item in all_data:
            round_type = item.get('Round', '').lower()
            if any(series in round_type for series in ['series a', 'series b', 'series c', 'series d']):
                filtered_data.append(item)
        
        print(f"Filtered to {len(filtered_data)} Series A+ entries")
        
        # Custom sorting by amount
        def extract_numeric_amount(amount_str):
            if not amount_str:
                return 0
            # Extract numeric value from amount string
            import re
            match = re.search(r'[\d,]+', amount_str.replace(',', ''))
            if match:
                return int(match.group())
            return 0
        
        sorted_data = sorted(filtered_data, 
                           key=lambda x: extract_numeric_amount(x.get('Amount', '')), 
                           reverse=True)
        
        # Export top 10 by amount
        top_10 = sorted_data[:10]
        export_to_csv(top_10, 'top_10_by_amount.csv')
        
        print("Exported top 10 entries by funding amount")

def example_error_handling():
    """Example of robust error handling"""
    print("\n=== Error Handling Example ===")
    
    logger = setup_logging()
    
    scrapers = {
        'crunchbase': CrunchbaseScraper(logger),
        'dealroom': DealroomScraper(logger),
        'techcrunch': TechCrunchScraper(logger)
    }
    
    successful_data = []
    failed_sources = []
    
    for source_name, scraper in scrapers.items():
        try:
            print(f"Attempting to scrape {source_name}...")
            data = scraper.scrape()
            successful_data.extend(data)
            print(f"✅ {source_name}: {len(data)} entries")
        except Exception as e:
            print(f"❌ {source_name}: {e}")
            failed_sources.append(source_name)
            logger.error(f"Failed to scrape {source_name}: {e}")
    
    if successful_data:
        print(f"\nSuccessfully scraped {len(successful_data)} entries")
        validated_data = validate_data(successful_data)
        unique_data = deduplicate_data(validated_data)
        
        export_to_csv(unique_data, 'successful_scrapes.csv')
        print_summary(unique_data)
    
    if failed_sources:
        print(f"\nFailed sources: {', '.join(failed_sources)}")

if __name__ == '__main__':
    print("🚀 Startup Funding Scraper - Example Usage")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_single_source()
    example_custom_processing()
    example_error_handling()
    
    print("\n✅ All examples completed!") 