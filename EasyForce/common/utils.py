from datetime import datetime,timedelta

from EasyForce.common.constants import *


def is_valid_ISO_schedule_time(schedule_start_time: str) -> bool:
    try:
        datetime.fromisoformat(schedule_start_time)
        return True
    except ValueError:
        return False

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_positive_integer(value):
    try:
        value = int(value)
        return value > 0
    except ValueError:
        return False

def initialize_table_names():
    table_names = {
        1: TIME_RANGE_TABLE,
        2: TEAM_TABLE,
        3: SOLDIER_TABLE,
        4: ROLE_TABLE,
        5: TEMPORARY_TASK_TABLE,
        6: RECURRING_TASK_TABLE,
        7: PRESENCE_TABLE,
        8: SOLDIER_ROLE_TABLE,
        9: TASK_ROLE_TABLE,
        10: CURRENT_TASK_ASSIGNMENT_TABLE,
        11: TASK_HISTORY_TABLE
    }
    return table_names

def questions(table, action, *args):
    """
    Call the appropriate function based on the table and action, and pass additional parameters.

    Args:
        table (str): The name of the table (e.g. "Soldier", "Team", "Role", etc.).
        action (str): The action to perform (e.g., "add", "update", "delete").
        *args: Additional positional arguments to pass to the specific action function.

    Returns:
        The return value of the called function, or None if the table/action combination is invalid.
    """
    from EasyForce.interface.user_questions_management.add_questions.add_entities import (
        add_Soldier_questions, add_Team_questions, add_Task_questions, add_Role_questions,add_TimeRange_questions
    )
    from EasyForce.interface.user_questions_management.add_questions.add_relationships import (
        add_SoldierRole_questions, add_Presence_questions,
        add_TaskRole_questions, add_CurrentTaskAssignment_questions, add_TaskHistory_questions
    )
    from EasyForce.interface.user_questions_management.update_questions.update_entities import (
        update_Soldier_questions, update_Team_questions,
        update_Task_questions, update_Role_questions, update_TimeRange_questions
    )
    from EasyForce.interface.user_questions_management.update_questions.update_relationships import (
        update_SoldierRole_questions,
        update_Presence_questions, update_TaskRole_questions,
        update_CurrentTaskAssignment_questions, update_TaskHistory_questions,
    )
    from EasyForce.interface.user_questions_management.delete_questions.delete_entities import (
        delete_Soldier_questions, delete_Team_questions, delete_Task_questions, delete_Role_questions,
        delete_TimeRange_questions
    )

    from EasyForce.interface.user_questions_management.delete_questions.delete_relationships import (
        delete_SoldierRole_questions,
        delete_Presence_questions, delete_TaskRole_questions,
        delete_CurrentTaskAssignment_questions, delete_TaskHistory_questions,
    )
    from EasyForce.interface.user_questions_management.general_questions import define_task_type,display_table_questions

    # Mapping of actions to functions for each table
    actions_mapping = {
        SOLDIER_TABLE: {
            ADD: add_Soldier_questions,
            UPDATE: update_Soldier_questions,
            DELETE: delete_Soldier_questions,
        },
        TEAM_TABLE: {
            ADD: add_Team_questions,
            UPDATE: update_Team_questions,
            DELETE: delete_Team_questions,
        },
        TEMPORARY_TASK_TABLE: {
            ADD: add_Task_questions,
            UPDATE: update_Task_questions,
            DELETE: delete_Task_questions,
        },
        RECURRING_TASK_TABLE: {
            ADD: add_Task_questions,
            UPDATE: update_Task_questions,
            DELETE: delete_Task_questions,
        },
        ROLE_TABLE: {
            ADD: add_Role_questions,
            UPDATE: update_Role_questions,
            DELETE: delete_Role_questions,
        },
        SOLDIER_ROLE_TABLE: {
            ADD: add_SoldierRole_questions,
            UPDATE: update_SoldierRole_questions,
            DELETE: delete_SoldierRole_questions,
        },
        PRESENCE_TABLE: {
            ADD: add_Presence_questions,
            UPDATE: update_Presence_questions,
            DELETE: delete_Presence_questions,
        },
        TASK_ROLE_TABLE: {
            ADD: add_TaskRole_questions,
            UPDATE: update_TaskRole_questions,
            DELETE: delete_TaskRole_questions,
        },
        CURRENT_TASK_ASSIGNMENT_TABLE: {
            ADD: add_CurrentTaskAssignment_questions,
            UPDATE: update_CurrentTaskAssignment_questions,
            DELETE: delete_CurrentTaskAssignment_questions,
        },
        TASK_HISTORY_TABLE: {
            ADD: add_TaskHistory_questions,
            UPDATE: update_TaskHistory_questions,
            DELETE: delete_TaskHistory_questions,
        },
        TIME_RANGE_TABLE: {
            ADD: add_TimeRange_questions,
            UPDATE: update_TimeRange_questions,
            DELETE: delete_TimeRange_questions,
        },
        "TaskType":{
            "define":define_task_type
        },
        "Display":{
            "table": display_table_questions
        }
    }

    table_names = initialize_table_names()
    if table in {"TemporaryTask","RecurringTask"}:
        args = (table,)
    # Check if the provided table name exists in the table_names dictionary,
    # and if the requested action exists in our actions_mapping.
    if table in {*table_names.values(), "TaskType","Display"} and action in {*actions_mapping.get(table, {}), "define","table"}:
        func = actions_mapping[table][action]
        # Call the function with the additional arguments and return its result
        return func(*args)
    else:
        print(f"Invalid table or action: table={table}, action={action}")
        return None

