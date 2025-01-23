"""
add_relationships.py

Functions for adding relationship records (Presence, SoldierRole, etc.)
All DB calls only happen in the class methods (no conn param).
"""
from datetime import timedelta

from EasyForce.data_mangement.data_structure.relationships_classes import (
    Presence, SoldierRole, TaskRole
)
from EasyForce.data_mangement.data_structure.entities_classes import TimeRange, Soldier, Role, Team
from EasyForce.common.constants import *
from EasyForce.common.utils import (
    is_positive_integer, yes_no_question, get_datetime_input
)
from EasyForce.interface.user_questions_management.general_questions import (
    ask_closed_ended_question, ask_open_ended_question
)


def add_Presence_questions(table, table_data, pos=""):
    if table == SOLDIER_TABLE:
        question = f"Add times when {table_data['FullName']} is {pos} the base"
        is_presence = 1 if pos == "in" else 0
        start_prompt = f"Enter {table_data['FullName']}'s {'arrival' if is_presence else 'departure'} time (DD/MM/YYYY HH:MM) or Enter for now: "
        end_prompt = f"Enter {table_data['FullName']}'s {'departure' if is_presence else 'return'} time (DD/MM/YYYY HH:MM) or Enter for unknowing: "
        more_prompt = f"Add more times when {table_data['FullName']} is {pos} the base"
    else:
        question = f"Add active time range for {table_data['TaskName']}"
        is_presence = 1
        start_prompt = "Enter the task's start time (DD/MM/YYYY HH:MM) or Enter for now: "
        end_prompt = "Enter the task's end time (DD/MM/YYYY HH:MM) or Enter for unknowing: "
        more_prompt = "Add more times for the task's presence?"

    if yes_no_question(question):
        while True:
            start_dt = get_datetime_input(start_prompt)
            end_dt = get_datetime_input(end_prompt,default_delta=timedelta(YEAR))
            if not start_dt[1] < end_dt[1]:
                print(f"The {'arrival' if is_presence else 'departure'} time must be earlier than the {'departure' if is_presence else 'return'} time.")
                continue
            # Create TimeRange
            new_range = TimeRange(
                StartDateTime=str(start_dt[1]),
                EndDateTime=str(end_dt[1])
            )
            new_range.add()

            # Create Presence
            pid = table_data["SoldierID"] if table == SOLDIER_TABLE else table_data["TaskID"]
            presence_obj = Presence(
                SoldierTeamTaskType=table,
                SoldierTeamTaskID=pid,
                TimeID=new_range.TimeID,
                isActive=is_presence
            )
            presence_obj.add()

            if (not start_dt[0] and not end_dt[0]) or not yes_no_question(more_prompt):
                break


def add_SoldierRole_questions(table_data):
    soldier_id = table_data["SoldierID"]
    soldier_name = table_data["FullName"]
    while True:
        role_name = ask_open_ended_question(f"{soldier_name}'s role: ", "Role name")
        if not role_name:
            break

        existing_roles = Role.get_all()
        found_role = next((r for r in existing_roles if r.RoleName == role_name), None)
        if not found_role:
            new_role = Role(RoleName=role_name)
            new_role.add()
            role_id = new_role.RoleID
        else:
            role_id = found_role.RoleID

        sr = SoldierRole(SoldierID=soldier_id, RoleID=role_id)
        sr.add()

        if not yes_no_question(f"add {soldier_name} another role"):
            break


def add_TaskRole_questions(table_type, table_data, entity_type):
    def add_role(enforcement_type):
        while True:
            if not role_names:
                print("No roles to choose from.")
                break
            chosen = ask_closed_ended_question("Select a role:", role_names)
            role_names.remove(chosen)
            found = next((r for r in existing_roles if r.RoleName == chosen), None)
            if not found:
                continue
            min_required_count = 0
            if enforcement_type == ADD:
                while True:
                    val = ask_open_ended_question("How many of this role are essential: ", "An amount")
                    if is_positive_integer(val):
                        min_required_count = int(val)
                        break

            tr = TaskRole(
                TaskType=table_type,
                TaskID=table_data["TaskID"],
                SoldierOrRole=ROLE_TABLE,
                SoldierOrRoleID=found.RoleID,
                MinRequiredCount=min_required_count,
                RoleEnforcementType=1 if enforcement_type == ADD else 0
            )
            tr.add()

            if not yes_no_question("Add another role?"):
                break

    def add_soldier(enforcement_type):
        while True:
            if not display_list:
                print("No soldiers available.")
                break
            chosen = ask_closed_ended_question("Choose a soldier:", display_list)
            display_list.remove(chosen)
            soldier_id = int(chosen.split("ID: ")[1])

            tr = TaskRole(
                TaskType=table_type,
                TaskID=table_data["TaskID"],
                SoldierOrRole=SOLDIER_TABLE,
                SoldierOrRoleID=soldier_id,
                MinRequiredCount=1,
                RoleEnforcementType=1 if enforcement_type == ADD else 0
            )
            tr.add()

            if not yes_no_question("Add another soldier?"):
                break

    def add_team(enforcement_type):
        while True:
            if not display_list:
                print("No teams available.")
                break
            chosen = ask_closed_ended_question("Choose a team:", display_list)
            display_list.remove(chosen)
            team_id = Team.get_by_unique_name(chosen).TeamID
            soldiers_in_team = Soldier.get_all_by_column_value("TeamID",team_id)

            if soldiers_in_team:
                for soldier in soldiers_in_team:
                    tr = TaskRole(
                        TaskType=table_type,
                        TaskID=table_data["TaskID"],
                        SoldierOrRole=SOLDIER_TABLE,
                        SoldierOrRoleID=soldier.SoldierID,
                        MinRequiredCount=1,
                        RoleEnforcementType=1 if enforcement_type == ADD else 0
                    )
                    existed_tr = tr.get_by_id({"TaskType":table_type, "TaskID":table_data["TaskID"],"SoldierOrRole":SOLDIER_TABLE,"SoldierOrRoleID":soldier.SoldierID})
                    if existed_tr:
                        existed_tr.RoleEnforcementType=1 if enforcement_type == ADD else 0
                        existed_tr.update()
                    else:
                        tr.add()

            if not yes_no_question("Add another team?"):
                break

    if entity_type == SOLDIER_TABLE:
        all_sol = Soldier.get_all()
        display_list = [f"{s.FullName}, ID: {s.SoldierID}" for s in all_sol]
        if yes_no_question("add specific soldiers that MUST be included?"):
            add_soldier(ADD)
        if yes_no_question("add specific soldiers that CANNOT be included?"):
            add_soldier(DELETE)
    elif entity_type == ROLE_TABLE:
        existing_roles = Role.get_all()
        role_names = [r.RoleName for r in existing_roles]
        if yes_no_question("add specific roles that MUST be included?"):
            add_role(ADD)
        if yes_no_question("add specific roles that CANNOT be included?"):
            add_role(DELETE)
    else: #Team
        all_team = Team.get_all()
        display_list = [f"{t.TeamName}" for t in all_team]
        if yes_no_question("add specific teams that MUST be included?"):
            add_team(ADD)
        if yes_no_question("add specific teams that CANNOT be included?"):
            add_team(DELETE)



def add_CurrentTaskAssignment_questions(*args):
    print("add_CurrentTaskAssignment_questions not yet implemented.")
    return args

def add_TaskHistory_questions(*args):
    print("add_TaskHistory_questions not yet implemented.")
    return args