#!/usr/bin/env python3
"""
Cloud deployment script for the startup funding scraper
"""

import os
import json
import subprocess
from datetime import datetime

def create_aws_config():
    """Create AWS deployment configuration"""
    config = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Startup Funding Scraper on AWS",
        "Resources": {
            "ScraperEC2": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "InstanceType": "t3.medium",
                    "ImageId": "ami-0c02fb55956c7d316",  # Amazon Linux 2
                    "SecurityGroups": ["sg-scraper"],
                    "UserData": {
                        "Fn::Base64": {
                            "Fn::Sub": """
                            #!/bin/bash
                            yum update -y
                            yum install -y docker git
                            systemctl start docker
                            systemctl enable docker
                            
                            # Clone and run scraper
                            git clone https://github.com/your-repo/scraper.git
                            cd scraper
                            docker-compose up -d
                            
                            # Create S3 bucket for data
                            aws s3 mb s3://startup-scraper-data
                            """
                        }
                    }
                }
            },
            "S3Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "startup-scraper-data",
                    "PublicReadPolicy": {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "PublicReadGetObject",
                                "Effect": "Allow",
                                "Principal": "*",
                                "Action": "s3:GetObject",
                                "Resource": "arn:aws:s3:::startup-scraper-data/*"
                            }
                        ]
                    }
                }
            }
        }
    }
    
    with open('aws-cloudformation.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ AWS CloudFormation template created: aws-cloudformation.json")

def create_gcp_config():
    """Create Google Cloud deployment configuration"""
    config = {
        "name": "startup-scraper",
        "machineType": "n1-standard-2",
        "zone": "us-central1-a",
        "disks": [
            {
                "deviceName": "boot",
                "type": "PERSISTENT",
                "boot": True,
                "autoDelete": True,
                "initializeParams": {
                    "sourceImage": "projects/debian-cloud/global/images/family/debian-11"
                }
            }
        ],
        "networkInterfaces": [
            {
                "network": "global/networks/default",
                "accessConfigs": [
                    {
                        "name": "External NAT",
                        "type": "ONE_TO_ONE_NAT"
                    }
                ]
            }
        ],
        "metadata": {
            "items": [
                {
                    "key": "startup-script",
                    "value": """
                    #!/bin/bash
                    apt-get update
                    apt-get install -y docker.io git
                    systemctl start docker
                    systemctl enable docker
                    
                    # Clone and run scraper
                    git clone https://github.com/your-repo/scraper.git
                    cd scraper
                    docker-compose up -d
                    
                    # Upload data to Google Cloud Storage
                    gsutil mb gs://startup-scraper-data
                    """
                }
            ]
        }
    }
    
    with open('gcp-instance.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Google Cloud instance template created: gcp-instance.json")

def create_heroku_config():
    """Create Heroku deployment configuration"""
    # Procfile for Heroku
    procfile_content = """
    web: python main.py --sources all --output-format both
    """
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content.strip())
    
    # Heroku app.json
    app_config = {
        "name": "startup-funding-scraper",
        "description": "Scrape startup funding data from multiple sources",
        "repository": "https://github.com/your-repo/scraper",
        "env": {
            "PYTHON_VERSION": "3.10.0"
        },
        "buildpacks": [
            {
                "url": "heroku/python"
            }
        ]
    }
    
    with open('app.json', 'w') as f:
        json.dump(app_config, f, indent=2)
    
    print("✅ Heroku configuration created: Procfile, app.json")

def create_github_actions():
    """Create GitHub Actions workflow for automated deployment"""
    workflow = {
        "name": "Deploy Scraper",
        "on": {
            "push": {
                "branches": ["main"]
            }
        },
        "jobs": {
            "deploy": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Checkout code",
                        "uses": "actions/checkout@v3"
                    },
                    {
                        "name": "Set up Python",
                        "uses": "actions/setup-python@v4",
                        "with": {
                            "python-version": "3.10"
                        }
                    },
                    {
                        "name": "Install dependencies",
                        "run": "pip install -r requirements.txt"
                    },
                    {
                        "name": "Run scraper",
                        "run": "python main.py --sources all --output-format both"
                    },
                    {
                        "name": "Upload data",
                        "uses": "actions/upload-artifact@v3",
                        "with": {
                            "name": "scraped-data",
                            "path": "*.csv,*.json"
                        }
                    }
                ]
            }
        }
    }
    
    os.makedirs('.github/workflows', exist_ok=True)
    with open('.github/workflows/deploy.yml', 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print("✅ GitHub Actions workflow created: .github/workflows/deploy.yml")

def main():
    """Main deployment configuration generator"""
    print("🚀 Cloud Deployment Configuration Generator")
    print("=" * 50)
    
    print("\nChoose deployment platform:")
    print("1. AWS (EC2 + S3)")
    print("2. Google Cloud Platform")
    print("3. Heroku")
    print("4. GitHub Actions")
    print("5. All platforms")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        create_aws_config()
    elif choice == "2":
        create_gcp_config()
    elif choice == "3":
        create_heroku_config()
    elif choice == "4":
        create_github_actions()
    elif choice == "5":
        create_aws_config()
        create_gcp_config()
        create_heroku_config()
        create_github_actions()
    else:
        print("❌ Invalid choice")
        return
    
    print("\n📋 Deployment Instructions:")
    print("=" * 30)
    
    if choice in ["1", "5"]:
        print("\n🌩️  AWS Deployment:")
        print("1. Install AWS CLI")
        print("2. Run: aws cloudformation create-stack --stack-name scraper --template-body file://aws-cloudformation.json")
        print("3. Access data at: https://startup-scraper-data.s3.amazonaws.com/")
    
    if choice in ["2", "5"]:
        print("\n☁️  Google Cloud Deployment:")
        print("1. Install gcloud CLI")
        print("2. Run: gcloud compute instances create-from-file gcp-instance.json")
        print("3. Access data at: gs://startup-scraper-data/")
    
    if choice in ["3", "5"]:
        print("\n⚡ Heroku Deployment:")
        print("1. Install Heroku CLI")
        print("2. Run: heroku create startup-funding-scraper")
        print("3. Run: git push heroku main")
        print("4. Access data at: https://startup-funding-scraper.herokuapp.com/")
    
    if choice in ["4", "5"]:
        print("\n🔄 GitHub Actions:")
        print("1. Push code to GitHub")
        print("2. Check Actions tab for deployment status")
        print("3. Download artifacts from Actions")

if __name__ == "__main__":
    main() 