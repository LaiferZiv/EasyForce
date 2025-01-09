from datetime import datetime

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
        1: "TimeRange",
        2: "Team",
        3: "Soldier",
        4: "Role",
        5: "TemporaryTask",
        6: "RecurringTask",
        7: "Presence",
        8: "SoldierRole",
        9: "TaskPeriod",
        10: "TaskRole",
        11: "CurrentTaskAssignment",
        12: "TaskHistory"
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
        add_Soldier_questions, add_Team_questions, add_TemporaryTask_questions,
        add_RecurringTask_questions, add_Role_questions,add_TimeRange_questions
    )
    from EasyForce.interface.user_questions_management.add_questions.add_relationships import (
        add_SoldierRole_questions, add_Presence_questions, add_TaskPeriod_questions,
        add_TaskRole_questions, add_CurrentTaskAssignment_questions, add_TaskHistory_questions
    )
    from EasyForce.interface.user_questions_management.update_questions.update_entities import (
        update_Soldier_questions, update_Team_questions, update_TemporaryTask_questions,
        update_RecurringTask_questions, update_Role_questions, update_SoldierRole_questions,
        update_Presence_questions, update_TaskPeriod_questions, update_TaskRole_questions,
        update_CurrentTaskAssignment_questions, update_TaskHistory_questions,
        update_TimeRange_questions
    )
    from EasyForce.interface.user_questions_management.delete_questions.delete_entities import (
        delete_Soldier_questions, delete_Team_questions, delete_TemporaryTask_questions,
        delete_RecurringTask_questions, delete_Role_questions, delete_SoldierRole_questions,
        delete_Presence_questions, delete_TaskPeriod_questions, delete_TaskRole_questions,
        delete_CurrentTaskAssignment_questions, delete_TaskHistory_questions,
        delete_TimeRange_questions
    )
    from EasyForce.interface.user_questions_management.general_questions import define_task_type,display_table_questions

    # Mapping of actions to functions for each table
    actions_mapping = {
        "Soldier": {
            "add": add_Soldier_questions,
            "update": update_Soldier_questions,
            "delete": delete_Soldier_questions,
        },
        "Team": {
            "add": add_Team_questions,
            "update": update_Team_questions,
            "delete": delete_Team_questions,
        },
        "TemporaryTask": {
            "add": add_TemporaryTask_questions,
            "update": update_TemporaryTask_questions,
            "delete": delete_TemporaryTask_questions,
        },
        "RecurringTask": {
            "add": add_RecurringTask_questions,
            "update": update_RecurringTask_questions,
            "delete": delete_RecurringTask_questions,
        },
        "Role": {
            "add": add_Role_questions,
            "update": update_Role_questions,
            "delete": delete_Role_questions,
        },
        "SoldierRole": {
            "add": add_SoldierRole_questions,
            "update": update_SoldierRole_questions,
            "delete": delete_SoldierRole_questions,
        },
        "Presence": {
            "add": add_Presence_questions,
            "update": update_Presence_questions,
            "delete": delete_Presence_questions,
        },
        "TaskPeriod": {
            "add": add_TaskPeriod_questions,
            "update": update_TaskPeriod_questions,
            "delete": delete_TaskPeriod_questions,
        },
        "TaskRole": {
            "add": add_TaskRole_questions,
            "update": update_TaskRole_questions,
            "delete": delete_TaskRole_questions,
        },
        "CurrentTaskAssignment": {
            "add": add_CurrentTaskAssignment_questions,
            "update": update_CurrentTaskAssignment_questions,
            "delete": delete_CurrentTaskAssignment_questions,
        },
        "TaskHistory": {
            "add": add_TaskHistory_questions,
            "update": update_TaskHistory_questions,
            "delete": delete_TaskHistory_questions,
        },
        "TimeRange": {
            "add": add_TimeRange_questions,
            "update": update_TimeRange_questions,
            "delete": delete_TimeRange_questions,
        },
        "TaskType":{
            "define":define_task_type
        },
        "Display":{
            "table": display_table_questions
        }
    }

    table_names = initialize_table_names()

    # Check if the provided table name exists in the table_names dictionary,
    # and if the requested action exists in our actions_mapping.
    if table in {*table_names.values(), "TaskType","Display"} and action in {*actions_mapping.get(table, {}), "define","table"}:
        func = actions_mapping[table][action]
        # Call the function with the additional arguments and return its result
        return func(*args)
    else:
        print(f"Invalid table or action: table={table}, action={action}")
        return None

def display_question_and_get_answer(question, options, previous_question = None):
    """
    Displays a question with its options, gets user input, and returns the selected option number.

    Args:
        question (str): The question to display.
        options (list): A list of possible answers.

    Returns:
        str: answer.
    """
    if previous_question:
        options.append("Return")
    print(question)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ").strip())
            if 1 <= choice <= len(options):
                return options[choice-1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Please enter a valid number.")

def yes_no_question(question):
    question = f"Would you like to {question} ?"
    options = ["Yes","No"]
    if "Yes" == display_question_and_get_answer(question,options):
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

def get_datetime_input(prompt,default_delta = None):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return datetime.now() + default_delta
        try:
            return datetime.strptime(user_input, "%Y-%m-%d %H:%M")
        except ValueError:
                print("invalid input. use format yyyy-mm-dd hh:mm")