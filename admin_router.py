from re import template
from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import BadSignature, URLSafeTimedSerializer
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import datetime
import random
from starlette.responses import RedirectResponse
from dependencies import get_current_user
from dependencies_adm import get_current_admin

router =  APIRouter()
client= AsyncIOMotorClient("mongodb://localhost:27017")
db= client.Bank 
users_collection = db.users 
template= Jinja2Templates(directory="templates")

@router.get("/admin_main/admin")
async def users_main(request:Request, admin=Depends(get_current_admin)):
    if(admin):
        total_money = 0
        total_accounts = 0
        

        async for account in db.users.find():
            total_accounts += 1
            total_money += account.get("balance", 0)


        return template.TemplateResponse(
                "admin.html",
                {
                    "request": request,
                    "login": True,
                    "total_money": total_money,
                    "total_accounts": total_accounts,
                },
            )
    return template.TemplateResponse("Signin.html", {"request" : request})

@router.get("/user/detail")
async def get_userdetail(request : Request,  admin = Depends(get_current_admin)):
    if (admin):
        print(admin)
        user_detail = []
        async for account in db.users.find():
            user_detail.append({
                "username": account.get("Username"),
                "account_number": account.get("Account"),
                "balance": account.get("balance")
            })
        print(admin,"A")
        return template.TemplateResponse("userdet-admin.html",{"request": request, "user_detail" : user_detail}) 

    return template.TemplateResponse("Signin.html", {"request" : request})

@router.post("/update/{account_number}")
async def update_balance(request: Request, account_number: int, admin = Depends(get_current_admin)):
    if (admin):

        form_data = await request.form()
        new_balance = float(form_data.get("new_balance"))

        # Update balance in the database
        await db.users.update_one({"Account": account_number}, {"$set": {"balance": new_balance}})
        

        user_detail = []
        async for account in db.users.find():
            user_detail.append({
                "username": account.get("Username"),
                "account_number": account.get("Account"),
                "balance": account.get("balance")
            })
        
        return template.TemplateResponse("userdet-admin.html", {"request": request, "user_detail" : user_detail })

    return template.TemplateResponse("Signin.html", {"request" : request})


@router.post("/user/delete/{account_number}")
async def delete_user(request: Request, account_number: int, admin = Depends(get_current_admin)):
    if (admin):
    # Delete user from the database
        await db.users.delete_one({"Account": account_number})

        user_detail = []
        async for account in db.users.find():
            user_detail.append({
                "username": account.get("Username"),
                "account_number": account.get("Account"),
                "balance": account.get("balance")
            })
        
        return template.TemplateResponse("userdet-admin.html", {"request": request, "user_detail" : user_detail})

    return template.TemplateResponse("Signin.html", {"request" : request})