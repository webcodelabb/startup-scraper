#!/usr/bin/env python3
"""
Main script for the startup funding scraper
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

@click.command()
@click.option('--sources', '-s', 
              type=click.Choice(['all', 'crunchbase', 'dealroom', 'techcrunch']),
              default='all', 
              help='Which sources to scrape')
@click.option('--output-format', '-f',
              type=click.Choice(['csv', 'json', 'both']),
              default='csv',
              help='Output format for the data')
@click.option('--output-file', '-o',
              default='funded_startups',
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
    Scrape recently funded startups from Crunchbase, Dealroom, and TechCrunch.
    
    This tool extracts funding data including company names, funding amounts,
    rounds, investors, and other relevant information.
    """
    
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logger = setup_logging()
    logger.setLevel(log_level)
    
    click.echo("🚀 Starting Startup Funding Scraper")
    click.echo(f"Sources: {sources}")
    click.echo(f"Output format: {output_format}")
    click.echo(f"Max pages per source: {max_pages}")
    click.echo("-" * 50)
    
    # Initialize scrapers
    scrapers = {}
    if sources in ['all', 'crunchbase']:
        scrapers['crunchbase'] = CrunchbaseScraper(logger)
    if sources in ['all', 'dealroom']:
        scrapers['dealroom'] = DealroomScraper(logger)
    if sources in ['all', 'techcrunch']:
        scrapers['techcrunch'] = TechCrunchScraper(logger)
    
    # Collect all data
    all_data = []
    
    for source_name, scraper in scrapers.items():
        try:
            click.echo(f"\n📊 Scraping {source_name.title()}...")
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
    
    click.echo(f"\n🎉 Scraping completed successfully!")
    click.echo(f"Total unique entries: {len(unique_data)}")

if __name__ == '__main__':
    main() 