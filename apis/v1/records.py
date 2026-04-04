from fastapi import APIRouter, Depends
from typing import Optional
from datetime import datetime
from dependencies.depends import require_role,is_admin

records = APIRouter(prefix='/records',tags=['records'])


@records.get('/summary')
def get_summary(is_user = Depends(require_role("user"))):
    return {'message':' records summary '}

@records.get('/')
def get_records(type:Optional[str]=None,category:Optional[str]=None,date=Optional[datetime],user=Depends(require_role("analyst" , "admin"))):
    if type and not category and not date:
        return {'message':'records filter by type'}
    elif category and not type and not date:
        return {'message':'records filter by category'}
    elif date and not category and not type:
        return {'message':'records filter by date'}
    return {'message':'all records '}

@records.post('/')
def add_records(is_admin = Depends(is_admin)):
    return {'message':'add records'}

@records.put('/{rec_id}')
def update_records(is_admin = Depends(is_admin)):
    return {'message':'update records'}

@records.delete('/{rec_id}')
def delete_records(is_admin = Depends(is_admin)):
    return {'message':'delete records'}