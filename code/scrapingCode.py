from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
options.add_argument("--remote-debugging-port=9222")


def scraping(urlToScrape, ages, breeds, genders):
    driver = webdriver.Chrome(options=options)
    driver.get(urlToScrape)

    time.sleep(3)

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.select("a.petCard-link")

        if not cards:
            print("No cards found, stopping.")
            break

        for card in cards:
            details = card.get("aria-label")
            gender = "Unknown"
            breed = "Unknown"
            age = "Unknown"

            if details:
                parts = details.split(",")
                print(parts)
                if len(parts) >= 2:
                    data = parts[-3].strip()
                    dataList = data.split(" ")
                    age = dataList[0]
                    gender = dataList[1]
                    breedList = dataList[2:]
                    breed = " ".join(breedList)


            ages.append(age)
            breeds.append(breed)
            genders.append(gender)

        try:
            next_button = driver.find_element(By.XPATH, "//span[text()='Next']/..")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)
        except:
            print("No next page. Done.")
            break

    driver.quit()
    return ages, breeds, genders
    

def main():    
    urlList =  ["https://www.petfinder.com/search/cats-for-adoption/us/maine/",
                "https://www.petfinder.com/search/cats-adopted/us/maine/",
                "https://www.petfinder.com/search/dogs-for-adoption/us/maine/",
                "https://www.petfinder.com/search/dogs-adopted/us/maine/"]
    
    ages = []
    breeds = []
    genders = []

    for url in urlList:
        ages = []
        breeds = []
        genders = []

        finAges, finBreed, finGneder = scraping(url, ages, breeds, genders)
        print(f"finished scraping {url}")
        newFile = "petData" + url[33:45] + ".csv"
        df = pd.DataFrame({

            "Age": finAges,
            "Breed": finBreed,
            "Gender": finGneder
        })
        df.to_csv(newFile, index=False, encoding="utf-8")

main()