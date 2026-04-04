from fastapi import APIRouter
from schemas.user_schemas import Login,Signup

users=APIRouter(prefix='/users',tags=['users'])



@users.post('/login')
def user_login(data:Login):
    return {'message':'user login successfully'}



@users.post('/')
def add_user()