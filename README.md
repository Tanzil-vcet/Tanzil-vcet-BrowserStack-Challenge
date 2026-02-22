# BrowserStack Technical Challenge: Multi-Platform Web Automation

This repository contains the complete solution for the Round 2 Technical Assignment for the Customer Engineering role. The project demonstrates an automation pipeline for scraping, translating, and analyzing international news content across a distributed cloud grid.

## Project Objectives
The objective was to build a Selenium-based automation suite that satisfies the following:

1. **Locale Enforcement:** Force the browser to display content in Spanish regardless of the testing server's location.
2. **Data Extraction:** Scrape the first 5 articles (Title and Content) from the *El País* Opinion section.
3. **Translation:** Use a translation library (`deep-translator`) to generate English versions of article headers.
4. **Text Analytics:** Identify repeated words across translated headers to highlight recurring themes.
5. **Cross-Browser Testing:** Execute the workflow in parallel across 5 desktop and mobile environments.

## Tech Stack
- **Language:** Python 3.13  
- **Automation:** Selenium 4.x (W3C compliant capabilities)  
- **Infrastructure:** BrowserStack Automate (Parallel execution)  
- **Translation:** `deep-translator`  
- **Dependency Management:** pip (`requirements.txt`)  

## Project Structure
- `main.py` — Local execution for validation  
- `parallel_test.py` — BrowserStack parallel execution  
- `requirements.txt` — Python dependencies  
- `.gitignore` — Excludes caches and generated files  

## ⚙️ Setup & Execution

### 1️⃣ Installation
```bash
git clone <your-repository-url>
cd BrowserStack_Assignment
pip install -r requirements.txt
