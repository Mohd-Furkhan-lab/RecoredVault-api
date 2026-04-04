from pydantic import BaseModel

class Signup(BaseModel):
    user_name : str
    user_email : str
    user_password : str


class Login(BaseModel):
    user_email : str
    user_password : str


