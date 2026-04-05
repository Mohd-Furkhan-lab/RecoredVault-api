from repo.db import SessionLocal,Base
from sqlalchemy import Column,String,Integer,DateTime,Float,func,ForeignKey
from sqlalchemy.exc import SQLAlchemyError

class Records(Base):
    __tablename__ = "records"
    record_id=Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(ForeignKey("Users.user_id"))
    record_type=Column(String,nullable=False)
    category=Column(String,nullable=False)
    amount=Column(Float,nullable=False)
    create_date=Column(DateTime,nullable=False)
    description=Column(String)


def  get_records(type,category):
    try:
        with SessionLocal() as db:
            if type is not None and category is None:
                data=db.query(Records).filter(Records.record_type == type).all()
                return data
            elif type is  None and category is not None:
                data=db.query(Records).filter(Records.category == category).all()
                return data
            elif type is not None and category is not None:
                data=db.query(Records).filter(Records.record_type == type , Records.category == category).all()
                return data
            data=db.query(Records).all()
    except SQLAlchemyError:
        return False

def add_records(user_id,type,category,amount,datetime,description):
    try :
        with SessionLocal() as db:
            record=Records(
                user_id = user_id,
                record_type = type,
                category=category,
                amount = amount,
                create_date = datetime,
                description = description
                )
            db.add(record)
            db.commit()
            return True
    except SQLAlchemyError:
        db.rollback()
        return False

def update_records(user_id,record_id,amount,description,type):
    try:
        if record_id :
            with SessionLocal() as db:
                is_records = db.query(1).filter(Records.user_id == user_id).first()
                if is_records:
                    record=db.query(Records).filter(Records.record_id == record_id,Records.user_id == user_id).first()
                    if amount is not None:
                        record.amount = amount
                    if description is not None:
                        record.description = description
                    if type is not None:
                        record.record_type = type            
                    db.commit()
                    return True
    except SQLAlchemyError:
        db.rollback()
        return False

def delete_record(record_id,user_id):
    try:
        with SessionLocal() as db:
            record=db.query(Records).filter(Records.record_id == record_id,Records.user_id == user_id).first()
            if record:
                db.delete(record)
                db.commit()
                return True
    except SQLAlchemyError:
        db.rollback()
        return False

def records_summary(user_id):
    try:
        with SessionLocal() as db:
            is_records=db.query(1).filter(Records.user_id == user_id).first()
            if is_records:
                total_expense = db.query(func.sum(Records.amount)).filter(Records.record_type  == "expense",Records.user_id == user_id).scalar()
                total_income = db.query(func.sum(Records.amount)).filter(Records.record_type == "income",Records.user_id == user_id).scalar()
                net_balance = total_income - total_expense
                return {
                    "total_income" : total_income,
                    "total_expense" : total_expense,
                    "net_balance" : net_balance
                }
    except SQLAlchemyError:
        return False