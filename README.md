# Cloud Log Monitoring and Failure Detection System

## Project Overview

The Cloud Log Monitoring and Failure Detection System is a web-based monitoring application designed to collect, analyze, and display cloud application logs.

The system automatically identifies log severity levels such as INFO, WARNING, ERROR, and CRITICAL. It detects failures from ERROR and CRITICAL logs and displays important information through a centralized dashboard.

## Objectives

- Monitor application logs from a centralized dashboard.
- Detect failures automatically.
- Classify logs according to severity.
- Display recent failure alerts.
- Maintain a history of application logs.
- Provide statistics about errors, warnings, and critical failures.
- Support DevOps practices such as monitoring, centralized logging, version control, and cloud deployment.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Git
- Microsoft Azure
- Terraform
- REST API

## System Features

### 1. Log Monitoring

The system reads application logs and stores them in a SQLite database.

### 2. Failure Detection

The failure detector analyzes each log and identifies:

- INFO
- WARNING
- ERROR
- CRITICAL

ERROR and CRITICAL logs are automatically classified as failures.

### 3. Dashboard

The dashboard displays:

- Total Logs
- Errors
- Warnings
- Critical Logs
- Recent Alerts
- Complete Log History

### 4. Log Analysis

Users can enter a new log message through the dashboard. The system automatically determines its severity and whether it represents a failure.

### 5. Centralized Logging

All processed logs are stored in the SQLite database and displayed through the dashboard.

## Project Structure

```text
cloud_log_monitoring/
│
├── app.py
├── requirements.txt
│
├── database/
│   └── logs.db
│
├── detector/
│   ├── __init__.py
│   └── failure_detector.py
│
├── logs/
│   └── sample.log
│
├── templates/
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── tests/
│   ├── __init__.py
│   └── test_detector.py
│
├── terraform/
│   └── main.tf
│
└── README.md