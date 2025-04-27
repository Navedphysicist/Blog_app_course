from fastapi import FastAPI,HTTPException,Depends,Request
import time
import asyncio



def log_request(request: Request):
    print(f"Request made to: {request.url}")
    print(f"request : {request}")
    return request


app = FastAPI(dependencies=[Depends(log_request)])

@app.get('/blocking')
def blocking_route():

    time.sleep(5)

    return {
        'route' : 'blocking'
    }


@app.get('/non-blocking')
async def non_blocking_router():

    await asyncio.sleep(5)

    return {
        'route' : 'non-blocking'
    }


def get_token():
    return 'secure'

def check_authorization(token:str = Depends(get_token) ):
    if token != 'secure':
        raise HTTPException(status_code=403,detail='Invalid Token')
    return {'user': 'User Authenticated'}


@app.get('/user-profile')
def get_profile(token:str):
    user = check_authorization(token)
    return user


@app.get('/user-profile-depedency')
def get_profile(user :dict = Depends(check_authorization)):
    return user

@app.get('/settings')
def settings(user :dict = Depends(check_authorization)):
    return user



class Account:
    def __init__(self,name,email):
        self.name = name
        self.email = email

@app.get("/")
def home(request = Depends(log_request), account : Account = Depends()): 
    return {"message": "Home Page", 'username' : account.name, 'email' : account.email}


