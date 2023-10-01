# Web Scraping with Python

## Description

**Web Scraping with Python** is a Python script designed to facilitate web scraping, the process of extracting data from websites. This script leverages Python libraries such as `requests` for making HTTP requests, `BeautifulSoup` for parsing HTML content, and multithreading for efficient data extraction. It can be used as a starting point for building web scrapers for various websites.

## Features

- **Configurability**: The script uses a configuration file, `config.py`, allowing users to specify the target website's URL and headers for making requests. This makes it adaptable to different websites.

- **Multithreading**: To expedite the scraping process, the script employs multithreading. It creates multiple threads to simultaneously collect product links from various pages and gather detailed product information from those links. The number of threads can be adjusted to suit system capabilities.

- **Data Export**: The scraped data is saved to an Excel file (`data.xlsx`) within a designated `data` folder in the script directory. This facilitates easy storage and analysis of the extracted information.

## Prerequisites

Before using this script, ensure you have the following prerequisites installed:

- **Python 3.x**: The script is compatible with Python 3.x versions.

- **Required Libraries**: Install the necessary Python libraries such as `requests`, `BeautifulSoup`, and `pandas` to enable web requests, HTML parsing, and data manipulation.

- **Configuration File**: Create a `config.py` file in the same directory as the script. This file should define the `SITE_DETAILS` variable, which includes the target website's URL and headers for HTTP requests. Customize these values according to the specific website you intend to scrape.

## Usage

To use this script for web scraping, follow these steps:

1. **Configuration**:
   - Clone the repository or download the script.

2. **Execution**:
   - Run the script either in your terminal or an integrated development environment (IDE).

3. **Scraping Process**:
   - The script performs the following tasks:
     - Fetches the specified URL and extracts the total number of pages to scrape.
     - Creates multiple threads to scrape product links from each page concurrently.
     - Utilizes additional threads to scrape detailed product information from the collected links.
     - Saves the scraped data to an Excel file named `data.xlsx` within a `data` folder in the script directory.

4. **Thread Adjustment**:
   - Adjust the number of threads (`threading.active_count() >= 20` and `threading.active_count() > 30`) to match your system's capabilities and the website's responsiveness. Finding the right balance can optimize the scraping process.

## Disclaimer

This script is provided for educational purposes and as a starting point for web scraping projects. It may require modifications to work with specific websites. Users should always scrape websites responsibly and within the boundaries of the website's terms of service and robots.txt file. Unauthorized or unethical web scraping may have legal consequences. Always obtain the necessary permissions and respect the website's policies when scraping data.
