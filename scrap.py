import re
import httpx

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_gmaps_url(url):
    options = Options()
    options.add_argument("--window-size=2560,1440")
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    btn = driver.find_element(By.XPATH, "//*[@id='list-details3']/section/div/div/div/div/div/div[4]/div[1]/div/div/a")
    gmaps_url = btn.get_attribute("href")
    btn.click()

    driver.switch_to.window(driver.window_handles[1])
    new_url = driver.current_url
    print(f"Success: {url}")
    return gmaps_url, new_url

def extract_lat_lng(url):
    # Regular expression to find latitude and longitude in the Google Maps URL
    pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
    match = re.search(pattern, url)
    if match:
        return match.groups()  # Returns a tuple with latitude and longitude as strings
    return ["",""]


class Scraper:
    def __init__(self):
        self.client = httpx.Client()

    def get_html(self, url):
        response = self.client.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code} on {url}")
        return response.text
    

if __name__ == "__main__":
    scraper = Scraper()
    url = "https://www.petfriendly123.com/pet-friendly/Sixtynine-Prime/r/recTBkyQkkrdGtIWd"

    html = scraper.get_html(url)
    with open('page.html', 'w') as f:
        f.write(html)