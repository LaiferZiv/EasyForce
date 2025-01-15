from datetime import timedelta
from EasyForce.common.constants import *
from EasyForce.data_mangement.data_modification import add_record
from EasyForce.common.utils import questions, is_positive_integer, is_number, \
    yes_no_question, get_datetime_input
from EasyForce.data_mangement.read_db import get_primary_key_column_names, \
    get_column_value_by_primary_key, get_primary_key_val_by_unique_column_val
from EasyForce.interface.user_questions_management.general_questions import ask_open_ended_question, ask_for_name, \
    ask_closed_ended_question


def add_TimeRange_questions(table, table_data):
    """
    Adds time ranges for a soldier's presence (in/out) at the base
    """
    ################## I need to add team option################################
    def add_time_ranges(pos = ""):
        time_format = "time (YYYY-MM-DD HH:MM) or press Enter"
        is_presence = 1
        if table == SOLDIER_TABLE:
            question = f"add times when {table_data['FullName']} is {pos} the base"
            is_presence = 1 if pos == "in" else 0
            (start_prompt,end_prompt) = ("arrival","departure") if is_presence else ("departure","return")
            start_prompt = f"Enter {table_data['FullName']}'s {start_prompt} {time_format} for now: "
            end_prompt = f"Enter {table_data['FullName']}'s {end_prompt} {time_format} if unknown: "
            more_question = f"add more times when {table_data['FullName']} is {pos} the base"
        else: #Tasks
            question = f"add the time range during which the task {table_data['TaskName']} is relevant ('No' indicates it's inactive)"
            start_prompt = f"Enter the task's start {time_format} for now: "
            end_prompt = f"Enter the task's end {time_format} if unknown: "
            more_question = f"add more times when {table_data['TaskName']} is active"

        is_active = yes_no_question(question)
        if is_active:
            while True:
                start_dt = get_datetime_input(start_prompt,timedelta(days=0))
                end_dt = get_datetime_input(end_prompt,timedelta(days=YEAR))
                time_range_data = {
                "StartDateTime" : start_dt,
                "EndDateTime" : end_dt
                }
                time_range_id = add_record(TIME_RANGE_TABLE,time_range_data)[0]
                presence_data = {
                "SoldierTeamTaskType" : table,
                "SoldierTeamTaskID" : table_data["SoldierID"] if table == SOLDIER_TABLE else table_data["TaskID"],
                "TimeID" : time_range_id,
                "isActive" : is_presence if table == SOLDIER_TABLE else 1
                }
                print(presence_data)
                questions(PRESENCE_TABLE,ADD,presence_data)

                if not yes_no_question(more_question):
                    break

    if table == SOLDIER_TABLE:
        add_time_ranges("in")
        add_time_ranges("out")
    else:
        add_time_ranges()

def add_Team_questions(soldier_name = None):
    question = "Please enter the team name: "
    if soldier_name:
        question = f"Please enter {soldier_name}'s team name ('R' to return): "
    data = {}

    # Request team name from the user
    team_name = ask_open_ended_question(question,"Team name",previous_question=True)
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
                question = f"add more soldiers to {team_name} team?"
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
            table_data["SoldierOrRole"] = ROLE_TABLE
            if yes_no_question("add specific roles that must be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,ROLE_TABLE,ADD)
            if yes_no_question("add specific roles that can't be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,ROLE_TABLE,DELETE)
            table_data["SoldierOrRole"] = SOLDIER_TABLE
            if yes_no_question("add specific soldiers that must be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,SOLDIER_TABLE,ADD)
            if yes_no_question("add specific soldiers that can't be included in the task"):
                questions(TASK_ROLE_TABLE,ADD,table,table_data,SOLDIER_TABLE,DELETE)

def add_Task_questions(table):
    data = {}
    task_rep = shift_dur = amount = 0

    #Request task name from the user
    task_name = "temporary " if table == TEMPORARY_TASK_TABLE else "recurring"
    task_name += "task"
    task_name = ask_for_name(task_name)

    # Request temporarily task reputation from the user
    if table == TEMPORARY_TASK_TABLE:
        question = "Please enter the task reputation:"
        options = ["Good","Bad","None"]
        task_rep = ask_closed_ended_question(question,options)
    # Request recurring task shift duration and required personal from the user
    else:
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


    # Add data to the dictionary
    data["TaskName"] = task_name
    if table == TEMPORARY_TASK_TABLE:
        data["TaskID"] = add_record(TEMPORARY_TASK_TABLE, data)[0]
        data["TaskReputation"] = task_rep
    else:
        data["TaskID"] = add_record(RECURRING_TASK_TABLE, data)[0]
        data["ShiftDurationInMinutes"] = int(float(shift_dur) * MIN_IN_HOUR)
        data["RequiredPersonnel"] = amount
    questions(TIME_RANGE_TABLE,ADD,table,data)
    questions(ROLE_TABLE,ADD,table,data)


    return data["TaskID"]