#!/usr/bin/env python3
"""
Lead Generation Script for Startup Funding Data
Identifies companies that just raised money for pitching opportunities
"""

import pandas as pd
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

class LeadGenerator:
    """Generate leads from scraped funding data"""
    
    def __init__(self):
        self.leads = []
    
    def load_data(self, csv_file: str = 'funded_startups.csv') -> pd.DataFrame:
        """Load scraped data"""
        try:
            df = pd.read_csv(csv_file)
            print(f"✅ Loaded {len(df)} funding records")
            return df
        except FileNotFoundError:
            print(f"❌ File {csv_file} not found")
            return pd.DataFrame()
    
    def filter_recent_funding(self, df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
        """Filter for recent funding (last N days)"""
        if df.empty:
            return df
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Filter for recent funding
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_df = df[df['Date'] >= cutoff_date]
        
        print(f"🎯 Found {len(recent_df)} recent funding opportunities (last {days} days)")
        return recent_df
    
    def score_leads(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score leads based on funding amount and industry"""
        if df.empty:
            return df
        
        # Calculate lead scores
        def calculate_score(row):
            amount = str(row.get('Amount', '')).lower()
            industry = str(row.get('Industry', '')).lower()
            
            score = 0
            
            # Score based on funding amount
            if 'billion' in amount or 'b' in amount:
                score += 3
            elif 'million' in amount or 'm' in amount:
                score += 2
            else:
                score += 1
            
            # Score based on industry
            if 'artificial intelligence' in industry or 'ai' in industry:
                score += 2
            elif 'data' in industry or 'analytics' in industry:
                score += 2
            elif 'fintech' in industry or 'finance' in industry:
                score += 1
            elif 'health' in industry or 'medical' in industry:
                score += 1
            
            # Score based on funding round
            round_type = str(row.get('Round', '')).lower()
            if 'series a' in round_type:
                score += 1
            elif 'series b' in round_type or 'series c' in round_type:
                score += 2
            elif 'series d' in round_type or 'series e' in round_type:
                score += 3
            
            return score
        
        df['Lead_Score'] = df.apply(calculate_score, axis=1)
        
        # Add lead categories
        def categorize_lead(score):
            if score >= 5:
                return 'High Priority'
            elif score >= 3:
                return 'Medium Priority'
            else:
                return 'Low Priority'
        
        df['Lead_Category'] = df['Lead_Score'].apply(categorize_lead)
        
        return df
    
    def identify_pitch_opportunities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Identify specific pitch opportunities"""
        if df.empty:
            return df
        
        def get_pitch_opportunity(row):
            industry = str(row.get('Industry', '')).lower()
            round_type = str(row.get('Round', '')).lower()
            amount = str(row.get('Amount', '')).lower()
            
            if 'artificial intelligence' in industry or 'ai' in industry:
                return 'AI/ML Platform Expansion'
            elif 'data' in industry or 'analytics' in industry:
                return 'Data Platform Scaling'
            elif 'fintech' in industry or 'finance' in industry:
                return 'Financial Technology Solutions'
            elif 'health' in industry or 'medical' in industry:
                return 'Healthcare Technology'
            elif 'series a' in round_type:
                return 'Early-Stage Growth Support'
            elif 'series b' in round_type or 'series c' in round_type:
                return 'Scale-Up Solutions'
            elif 'billion' in amount or 'b' in amount:
                return 'Enterprise-Level Solutions'
            else:
                return 'General Business Solutions'
        
        df['Pitch_Opportunity'] = df.apply(get_pitch_opportunity, axis=1)
        
        return df
    
    def generate_contact_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate contact information for leads"""
        if df.empty:
            return df
        
        def get_contact_info(row):
            website = str(row.get('Website', ''))
            company = str(row.get('Company', ''))
            
            if website and website != 'nan':
                return f"{website}/contact"
            else:
                return f"LinkedIn: {company}"
        
        df['Contact_Info'] = df.apply(get_contact_info, axis=1)
        
        return df
    
    def create_pitch_deck_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Create data for pitch deck preparation"""
        pitch_data = []
        
        for _, row in df.iterrows():
            pitch_info = {
                'Company': row.get('Company', ''),
                'Industry': row.get('Industry', ''),
                'Funding_Amount': row.get('Amount', ''),
                'Funding_Round': row.get('Round', ''),
                'Investors': row.get('Investors', ''),
                'Location': row.get('Location', ''),
                'Lead_Score': row.get('Lead_Score', 0),
                'Lead_Category': row.get('Lead_Category', ''),
                'Pitch_Opportunity': row.get('Pitch_Opportunity', ''),
                'Contact_Info': row.get('Contact_Info', ''),
                'Website': row.get('Website', ''),
                'Date_Funded': row.get('Date', ''),
                'Description': row.get('Description', '')
            }
            pitch_data.append(pitch_info)
        
        return pitch_data
    
    def export_lead_data(self, df: pd.DataFrame, filename: str = 'lead_generation_data.csv'):
        """Export lead generation data"""
        if not df.empty:
            df.to_csv(filename, index=False)
            print(f"📊 Lead data exported to {filename}")
            
            # Also export as JSON for API consumption
            json_filename = filename.replace('.csv', '.json')
            df.to_json(json_filename, orient='records', indent=2)
            print(f"📄 Lead data exported to {json_filename}")
    
    def print_lead_summary(self, df: pd.DataFrame):
        """Print summary of lead generation results"""
        if df.empty:
            print("❌ No leads found")
            return
        
        print("\n🎯 LEAD GENERATION SUMMARY")
        print("=" * 50)
        
        # High priority leads
        high_priority = df[df['Lead_Category'] == 'High Priority']
        print(f"🔥 High Priority Leads: {len(high_priority)}")
        
        for _, lead in high_priority.head(5).iterrows():
            print(f"   • {lead['Company']} - {lead['Amount']} {lead['Round']}")
            print(f"     Industry: {lead['Industry']} | Opportunity: {lead['Pitch_Opportunity']}")
        
        # Industry breakdown
        print(f"\n📊 Industry Breakdown:")
        industry_counts = df['Industry'].value_counts()
        for industry, count in industry_counts.head(5).items():
            print(f"   • {industry}: {count} leads")
        
        # Funding amount breakdown
        print(f"\n💰 Funding Amount Breakdown:")
        amount_counts = df['Amount'].value_counts()
        for amount, count in amount_counts.head(5).items():
            print(f"   • {amount}: {count} companies")
        
        # Top opportunities
        print(f"\n🎯 Top Pitch Opportunities:")
        opportunity_counts = df['Pitch_Opportunity'].value_counts()
        for opportunity, count in opportunity_counts.head(5).items():
            print(f"   • {opportunity}: {count} leads")

def main():
    """Main lead generation process"""
    print("🚀 Starting Lead Generation Process...")
    
    # Initialize lead generator
    generator = LeadGenerator()
    
    # Load scraped data
    df = generator.load_data()
    if df.empty:
        print("❌ No data to process")
        return
    
    # Filter for recent funding
    recent_df = generator.filter_recent_funding(df, days=30)
    if recent_df.empty:
        print("❌ No recent funding found")
        return
    
    # Score leads
    scored_df = generator.score_leads(recent_df)
    
    # Identify pitch opportunities
    opportunity_df = generator.identify_pitch_opportunities(scored_df)
    
    # Generate contact info
    final_df = generator.generate_contact_info(opportunity_df)
    
    # Export results
    generator.export_lead_data(final_df)
    
    # Print summary
    generator.print_lead_summary(final_df)
    
    # Create pitch deck data
    pitch_data = generator.create_pitch_deck_data(final_df)
    
    print(f"\n✅ Lead generation completed!")
    print(f"📈 Total leads identified: {len(final_df)}")
    print(f"🎯 High priority leads: {len(final_df[final_df['Lead_Category'] == 'High Priority'])}")

if __name__ == "__main__":
    main() 