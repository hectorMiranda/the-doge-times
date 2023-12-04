
# CryptoFluxMonitor

## Introduction
CryptoFluxMonitor is a Python-based microservice designed to fetch real-time cryptocurrency prices and Dogecoin-related news, exposing them through a RESTful API.

## Environment Setup
Ensure Python 3 is installed. Set up a virtual environment and install required libraries. Set up environment variables for the Twitter bearer token and cache duration.

## Installation

### Clone the Repository
```bash
git clone https://github.com/hectorMiranda/the-doge-times.git
cd the-doge-times/minux
```

### Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```bash
python -m venv venv
source venv/bin/activate  
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Environment Variables
```bash
export TWITTER_BEARER_TOKEN='your-twitter-bearer-token'
export CACHE_DURATION=300  # In seconds
```

## Running the Program
```bash
python3 crypto_flux_monitor.py
```

## API Endpoints
- `/prices`: Fetches current prices of Bitcoin and Dogecoin.
- `/dogecoin-news`: Aggregates news related to Dogecoin from Twitter.

## Security
Keep environment variables secure. Do not expose sensitive information.

## Support
For issues or questions, open an issue in the GitHub repository.
