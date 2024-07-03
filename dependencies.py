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

async def get_current_user(request: Request):
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        # return None
        return None
    try:
        
        data = serializer.loads(session_cookie)
        print(type(data))
        print(data)
        # data = str(data)
    except BadSignature:
        # return None
        return None
    
    # print(len(data))
    user = await db.users.find_one({"Email": data['Email']})

    print(data)
    print("A1",user)

    if not user:
        print(user)
        # return None
        return None
    return user