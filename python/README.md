Welcome to the python playground for the dogetimes.com

Here are the supported projects:

# CryptoFluxMonitor

## Introduction
CryptoFluxMonitor is a Python-based microservice designed to fetch real-time cryptocurrency prices for Bitcoin and Dogecoin and expose them through a RESTful API. It's a handy tool for those interested in tracking cryptocurrency market trends.

## Environment Setup
Before running CryptoFluxMonitor, make sure you have Python 3 installed on your system. You can download Python from [Python's official website](https://www.python.org/downloads/).

## Installation

### Step 1: Clone the Repository
Begin by cloning the CryptoFluxMonitor repository to your local machine:
```bash
git clone https://github.com/hectorMiranda/the-doge-times.git
cd the-doge-times/python
```

### Step 2: Install Dependencies
Install the required Python libraries using pip:
```bash
pip3 install -r requirements.txt
```

## Running the Program

To run CryptoFluxMonitor locally, navigate to the `python` directory and execute the following command:
```bash
python3 crypto_flux_monitor.py
```
After the service starts, the API will be accessible at `http://localhost:5000/prices`, where you can view the latest cryptocurrency prices.

## Additional Notes

- Ensure you're in the `the-doge-times/python` directory when executing the script.
- The application requires an internet connection to fetch data from cryptocurrency markets.
- Feel free to modify or enhance the script by forking the GitHub repository.

## Support
For issues or questions, please open an issue in the [GitHub repository](https://github.com/hectorMiranda/the-doge-times).
