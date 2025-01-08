from datetime import datetime,timedelta
from EasyForce.data_mangement.data_modification import add_record
from EasyForce.utils import questions,is_positive_integer,is_number
from EasyForce.data_mangement.read_db import get_primary_key_column_names,get_column_value_by_primary_key,get_primary_key_val_by_unique_column_val

def add_TimeRange_questions(table, table_data):
    """
    Adds time ranges for a soldier's presence (in/out) at the base
    """

    # Ensure we're dealing with the "Soldier" table
    if table == "Soldier":

        # Ask if the user wants to add time ranges for "in"
        while True:
            ans_in = input(f"Would you like to add times when {table_data['FullName']} is present at the base? (Y/N): ").strip()
            if ans_in in {'y', 'Y', 'n', 'N'}:
                break
            else:
                print("Invalid input! Please enter Y or N.")

        if ans_in in {'y', 'Y'}:
            while True:
                #Get start time
                while True:
                    start_input = input(
                        f"Enter {table_data['FullName']}'s arrival time (YYYY-MM-DD HH:MM) or 'n'/'N' for now: ").strip()
                    if start_input in {'n', 'N'}:
                        start_dt = datetime.now()
                        break
                    else:
                        try:
                            start_dt = datetime.strptime(start_input, "%Y-%m-%d %H:%M")
                            break
                        except ValueError:
                            print("Invalid format. Please use 'YYYY-MM-DD HH:MM' or 'n'/'N' for now.")

                # Get end time
                while True:
                    end_input = input(
                        f"Enter {table_data['FullName']}'s departure time (YYYY-MM-DD HH:MM), or press Enter if unknown: "
                    ).strip()
                    if end_input == "":
                        # Default: 1 year from now if unknown
                        end_dt = start_dt + timedelta(days=365)
                        break
                    else:
                        try:
                            end_dt = datetime.strptime(end_input, "%Y-%m-%d %H:%M")
                            break
                        except ValueError:
                            print("Invalid format. Please use 'YYYY-MM-DD HH:MM' or press Enter if unknown.")

                # Convert datetime objects to string format
                start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

                # add to TimeRange table
                time_range_id = add_record("TimeRange", {"StartDateTime": start_str, "EndDateTime": end_str})

                # add to Presence table (indicating "in")
                data = {
                    "SoldierOrTeamType": "Soldier",
                    "SoldierOrTeamID": table_data["SoldierID"],
                    "TimeID": time_range_id[0],
                    "isPresence": 1,  # 1 = in
                }
                questions("Presence", "add", data)

                # Ask if user wants to add more "in" time ranges
                while True:
                    ans_more_in = input(f"Would you like to add more times when {table_data['FullName']} is in the base? (Y/N): ").strip()
                    if ans_more_in in {'y', 'Y', 'n', 'N'}:
                        break
                    else:
                        print("Invalid input! Please enter Y or N.")

                if ans_more_in not in {'y', 'Y'}:
                    break

        # Ask if the user wants to add time ranges for "out"
        while True:
            ans_out = input(f"Would you like to add times when {table_data['FullName']} is out of the base? (Y/N): ").strip()
            if ans_out in {'y', 'Y', 'n', 'N'}:
                break
            else:
                print("Invalid input! Please enter Y or N.")

        if ans_out in {'y', 'Y'}:
            while True:
                # Get start time (out = departure)
                while True:
                    start_input = input(
                        f"Enter {table_data['FullName']}'s departure time (YYYY-MM-DD HH:MM) or 'n'/'N' for now: "
                    ).strip()
                    if start_input in {'n', 'N'}:
                        start_dt = datetime.now()
                        break
                    else:
                        try:
                            start_dt = datetime.strptime(start_input, "%Y-%m-%d %H:%M")
                            break
                        except ValueError:
                            print("Invalid format. Please use 'YYYY-MM-DD HH:MM' or 'n'/'N' for now.")

                # 2b) Get end time (return)
                while True:
                    end_input = input(
                        f"Enter {table_data['FullName']}'s return time (YYYY-MM-DD HH:MM), or press Enter if unknown: "
                    ).strip()
                    if end_input == "":
                        end_dt = start_dt + timedelta(days=365)
                        break
                    else:
                        try:
                            end_dt = datetime.strptime(end_input, "%Y-%m-%d %H:%M")
                            break
                        except ValueError:
                            print("Invalid format. Please use 'YYYY-MM-DD HH:MM' or press Enter if unknown.")

                # Convert datetime objects to string format
                start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

                # add to TimeRange table
                time_range_id = add_record("TimeRange", {"StartDateTime": start_str, "EndDateTime": end_str})

                #add to Presence table (indicating "out")
                data = {
                    "SoldierOrTeamType": "Soldier",
                    "SoldierOrTeamID": table_data["SoldierID"],
                    "TimeID": time_range_id[0],
                    "isPresence": 0,  # 0 = out
                }
                questions("Presence", "add", data)

                #Ask if user wants to add more "out" time ranges
                while True:
                    ans_more_out = input(f"Would you like to add more times when {table_data['FullName']} is out the base? (Y/N): ").strip()
                    if ans_more_out in {'y', 'Y', 'n', 'N'}:
                        break
                    else:
                        print("Invalid input! Please enter Y or N.")

                if ans_more_out not in {'y', 'Y'}:
                    break

