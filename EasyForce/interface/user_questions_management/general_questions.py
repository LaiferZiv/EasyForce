# Task - Define task type (either TemporaryTask or RecurringTask)
from EasyForce.common.constants import RECURRING_TASK_TABLE, TEMPORARY_TASK_TABLE
from EasyForce.common.utils import initialize_table_names, extract_match_from_text
from EasyForce.data_mangement.read_db import display_table

def define_task_type():
    question = "Which task would you like to add?"
    task_types = ["recurring", "temporarily"]
    options = [f"A {task_type} task" for task_type in task_types]
    answer = ask_closed_ended_question(question,options)
    if "recurring" == extract_match_from_text(answer,task_types):
        return RECURRING_TASK_TABLE
    return TEMPORARY_TASK_TABLE

def display_table_questions():
    question = "Please select the number of the table you would like to display:"
    options = [table_name for table_name in initialize_table_names().values()]
    options.append("Return")
    table_name = ask_closed_ended_question(question,options)
    if table_name == "Return":
        return False
    display_table(table_name)
    return True

def ask_open_ended_question(question,empty_name = "",previous_question = False):
    while True:
        answer = input(question).strip()
        if not answer:
            print(f"{empty_name} cannot be empty. Please try again.")
        elif answer in {'r','R'}:
            if previous_question:
                return None
            else:
                print("There is no option to choose the letter 'R'.")
        else:
            return answer

def ask_for_name(name):
    question = f"Please enter the {name} name ('R' to return): "
    return ask_open_ended_question(question,name,previous_question=True)

def ask_closed_ended_question(question, original_options, previous_question = False):
    """
    Displays a question with its options, gets user input, and returns the selected option number.

    Args:
        question (str): The question to display.
        original_options (list): A list of possible answers.
        previous_question(bool): A bool indicates to add Return option

    Returns:
        str: answer.
    """
    options = original_options[::]
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
