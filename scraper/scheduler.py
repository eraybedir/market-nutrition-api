import schedule
import time
from scraper.product_scraper import ProductScraper
from scraper.matcher import NutritionMatcher

class ScrapingScheduler:
    def __init__(self):
        self.scraper = ProductScraper()
        self.matcher = NutritionMatcher()

    def job(self):
        print("🚀 Scraping & Matching başlatılıyor...")
        self.scraper.run()
        self.matcher.run()
        print("✅ Tüm işlem tamamlandı.\n")

    def run_daily(self):
        print("📅 Zamanlayıcı başlatıldı (her 7 günde bir çalışacak)...")
        schedule.every(7).days.do(self.job)

        # İlk çalıştırma hemen yapılsın (isteğe bağlı)
        self.job()

        while True:
            schedule.run_pending()
            time.sleep(60)
