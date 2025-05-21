import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

class ProductScraper:
    def __init__(self, map_path="scraper/product_category_map.json", output_dir="data/raw_products"):
        self.map_path = Path(map_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.product_list = []
        self.driver = None

    def setup_driver(self):
        service = Service(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service)

    def scrape_page(self, url, category, subcategory, item_category):
        page = 1
        while True:
            full_url = f"{url}?page={page}"
            self.driver.get(full_url)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            names = [tag.get_text(strip=True) for tag in soup.find_all("div", class_="ProductCard_productName__35zi5")]
            markets = [m.find("img")["alt"] if m.find("img") else "Bilinmiyor"
                       for m in soup.find_all("div", class_="WrapperBox_wrapper__1_OBD")]
            prices = []
            for footer in soup.find_all("div", class_="ProductCard_footer__Fc9OL"):
                spans = footer.find_all("span", class_="ProductCard_price__10UHp")
                prices.append(spans[0].get_text(strip=True) if spans else "Fiyat Bilinmiyor")
            images = [
                img["src"] if (img := div.find("img")) and img.has_attr("src") else "Yok"
                for div in soup.find_all("div", class_="ProductCard_imageContainer__ASSCc")
            ]

            for i, name in enumerate(names):
                self.product_list.append({
                    "category": category,
                    "subcategory": subcategory,
                    "item_category": item_category,
                    "name": name,
                    "price": prices[i] if i < len(prices) else "Fiyat Bilinmiyor",
                    "market": markets[i] if i < len(markets) else "Bilinmiyor",
                    "image_url": images[i] if i < len(images) else "Yok"
                })

            # Sayfa kontrolü
            next_page_btn = self.driver.find_elements(By.CSS_SELECTOR, "a[btnmode='next']")
            if not next_page_btn:
                break
            page += 1

    def run(self):
        print("📦 Scraping başlatılıyor...")
        self.setup_driver()
        with open(self.map_path, "r", encoding="utf-8") as f:
            category_map = json.load(f)

        for entry in category_map:
            print(f"🔍 {entry['item_category']} scrape ediliyor...")
            self.scrape_page(entry["url"], entry["category"], entry["subcategory"], entry["item_category"])
        
        self.driver.quit()
        self.save()

    def save(self):
        today = datetime.today().strftime("%Y_%m_%d")
        file_path = self.output_dir / f"products_{today}.csv"
        df = pd.DataFrame(self.product_list)
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"✅ Scraping tamamlandı. Dosya kaydedildi: {file_path.resolve()}")
