from pydantic import BaseModel
from typing import Optional

class ScrapingSettings(BaseModel):
    limit_pages: Optional[int] = None
    proxy: Optional[str] = None
