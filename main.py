import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator

def run_local_task():
    # 1. Setup Driver with Spanish Language Preference
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=es") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    translator = GoogleTranslator(source='es', target='en')
    
    if not os.path.exists('scraped_images_local'):
        os.makedirs('scraped_images_local')

    try:
        # 2. Visit El País and navigate to Opinion
        driver.get("https://elpais.com/opinion/")
        
        # Handle cookie banner if it appears
        try:
            driver.find_element(By.ID, "didomi-notice-agree-button").click()
        except:
            pass

        # 3. Fetch first 5 articles
        articles = driver.find_elements(By.TAG_NAME, "article")[:5]
        translated_headers = []

        print(f"--- Processing {len(articles)} Articles (Local Run) ---\n")

        for i, article in enumerate(articles):
            # 4. SCRAPE: Spanish Title and Content
            title_es = article.find_element(By.TAG_NAME, "h2").text
            try:
                content_es = article.find_element(By.TAG_NAME, "p").text
            except:
                content_es = "No content summary found."

            # 5. PRINT: Original Spanish (Requirement)
            print(f"ARTICLE {i+1} - SPANISH:")
            print(f"Title: {title_es}")
            print(f"Content: {content_es}\n")

            # 6. DOWNLOAD: Image
            try:
                img_element = article.find_element(By.TAG_NAME, "img")
                img_url = img_element.get_attribute("src")
                if img_url and img_url.startswith("http"):
                    img_data = requests.get(img_url).content
                    with open(f"scraped_images_local/article_{i+1}.jpg", 'wb') as f:
                        f.write(img_data)
            except:
                pass

            # 7. TRANSLATE & PRINT: English (Requirement)
            title_en = translator.translate(title_es)
            translated_headers.append(title_en)
            print(f"ARTICLE {i+1} - ENGLISH TRANSLATION:")
            print(f"Translated Title: {title_en}\n" + "-"*40)

        # 8. ANALYZE: Repeated words > 2
        all_words = " ".join(translated_headers).lower().split()
        word_counts = {}
        for word in all_words:
            word = word.strip(".,!?:;\"")
            if len(word) > 3:
                word_counts[word] = word_counts.get(word, 0) + 1

        print("\n--- WORD REPETITION ANALYSIS (Count > 2) ---")
        found = False
        for word, count in word_counts.items():
            if count > 2:
                print(f"'{word}': {count} occurrences")
                found = True
        
        if not found:
            print("No words were repeated more than twice across all headers.")

    finally:
        driver.quit()
        
if __name__ == "__main__":
    run_local_task()