from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class addrecords(BaseModel):
    type : str
    category : str
    amount : float
    create_date : datetime
    description : str

class updaterecords(BaseModel):
    amount : Optional[float] = None
    description : Optional[str] = None
    type : Optional[str] = None

class getrecords(BaseModel):
    type : Optional[str] = None
    category : Optional[str] = None