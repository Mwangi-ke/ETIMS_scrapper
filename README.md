# 🧾 KRA eTIMS Invoice Scraper
Automated Invoice Retrieval & Structuring for Finance Workflow Efficiency
Author: Hillary Mwangi

 ## 📌 Overview
This project is a Selenium-based automated data collection tool designed to log into the Kenya Revenue Authority’s (KRA) eTIMS system, extract sales invoice PDFs, and rename/archive them in a structured format for downstream finance analysis and reporting.

It was developed to support the Finance Team's month-end closing by eliminating repetitive manual downloads, improving accuracy, and saving time.

## 🎯 Key Objectives

✅ Automate KRA portal login and navigation through secured user credentials.

✅ Detect total number of pages dynamically and loop through invoices.

✅ Click, download, and rename PDF invoice files using an intelligent naming pattern.

✅ Organize and store the files in a structured local folder.

✅ Streamline the invoice collection process for reconciliation and reporting.

## 🔍 Use Case & Business Impact
This tool was used internally to:

📁 Download and archive 200+ .

💼 Improve audit traceability by following strict naming conventions.




## 🧠 Tech Stack

Component	Purpose
Python	Core scripting logic
Selenium	Browser automation
dotenv	Secure credential management
re	Invoice number detection and pattern matching
os, shutil, time	File handling, waits, and system operations



## 🚀 How to Run
Clone the repo:
git clone https://github.com/Mwangi-ke/kra-invoice-scraper.git

cd kra-invoice-scraper

Install dependencies:
pip install selenium python-dote

Create a .env file with your credentials:

KRA_USERNAME=your_username

KRA_PASSWORD=your_password

Run the script:
python scraper.py
