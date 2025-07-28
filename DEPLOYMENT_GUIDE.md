# 🚀 Deployment Guide - Where to Find Your Scraped Data

This guide shows you exactly where to find your scraped startup funding data after deployment on different platforms.

## 📁 Local Deployment

### Docker Compose (Recommended)
```bash
# Deploy with Docker Compose
chmod +x deploy.sh
./deploy.sh
```

**Where to find your data:**
- **Web Interface**: http://localhost:8080
- **CSV File**: http://localhost:8080/funded_startups.csv
- **JSON File**: http://localhost:8080/funded_startups.json
- **Local Files**: `./data/` directory

### Direct Python
```bash
python main.py --sources all --output-format both
```

**Where to find your data:**
- **CSV File**: `funded_startups.csv` in project directory
- **JSON File**: `funded_startups.json` in project directory
- **Logs**: `scraper.log` in project directory

## ☁️ Cloud Deployments

### 1. AWS Deployment

**Deploy to AWS:**
```bash
python cloud_deploy.py
# Choose option 1 (AWS)
```

**Where to find your data:**
- **S3 Bucket**: https://startup-scraper-data.s3.amazonaws.com/
- **EC2 Instance**: SSH into your EC2 instance and check `/app/data/`
- **CloudWatch Logs**: Check AWS Console for scraper logs

**Access URLs:**
- CSV: `https://startup-scraper-data.s3.amazonaws.com/funded_startups.csv`
- JSON: `https://startup-scraper-data.s3.amazonaws.com/funded_startups.json`

### 2. Google Cloud Platform

**Deploy to GCP:**
```bash
python cloud_deploy.py
# Choose option 2 (Google Cloud)
```

**Where to find your data:**
- **Cloud Storage**: `gs://startup-scraper-data/`
- **Compute Instance**: SSH into your VM and check `/app/data/`
- **Cloud Logging**: Check GCP Console for logs

**Access URLs:**
- CSV: `https://storage.googleapis.com/startup-scraper-data/funded_startups.csv`
- JSON: `https://storage.googleapis.com/startup-scraper-data/funded_startups.json`

### 3. Heroku Deployment

**Deploy to Heroku:**
```bash
python cloud_deploy.py
# Choose option 3 (Heroku)
heroku create startup-funding-scraper
git push heroku main
```

**Where to find your data:**
- **Web App**: https://startup-funding-scraper.herokuapp.com/
- **Heroku Logs**: `heroku logs --tail`
- **Downloads**: Use the web interface to download files

### 4. GitHub Actions

**Deploy with GitHub Actions:**
```bash
python cloud_deploy.py
# Choose option 4 (GitHub Actions)
git push origin main
```

**Where to find your data:**
- **GitHub Actions**: Go to your repo → Actions tab
- **Artifacts**: Download from Actions page
- **Repository**: Check for uploaded files in repo

## 🌐 Web Interface

### Built-in Data Viewer
```bash
python data_viewer.py
```

**Access your data at:**
- **Web Interface**: http://localhost:5000
- **API Endpoint**: http://localhost:5000/api/data
- **Download Links**: Available in the web interface

### Features:
- 📊 Real-time data visualization
- 🔍 Search and filter functionality
- 📈 Statistics dashboard
- 📥 Direct download links
- 🔄 Auto-refresh capability

## 📊 Data Formats

### CSV Format
```csv
Company,Website,Round,Amount,Investors,Date,Industry,Location,Source_URL,Description
Sample Tech Company,https://sample.com,Series A,$5M,VC Fund,2024-01-15,Technology,San Francisco,https://crunchbase.com,Description...
```

### JSON Format
```json
[
  {
    "Company": "Sample Tech Company",
    "Website": "https://sample.com",
    "Round": "Series A",
    "Amount": "$5M",
    "Investors": "VC Fund",
    "Date": "2024-01-15",
    "Industry": "Technology",
    "Location": "San Francisco",
    "Source_URL": "https://crunchbase.com",
    "Description": "Description..."
  }
]
```

## 🔧 Monitoring & Logs

### Local Logs
- **Log File**: `scraper.log`
- **Console Output**: Real-time during scraping
- **Error Logs**: Check for failed requests

### Cloud Logs
- **AWS**: CloudWatch Logs
- **GCP**: Cloud Logging
- **Heroku**: `heroku logs --tail`
- **GitHub Actions**: Actions tab in repository

## 📈 Data Analytics

### Built-in Statistics
The web interface provides:
- Total companies scraped
- Total funding rounds
- Average funding amount
- Number of data sources

### Custom Analysis
```python
import pandas as pd

# Load your data
df = pd.read_csv('funded_startups.csv')

# Top funding rounds
print(df['Round'].value_counts())

# Companies by location
print(df['Location'].value_counts())

# Funding amounts
print(df['Amount'].value_counts())
```

## 🔄 Automated Updates

### Scheduled Scraping
```bash
# Add to crontab for daily updates
0 9 * * * cd /path/to/scraper && python main.py --sources all
```

### GitHub Actions (Automated)
- Runs on every push to main branch
- Uploads artifacts automatically
- Sends notifications on completion

## 🚨 Troubleshooting

### No Data Found
1. Check if scraper ran successfully
2. Verify internet connection
3. Check log files for errors
4. Ensure target websites are accessible

### Access Issues
1. **Local**: Check file permissions
2. **Cloud**: Verify security groups/firewall rules
3. **Web Interface**: Ensure port 5000/8080 is open

### Data Quality Issues
1. Check for rate limiting
2. Verify website structure hasn't changed
3. Update scraper selectors if needed

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify all dependencies are installed
3. Ensure proper permissions
4. Test with a single source first

## 🎯 Quick Start

1. **Local Testing:**
   ```bash
   python main.py --sources techcrunch --max-pages 1
   ```

2. **Docker Deployment:**
   ```bash
   ./deploy.sh
   ```

3. **Cloud Deployment:**
   ```bash
   python cloud_deploy.py
   ```

4. **View Results:**
   - Local: http://localhost:8080
   - Web Interface: http://localhost:5000
   - Cloud: Check platform-specific URLs above

Your scraped data will be available in the locations specified above based on your chosen deployment method! 