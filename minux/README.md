
# CryptoFluxMonitor

## Introduction
CryptoFluxMonitor is a Python-based microservice designed to fetch real-time cryptocurrency prices and Dogecoin-related news, exposing them through a RESTful API.

## Environment Setup
Ensure Python 3 is installed. Set up a virtual environment and install required libraries. Set up environment variables for the Twitter bearer token, cache duration, and admin bearer token.

## Installation

### Clone the Repository
```bash
git clone https://github.com/hectorMiranda/the-doge-times.git
cd the-doge-times/minux
```

### Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Environment Variables
```bash
export TWITTER_BEARER_TOKEN='your-twitter-bearer-token'
export CACHE_DURATION=300  # In seconds
export ADMIN_BEARER_TOKEN='your-admin-bearer-token'
```

## Running the Program
```bash
python3 crypto_flux_monitor.py
```

## API Endpoints
- `/prices`: Fetches current prices of Bitcoin and Dogecoin.
- `/dogecoin-news`: Aggregates news related to Dogecoin from Twitter.
- `/flush`: Flushes the current cache, requires an admin bearer token defined as an environment variable.

## Swagger UI
Access the Swagger UI to interactively explore and test the APIs exposed by this service. Once the service is running, navigate to:
```bash
http://localhost:5000/
```
Here, you can see all the available endpoints, try them out, and view their responses.

## Security
Keep environment variables secure. Do not expose sensitive information.

## Support
For issues or questions, open an issue in the GitHub repository.
