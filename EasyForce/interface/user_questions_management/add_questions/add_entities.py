from datetime import timedelta
from EasyForce.common.constants import *
from EasyForce.data_mangement.data_modification_old import add_record
from EasyForce.common.utils import questions, is_positive_integer, is_number, \
    yes_no_question, get_datetime_input
from EasyForce.data_mangement.read_db import get_primary_key_column_names, \
    get_column_value_by_primary_key, get_primary_key_val_by_unique_column_val,get_column_values
from EasyForce.interface.user_questions_management.general_questions import ask_open_ended_question, ask_for_name, \
    ask_closed_ended_question


def add_TimeRange_questions(table, table_data):
    """
    Adds time ranges for a soldier's presence (in/out) at the base
    """
    ################## I need to add team option################################
    if table == SOLDIER_TABLE:
        questions(PRESENCE_TABLE,ADD,table,table_data,"in")
        questions(PRESENCE_TABLE,ADD,table,table_data,"out")
    else:
        questions(PRESENCE_TABLE,ADD,table,table_data)

def add_Team_questions(soldier_name = None):
    question = "Please enter the team name ('R' to return): "
    data = {}

    if soldier_name:
        question = f"Please enter {soldier_name}'s team name: "


    # Request team name from the user
    team_name = ask_open_ended_question(question,"Team name",previous_question=True if not soldier_name else False)
    if not team_name:
        return None

    data["TeamName"] = team_name
    team_id = add_record(TEAM_TABLE, data)
    team_table_primary_columns = get_primary_key_column_names(TEAM_TABLE)
    team_name = get_column_value_by_primary_key(TEAM_TABLE,"TeamName",team_table_primary_columns,team_id)
    if not soldier_name:
        question = f"add soldiers to {team_name} team"
        while True:
            answer = yes_no_question(question)
            if answer:
                if not questions(SOLDIER_TABLE, ADD, team_name):
                    return team_id
                question = f"add more soldiers to {team_name} team"
            else:
                break
    return team_id

def add_Soldier_questions(team_name = None):
    data = {}
    question = f"Please enter the soldier name ('R' to return): "
    if team_name:
        question = f"Please enter a soldier name ('R' to return): "

    # Request soldier name from the user
    soldier_name = ask_open_ended_question(question,"Soldier name",previous_question=True)
    if not soldier_name:
        return None

    # Request soldier name from the user
    question = f"Please enter {soldier_name}'s ID: "
    while True:
        soldier_id = ask_open_ended_question(question,"Soldier ID")
        if not is_positive_integer(soldier_id):
            print("Soldier ID has to be a positive number. Please try again.")
        else:
            break

    # Add data to the dictionary
    data["FullName"] = soldier_name
    data["SoldierID"] = soldier_id

    #add roles
    questions(ROLE_TABLE,ADD,SOLDIER_TABLE,data)

    #add soldier's team
    if team_name:
        data["TeamID"] = get_primary_key_val_by_unique_column_val(TEAM_TABLE,team_name)
    else:
        question = f"Please select {soldier_name}'s team:"
        teams = get_column_values(TEAM_TABLE,"TeamName")
        if teams:
            teams.append("Add a new team")
            team_name = ask_closed_ended_question(question, teams)
            if team_name == "Add a new team":
                data["TeamID"] = questions(TEAM_TABLE, ADD, soldier_name)[0]
            else:
                team_id = get_primary_key_val_by_unique_column_val(TEAM_TABLE, team_name)
                data["TeamID"] = team_id
        else:
            print("There are no existing teams. Please add a team first")
            data["TeamID"] = questions(TEAM_TABLE,ADD,soldier_name)[0]
    soldier_id = add_record(SOLDIER_TABLE,data)
    questions(TIME_RANGE_TABLE,ADD,SOLDIER_TABLE,data)
    return soldier_id

def add_Role_questions(table,table_data):
    if table == SOLDIER_TABLE:
        if yes_no_question(f"add {table_data['FullName']} a role"):
            questions(SOLDIER_ROLE_TABLE,ADD,table_data)
    elif table == TEMPORARY_TASK_TABLE or table == RECURRING_TASK_TABLE:
        if yes_no_question("add any restrictions to this task (in terms of roles or soldiers)"):
            if yes_no_question("add specific roles that must be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,ROLE_TABLE,ADD)
            if yes_no_question("add specific roles that can't be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,ROLE_TABLE,DELETE)
            if yes_no_question("add specific soldiers that must be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,SOLDIER_TABLE,ADD)
            if yes_no_question("add specific soldiers that can't be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,SOLDIER_TABLE,DELETE)

def add_Task_questions(table):
    data = {}
    task_rep = shift_dur = amount = 0

    #Request task name from the user
    task_name = "temporary " if table == TEMPORARY_TASK_TABLE else "recurring "
    task_name += "task"
    task_name = ask_for_name(task_name)

    # Request temporarily task reputation from the user
    if table == TEMPORARY_TASK_TABLE:
        question = "Please enter the task reputation:"
        options = ["Good","Bad","None"]
        task_rep = ask_closed_ended_question(question,options)
    # Request recurring task shift duration and required personal from the user
    else: #Recurring task
        question = "Please enter a shift duration (in hours): "
        empty_name = "A shift"
        while True:
            shift_dur = ask_open_ended_question(question,empty_name)
            if not is_number(shift_dur):
                print("A shift duration has to be a number. Please try again.")
            elif float(shift_dur) <= 0:
                print("A shift duration has to be a positive number. Please try again.")
            else:
                break
        question = "Please enter the required personnel for the task: "
        empty_name = "A required"
        while True:
            amount = ask_open_ended_question(question,empty_name)
            if not is_number(amount):
                print("A required personnel has to be a number. Please try again.")
            elif float(amount) <= 0:
                print("A required personnel has to be a positive number. Please try again.")
            else:
                amount = int(amount)
                break
        question = "Please enter the time when the task starts each day (press Enter if the task lasts all day): "
        start_time = get_datetime_input(question,timedelta(days=0),"%H:%M")
        if not start_time[0]:
            data["EveryDayStartTime"] = data["EveryDayEndTime"] = MIDNIGHT
        else:
            question = "Please enter the time when the task ends each day (you can enter a time after midnight if the task continues into the next day): "
            while True:
                end_time = get_datetime_input(question, timedelta(days=0),"%H:%M")
                if not end_time[0]:
                    print("You must specify an end time for the task.")
                else:
                    break
            data["EveryDayStartTime"] = start_time[1]
            data["EveryDayEndTime"] = end_time[1]

    # Add data to the dictionary
    data["TaskName"] = task_name
    if table == TEMPORARY_TASK_TABLE:
        data["TaskReputation"] = task_rep
        data["TaskID"] = add_record(TEMPORARY_TASK_TABLE, data)[0]
    else:
        data["ShiftDurationInMinutes"] = int(float(shift_dur) * MIN_IN_HOUR)
        data["RequiredPersonnel"] = amount
        data["TaskID"] = add_record(RECURRING_TASK_TABLE, data)[0]
    questions(TIME_RANGE_TABLE,ADD,table,data)
    questions(ROLE_TABLE,ADD,table,data)

    return data["TaskID"]