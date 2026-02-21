import threading
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from deep_translator import GoogleTranslator

def run_session(url, cap):
    session_name = cap.get('bstack:options', {}).get('sessionName', 'Test')
    print(f"--- Starting: {session_name} ---")
    
    try:
        options = ChromeOptions()
        for key, value in cap.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(command_executor=url, options=options)
        translator = GoogleTranslator(source='es', target='en')
        
        driver.get("https://elpais.com/opinion/")
        
        # FIXED: Added the missing 'except' block for the cookie banner
        try:
            driver.find_element(By.ID, "didomi-notice-agree-button").click()
        except:
            pass # Banner didn't appear or already closed

        articles = driver.find_elements(By.TAG_NAME, "article")[:5]
        translated_headers = []

        if not os.path.exists('scraped_images'):
            os.makedirs('scraped_images')

        for i, article in enumerate(articles):
            title_es = article.find_element(By.TAG_NAME, "h2").text
            
            try:
                img_element = article.find_element(By.TAG_NAME, "img")
                img_url = img_element.get_attribute("src")
                if img_url and img_url.startswith("http"):
                    img_data = requests.get(img_url).content
                    filename = f"scraped_images/{session_name.replace(' ', '_')}_art_{i+1}.jpg"
                    with open(filename, 'wb') as f:
                        f.write(img_data)
            except:
                pass 

            title_en = translator.translate(title_es)
            translated_headers.append(title_en)
            print(f"[{session_name}] Translated Header {i+1}: {title_en}")

        # HEADER ANALYSIS
        all_words = " ".join(translated_headers).lower().split()
        word_counts = {}
        for word in all_words:
            word = word.strip(".,!?:;\"")
            if len(word) > 3:
                word_counts[word] = word_counts.get(word, 0) + 1

        print(f"\n[{session_name}] Repeated Words (>2):")
        for word, count in word_counts.items():
            if count > 2:
                print(f"  - {word}: {count}")

        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Logic verified!"}}')
    
    except Exception as e:
        print(f"Error in {session_name}: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    USER_NAME = "YOUR_USERNAME" 
    ACCESS_KEY = "YOUR_ACCESS_KEY" 
    BS_URL = f"https://{USER_NAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

    capabilities = [
        {'browserName': 'chrome', 'browserVersion': 'latest', 'bstack:options': {'os': 'Windows', 'osVersion': '11', 'sessionName': 'Win 11 - Chrome'}},
        {'browserName': 'firefox', 'browserVersion': 'latest', 'bstack:options': {'os': 'Windows', 'osVersion': '10', 'sessionName': 'Win 10 - Firefox'}},
        {'browserName': 'safari', 'browserVersion': 'latest', 'bstack:options': {'os': 'OS X', 'osVersion': 'Ventura', 'sessionName': 'Mac - Safari'}},
        {'browserName': 'chrome', 'browserVersion': 'latest', 'bstack:options': {'os': 'OS X', 'osVersion': 'Sonoma', 'sessionName': 'Mac - Chrome'}},
        {'browserName': 'safari', 'deviceName': 'iPhone 14', 'osVersion': '16', 'realMobile': 'true', 'bstack:options': {'sessionName': 'iPhone 14 - Safari'}}
    ]

    threads = []
    for cap in capabilities:
        t = threading.Thread(target=run_session, args=(BS_URL, cap))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n--- ALL TASKS COMPLETE ---")