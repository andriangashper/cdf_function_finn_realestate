# Norwegian Real Estate Data Scraper

## Overview

This project is a data engineering effort to scrape Norwegian real estate data from [Finn.no](https://www.finn.no) and populate a MongoDB database. The primary goal is to gather data for later analysis and predictions in the field of real estate.

## Table of Contents

- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [MongoDB Configuration](#mongodb-configuration)
- [Example Analysis](#example-analysis)

## Project Structure

The project is organized into three main files:

- **main_pipeline.py**: Contains the main functionality to orchestrate the data scraping process.
- **scraper.scraper.py**: Implements the web scraping logic using asynchronous methods.
- **data.data_management.py**: Manages the MongoDB connection and provides functions for data insertion, retrieval, and manipulation.
- **analysis.ipynb**: Example of analysis one can do with the scraped data. 

## Dependencies

The project relies on the following dependencies:

- `aiohttp`: Asynchronous HTTP client for making web requests.
- `pymongo`: MongoDB driver for Python.
- `beautifulsoup4`: Parsing html text.
- `python-dotenv`: Managing evnironmental variables.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

To run the data scraping process, execute the main_pipeline.py script. It accepts the number of pages to scrape as an argument. For example:

```bash
python main_pipeline.py
```

## MongoDB Configuration

To ensure the seamless functionality of the MongoDB connection string, create a .env file containing the following essential parameters:

- MONGODB_CLUSTER_NAME 
- MONGODB_USERNAME
- MONGODB_PASSWORD 
- MONGODB_COLLECTION_NAME
- MONGODB_DATABASE_NAME 

## Example Analysis

In this repo you can find in the **analysis.ipynb** file some examples of analysis one can do with the scraped data.
Note that here I used PySpark for personal learning purposes. 

## Extra

If you are interested in the data only and/or do not want to go through the troubles of setting up MongoDB and scraping the data yourself, you can find the dataset publicly available here:
[Kaggle](https://www.kaggle.com/datasets/gasperandrian/norwegian-real-estate-ad-scraped-data-from-finn-no)