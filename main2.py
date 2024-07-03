# from urllib import response
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import  URLSafeTimedSerializer
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import random
from starlette.responses import RedirectResponse
from dependencies import get_current_user
from admin_router import router as adminrouter
from user_router import router as userrouter
from dependencies_adm import get_current_admin


app= FastAPI()


app.include_router(adminrouter, prefix="/admin")
app.include_router(userrouter, prefix="/users")

SECRET_KEY = "sdsfe45456@21!!"
serializer = URLSafeTimedSerializer(SECRET_KEY)



# connecting to db
client= AsyncIOMotorClient("mongodb://localhost:27017")
db= client.Bank 
users_collection = db.users 
template= Jinja2Templates(directory="templates")



@app.get("/")
async def home(request : Request):
    return template.TemplateResponse("Signin.html" ,{ "request" : request})


#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Sign In=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    


@app.post("/user/sign_in")
async def login(request: Request):
    x = 0
    form_data = await request.form()
    login_email = str(form_data.get("log_email"))
    login_pass =  str(form_data.get("log_pass"))
    
#    =================== For Admin===========================
    admin_email = "afnanajmal@gmail.com"
    admin_password = "Afnan@123"
    if login_email == admin_email and login_pass == admin_password:
        response = RedirectResponse(url="/admin/admin_main/admin", status_code= 303)
        session_data = {"Email": admin_email}
        session_cookie = serializer.dumps(session_data)
        response.set_cookie("admin", session_cookie)
        return response
    
  #======================For Normal Users====================== 
    user = await db.users.find_one({"Email": login_email})

    if user and user["Password"] == login_pass:
        
        response = RedirectResponse(url="/users/users_main/user", status_code= 303)
        session_data = {"Email": login_email}
        session_cookie = serializer.dumps(session_data)
        response.set_cookie("session", session_cookie)
        return response
    else:
        x = 1
        return template.TemplateResponse("Signin.html", {"request" : request, "x" : x})
    
#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def generate_account_number():
        return random.randint(10000, 99999)



@app.post("/user/sign_up")
async def sign_up(request : Request):
    x = 0
    response= await request.json()
    su_name = str(response.get("username"))
    su_email = str(response.get("email"))
    su_pass = str(response.get("password"))
    su_cpass = str(response.get("confirmPassword"))
    if su_pass != su_cpass:
        return {"error": "Passwords do not match"}  

    if await db.users.find_one({"Email": su_email}):
        return {"error": "Email address already exists"} 
    

    
    su_account = generate_account_number()  
    sent =[]
    recieve =[]
    
    await db.users.insert_one({
        "Username" : su_name,
        "Email" : su_email,
        "Password" : su_pass,
        "Account" : su_account,
        "balance": 0,
        "Sent" : sent,
        "Recieve" : recieve

        
    })
    



#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


@app.get("/signup")
async def Register_here(request: Request, response_class=HTMLResponse):
    
    return template.TemplateResponse("Signup.html", {"request": request})



#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


@app.get("/signin")
async def Signin_here(request: Request):
    return template.TemplateResponse("Signin.html", {"request": request})

#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


app.mount("/static", StaticFiles(directory="templates/styles"), name="static")




@app.get("/logout", response_class=HTMLResponse)
async def logout(request : Request):
    response = RedirectResponse(url= "/signin")
    new = request.cookies.get("session")
    old = request.cookies.get("admin")
    print(old)
    print(new)
    response.delete_cookie("session")
    response.delete_cookie("admin")
    new = request.cookies.get("session")
    old = request.cookies.get("admin")
    print(old)
    print(new)
    return response



    


# @app.get("/admin/user/detail")
# async def get_userdetail(request : Request,  admin = Depends(get_current_admin)):

#     user_detail = []
#     async for account in db.users.find():
#         user_detail.append({
#             "username": account.get("Username"),
#             "account_number": account.get("Account"),
#             "balance": account.get("balance")
#         })
    
#     return template.TemplateResponse("userdet-admin.html",{"request": request, "user_detail" : user_detail}) 

        
# @app.post("/admin/update/{account_number}")
# async def update_balance(request: Request, account_number: int, admin = Depends(get_current_admin)):
#     form_data = await request.form()
#     new_balance = float(form_data.get("new_balance"))

#     # Update balance in the database
#     await db.users.update_one({"Account": account_number}, {"$set": {"balance": new_balance}})
    

#     user_detail = []
#     async for account in db.users.find():
#         user_detail.append({
#             "username": account.get("Username"),
#             "account_number": account.get("Account"),
#             "balance": account.get("balance")
#         })
    
#     return template.TemplateResponse("userdet-admin.html", {"request": request, "user_detail" : user_detail })



# @app.post("/admin/user/delete/{account_number}")
# async def delete_user(request: Request, account_number: int, admin = Depends(get_current_admin)):
#     # Delete user from the database
#     await db.users.delete_one({"Account": account_number})

#     user_detail = []
#     async for account in db.users.find():
#         user_detail.append({
#             "username": account.get("Username"),
#             "account_number": account.get("Account"),
#             "balance": account.get("balance")
#         })
    
#     return template.TemplateResponse("userdet-admin.html", {"request": request, "user_detail" : user_detail})


# jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj


# ==============================================================JJJ=================================================


# @app.get("/users/users_main/user")
# async def users_main(request:Request, user=Depends(get_current_user)):
#     print(user)
#     print("a3",user)
#     return template.TemplateResponse("user_main.html", {"request": request, "user":user})

# @app.get("/users/transferpage")
# async def transfer_page(request: Request, user=Depends(get_current_user)):
#     print("a2",user)
#     return template.TemplateResponse("transferpage.html", {"request": request, "transferred": False,"insufficient":False, "user" : user})


# @app.post("/users/transfer/transferto")
# async def tranferhere(request:Request,user=Depends(get_current_user)):
#     sender_account = user["Account"]
#     print(sender_account)
#     form_data= await request.form()
#     receiver_account= int(form_data.get("account"))
#     print(receiver_account)
#     amount= int(form_data.get("amount"))
#     print(amount)

#     receiver=await  db.users.find_one({"Account": receiver_account})
    
#     sender= await db.users.find_one({"Account":sender_account})

    
#     if sender["balance"]<amount:
#         return template.TemplateResponse("transferpage.html", {"request": request,"transferred": False,"insufficient":True})
#     else:
#         newbalance= receiver["balance"]+amount
#         deduction= sender["balance"]-amount
#         sent_update=[receiver_account,receiver["Username"], amount, datetime.datetime.now()]
#         receive_update= [sender_account, sender["Username"] ,amount, datetime.datetime.now()]
#         sender_update = db.users.update_one(
#         {"Account": sender["Account"]},
#         {
#         "$set": {"balance": deduction},
#         "$push": {"Sent": {"$each": [sent_update], "$position": 0}}
#         },
#     upsert=False
# )
        
#         receiver_update = db.users.update_one(
#     {"Account": receiver["Account"]},
#     {
#         "$set": {"balance": newbalance},
#         "$push": {"Recieve": {"$each": [receive_update], "$position": 0}}
#     },
#     upsert=False
# )
#         return template.TemplateResponse("transferpage.html", {"request": request, "transferred":True, "insufficient":False, "user":user})

# @app.get("/users/user/transactions")
# async def transaction_page(request:Request, user=Depends(get_current_user)):
#     return template.TemplateResponse("transactions.html", {"request": request, "sents":user["Sent"], "received":user["Recieve"]})

# #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
# #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj



