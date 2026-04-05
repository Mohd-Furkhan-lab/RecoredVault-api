from repo.db import SessionLocal,base
from sqlalchemy import Column,Integer,String
from sqlalchemy.exc import SQLAlchemyError

class Users(base):
    __tablename__ = "users"
    user_id = Column(String,primary_key=True,nullable=False)
    user_name = Column(String,nullable=False)
    user_email = Column(String,nullable=False,unique=True)
    user_password = Column(String,nullable=False)
    role = Column(String,nullable=False)
    is_active = Column(String,nullable=False)

def add_user(id,name,email,password,role,status):
        try :
            with SessionLocal() as db:
                user=Users(
                    user_id = id,
                    user_name = name,
                    user_email = email,
                    user_password = password,
                    role = role,
                    is_active=status 
                )
                db.add(user)
                db.commit()
                return True
        except SQLAlchemyError :
             db.rollback()
             return False


def update_user(user_id,new_role,status):
        try :
            with SessionLocal() as db:
                user=db.query(Users).filter(Users.user_id == user_id).first()
                if new_role is not None:
                    user.role = new_role
                    db.commit()
                    return True
                if status is not None:
                    user.is_active = status
                    db.commit()
                    return True
        except SQLAlchemyError :
             db.rollback()
             return False


def get_users(role,status):
        try :
            with SessionLocal() as db:
                if role is not None and status is None:
                    users=db.query(Users).filter(Users.role == role).all()
                    return users
                elif role is None and status is not None:
                    users=db.query(Users).filter(Users.is_active == status).all()
                    return users
                users=db.query(Users).all()
                return users
        except SQLAlchemyError:
             return False

def delete_users(userid):
        try:
            with SessionLocal() as db:
                user=db.query(Users).filter(Users.user_id == userid).first()
                db.delete(user)
                db.commit()
                return True
        except SQLAlchemyError:
             db.rollback()
             return False

def getpassword(email):
    try : 
          with SessionLocal() as db:
               password = db.query(Users.user_password).filter(Users.user_email == email).first()
               return password
    except SQLAlchemyError :
         return False


def getroleandid(is_authenticate,email):
     if is_authenticate:
        try :  
            with SessionLocal() as db:
                 role = db.query(Users.role).filter(Users.user_email == email).first()
                 userid = db.query(Users.user_id).filter(Users.user_email == email).first()
                 return {"role" : role,"userid" : userid}
        except SQLAlchemyError:
             return False
               
