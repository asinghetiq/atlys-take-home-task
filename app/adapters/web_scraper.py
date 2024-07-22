import os
import asyncio
import logging
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from typing import List
from app.core.entities.product import Product
from app.core.entities.scraping_settings import ScrapingSettings
from app.session_manager import SessionManager

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, settings: ScrapingSettings):
        self.settings = settings
        self.base_url = os.getenv('BASE_URL')
        self.image_dir = 'product_images'

        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    async def fetch_page(self, session: ClientSession, url: str) -> str:
        for attempt in range(3):  # Retry Mechanism
            try:
                async with session.get(url, proxy=self.settings.proxy) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}, status code: {response.status}")
                        raise Exception(f"Failed to fetch {url}")
                    return await response.text()
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}: {e}")
                await asyncio.sleep(2)
        logger.error(f"Failed to fetch page after multiple attempts: {url}")
        return None

    async def download_image(self, session: ClientSession, url: str, product_title: str) -> str:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    file_name = os.path.join(self.image_dir, f"{product_title}.jpg")
                    with open(file_name, 'wb') as f:
                        f.write(await response.read())
                    return file_name
                else:
                    logger.warning(f"Failed to download image from {url}")
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
        return ""

    async def scrape_page(self, session: ClientSession, page_number: int) -> List[Product]:
        url = f"{self.base_url}{page_number}/"
        logger.info(f"Scraping page {page_number}: {url}")
        html_content = await self.fetch_page(session, url)
        products = []
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            product_elements = soup.select('.product')
            logger.info(f"Found {len(product_elements)} products on page {page_number}")
            for product in product_elements:
                product_title_elem = product.select_one('.woo-loop-product__title')
                product_price_elem = product.select_one('.woocommerce-Price-amount bdi')
                product_image_elem = product.select_one('.mf-product-thumbnail img')
                if product_title_elem and product_price_elem and product_image_elem:
                    product_title = product_title_elem.text
                    product_price = product_price_elem.text.strip()
                    product_image_url = product_image_elem['data-lazy-src']
                    total_price = ''.join(c for c in product_price if c.isdigit() or c == '.')
                    image_path = await self.download_image(session, product_image_url, product_title)
                    products.append(Product(
                        product_title=product_title,
                        product_price=int(float(total_price)),
                        path_to_image=image_path
                    ))
                else:
                    logger.warning(f"Missing elements in product on page {page_number}")
        else:
            logger.warning(f"No content found on page {page_number}")
        return products

    async def scrape(self) -> List[Product]:
        logger.info(f"Starting scrape with settings: {self.settings}")
        tasks = []
        products = []
        session_manager = SessionManager()
        await session_manager.init()
        try:
            async with session_manager.session as session:
                for page_number in range(1, self.settings.limit_pages + 1):
                    tasks.append(self.scrape_page(session, page_number))
                results = await asyncio.gather(*tasks)
                for result in results:
                    products.extend(result)
        finally:
            await session_manager.close()
        logger.info(f"Scraping completed. Total products scraped: {len(products)}")
        return products
