"""
add_entities.py

Functions for adding new entity records (TimeRange, Team, Soldier, Role, Tasks, etc.)
All DB calls happen inside the entity class methods (no conn param).
"""

from EasyForce.data_mangement.data_structure.entities_classes import (
    Team, Soldier, TemporaryTask, RecurringTask
)
from EasyForce.common.constants import *
from EasyForce.common.utils import questions, is_positive_integer, is_number, yes_no_question, get_datetime_input
from EasyForce.interface.user_questions_management.general_questions import (
    ask_open_ended_question, ask_for_name, ask_closed_ended_question
)


def add_TimeRange_questions(table, table_data):
    """
    If table == SOLDIER_TABLE, create presence in/out (Presence subcalls).
    Otherwise, presence for tasks. No direct DB calls here.
    """
    if table == SOLDIER_TABLE:
        questions(PRESENCE_TABLE, ADD, table, table_data, "in")
        questions(PRESENCE_TABLE, ADD, table, table_data, "out")
    else:
        questions(PRESENCE_TABLE, ADD, table, table_data)


def add_Team_questions(soldier_name=None):
    question = "Please enter the team name ('R' to return): "
    if soldier_name:
        question = f"Please enter {soldier_name}'s team name: "

    team_name = ask_open_ended_question(question, "Team name", previous_question=(not bool(soldier_name)))
    if not team_name:
        return None

    # Create and .add() -> DB is accessed inside .add()
    new_team = Team(TeamName=team_name)
    new_team.add()
    if not new_team.TeamID:
        return None

    team_id = new_team.TeamID
    if not soldier_name:
        prompt = f"add soldiers to {new_team.TeamName} team"
        while True:
            if yes_no_question(prompt):
                if not questions(SOLDIER_TABLE, ADD, new_team.TeamName):
                    return team_id
                prompt = f"add more soldiers to {new_team.TeamName} team"
            else:
                break
    return team_id


def add_Soldier_questions(team_name=None):
    prompt = "Please enter the soldier name ('R' to return): "
    if team_name:
        prompt = "Please enter a soldier name ('R' to return): "

    soldier_name = ask_open_ended_question(prompt, "Soldier name", previous_question=True)
    if not soldier_name:
        return None

    prompt_id = f"Please enter {soldier_name}'s ID: "
    while True:
        soldier_id = ask_open_ended_question(prompt_id, "Soldier ID")
        if not is_positive_integer(soldier_id):
            print("Soldier ID must be positive integer.")
        else:
            soldier_id = int(soldier_id)
            break

    data = {
        "FullName": soldier_name,
        "SoldierID": soldier_id
    }

    # Add roles for soldier
    questions(ROLE_TABLE, ADD, SOLDIER_TABLE, data)

    # Assign or create team
    if team_name:
        # We rely on the classes to do DB calls
        # We'll just create or get a Team in memory if needed
        possible_team = Team.get_all()
        found = next((t for t in possible_team if t.TeamName == team_name), None)
        if found:
            data["TeamID"] = found.TeamID
        else:
            new_team = Team(TeamName=team_name)
            new_team.add()
            data["TeamID"] = new_team.TeamID
    else:
        existing_teams = Team.get_all()
        if existing_teams:
            team_names = [t.TeamName for t in existing_teams]
            team_names.append("Add a new team")
            chosen = ask_closed_ended_question(f"Select {soldier_name}'s team:", team_names)
            if chosen == "Add a new team":
                data["TeamID"] = questions(TEAM_TABLE, ADD, soldier_name)
            else:
                found = next((t for t in existing_teams if t.TeamName == chosen), None)
                data["TeamID"] = found.TeamID if found else None
        else:
            print("No existing teams. Please add a team first.")
            data["TeamID"] = questions(TEAM_TABLE, ADD, soldier_name)

    # Create soldier
    new_soldier = Soldier(**data)
    new_soldier.add()
    if not new_soldier.SoldierID:
        return None

    # Add TimeRange
    questions(TIME_RANGE_TABLE, ADD, SOLDIER_TABLE, data)
    return soldier_id


def add_Role_questions(table, table_data):
    if table == SOLDIER_TABLE:
        if yes_no_question(f"add {table_data['FullName']} a role"):
            questions(SOLDIER_ROLE_TABLE, ADD, table_data)
    elif table in (TEMPORARY_TASK_TABLE, RECURRING_TASK_TABLE):
        if yes_no_question("add role/soldier restrictions?"):
            if yes_no_question("add specific roles that MUST be included?"):
                questions(TASK_ROLE_TABLE, ADD, table, table_data, ROLE_TABLE, ADD)
            if yes_no_question("add specific roles that CANNOT be included?"):
                questions(TASK_ROLE_TABLE, ADD, table, table_data, ROLE_TABLE, DELETE)
            if yes_no_question("add specific soldiers that MUST be included?"):
                questions(TASK_ROLE_TABLE, ADD, table, table_data, SOLDIER_TABLE, ADD)
            if yes_no_question("add specific soldiers that CANNOT be included?"):
                questions(TASK_ROLE_TABLE, ADD, table, table_data, SOLDIER_TABLE, DELETE)


def add_Task_questions(table):
    data = {}
    t_str = "temporary" if table == TEMPORARY_TASK_TABLE else "recurring"
    t_name = ask_for_name(f"{t_str} task")
    if not t_name:
        return None

    if table == TEMPORARY_TASK_TABLE:
        rep_q = "Please enter the task reputation:"
        rep_opts = ["Good", "Bad", "None"]
        task_rep = ask_closed_ended_question(rep_q, rep_opts)
        new_temp = TemporaryTask(TaskName=t_name, TaskReputation=task_rep)
        new_temp.add()
        if not new_temp.TaskID:
            return None
        data["TaskID"] = new_temp.TaskID
        data["TaskName"] = new_temp.TaskName
        data["TaskReputation"] = new_temp.TaskReputation
    else:
        # Recurring
        while True:
            shift = ask_open_ended_question("Enter shift duration (hours): ", "A shift")
            if not is_number(shift) or float(shift) <= 0:
                print("Must be positive.")
            else:
                shift = float(shift)
                break
        while True:
            amt = ask_open_ended_question("Enter required personnel: ", "A required")
            if not is_number(amt) or float(amt) <= 0:
                print("Must be positive.")
            else:
                amt = int(float(amt))
                break

        start_prompt = "Time the task starts each day (HH:MM) or Enter for all day: "
        start_dt = get_datetime_input(start_prompt)
        if not start_dt[0]:
            e_start = MIDNIGHT
            e_end = MIDNIGHT
        else:
            e_start = str(start_dt[1])
            end_prompt = "Time the task ends each day (can be after midnight, HH:MM): "
            while True:
                end_dt = get_datetime_input(end_prompt)
                if not end_dt[0]:
                    print("Must specify end time.")
                else:
                    e_end = str(end_dt[1])
                    break

        new_rec = RecurringTask(
            TaskName=t_name,
            ShiftDurationInMinutes=int(shift * MIN_IN_HOUR),
            EveryDayStartTime=e_start,
            EveryDayEndTime=e_end,
            RequiredPersonnel=amt
        )
        new_rec.add()
        if not new_rec.TaskID:
            return None
        data["TaskID"] = new_rec.TaskID
        data["TaskName"] = new_rec.TaskName

    # Add TimeRange
    questions(TIME_RANGE_TABLE, ADD, table, data)
    # Add Roles
    questions(ROLE_TABLE, ADD, table, data)
    return data.get("TaskID")