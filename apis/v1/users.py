from fastapi import APIRouter,Depends
from schemas.user_schemas import Login,adduser,Updateuser,GetUsers
from dependencies.depends import is_admin


users=APIRouter(prefix='/users',tags=['users'])



@users.post('/login')
def user_login(data:Login):
    return {'message':'user login successfully'}



@users.post('/')
def add_user(data : adduser,admin_id = Depends(is_admin)):
    return {'message':'added successfully'}


@users.put('/{user_id}')
def update_user(data:Updateuser,admin_id = Depends(is_admin)):
    return {'message':'updated user'}

@users.delete('/{user_id}')
def delete(admin_id = Depends(is_admin)):
    return {'message':'updated user'}


@users.get('/')
def get_allusers(data:GetUsers,admin_id = Depends(is_admin)):
    role = data['role'],status=data['status']
    if role and not status:
        return {'message' : 'get users by role'}
    elif not role and  status:
        return {'message' : 'get users by status'}  
    return {'message':'all users '}

