import os
from dotenv import load_dotenv
from app.logging.config import setup_logging
from app.frameworks.web.fastapi_app import app

# load env variables and setup logger
load_dotenv()
setup_logging()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
