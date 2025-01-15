from EasyForce.common.constants import *
from EasyForce.data_mangement.data_modification import add_record

def add_Presence_questions(table_data):
    return add_record(PRESENCE_TABLE,table_data)

def add_SoldierRole_questions(table_data):
    return add_record(SOLDIER_ROLE_TABLE, {"SoldierID": table_data["SoldierID"], "RoleID": table_data["RoleID"][0]})

def add_TaskRole_questions(table_data):
    add_record(TASK_ROLE_TABLE,table_data)
    return

def add_CurrentTaskAssignment_questions():
    return

def add_TaskHistory_questions():
    return