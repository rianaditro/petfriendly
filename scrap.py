import re
import httpx
import time

from PIL import Image
from io import BytesIO

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_gmaps_url(url):
    options = Options()
    options.add_argument("--window-size=2560,1440")
    options.add_argument("--enable-javascript")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    btn = driver.find_element(By.XPATH, "//*[@id='list-details3']/section/div/div/div/div/div/div[4]/div[1]/div/div/a")
    gmaps_url = btn.get_attribute("href")
    btn.click()

    driver.switch_to.window(driver.window_handles[1])
    new_url = driver.current_url
    driver.quit()

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
        self.html = None
        self.url = None

    def get_html(self, url):
        response = self.client.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code} on {url}")
        time.sleep(1)
        self.html = BeautifulSoup(response.text, 'html.parser')
        return self
    
    def get_address(self):
        try:
            address = self.html.find_all('span', 'BNeawe tAd8D AP7Wnd')
            if address:
                return address[0].text.strip()
            else:
                match = re.search(r'Alamat: (.*?)(?=<|,|$)', str(self.html))
                if match:
                    return match.group(1).strip()
                else:
                    print("Alamat tidak ditemukan")
                    return None
        except:
            print(f"Error: Address not found on {self.url}")
            return None

    def get_image(self, url, filename):
        response = self.client.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code} on {url}")
        image = Image.open(BytesIO(response.content))
        img_path = f'img/{filename}.jpg'
        image.save(img_path, 'JPEG', quality=100)
        return img_path
    

if __name__ == "__main__":
    scraper = Scraper()
    url = "https://v5.airtableusercontent.com/v3/u/28/28/1715392800000/86e0APO7_eBxFDPXXbXFzQ/HE3gbSvcQu8apFE75U-Y9czqQhg-AV77HD29HWp2YKT0XbK7JtdW57gsm2fIDO7eO1S81aYo85G2m349Q5SZU_f25eySZu0OLROrcb41Fv3jBxAwh7FLFap0Nqxda1JfJcEJNXSQeNmg2Ye_l8LQX32KLWM2E27BtBooWDccKbE/5A-GvurqDkN0YuwIdlYQfmtF_MDKd9mq7e-GokzlXTo"
    img = scraper.get_image(url)