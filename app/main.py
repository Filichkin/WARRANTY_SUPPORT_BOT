from fastapi import FastAPI

from app.users.router import router as router_users


app = FastAPI()


@app.get('/', summary='Warranty bot homepage')
def home_page():
    return {'message': 'Main page of warranty bot'}


app.include_router(router_users)
