# gcp_project_credit_card_transaction_analysis
# Credit Card Transaction Analysis

A data analytics project to explore, clean, process, and analyze credit card transaction data to uncover spending patterns, detect anomalies, and generate meaningful insights. This project demonstrates end-to-end data handling using Python, Pandas, SQL, and visualization tools.

**📌 Project Overview**
This project focuses on analyzing large volumes of credit card transaction data to understand customer behavior, merchant trends, high-risk patterns, and possible fraud indicators.
The analysis pipeline includes:
**Data ingestion and cleaning
Exploratory Data Analysis (EDA)
Feature engineering
Spending pattern analysis
Fraud detection signals
Visual insights and reporting**

The goal is to help financial teams understand transaction trends, improve risk management, and make data-driven decisions.
**🛠️ Tech Stack**
Python
Pyspark
SQL
Jupyter Notebook

**📂 Dataset Description**
Typical fields used in the dataset:
Column Name	Description
transaction_id	Unique ID for each transaction
customer_id	Customer identifier
amount	Transaction amount
merchant_category	Category of merchant
transaction_type	POS/Online/ATM
timestamp	Date & time of transaction
city	Location of transaction
is_fraud	0/1 fraud indicator (if available)

**🔍 Key Features & Analysis Performed**
**1️⃣ Data Cleaning & Preprocessing**

Handling missing values

Removing duplicates

Converting timestamps

Normalizing categories

Detecting outliers

**2️⃣ Exploratory Data Analysis (EDA)**

Hourly, daily, weekly spending trends

Customer-wise spending distribution

Merchant category analysis

Top cities by transaction volume

High-value transaction analysis

**3️⃣ Fraud Pattern Indicators**

Unusual transaction amounts

Rapid transaction frequency

Location anomalies

Category deviation

Time-based risk scoring

**4️⃣ Visualizations**

Spending trend graphs

Category distribution charts

Heatmaps for correlation

Fraud vs Non-Fraud comparison

**📊 Project Architecture**

Import & Clean Data

Transform & Feature Engineer

EDA + Visual Insights

Fraud Detection Signals

Final Reports & Dashboards

**🚀 How to Run the Project**

Clone the repo:

git clone https://github.com/aj1120/credit-card-analysis
cd credit-card-analysis


**Install requirements:**

pip install -r requirements.txt
