from datetime import timedelta
from EasyForce.data_mangement.data_modification import add_record
from EasyForce.common.utils import questions, is_positive_integer, is_number, \
    yes_no_question,get_datetime_input
from EasyForce.data_mangement.read_db import get_primary_key_column_names,\
    get_column_value_by_primary_key,get_primary_key_val_by_unique_column_val


def add_TimeRange_questions(table, table_data):
    """
    Adds time ranges for a soldier's presence (in/out) at the base
    """
    def add_time_ranges(pos = ""):
        time_format = "time (YYYY-MM-DD HH:MM) or press Enter"
        is_presence = 1
        if table == "Soldier":
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
                end_dt = get_datetime_input(end_prompt,timedelta(days=365))
                time_range_data = {
                "StartDateTime" : start_dt,
                "EndDateTime" : end_dt
                }
                time_range_id = add_record("TimeRange",time_range_data)
                presence_data = {
                "TimeID" : time_range_id,
                "SoldierOrTeamType" : table,
                "SoldierOrTeamID" : table_data["SoldierID"] if table == "Soldier" else table_data["TeamID"],
                "isPresence" : is_presence if table == "Soldier" else 1
                }
                questions("Presence" if table == "Soldier" else "TaskPeriod","add",presence_data)

                if not yes_no_question(more_question):
                    break

    if table == "Soldier":
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
    while True:
        team_name = input(question).strip()
        if team_name:
            break
        else:
            print("Team name cannot be empty. Please try again.")
    if team_name in {'R','r'}:
        return None

    data["TeamName"] = team_name
    team_id = add_record("Team", data)
    team_table_primary_columns = get_primary_key_column_names("Team")
    team_name = get_column_value_by_primary_key("Team","TeamName",team_table_primary_columns,team_id)
    if not soldier_name:
        question = f"add soldiers to {team_name} team"
        while True:
            answer = yes_no_question(question)
            if answer:
                if not questions("Soldier", "add", team_name):
                    return team_id
                question = f"add more soldiers to {team_name} team?"
            else:
                break
    return team_id

def add_Soldier_questions(team_name):
    data = {}
    question = f"Please enter the soldier name ('R' to return): "
    if team_name:
        question = f"Please enter a soldier name ('R' to return): "

    # Request soldier name from the user
    while True:
        soldier_name = input(question).strip()
        if not soldier_name:
            print("Soldier name cannot be empty. Please try again.")
            continue
        elif soldier_name in {'R','r'}:
            return None
        else:
            break

    # Request soldier name from the user
    while True:
        question = f"Please enter {soldier_name}'s ID: "
        soldier_id = input(question).strip()
        if not soldier_id:
            print("Soldier ID cannot be empty. Please try again.")
        elif not is_positive_integer(soldier_id):
            print("Soldier ID has to be a positive number. Please try again.")
        else:
            break

    # Add data to the dictionary
    data["FullName"] = soldier_name
    data["SoldierID"] = soldier_id

    #add roles
    questions("Role","add","Soldier",data)

    #add soldier's team
    if team_name:
        data["TeamID"] = get_primary_key_val_by_unique_column_val("Team",team_name)
    else:
        data["TeamID"] = questions("Team","add",soldier_name)[0]

    soldier_id = add_record("Soldier",data)
    questions("TimeRange","add","Soldier",data)
    return soldier_id

def add_Role_questions(table,table_data):
    if table == "Soldier":
        question = f"add {table_data['FullName']} a role"
        has_role = yes_no_question(question)

        if has_role:
            while True:
                role_name = input(f"{table_data['FullName']}'s role: ")
                if not role_name:
                    print("Role name cannot be empty. Please try again.")
                    continue
                table_data["RoleID"] = add_record("Role", {"RoleName": role_name})
                questions("SoldierRole","add",table_data)
                question = f"add {table_data['FullName']} another role"
                another_role = yes_no_question(question)
                if not another_role:
                    break
    elif table == "TemporaryTask" or table == "RecurringTask":
        return

def add_TemporaryTask_questions():
    data = {}

    # Request task name from the user
    while True:
        task_name = input("Please enter the temporary task name ('R' to return): ").strip()
        if not task_name:
            print("Task name cannot be empty. Please try again.")
        elif task_name in {'r','R'}:
            return None
        else:
            break

    # Request task reputation (good or bad) from the user
    while True:
        task_rep = input("Please enter the task reputation (good/bad/none): ").strip()
        if not ( task_rep == 'good' or task_rep == 'bad' or task_rep == 'none') :
            print("Task reputation has to be 'good' or 'bad' or 'none'. Please try again.")
        else:
            break

    while True:
        task_active = input("Does it active? enter 'y' or 'n' (yes/no): ").strip()
        if not ( task_active == 'y' or task_active == 'n') :
            print("you have to fill either y or n. Please try again.")
        else:
            break
    # Add data to the dictionary
    data["TaskName"] = task_name
    data["TaskReputation"] = task_rep
    data["isActive"] = task_active

    return data

def add_RecurringTask_questions():
    data = {}

    # Request task name from the user
    task_name = input("Please enter the recurring task name: ").strip()

    if not task_name:
        print("Task name cannot be empty. Please try again.")
        return None

    # Request a shift duration from the user
    while True:
        task_shift = input("Please enter a shift duration (in hours): ").strip()
        if not is_number(task_shift):
            print("A shift duration has to be a number. Please try again.")
        elif float(task_shift) <= 0:
            print("A shift duration has to be a positive number. Please try again.")
        else:
            break
    # Request a Required personnel from the user
    while True:
        amount = input("Please enter the required personnel for the task: ").strip()
        if not is_number(amount):
            print("A required personnel has to be a number. Please try again.")
        elif float(amount) <= 0:
            print("A required personnel has to be a positive number. Please try again.")
        else:
            break

    # Add data to the dictionary
    data["TaskName"] = task_name
    data["ShiftDurationInMinutes"] = float(task_shift) * 60
    data["RequiredPersonnel"] = float(amount)



    return data