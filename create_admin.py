from repo.db import SessionLocal,Base,engine
from models.users_models import Users
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

admin_name = os.getenv("admin_name")
admin_password = os.getenv("admin_password")

Base.metadata.create_all(bind=engine)



hash_passsword = bcrypt.hashpw(admin_password.encode(),bcrypt.gensalt())

def createadmin():
    with SessionLocal() as db:
        existing = db.query(Users).filter(Users.user_name == admin_name).first()

        if existing:
            print("Admin already exists")
            return

        hash_password = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt())

        admin = Users(
            user_name=admin_name,
            user_email="admin@recordvault.com",
            user_password=hash_password,
            role="admin",
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("Admin created")