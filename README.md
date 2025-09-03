# 📚 Books to Scrape

A Python project that extracts book data (title, price, rating, availability, etc.) from [Books to Scrape](http://books.toscrape.com/), and saves it into CSV files. Related images are also downloaded and organized by category.  
This project perfectly illustrates how an ETL pipeline works. This method is also called webscraping. 

---

## 📑 Table of Contents
- [Requirements](#-requirements)  
- [Getting Started](#-getting-started)  
  - [1. Project Setup](#1-project-setup)  
  - [2. Install Dependencies with Poetry](#2-install-dependencies)  
  - [3. Run the Program](#3-run-the-program)  
  - [4. Access the Data](#4-access-the-data)  
- [Notes](#-notes)  

---

## ✅ Requirements

- Python **3.8+**  
- [Poetry](https://python-poetry.org/) installed  
- Internet connection  
- Recommended: Excel to open CSV files  
  

---

## 🚀 Getting Started

### 1. Project Setup
1. Create a new directory for your project.  
2. Clone this repository inside it.  
3. Make sure Poetry is installed:  
   ```powershell  
   pip install poetry  
   ```  

### 2. Install dependencies with Poetry  

Poetry is a modern Python tool that manages dependencies and virtual environments with ease. By using a single pyproject.toml and a lock file, it ensures consistent setups across machines, making teamwork and collaboration much smoother.  

1. Install all dependecies defined in pyproject.toml:  
   ```powershell  
   poetry install 
   ```  
2. Activate the virtual env created by Poetry:  
   ```powershell
   poetry shell
   ```  

### 3. Run the program
1. Run the script inside Poetry's virtual environment:  
   ```powershell   
   poetry run python main.py
   ```  
   The process pay take a few minutes depending on your system and internet speed.  
2. If you already run the project before:  
   - The message : "The file *category name* has been deleted" will appear.  
   It's normal. The previous CSV file is now replaced by the one from the actual script running.  
3. At the end, you should have the message: "Scraping is now completed."  
   and this folder structure:  

    project/
    ├─ .venv/
    ├─ results/
    │  ├─ Poetry/
    │  │  ├─ poem.jpg
    │  │  ├─ another-poem.jpg
    │  │  └─ Poetry.csv
    │  ├─ Other categories...
    ├─ book.py
    ├─ categories
    ├─ category.py
    ├─ utils.py
    ├─ main.py
    ├─ poetry.lock
    ├─ pyproject.toml
    ├─ README.md


### 4. Access the Data
1. Open a new Excel workbook.  
2. Import the CSV file of your choix:  
   - Go to File > Open and select the CSV file.  
   - When prompted, choose Delimited > Next.  
   - Select Comma (,) as the delimiter > Next > Finish.  
3. You can now view the extracted data in Excel.  
   All images are also stored in each category folder.  


---

## 🛠️ Notes

This project is intended for educational purposes only.  

Data comes from the public demo site Books to Scrape : https://books.toscrape.com/  











