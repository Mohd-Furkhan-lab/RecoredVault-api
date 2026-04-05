from models.records_models import add_records,update_records,delete_record,get_records,records_summary

def addRecords(is_admin,data):
    if is_admin:
        userid = data.user_id
        rectype = data.type
        category = data.category
        amount = data.amount
        date = data.create_date
        description = data.description
        res = add_records(userid,rectype,category,amount,date,description)
        if res:
            return {'message' : 'added successfully'}
        else:
            return {'message' : 'an error occured'}

def updateRecords(is_admin,data,recordId):
    if is_admin:
        userid = data.user_id
        amount = data.amount
        description = data.description
        type = data.type
        res = update_records(userid,recordId,amount,description,type)
        if res:
            return {'message':'updated successfully'}
        else:
            return {'message':'an error occured'}

def deleteRecords(data,is_admin,record_id):
    if is_admin:
        userid = data.user_id
        res=delete_record(record_id,userid)
        if res:
            return {'message':'deleted successfully'}
        else:
            return {'message':'an error occured'}
        

def getRecords(is_authorize,data):
    if is_authorize:
        type = data.type
        category = data.category
        records=get_records(type,category)
        if records:
            return {'data': records }
        else:
            return {'message':'an error occured'}
        
def getrecordSummary(is_allowed,userid):
    if is_allowed:
        user_id = userid
        data = records_summary(user_id)
        if data:
            return {'summary' : data}
        else:
            return {'message' : 'an error occured'}
