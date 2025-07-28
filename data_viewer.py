#!/usr/bin/env python3
"""
Simple web interface to view scraped startup funding data
"""

import os
import json
import pandas as pd
from flask import Flask, render_template_string, request, jsonify, send_file
from datetime import datetime

app = Flask(__name__)

# HTML template for the data viewer
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Startup Funding Data Viewer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .controls {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
        }
        .search-box {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .filters {
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        .filter-select {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: white;
        }
        .data-table {
            padding: 20px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .download-buttons {
            padding: 20px;
            text-align: center;
        }
        .btn {
            padding: 10px 20px;
            margin: 0 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .btn:hover {
            opacity: 0.8;
        }
        .no-data {
            text-align: center;
            padding: 50px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Startup Funding Data</h1>
            <p>Real-time view of scraped startup funding information</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_companies }}</div>
                <div class="stat-label">Total Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_funding }}</div>
                <div class="stat-label">Total Funding Rounds</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.avg_amount }}</div>
                <div class="stat-label">Average Funding</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.sources }}</div>
                <div class="stat-label">Data Sources</div>
            </div>
        </div>
        
        <div class="controls">
            <input type="text" id="search" class="search-box" placeholder="Search companies, investors, or descriptions...">
            <div class="filters">
                <select id="roundFilter" class="filter-select">
                    <option value="">All Rounds</option>
                    <option value="Seed">Seed</option>
                    <option value="Series A">Series A</option>
                    <option value="Series B">Series B</option>
                    <option value="Series C">Series C</option>
                </select>
                <select id="sourceFilter" class="filter-select">
                    <option value="">All Sources</option>
                    <option value="Crunchbase">Crunchbase</option>
                    <option value="Dealroom">Dealroom</option>
                    <option value="TechCrunch">TechCrunch</option>
                </select>
            </div>
        </div>
        
        <div class="data-table">
            {% if data %}
            <table id="dataTable">
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Round</th>
                        <th>Amount</th>
                        <th>Investors</th>
                        <th>Location</th>
                        <th>Industry</th>
                        <th>Date</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in data %}
                    <tr>
                        <td><strong>{{ item.Company }}</strong></td>
                        <td>{{ item.Round }}</td>
                        <td>{{ item.Amount }}</td>
                        <td>{{ item.Investors }}</td>
                        <td>{{ item.Location }}</td>
                        <td>{{ item.Industry }}</td>
                        <td>{{ item.Date }}</td>
                        <td>{{ item.Source_URL.split('/')[2] if item.Source_URL else '' }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="no-data">
                <h3>No data available</h3>
                <p>Run the scraper first to see data here.</p>
            </div>
            {% endif %}
        </div>
        
        <div class="download-buttons">
            <a href="/download/csv" class="btn btn-primary">📊 Download CSV</a>
            <a href="/download/json" class="btn btn-secondary">📄 Download JSON</a>
            <a href="/refresh" class="btn btn-secondary">🔄 Refresh Data</a>
        </div>
    </div>
    
    <script>
        // Search functionality
        document.getElementById('search').addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('#dataTable tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
        
        // Filter functionality
        function filterTable() {
            const roundFilter = document.getElementById('roundFilter').value;
            const sourceFilter = document.getElementById('sourceFilter').value;
            const rows = document.querySelectorAll('#dataTable tbody tr');
            
            rows.forEach(row => {
                const cells = row.cells;
                const round = cells[1].textContent;
                const source = cells[7].textContent;
                
                const roundMatch = !roundFilter || round.includes(roundFilter);
                const sourceMatch = !sourceFilter || source.includes(sourceFilter);
                
                row.style.display = (roundMatch && sourceMatch) ? '' : 'none';
            });
        }
        
        document.getElementById('roundFilter').addEventListener('change', filterTable);
        document.getElementById('sourceFilter').addEventListener('change', filterTable);
    </script>
</body>
</html>
"""

def load_data():
    """Load scraped data from files"""
    data = []
    
    # Try to load CSV file
    csv_file = 'funded_startups.csv'
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            data = df.to_dict('records')
        except Exception as e:
            print(f"Error loading CSV: {e}")
    
    # Try to load JSON file
    json_file = 'funded_startups.json'
    if os.path.exists(json_file) and not data:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
    
    return data

def calculate_stats(data):
    """Calculate statistics from the data"""
    if not data:
        return {
            'total_companies': 0,
            'total_funding': 0,
            'avg_amount': '$0',
            'sources': 0
        }
    
    total_companies = len(data)
    total_funding = len(data)
    
    # Calculate average funding amount
    amounts = []
    for item in data:
        amount_str = item.get('Amount', '')
        if amount_str:
            # Extract numeric value
            import re
            match = re.search(r'[\d,]+', amount_str.replace(',', ''))
            if match:
                amounts.append(int(match.group()))
    
    avg_amount = f"${sum(amounts) // len(amounts)}M" if amounts else "$0"
    
    # Count unique sources
    sources = set()
    for item in data:
        source = item.get('Source_URL', '')
        if source:
            domain = source.split('/')[2] if len(source.split('/')) > 2 else source
            sources.add(domain)
    
    return {
        'total_companies': total_companies,
        'total_funding': total_funding,
        'avg_amount': avg_amount,
        'sources': len(sources)
    }

@app.route('/')
def index():
    """Main page"""
    data = load_data()
    stats = calculate_stats(data)
    return render_template_string(HTML_TEMPLATE, data=data, stats=stats)

@app.route('/download/csv')
def download_csv():
    """Download CSV file"""
    csv_file = 'funded_startups.csv'
    if os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name='startup_funding_data.csv')
    return "CSV file not found", 404

@app.route('/download/json')
def download_json():
    """Download JSON file"""
    json_file = 'funded_startups.json'
    if os.path.exists(json_file):
        return send_file(json_file, as_attachment=True, download_name='startup_funding_data.json')
    return "JSON file not found", 404

@app.route('/api/data')
def api_data():
    """API endpoint for data"""
    data = load_data()
    return jsonify(data)

@app.route('/refresh')
def refresh():
    """Refresh data by running scraper"""
    try:
        import subprocess
        result = subprocess.run(['python', 'main.py', '--sources', 'all', '--output-format', 'both'], 
                              capture_output=True, text=True)
        return f"Scraper executed. Output: {result.stdout}"
    except Exception as e:
        return f"Error running scraper: {str(e)}"

if __name__ == '__main__':
    print("🌐 Starting Startup Funding Data Viewer...")
    print("📊 Access the web interface at: http://localhost:5000")
    print("📁 Data files will be loaded from: funded_startups.csv/json")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 