from EasyForce.data_mangement.data_modification import add_record

def add_Presence_questions(table_data):
    return add_record("Presence",table_data)

def add_SoldierRole_questions(table_data):
    return add_record("SoldierRole", {"SoldierID": table_data["SoldierID"], "RoleID": table_data["RoleID"][0]})

def add_TaskPeriod_questions():
    return

def add_TaskRole_questions():
    return

def add_CurrentTaskAssignment_questions():
    return

def add_TaskHistory_questions():
    return