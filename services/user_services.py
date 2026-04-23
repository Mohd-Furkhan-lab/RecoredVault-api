from models.users_models import add_user,update_user,get_users,delete_users,getpassword,getroleandid
from auth.jwt_token import create_token
import uuid
import bcrypt
from fastapi import HTTPException

def addUsers(is_admin,data):
    if is_admin:
        try:
            id=str(uuid.uuid4())
            name = data.user_name
            email = data.user_email
            password = data.user_password
            role = data.user_role
            status = data.user_status
            hash_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            res=add_user(id,name,email,hash_password,role,status)
            if res:
                return {'message': 'added successfully'}
            else:
                raise HTTPException(status_code=500, detail="failed to add user")
        except HTTPException:
            raise  # re-raise HTTP exceptions as-is
        except Exception as e:
            raise HTTPException(status_code=409, detail="user already exists") 
            
            

def upateUsers(is_admin,data,userid):
    if is_admin:
        newRole = data.new_role
        status = data.new_status
        res = update_user(userid,newRole,status)
        if res:
            return {'message':'update seccessfully'}
        else:
            raise HTTPException(404,detail="user not found")

def deleteUser(is_admin,user_id):
    if is_admin:
        user_id = user_id
        res = delete_users(user_id)
        if res:
            return {'message':'user deleted successfully'}
        else:
            raise HTTPException(404,detail="user not found")

def getUsers(is_admin,data):
    if is_admin:
        status = data.status
        role = data.role
        data = get_users(role,status)
        if data:
            return {'users' : data}
        else:
            raise HTTPException(404,detail="no data found")
    
def LoginUser(data):
    email = data.user_email
    password = data.user_password 
    storedpassword = getpassword(email)
    if storedpassword:
        is_authenticate = bcrypt.checkpw(password.encode(),storedpassword[0])
        credentials = getroleandid(is_authenticate,email)
        role = credentials['role']
        userid = credentials['userid']
        token =  create_token(userid[0],role[0])
        return {'message':f'token = {token}'}
    else:
        raise HTTPException(404,detail="user not found")


