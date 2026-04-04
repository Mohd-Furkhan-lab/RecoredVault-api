import jwt
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os

load_dotenv()

def create_token(userid,role):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    secret_key = os.getenv("SECRET_KEY")

    payload = {
        "user_id" : userid,
        "role" : role,
        "exp" : expire
    }
    token = jwt.encode(payload=payload,key=secret_key,algorithm="HS256")
    return token


def verify_token(token):
    if token:
        secret_key=os.getenv("SECRET_KEY")
        try :
            payload = jwt.decode(token,algorithms=["HS256"],key=secret_key)
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        

