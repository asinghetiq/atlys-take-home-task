from typing import List
from app.core.entities.product import Product
from app.core.entities.scraping_settings import ScrapingSettings
from app.adapters.web_scraper import WebScraper
from app.adapters.storage_adapter import StorageHandler
from app.adapters.notification_adapter import NotificationStrategy

class ScrapeProductsUseCase:
    def __init__(self, scraper: WebScraper, storage_handler: StorageHandler, notification_strategy: NotificationStrategy):
        self.scraper = scraper
        self.storage_handler = storage_handler
        self.notification_strategy = notification_strategy

    async def execute(self, settings: ScrapingSettings) -> None:
        self.scraper = WebScraper(settings=settings)
        products: List[Product] = await self.scraper.scrape()
        
        # Store results
        self.storage_handler.save(products)

        # Notify Status
        self.notification_strategy.notify(f"Scraping completed. Total products scraped: {len(products)}")
