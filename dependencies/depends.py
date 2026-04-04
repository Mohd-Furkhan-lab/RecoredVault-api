from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer
from auth.jwt_token import verify_token


security = HTTPBearer()

async def get_current_user(credentials= Depends(security)):
    token=credentials.credentials 
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401,details="Invalid Token")
    
    return payload


async def is_admin(user = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="not enough permission")
    return user["user_id"]


async def require_role(*role:str):
    async def checker(user = Depends(get_current_user)):
        if user['role'] != role:
            raise HTTPException(status_code=403,detail="Forbidden")
        return user
    return checker
    