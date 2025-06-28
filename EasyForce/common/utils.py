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
    if table in {"TemporaryTask", "RecurringTask"}:
        args = (table,)

    table_actions = actions_mapping.get(table, {})
    func = table_actions.get(action)

    if func:
        # Call the function with the additional arguments and return its result
        return func(*args)

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

def get_datetime_input(prompt, default_delta=None) -> list:
    """
    Prompts the user for a date/time in dd/mm/yyyy hh:mm format, but also allows:
      1) Press Enter => use 'now' or 'now + default_delta' (truncated to minute, in ISO).
      2) If user typed dd/mm/yyyy only (no space => e.g. '27/02/2025'),
         we append a default hour (from constants), e.g. '08:00'.
      3) If user typed full 'dd/mm/yyyy hh:mm', parse it directly.
    Returns [bool, iso_string]:
      - bool indicates if the user typed something (True) or pressed Enter (False).
      - iso_string is the ISO 8601 string.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            # The user pressed Enter => return 'now' or 'now+delta', truncated to minute, in ISO
            now = datetime.now().replace()
            if default_delta:
                now = (now + default_delta).replace()
            return [False, now.isoformat().replace('T',' ')]
        else:
            # Check if user input has a space => dd/mm/yyyy hh:mm
            if ' ' in user_input:
                # Parse exactly dd/mm/yyyy hh:mm
                try:
                    dt_value = datetime.strptime(user_input, "%d/%m/%Y %H:%M")
                    return [True, dt_value.isoformat().replace('T',' ')]
                except ValueError:
                    print("Invalid input. Please use dd/mm/yyyy hh:mm or just dd/mm/yyyy.")
            else:
                # We assume user typed only dd/mm/yyyy => append default hour
                # e.g. '27/02/2025' + ' 08:00'
                candidate = user_input + " " + DEFAULT_MORNING_HOUR
                try:
                    dt_value = datetime.strptime(candidate, "%d/%m/%Y %H:%M")
                    return [True, dt_value.isoformat().replace('T',' ')]
                except ValueError:
                    print("Invalid input. Please use dd/mm/yyyy hh:mm or just dd/mm/yyyy.")

def get_hours_input(prompt: str):
    """
    Prompts for a time in HH:MM format.
    If the user presses Enter, returns [False, None].
    Otherwise, parses HH:MM. On success, returns [True, "HH:MM"].
    On failure, prints an error and repeats.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            # User pressed Enter => no input
            return [False, None]
        try:
            parsed_time = datetime.strptime(user_input, "%H:%M")
            # Convert back to HH:MM to store as string
            hhmm_str = parsed_time.strftime("%H:%M")
            return [True, hhmm_str]
        except ValueError:
            print("Invalid input. Please use the format HH:MM (00:00 - 23:59).")

def iso_to_ddmmyyyy(time_iso: str) -> str:
    """
    Converts an ISO 8601 datetime string (e.g. '2025-02-27T14:15:00')
    into a 'dd/mm/yyyy hh:mm' format string (e.g. '27/02/2025 14:15').
    """
    dt = datetime.fromisoformat(time_iso)      # Parse the ISO string
    return dt.strftime('%d/%m/%Y %H:%M')       # Format to dd/mm/yyyy hh:mm