# Data Engineering Pipeline with Hadoop

This project demonstrates an end-to-end data engineering pipeline, covering data collection, processing, distributed storage, and querying using modern big data technologies.

---

## Project Overview

The goal of this project is to design and implement a scalable data pipeline capable of handling diverse data sources, including APIs and web scraping, and storing them efficiently using distributed systems.

The pipeline integrates multiple data sources such as financial data, web-scraped content, and image metadata, processes them, and stores them in both distributed and relational systems for analysis.

---

## Architecture

- Hadoop Cluster (1 Master + 3 Worker Nodes)  
- HDFS for distributed data storage  
- Docker for containerized deployment  
- PostgreSQL for structured data management  

---

## Data Pipeline Workflow

### 1. Data Collection
- Stock market data using Yahoo Finance API  
- Image and metadata scraping from Unsplash using Selenium  
- Web scraping of structured data using BeautifulSoup  

---

### 2. Data Processing
- Data cleaning and preprocessing  
- Handling missing and inconsistent values  
- Feature extraction and transformation  
- Conversion into structured formats (CSV, JSON)  

---

### 3. Data Storage
- HDFS for scalable distributed storage  
- PostgreSQL database for relational storage  
- Normalized schema including:
  - Images  
  - Photographers  
  - Tags  
  - Locations  

---

### 4. Data Ingestion
- Automated ingestion scripts  
- Batch processing for database insertion  
- Use of caching mechanisms to reduce redundant queries  
- Data consistency and integrity checks  

---

### 5. Data Analysis
- SQL queries for business insights  
- Ranking and aggregation queries  
- Pattern analysis across datasets  
- Performance evaluation of data  

---

## Project Structure

data-engineering-pipeline-hadoop/
│
├── report/ # Project documentation (PDF)
├── scripts/ # Python scripts (scraping, ingestion, DB loading)
├── ingestion/ # Pipeline files and configurations
├── data/ # (Optional) metadata / processed data
└── README.md

---

## Scripts Description

- `yfinance_scraper.py`  
  Downloads stock market data using Yahoo Finance API and stores it as CSV  

- `webscraping_unsplash.py`  
  Scrapes images and metadata (views, downloads, tags, photographer) from Unsplash  

- `load_metadata_db.py`  
  Loads processed metadata into PostgreSQL database with proper relational mapping  

- `books_scraper.py`  
  Scrapes structured web data using BeautifulSoup  

---

## Technology Stack

- Python (Pandas, NumPy)  
- Selenium (dynamic web scraping)  
- BeautifulSoup (HTML parsing)  
- PostgreSQL (relational database)  
- Hadoop (HDFS for distributed storage)  
- Docker (environment setup)  

---

## Key Features

- End-to-end data engineering pipeline  
- Integration of multiple heterogeneous data sources  
- Automated web scraping and API ingestion  
- Distributed storage using Hadoop HDFS  
- Relational database design with normalized schema  
- Efficient ingestion using caching techniques  

---

## Technical Insights

- API-based and scraping-based data ingestion require different handling strategies  
- Distributed storage improves scalability and fault tolerance  
- Proper schema design is critical for efficient querying  
- Caching significantly reduces database overhead during ingestion  

---

## Challenges

- Handling dynamic content using Selenium  
- Managing large datasets in distributed systems  
- Designing efficient relational schemas for semi-structured data  
- Avoiding duplicate entries during ingestion  

---

## Future Improvements

- Real-time data streaming using Kafka  
- Workflow orchestration using Apache Airflow  
- Cloud deployment (AWS / GCP)  
- Dashboard visualization using Power BI or Tableau  

---

## Outcome

This project demonstrates practical knowledge of:
- Data engineering pipelines  
- Distributed storage systems (HDFS)  
- Data ingestion and transformation  
- Integration of structured and unstructured data sources  

It reflects the ability to build scalable and production-oriented data workflows.

