# BrowserStack Technical Challenge: Multi-Platform Web Automation

This repository contains the complete solution for the Round 2 Technical Assignment for the Customer Engineering role. The project demonstrates a robust automation pipeline for scraping, translating, and analyzing international news content across a distributed cloud grid.

## Project Objectives
The objective was to build a Selenium-based automation suite that satisfies the following:
1. **Locale Enforcement:** Forcing the browser to display content in Spanish regardless of the testing server's location.
2. **Data Extraction:** Scrapping the first 5 articles (Title and Content) from the *El País* Opinion section.
3. **API Orchestration:** Leveraging the Google Translate API to provide English translations for all headers.
4. **Text Analytics:** Programmatically identifying repeated words across translated headers to find recurring themes.
5. **Cross-Browser Testing:** Executing the entire workflow in parallel across 5 different desktop and mobile environments.

## Tech Stack
- **Language:** Python 3.13
- **Automation:** Selenium 4.x (using W3C compliant Capabilities)
- **Infrastructure:** BrowserStack Automate (Parallel Threading)
- **APIs:** `deep-translator` for Spanish-to-English processing
- **Dependency Management:** pip (`requirements.txt`)

## Project Structure
- `main.py`: Local execution script for initial validation and single-browser testing.
- `parallel_test.py`: Cloud execution script configured for 5 parallel threads on BrowserStack.
- `requirements.txt`: Python dependencies required for the project.
- `.gitignore`: Ensures local caches and scraped images are not pushed to the repository.

## Setup & Execution

### 1. Installation
Clone the repository and install the required Python libraries:
```bash
git clone <your-repository-url>
cd BrowserStack_Assignment
pip install -r requirements.txt