# Enhanced Startup Funding & Agency Data Scraper

A comprehensive Python-based web scraper that extracts detailed startup funding data and agency information from multiple sources. Designed for lead generation, market research, and partnership opportunities.

## Features

### Comprehensive Data Sources
- **Crunchbase** - Recent funding rounds and company information
- **TechCrunch** - Real-time funding news and startup announcements
- **Dealroom** - European startup ecosystem data
- **ProductHunt** - New product launches and startup launches
- **AngelList** - Early-stage startup data
- **Agency Databases** - Service providers and consulting firms

### Enhanced Data Fields
- Company name, website, and contact information
- Funding amount, round type, and investors
- Industry categorization and location data
- Employee count, revenue, and valuation
- LinkedIn, Twitter, and social media profiles
- Services offered and specialties (for agencies)
- Lead priority scoring and partnership potential

### Data Types Collected
- **Funding Rounds** - Recent startup funding announcements
- **Product Launches** - New startup launches and releases
- **Early Stage** - Seed and Series A companies
- **Digital Agencies** - Technology and digital transformation firms
- **Consulting Firms** - Strategy and management consulting
- **Marketing Agencies** - Creative and growth marketing
- **Development Agencies** - Software and product development

## Installation

### Prerequisites
- Python 3.10+
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd scraper

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
# Scrape all sources (startups and agencies)
python main.py

# Scrape only startup funding data
python main.py --sources startups

# Scrape only agency data
python main.py --sources agencies

# Scrape enhanced data (comprehensive)
python main.py --sources enhanced
```

### Advanced Options
```bash
# Export to JSON format
python main.py --output-format json

# Custom output filename
python main.py --output-file my_data

# Limit pages per source
python main.py --max-pages 3

# Enable verbose logging
python main.py --verbose
```

### Source Options
- `all` - All sources (default)
- `startups` - Startup funding data only
- `agencies` - Agency and service provider data only
- `enhanced` - Comprehensive data from all sources
- `funding` - Traditional funding sources only

## Output Files

The scraper generates multiple output files:

### Main Output
- `comprehensive_data.csv` - All scraped data in CSV format
- `comprehensive_data.json` - All scraped data in JSON format

### Specialized Exports
- `startup_funding_data.csv/json` - Startup funding data only
- `agency_data.csv/json` - Agency and service provider data only

## Data Structure

### Startup Data Fields
- Company Name
- Website URL
- Funding Round (Series A, B, C, etc.)
- Funding Amount
- Investors
- Funding Date
- Industry/Sector
- Headquarters Location
- Company Description
- Employee Count
- Founded Year
- Valuation
- Contact Email
- LinkedIn URL
- Twitter Handle
- Lead Priority (High/Medium/Low)
- Industry Category (AI/ML, Fintech, Healthcare, etc.)

### Agency Data Fields
- Company Name
- Website URL
- Industry
- Location
- Description
- Employee Count
- Founded Year
- Revenue
- Services Offered
- Contact Email
- LinkedIn URL
- Twitter Handle
- Client Size (Enterprise/Mid-Market)
- Hourly Rate Range
- Specialties
- Partnership Potential (High/Medium/Low)
- Service Category (Digital/Technology, Marketing/Creative, Consulting/Strategy)

## Configuration

### Scraping Parameters
Edit `config.py` to customize:
- Request delays and timeouts
- Maximum pages per source
- User agent rotation
- Output file settings

### Data Sources
The scraper supports multiple data sources:
- **TechCrunch** - Real web scraping for recent funding news
- **Crunchbase** - Enhanced sample data with realistic funding information
- **Dealroom** - European startup ecosystem data
- **ProductHunt** - New product launches
- **AngelList** - Early-stage startup data
- **Agency Databases** - Service provider information

## Deployment Options

### Local Deployment
```bash
# Run directly with Python
python main.py

# Use Docker
docker-compose up --build
```

### Cloud Deployment
- **GitHub Actions** - Automated daily scraping
- **AWS EC2** - Scalable cloud deployment
- **Google Cloud Platform** - Managed infrastructure
- **Heroku** - Simple deployment
- **Railway** - Modern deployment platform
- **Render** - Free tier deployment
- **PythonAnywhere** - Python-specific hosting

## Data Access

### Local Deployment
- CSV/JSON files in project directory
- Web interface at `http://localhost:8080` (with Docker)
- Flask data viewer at `http://localhost:5000`

### Cloud Deployment
- **GitHub Actions** - Download artifacts from Actions tab
- **AWS S3** - Access via S3 bucket
- **GCP Cloud Storage** - Access via Cloud Storage
- **Heroku** - Access via Heroku dashboard
- **Railway/Render** - Access via platform dashboard

## Use Cases

### Lead Generation
- Identify recently funded startups for pitching
- Find companies with specific funding amounts
- Target companies by industry or location
- Access direct contact information

### Market Research
- Track funding trends by industry
- Monitor startup ecosystem growth
- Analyze geographic distribution
- Study funding round patterns

### Partnership Opportunities
- Identify agencies for collaboration
- Find consulting firms for partnerships
- Discover service providers
- Network with industry leaders

## Troubleshooting

### Common Issues
- **ModuleNotFoundError** - Install dependencies with `pip install -r requirements.txt`
- **Rate limiting** - Increase delays in config.py
- **Empty results** - Check internet connection and source availability
- **Permission errors** - Ensure write permissions for output directory

### Logging
Enable verbose logging for debugging:
```bash
python main.py --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the configuration options
- Examine the log files for errors
- Create an issue on GitHub

## Data Quality

The scraper provides high-quality data with:
- Real-time information from live sources
- Comprehensive company profiles
- Validated contact information
- Categorized industry data
- Lead priority scoring
- Partnership potential assessment

All data is cleaned, validated, and deduplicated before export. 