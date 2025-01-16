from EasyForce.common.constants import *
from EasyForce.data_mangement.read_db import get_column_values,get_primary_key_val_by_unique_column_val
from EasyForce.data_mangement.data_modification import add_record
from EasyForce.interface.user_questions_management.general_questions import ask_closed_ended_question,ask_open_ended_question
from EasyForce.common.utils import is_positive_integer,yes_no_question


def add_Presence_questions(table_data):
    return add_record(PRESENCE_TABLE,table_data)

def add_SoldierRole_questions(table_data):
    question = f"{table_data['FullName']}'s role: "
    empty_name = "Role name"
    while True:
        role_name = ask_open_ended_question(question, empty_name)
        table_data["RoleID"] = add_record("Role", {"RoleName": role_name})
        add_record(SOLDIER_ROLE_TABLE, {"SoldierID": table_data["SoldierID"], "RoleID": table_data["RoleID"][0]})
        another_role = f"add {table_data['FullName']} another role"
        if not yes_no_question(another_role):
            break

def add_TaskRole_questions(table_type,table_data,entity_type,enforcement_type,min_required_count = 0):
    def add_role():
        nonlocal min_required_count
        role_name_list = get_column_values(ROLE_TABLE, "RoleName")
        while True:
            if not role_name_list:
                print("There are no roles to choose from")
                break
            question_name = "Role name:"
            role_name = ask_closed_ended_question(question_name, role_name_list)
            role_name_list.remove(role_name)
            if enforcement_type == ADD:
                question_amount = "How many of this role are essential for this task? "
                while True:
                    min_required_count = ask_open_ended_question(question_amount, "An amount")
                    if is_positive_integer(min_required_count):
                        min_required_count = int(min_required_count)
                        break

            task_role_data = {
                "TaskType": table_type,
                "TaskID": table_data["TaskID"],
                "SoldierOrRole": ROLE_TABLE,
                "SoldierOrRoleID": get_primary_key_val_by_unique_column_val(ROLE_TABLE, role_name),
                "MinRequiredCount": min_required_count,
                "RoleEnforcementType": role_enforcement_type
            }
            add_record(TASK_ROLE_TABLE,task_role_data)
            if not yes_no_question("add another role"):
                break
    def add_soldier():
        id_list = get_column_values(SOLDIER_TABLE, "SoldierID")
        if not id_list:
            print("There are no soldiers to choose from")
            return
        name_list = get_column_values(SOLDIER_TABLE, "FullName")
        name_and_id = [f"{name}, ID: {ID}" for name, ID in zip(name_list, id_list)]
        while True:
            if not name_and_id:
                print("There are no soldiers to choose from")
                break
            question_name = "Choose a soldier:"
            soldier_name = ask_closed_ended_question(question_name, name_and_id)
            name_and_id.remove(soldier_name)
            soldier_id = int(soldier_name.split("ID: ")[1])

            task_role_data = {
                "TaskType": table_type,
                "TaskID": table_data["TaskID"],
                "SoldierOrRole": SOLDIER_TABLE,
                "SoldierOrRoleID": soldier_id,
                "MinRequiredCount": 1,
                "RoleEnforcementType": role_enforcement_type
            }
            add_record(TASK_ROLE_TABLE, task_role_data)
            if not yes_no_question("add another soldier"):
                break

    role_enforcement_type = 1 if enforcement_type == ADD else 0
    if entity_type == SOLDIER_TABLE:
        add_soldier()
    else:
        add_role()

def add_CurrentTaskAssignment_questions():
    return

def add_TaskHistory_questions():
    return