def add_Team_questions(soldier_name = "the "):
    data = {}
    return_to_last_question = " ('R' to return)"
    more = ""
    by_soldier = False
    if soldier_name != "the ":
        by_soldier = True
        soldier_name = f"{soldier_name}'s "
        return_to_last_question = ""

    # Request team name from the user
    while True:
        team_name = input(f"Please enter {soldier_name}team name{return_to_last_question}: ").strip()
        if not team_name:
            print("Team name cannot be empty. Please try again.")
        else:
            break
    if return_to_last_question == " ('R' to return)" and team_name in {'R','r'}:
        return None

    data["TeamName"] = team_name
    team_id = add_record("Team", data)
    team_primary_columns = get_primary_key_column_names("Team")
    team_name = get_column_value_by_primary_key("Team","TeamName",team_primary_columns,team_id)
    if not by_soldier:
        while True:
            ans = input(f"Would you like to add {more}soldiers to {team_name} team? (Y/N): ").strip()
            if ans not in {'y','Y','n','N'}:
                print("Invalid input! Please enter Y or N.")
                continue
            elif ans in {'y','Y'}:
                if questions("Soldier", "add", team_name):
                    more = "more "
            else: # N
                break
    return team_id

def add_Soldier_questions(team_name):
    data = {}
    prefix = "a" if team_name else "the"
    # Request soldier name from the user
    soldier_name = input(f"Please enter {prefix} soldier name ('R' to return): ").strip()

    if not soldier_name:
        print("Soldier name cannot be empty. Please try again.")
        return None
    elif soldier_name in {'R','r'}:
        return None

    # Request soldier name from the user
    while True:
        soldier_id = input(f"Please enter {soldier_name}'s ID: ").strip()
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
    if not team_name:
        data["TeamID"] = questions("Team","add",soldier_name)[0]
    else:
        data["TeamID"] = get_primary_key_val_by_unique_column_val("Team",team_name)
    soldier_id = add_record("Soldier",data)
    questions("TimeRange","add","Soldier",data)
    return soldier_id

def add_Role_questions(table,table_data):
    if table == "Soldier":
        while True:
            has_role = input(f"Does {table_data['FullName']} has a Role? (Y/N): ")
            if has_role in {'y', 'Y', 'n', 'N'}:
                break
            else:
                print("Invalid input! Please enter Y or N.")

        if has_role == 'Y' or has_role == 'y':
            print(f"Enter {table_data['FullName']}'s roles one by one, when you finish enter 'N'.")
            while True:
                role_name = input(f"{table_data['FullName']}'s role ('N' to end): ")
                if not role_name:
                    print("Role name cannot be empty. Please try again.")
                    continue
                if role_name == 'n' or role_name == 'N':
                    break
                table_data["RoleID"] = add_record("Role", {"RoleName": role_name})
                questions("SoldierRole","add",table_data)
    elif table == "TemporaryTask" or table == "RecurringTask":
        return

def add_TemporaryTask_questions():
    data = {}

    # Request task name from the user
    task_name = input("Please enter the temporary task name: ").strip()

    if not task_name:
        print("Task name cannot be empty. Please try again.")
        return None

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