
# DogeDataHub

## Introduction
DogeDataHub is a Python-based microservice designed to fetch real-time cryptocurrency prices, Dogecoin-related news, and provide comprehensive Dogecoin data, exposing them through a RESTful API. This service integrates with the Twitter API and implements caching for enhanced performance.

## Environment Setup
Ensure Python 3 is installed. Set up a virtual environment and install required libraries. Set up environment variables for the Twitter bearer token, cache duration, admin bearer token, and additional configuration as required by DogeDataHub.

## Features
- RESTful API for fetching real-time cryptocurrency prices.
- Integration with Twitter API for Dogecoin-related news.
- Caching mechanism for improved performance.
- Extended endpoints for comprehensive Dogecoin data analysis.

## Installation

### Clone the Repository
```bash
git clone https://github.com/hectorMiranda/the-doge-times.git
cd the-doge-times/minux
```

### Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```bash
python3 -m venv .venv

source .venv/bin/activate
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
To run DogeDataHub, execute:
```bash
python3 DogeDataHub.py
```

## API Endpoints
DogeDataHub offers the following endpoints:

- `/currentPrice`: Fetch the current price of Dogecoin.
- `/prices`: Fetches current prices of Bitcoin and Dogecoin.
- `/priceHistory`: Retrieve historical price data for Dogecoin.
- `/marketCap`: Access market capitalization details of Dogecoin.
- `/tradingVolume`: Fetch trading volume data of Dogecoin.
- `/exchangeRates`: Obtain exchange rates of Dogecoin against various currencies.
- `/transactions`: View recent transaction data in the Dogecoin network.
- `/networkStats`: Get statistics about the Dogecoin network.
- `/blockInfo`: Retrieve information about specific blocks in the Dogecoin blockchain.
- `/walletInfo`: Fetch data about specific Dogecoin wallets.
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
