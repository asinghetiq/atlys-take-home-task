import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.frameworks.web.auth import authenticate
from app.core.entities.scraping_settings import ScrapingSettings
from app.adapters.web_scraper import WebScraper
from app.frameworks.db.json_storage import JSONStorageHandler
from app.adapters.notification_adapter import ConsoleNotificationStrategy
from app.core.usecases.scrape_products import ScrapeProductsUseCase
from app.frameworks.db.redis_cache import RedisCache
from app.frameworks.db.in_memory_cache import InMemoryCache

logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_cache_strategy():
    cache_type = os.getenv('CACHE_TYPE')
    if cache_type == 'redis':
        return RedisCache()
    elif cache_type == 'in_memory':
        return InMemoryCache()
    else:
        logger.error(f"Unsupported cache type: {cache_type}")
        raise ValueError(f"Unsupported cache type: {cache_type}")

# API endpoint to start scraping
@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: ScrapingSettings):
    try:
        scraper = WebScraper(settings=settings)
        cache_strategy = get_cache_strategy()
        storage_handler = JSONStorageHandler(cache_strategy)
        notification_strategy = ConsoleNotificationStrategy()
        use_case = ScrapeProductsUseCase(scraper, storage_handler, notification_strategy)

        await use_case.execute(settings)
        return {"message": f"Scraping completed. Check products.json for results."}
    except Exception as e:
        logger.exception(f"An error occurred during scraping. {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred during scraping. Please try again later. {e}")
