from fastapi import APIRouter, Depends
from dependencies.depends import require_role,is_admin
from services.records_services import addRecords,getRecords,updateRecords,deleteRecords,getrecordSummary
from schemas.records_schemas import getrecords,updaterecords,addrecords
records = APIRouter(prefix='/records',tags=['records'])


@records.get('/summary')
def get_summary(is_user = Depends(require_role("user","admin","analyst"))):
   user_id = is_user['user_id']
   return getrecordSummary(is_user,user_id)
    

@records.get('/')
def get_records(data:getrecords,user=Depends(require_role("analyst" , "admin"))):
    return getRecords(user,data)

@records.post('/')
def add_records(data:addrecords,is_admin = Depends(is_admin)):
    return addRecords(is_admin,data)

@records.put('/{rec_id}')
def update_records(rec_id,data:updaterecords,is_admin = Depends(is_admin)):
    return updateRecords(is_admin,data,rec_id)

@records.delete('/{rec_id}')
def delete_records(rec_id,is_admin = Depends(is_admin)):
    return deleteRecords(is_admin,rec_id)