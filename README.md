# BrowserStack Technical Assignment: Selenium & Automation

This repository contains the solution for the Round 2 Technical Assignment for the Customer Engineering role. It demonstrates a complete automation workflow involving web scraping, API integration, and parallel cross-browser testing.

## 📋 Features
- **Local Scraping (`main.py`):** - Navigates to the *El País* Opinion section.
  - Fetches the first 5 articles and prints titles/content in Spanish.
  - Downloads cover images to a local directory.
  - Translates headers to English using the Google Translate API (via `deep-translator`).
  - Performs text analysis to identify repeated words across headers.
- **Parallel Testing (`parallel_test.py`):** - Executes the same scraping and translation logic across 5 parallel threads.
  - Tests compatibility across multiple OS/Browser combinations (Windows, macOS, iPhone) using **BrowserStack Automate**.

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Framework:** Selenium 4.x
- **Infrastructure:** BrowserStack Selenium Grid
- **Translation:** Deep Translator API

## 🚀 Execution Instructions

### 1. Prerequisites
Ensure you have Python 3.13 installed. Install the necessary dependencies:
```bash
pip install -r requirements.txt