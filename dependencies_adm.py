from fastapi import  HTTPException
# from routes import users_router, courses_router
from starlette.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import  Request
from itsdangerous import URLSafeTimedSerializer, BadSignature
from bson import ObjectId

# import serializer
SECRET_KEY = "sdsfe45456@21!!"
serializer = URLSafeTimedSerializer(SECRET_KEY)

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.Bank

async def get_current_admin(request: Request):
    session_cookie = request.cookies.get("admin")
    if not session_cookie:
        return None
    
    try:
        
        data = serializer.loads(session_cookie)
        data = str(data)
    except BadSignature:
        return None
    
    # print(len(data))
    user = await db.admin.find_one({"Email": "afnanajmal@gmail.com"})



    if not user:
        return None
    
    
    return user