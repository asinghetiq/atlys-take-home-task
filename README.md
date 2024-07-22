
# Atlys Take Home Task

## Project Structure

```plaintext
.
├── app
│   ├── adapters
│   │   ├── notification_adapter.py
│   │   ├── storage_adapter.py
│   │   ├── web_scraper.py
│   ├── core
│   │   ├── entities
│   │   │   ├── product.py
│   │   │   ├── scraping_settings.py
│   │   ├── usecases
│   │       └── scrape_products.py
│   ├── frameworks
│   │   ├── db
│   │   │   ├── cache_strategy.py
│   │   │   ├── in_memory_cache.py
│   │   │   ├── json_storage.py
│   │   │   ├── redis_cache.py
│   │   ├── web
│   │       ├── auth.py
│   │       ├── fastapi_app.py
│   ├── logging
│   │   └── config.py
│   ├── session_manager.py
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.8+
- Redis (optional, if using RedisCache)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/asinghetiq/atlys-take-home-task
    cd atlys-take-home-task
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add the following variables:
    ```env
    BASE_URL=https://dentalstall.com/shop/page/
    STATIC_TOKEN=your_static_token
    CACHE_TYPE=in_memory  # or 'redis' for RedisCache
    REDIS_HOST=localhost  # Only if using RedisCache
    REDIS_PORT=6379       # Only if using RedisCache
    REDIS_DB=0            # Only if using RedisCache
    ```

### Running the Application

1. **Run the FastAPI application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

2. **Start scraping:**
    Use an HTTP client like Postman or cURL to make a POST request to `/scrape` with the required scraping settings and authentication token.
    ```bash
    curl -X POST "http://localhost:8000/scrape" -H "Authorization: your_static_token" -H "Content-Type: application/json" -d '{"limit_pages": 5}'
    ```
    With Proxy
    ```bash
    curl -X POST "http://localhost:8000/scrape" -H "Authorization: your_static_token" -H "Content-Type: application/json" -d '{"limit_pages": 5, "proxy": "http://yourproxy:port"}'
    ```

## Configuration

- **ScrapingSettings:**
  - `limit_pages` (int): Limit the number of pages to scrape.
  - `proxy` (str): Proxy string to use for scraping.

- **Storage:**
  - Default: JSON file storage (`products.json`).
  - Easily extendable to other storage strategies by implementing the `StorageHandler` interface.

- **Notification:**
  - Default: Console notification.
  - Easily extendable to other notification strategies by implementing the `NotificationStrategy` interface.

- **Caching:**
  - Default: In-memory caching.
  - Redis caching can be enabled by setting `CACHE_TYPE=redis` in the `.env` file.

