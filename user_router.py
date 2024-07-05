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

router =  APIRouter()
client= AsyncIOMotorClient("mongodb://eastransferdb:uAIrd9Uan0kg4pwc4Rq8Dv6PvOMweY8YB57Bu6nFwsUy21nvcbJp55tCu3KRmV2Y94OWip7HvPwdACDb2REwhA==@eastransferdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@eastransferdb@")
db= client.Bank 
users_collection = db.users 
template= Jinja2Templates(directory="templates")


@router.get("/users_main/user")
async def users_main(request:Request, user=Depends(get_current_user)):
    if(user):
        print(user)
        print("a3",user)
        return template.TemplateResponse("user_main.html", {"request": request, "user":user})
    return template.TemplateResponse("Signin.html", {"request" : request})


@router.get("/transferpage")
async def transfer_page(request: Request, user=Depends(get_current_user)):
    if(user):
        print("a2",user)
        return template.TemplateResponse("transferpage.html", {"request": request, "transferred": False,"insufficient":False, "user" : user})
    return template.TemplateResponse("Signin.html", {"request" : request})

@router.post("/transfer/transferto")
async def tranferhere(request:Request,user=Depends(get_current_user)):
    if(user):
        sender_account = user["Account"]
        print(sender_account)
        form_data= await request.form()
        receiver_account= int(form_data.get("account"))
        print(receiver_account)
        amount= int(form_data.get("amount"))
        print(amount)

        receiver=await  db.users.find_one({"Account": receiver_account})
        if(receiver == None):
            return template.TemplateResponse("transferpage.html", {"request": request,"transferred": False,"insufficient":False, "Valid" : True})

        sender= await db.users.find_one({"Account":sender_account})

        
        if sender["balance"]<amount:
            return template.TemplateResponse("transferpage.html", {"request": request,"transferred": False,"insufficient":True,"Valid" : False})
        else:
            newbalance= receiver["balance"]+amount
            deduction= sender["balance"]-amount
            sent_update=[receiver_account,receiver["Username"], amount, datetime.datetime.now()]
            receive_update= [sender_account, sender["Username"] ,amount, datetime.datetime.now()]
            sender_update = db.users.update_one(
            {"Account": sender["Account"]},
            {
            "$set": {"balance": deduction},
            "$push": {"Sent": {"$each": [sent_update], "$position": 0}}
            },
            upsert=False
            )
            
            receiver_update = db.users.update_one(
                {"Account": receiver["Account"]},
                {
                "$set": {"balance": newbalance},
                "$push": {"Recieve": {"$each": [receive_update], "$position": 0}}
                },
                upsert=False
                )
            return template.TemplateResponse("transferpage.html", {"request": request, "transferred":True, "insufficient":False, "user":user,"Valid" : False})
    return template.TemplateResponse("Signin.html", {"request" : request})


@router.get("/user/transactions")
async def transaction_page(request:Request, user=Depends(get_current_user)):
    if(user):
        return template.TemplateResponse("transactions.html", {"request": request, "sents":user["Sent"], "received":user["Recieve"]})
    return template.TemplateResponse("Signin.html", {"request" : request})

#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
