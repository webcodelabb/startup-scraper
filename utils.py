"""
Utility functions for data processing and export
"""

import re
import pandas as pd
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from config import CSV_COLUMNS, FUNDING_ROUNDS

def setup_logging(log_filename: str = 'scraper.log') -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text data"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def extract_funding_round(text: str) -> str:
    """Extract funding round type from text"""
    if not text:
        return ""
    
    text_lower = text.lower()
    
    for round_type in FUNDING_ROUNDS:
        if round_type in text_lower:
            return round_type.title()
    
    return ""

def extract_amount(text: str) -> str:
    """Extract funding amount from text"""
    if not text:
        return ""
    
    # Common patterns for funding amounts
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

def extract_date(text: str) -> str:
    """Extract and standardize date from text"""
    if not text:
        return ""
    
    # Common date patterns
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',
        r'\d{1,2}-\d{1,2}-\d{4}',
        r'\d{4}-\d{1,2}-\d{1,2}',
        r'\w+ \d{1,2},? \d{4}',
        r'\d{1,2} \w+ \d{4}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return clean_text(matches[0])
    
    return ""

def deduplicate_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate entries based on company name and funding round"""
    seen = set()
    unique_data = []
    
    for item in data:
        # Create a unique key based on company and round
        key = f"{item.get('Company', '').lower()}_{item.get('Round', '').lower()}"
        
        if key not in seen:
            seen.add(key)
            unique_data.append(item)
    
    return unique_data

def export_to_csv(data: List[Dict[str, Any]], filename: str = 'funded_startups.csv') -> None:
    """Export data to CSV format"""
    if not data:
        print("No data to export")
        return
    
    # Ensure all data has the required columns
    df_data = []
    for item in data:
        row = {}
        for column in CSV_COLUMNS:
            row[column] = item.get(column, "")
        df_data.append(row)
    
    df = pd.DataFrame(df_data, columns=CSV_COLUMNS)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data exported to {filename}")

def export_to_json(data: List[Dict[str, Any]], filename: str = 'funded_startups.json') -> None:
    """Export data to JSON format"""
    if not data:
        print("No data to export")
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Data exported to {filename}")

def validate_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate and clean scraped data"""
    validated_data = []
    
    for item in data:
        # Clean all text fields
        cleaned_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                cleaned_item[key] = clean_text(value)
            else:
                cleaned_item[key] = value
        
        # Extract funding round if not already present
        if not cleaned_item.get('Round') and cleaned_item.get('Description'):
            cleaned_item['Round'] = extract_funding_round(cleaned_item['Description'])
        
        # Extract amount if not already present
        if not cleaned_item.get('Amount') and cleaned_item.get('Description'):
            cleaned_item['Amount'] = extract_amount(cleaned_item['Description'])
        
        validated_data.append(cleaned_item)
    
    return validated_data

def print_summary(data: List[Dict[str, Any]]) -> None:
    """Print a summary of scraped data"""
    if not data:
        print("No data scraped")
        return
    
    print(f"\n=== Scraping Summary ===")
    print(f"Total entries: {len(data)}")
    
    # Count by source
    sources = {}
    for item in data:
        source = item.get('Source_URL', 'Unknown')
        if 'crunchbase' in source.lower():
            sources['Crunchbase'] = sources.get('Crunchbase', 0) + 1
        elif 'dealroom' in source.lower():
            sources['Dealroom'] = sources.get('Dealroom', 0) + 1
        elif 'techcrunch' in source.lower():
            sources['TechCrunch'] = sources.get('TechCrunch', 0) + 1
        else:
            sources['Other'] = sources.get('Other', 0) + 1
    
    print("Entries by source:")
    for source, count in sources.items():
        print(f"  {source}: {count}")
    
    # Count by funding round
    rounds = {}
    for item in data:
        round_type = item.get('Round', 'Unknown')
        rounds[round_type] = rounds.get(round_type, 0) + 1
    
    print("\nEntries by funding round:")
    for round_type, count in rounds.items():
        print(f"  {round_type}: {count}") 