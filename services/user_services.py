from models.users_models import add_user,update_user,get_users,delete_users
import uuid

def addusers(data,is_admin):
    if is_admin:
        id=uuid.uuid4()
        name = data.user_name
        email = data.user_email
        password = data.user_password
        role = data.user_role
        status = data.user_status
        res= add_user(id,name,email,password,role,status)
        if res:
            return {'message':'user added successfully'}
        else:
            return {'message':'an error occured'}