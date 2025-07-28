# 🚀 Startup Funding Scraper

A comprehensive Python-based web scraper that extracts recently funded startup data from Crunchbase, Dealroom, and TechCrunch. This tool is designed for lead generation, market research, and monitoring newly funded startups in tech, health, AI, and finance sectors.

## 📋 Features

- **Multi-Source Scraping**: Extract data from Crunchbase, Dealroom, and TechCrunch
- **Structured Data Export**: CSV and JSON output formats
- **Data Cleaning**: Automatic deduplication and validation
- **Configurable**: CLI options for source selection and output format
- **Rate Limiting**: Built-in delays to respect website policies
- **Error Handling**: Robust error handling and logging
- **User Agent Rotation**: Anti-detection measures

## 🎯 Extracted Data Fields

### From Crunchbase & Dealroom:
- Company Name
- Website URL
- Funding Amount
- Funding Type (Seed, Series A, etc.)
- Funding Date
- Headquarters Location
- Industry/Sector
- Investors (if available)
- Company Description

### From TechCrunch:
- Article Title
- Company Name (parsed from title/content)
- Date Published
- Funding Round Type
- Article URL

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd scraper
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python main.py --help
```

## 🚀 Usage

### Basic Usage

Scrape all sources and export to CSV:
```bash
python main.py
```

### Advanced Usage

**Scrape specific sources:**
```bash
# Only Crunchbase
python main.py --sources crunchbase

# Only TechCrunch
python main.py --sources techcrunch

# Multiple sources
python main.py --sources crunchbase,techcrunch
```

**Export to different formats:**
```bash
# Export to JSON
python main.py --output-format json

# Export to both CSV and JSON
python main.py --output-format both
```

**Custom output file:**
```bash
python main.py --output-file my_startups
```

**Limit pages per source:**
```bash
python main.py --max-pages 3
```

**Verbose logging:**
```bash
python main.py --verbose
```

### CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--sources` | `-s` | Sources to scrape (all/crunchbase/dealroom/techcrunch) | `all` |
| `--output-format` | `-f` | Output format (csv/json/both) | `csv` |
| `--output-file` | `-o` | Output filename (without extension) | `funded_startups` |
| `--max-pages` | `-m` | Max pages per source | `5` |
| `--verbose` | `-v` | Enable verbose logging | `False` |

## 📊 Output Format

### CSV Output
The CSV file contains the following columns:
- Company
- Website
- Round
- Amount
- Investors
- Date
- Industry
- Location
- Source_URL
- Description

### JSON Output
The JSON file contains an array of objects with the same fields as the CSV.

## 🔧 Configuration

### Rate Limiting
Adjust scraping delays in `config.py`:
```python
SCRAPING_CONFIG = {
    'delay_between_requests': 2,  # seconds
    'max_retries': 3,
    'timeout': 30,
    'max_pages': 10,
}
```

### User Agents
The scraper automatically rotates user agents to avoid detection. You can modify the user agent settings in `config.py`.

## ⚠️ Important Notes

### Legal and Ethical Considerations
- **Respect robots.txt**: Always check and respect the robots.txt file of target websites
- **Rate limiting**: The scraper includes built-in delays to avoid overwhelming servers
- **Terms of Service**: Ensure compliance with each website's terms of service
- **Data usage**: Use scraped data responsibly and in accordance with applicable laws

### Technical Limitations
- **Anti-bot protection**: Some sites may have sophisticated anti-bot measures
- **JavaScript rendering**: Some content may require JavaScript execution
- **Authentication**: Some sites may require login credentials
- **Dynamic content**: Site structures may change over time

## 🏗️ Project Structure

```
scraper/
├── main.py                 # Main CLI script
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── base_scraper.py        # Base scraper class
├── crunchbase_scraper.py  # Crunchbase scraper
├── dealroom_scraper.py    # Dealroom scraper
├── techcrunch_scraper.py  # TechCrunch scraper
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔍 Customization

### Adding New Sources
1. Create a new scraper class inheriting from `BaseScraper`
2. Implement the `scrape()` method
3. Add the scraper to the main script
4. Update the CLI options

### Modifying Data Fields
1. Update the `CSV_COLUMNS` list in `config.py`
2. Modify the data extraction logic in individual scrapers
3. Update the validation functions in `utils.py`

## 🐛 Troubleshooting

### Common Issues

**Import errors:**
```bash
pip install -r requirements.txt
```

**Permission errors:**
```bash
chmod +x main.py
```

**No data scraped:**
- Check internet connection
- Verify target websites are accessible
- Enable verbose logging for debugging
- Check if sites have changed their structure

**Rate limiting:**
- Increase delays in `config.py`
- Reduce `max_pages` parameter
- Use different user agents

## 📈 Example Output

```csv
Company,Website,Round,Amount,Investors,Date,Industry,Location,Source_URL,Description
Sample Tech Company 1,https://sample1.com,Series A,$5M,Venture Capital Fund A,2024-01-15,Technology,San Francisco CA,https://crunchbase.com/funding-rounds,Sample Tech Company 1 raised $5M in Series A funding round led by Venture Capital Fund A.
AI Startup 2,https://aistartup2.com,Seed,$2.5M,Seed Fund X,2024-01-10,Artificial Intelligence,New York NY,https://crunchbase.com/funding-rounds,AI Startup 2 secured $2.5M in seed funding to develop machine learning solutions.
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with applicable laws and website terms of service.

## ⚡ Performance Tips

- Use `--max-pages` to limit scraping depth
- Enable `--verbose` for debugging
- Consider running during off-peak hours
- Monitor log files for errors

## 🔗 Related Projects

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Requests](https://requests.readthedocs.io/) - HTTP library
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Click](https://click.palletsprojects.com/) - CLI framework 