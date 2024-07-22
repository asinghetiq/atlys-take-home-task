import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends

security = HTTPBearer()

async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = os.getenv('STATIC_TOKEN')
    if credentials.credentials != token:
        raise HTTPException(status_code=401, detail="Unauthorized")
