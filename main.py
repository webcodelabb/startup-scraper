#!/usr/bin/env python3
"""
Main script for the enhanced startup funding scraper
"""

import click
import logging
from typing import List, Dict, Any
from utils import (
    setup_logging, validate_data, deduplicate_data, 
    export_to_csv, export_to_json, print_summary
)
from crunchbase_scraper import CrunchbaseScraper
from dealroom_scraper import DealroomScraper
from techcrunch_scraper import TechCrunchScraper
from enhanced_scraper import EnhancedScraper
from agency_scraper import AgencyScraper

@click.command()
@click.option('--sources', '-s', 
              type=click.Choice(['all', 'startups', 'agencies', 'enhanced', 'funding']),
              default='all', 
              help='Which sources to scrape')
@click.option('--output-format', '-f',
              type=click.Choice(['csv', 'json', 'both']),
              default='csv',
              help='Output format for the data')
@click.option('--output-file', '-o',
              default='comprehensive_data',
              help='Output filename (without extension)')
@click.option('--max-pages', '-m',
              type=int,
              default=5,
              help='Maximum pages to scrape per source')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Enable verbose logging')
def main(sources: str, output_format: str, output_file: str, max_pages: int, verbose: bool):
    """
    Enhanced scraper for startup funding data and agency information.
    
    This tool extracts comprehensive data including:
    - Recent startup funding rounds
    - Agency and service provider information
    - Contact details and lead generation data
    - Market research and partnership opportunities
    """
    
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logger = setup_logging()
    logger.setLevel(log_level)
    
    click.echo("🚀 Starting Enhanced Startup & Agency Data Scraper")
    click.echo(f"Sources: {sources}")
    click.echo(f"Output format: {output_format}")
    click.echo(f"Max pages per source: {max_pages}")
    click.echo("-" * 50)
    
    # Initialize scrapers based on source selection
    scrapers = {}
    
    if sources in ['all', 'funding']:
        scrapers['crunchbase'] = CrunchbaseScraper(logger)
        scrapers['dealroom'] = DealroomScraper(logger)
        scrapers['techcrunch'] = TechCrunchScraper(logger)
    
    if sources in ['all', 'enhanced']:
        scrapers['enhanced'] = EnhancedScraper(logger)
    
    if sources in ['all', 'agencies']:
        scrapers['agencies'] = AgencyScraper(logger)
    
    if sources == 'startups':
        scrapers['crunchbase'] = CrunchbaseScraper(logger)
        scrapers['techcrunch'] = TechCrunchScraper(logger)
        scrapers['enhanced'] = EnhancedScraper(logger)
    
    # Collect all data
    all_data = []
    
    for source_name, scraper in scrapers.items():
        try:
            click.echo(f"\n📊 Scraping {source_name.title()}...")
            
            if source_name == 'enhanced':
                data = scraper.scrape_all_sources()
            elif source_name == 'agencies':
                data = scraper.scrape()
            else:
                data = scraper.scrape()
                
            all_data.extend(data)
            click.echo(f"✅ {source_name.title()}: {len(data)} entries found")
        except Exception as e:
            click.echo(f"❌ Error scraping {source_name.title()}: {str(e)}")
            logger.error(f"Error scraping {source_name}: {str(e)}")
    
    if not all_data:
        click.echo("❌ No data was scraped. Please check your configuration.")
        return
    
    # Process data
    click.echo(f"\n🔧 Processing {len(all_data)} entries...")
    
    # Validate and clean data
    validated_data = validate_data(all_data)
    click.echo(f"✅ Validated {len(validated_data)} entries")
    
    # Remove duplicates
    unique_data = deduplicate_data(validated_data)
    click.echo(f"✅ Removed duplicates: {len(unique_data)} unique entries")
    
    # Print summary
    print_summary(unique_data)
    
    # Export data
    click.echo(f"\n💾 Exporting data...")
    
    if output_format in ['csv', 'both']:
        csv_filename = f"{output_file}.csv"
        export_to_csv(unique_data, csv_filename)
    
    if output_format in ['json', 'both']:
        json_filename = f"{output_file}.json"
        export_to_json(unique_data, json_filename)
    
    # Create specialized exports
    if sources in ['all', 'enhanced']:
        # Export startup data separately
        startup_data = [item for item in unique_data if item.get('Data_Type') in ['Funding Round', 'Product Launch', 'Early Stage']]
        if startup_data:
            export_to_csv(startup_data, 'startup_funding_data.csv')
            export_to_json(startup_data, 'startup_funding_data.json')
            click.echo(f"📊 Startup funding data: {len(startup_data)} entries")
        
        # Export agency data separately
        agency_data = [item for item in unique_data if item.get('Data_Type') in ['Digital Agency', 'Consulting', 'Technology Agency', 'Marketing Agency', 'Development Agency']]
        if agency_data:
            export_to_csv(agency_data, 'agency_data.csv')
            export_to_json(agency_data, 'agency_data.json')
            click.echo(f"🏢 Agency data: {len(agency_data)} entries")
    
    click.echo(f"\n🎉 Enhanced scraping completed successfully!")
    click.echo(f"Total unique entries: {len(unique_data)}")
    
    # Print data breakdown
    if unique_data:
        data_types = {}
        for item in unique_data:
            data_type = item.get('Data_Type', 'Unknown')
            data_types[data_type] = data_types.get(data_type, 0) + 1
        
        click.echo(f"\n📊 Data Breakdown:")
        for data_type, count in data_types.items():
            click.echo(f"   • {data_type}: {count} entries")

if __name__ == '__main__':
    main() 