
# CryptoFluxMonitor

## Introduction
CryptoFluxMonitor is a Python-based microservice designed to fetch real-time cryptocurrency prices for Bitcoin and Dogecoin and expose them through a RESTful API. It includes caching to enhance performance and an admin-only flush endpoint secured with a bearer token.

## Environment Setup
Before running CryptoFluxMonitor, make sure you have Python 3 and the required libraries installed. You also need to set up environment variables for the admin bearer token and cache duration.

## Installation

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/hectorMiranda/the-doge-times.git
cd the-doge-times/python
```

### Step 2: Install Dependencies
Install the required Python libraries using pip:
```bash
pip3 install -r requirements.txt
```

### Step 3: Set Environment Variables
Set the `ADMIN_BEARER_TOKEN` environment variable for secure access to the flush endpoint and `CACHE_DURATION` for cache expiration time in seconds:
```bash
export ADMIN_BEARER_TOKEN='your-secret-token'
export CACHE_DURATION=60
```

## Running the Program

Run CryptoFluxMonitor using the following command:
```bash
python3 crypto_flux_monitor.py
```

## API Endpoints

1. **Get Prices**: `GET /prices`
   - Fetches the current prices of Bitcoin and Dogecoin.
   - Cached for a duration specified by the `CACHE_DURATION` environment variable.

2. **Flush Cache**: `POST /flush`
   - Clears the cached cryptocurrency prices. 
   - Requires a bearer token for authentication.

## Security
The `/flush` endpoint requires a bearer token for authentication. Ensure the `ADMIN_BEARER_TOKEN` environment variable is securely set and not exposed.

## Support
For issues or questions, open an issue in the [GitHub repository](https://github.com/hectorMiranda/the-doge-times).
