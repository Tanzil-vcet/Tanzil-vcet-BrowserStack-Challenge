import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator

def run_local_task():
    # 1. Setup Driver and Translator
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    translator = GoogleTranslator(source='es', target='en')
    
    # Create directory for images
    if not os.path.exists('scraped_images_local'):
        os.makedirs('scraped_images_local')

    try:
        # 2. Visit El País and navigate to Opinion
        driver.get("https://elpais.com/opinion/")
        
        # 3. Fetch first 5 articles
        articles = driver.find_elements(By.TAG_NAME, "article")[:5]
        translated_headers = []

        print(f"--- Processing {len(articles)} Articles ---\n")

        for i, article in enumerate(articles):
            # Fetch Spanish Title and Content
            title_es = article.find_element(By.TAG_NAME, "h2").text
            try:
                content_es = article.find_element(By.TAG_NAME, "p").text
            except:
                content_es = "No content found."

            # PRINT: Title and Content in Spanish
            print(f"ARTICLE {i+1} (SPANISH):")
            print(f"Title: {title_es}")
            print(f"Content: {content_es}\n")

            # 4. DOWNLOAD: Cover image
            try:
                img_url = article.find_element(By.TAG_NAME, "img").get_attribute("src")
                img_data = requests.get(img_url).content
                with open(f"scraped_images_local/article_{i+1}.jpg", 'wb') as f:
                    f.write(img_data)
            except:
                print(f"Could not download image for article {i+1}")

            # 5. TRANSLATE: Title to English
            title_en = translator.translate(title_es)
            translated_headers.append(title_en)
            print(f"TRANSLATED HEADER: {title_en}\n" + "-"*30)

        # 6. ANALYZE: Repeated words > 2
        all_words = " ".join(translated_headers).lower().split()
        word_counts = {}
        for word in all_words:
            # Strip basic punctuation
            word = word.strip(".,!?:;\"")
            if len(word) > 3: # Focus on meaningful words
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