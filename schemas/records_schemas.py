from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class add_records(BaseModel):
    type : str
    category : str
    amount : float
    create_date : datetime
    description : str

class update_records(BaseModel):
    amount : Optional[float] = None
    description : Optional[str] = None
    type : Optional[str] = None
