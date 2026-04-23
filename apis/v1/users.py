from fastapi import APIRouter,Depends
from schemas.user_schemas import Login,adduser,Updateuser,GetUsers
from dependencies.depends import is_admin
from services.user_services import addUsers,upateUsers,deleteUser,getUsers,LoginUser

users=APIRouter(prefix='/users',tags=['users'])



@users.post('/login')
def user_login(data:Login):
    return LoginUser(data)



@users.post('/')
def add_user(data : adduser,is_admin = Depends(is_admin)):
    return addUsers(is_admin,data)


@users.put('/{user_id}')
def update_user(user_id,data:Updateuser,admin_id = Depends(is_admin)):
    return upateUsers(is_admin,data,user_id)

@users.delete('/{user_id}')
def delete(user_id,is_admin = Depends(is_admin)):
    return deleteUser(is_admin,user_id)


@users.get('/')
def get_allusers(data:GetUsers,is_admin = Depends(is_admin)):
    return getUsers(is_admin,data)