def yes_no_question(question):
    from EasyForce.interface.user_questions_management.general_questions import ask_closed_ended_question

    question = f"Would you like to {question}?"
    options = ["Yes","No"]
    if "Yes" == ask_closed_ended_question(question, options):
        return True
    return False

def extract_match_from_text(selected_text, candidates):
    """
    Extracts a matching value from a list of candidates based on the selected text.

    Args:
        selected_text (str): The full text from which to extract a match.
        candidates (list): A list of possible values to match against.

    Returns:
        str: The first matching candidate found in the selected text.

    Raises:
        ValueError: If no matching candidate is found in the selected text.
    """
    for candidate in candidates:
        if candidate.lower() in selected_text.lower():
            return candidate
    raise ValueError("No matching candidate found in the selected text.")

def get_datetime_input(prompt, default_delta=None, time_format="%Y-%m-%d %H:%M"):
    """
    Prompts the user for a datetime input and handles cases where the user presses Enter.
    - If the user presses Enter:
      - Returns the current time if `default_delta` is None.
      - Returns the current time + `default_delta` if `default_delta` is provided.

    Args:
        prompt (str): The prompt message to show to the user.
        default_delta (timedelta or None): The default time difference to add if the user presses Enter.
        time_format (str): The expected format of the datetime input.

    Returns:
        list: [Boolean indicating if the user provided input, datetime object of the result].
    """
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            # Handle Enter case
            now = datetime.now().replace(second=0, microsecond=0)
            if default_delta is None:
                # Return the current time if no default_delta is provided
                return [False, now]
            else:
                # Return current time + default_delta
                future_time = (now + default_delta).replace(second=0, microsecond=0)
                return [False, future_time]
        else:
            try:
                # Parse user input based on the given time_format
                dt_value = datetime.strptime(user_input, time_format)
                return [True, dt_value]
            except ValueError:
                if time_format == "%Y-%m-%d %H:%M":
                    print("Invalid input. Please use the format: YYYY-MM-DD HH:MM.")
                elif time_format == "%H:%M":
                    print("Invalid input. Please use the format: HH:MM.")
                else:
                    print("Invalid input.")

def iso_to_ddmmyyyy(time_iso: str) -> str:
    """
    Converts an ISO 8601 datetime string (e.g. '2025-02-27T14:15:00')
    into a 'dd/mm/yyyy hh:mm' format string (e.g. '27/02/2025 14:15').
    """
    dt = datetime.fromisoformat(time_iso)      # Parse the ISO string
    return dt.strftime('%d/%m/%Y %H:%M')       # Format to dd/mm/yyyy hh:mm

def ddmmyyyy_to_iso(time_dmy: str) -> str:
    """
    Converts a 'dd/mm/yyyy hh:mm' format string (e.g. '27/02/2025 14:15')
    into an ISO 8601 datetime string (e.g. '2025-02-27T14:15:00').
    """
    dt = datetime.strptime(time_dmy, '%d/%m/%Y %H:%M')  # Parse the dd/mm/yyyy hh:mm string
    return dt.isoformat()                               # Convert to ISO 8601 string