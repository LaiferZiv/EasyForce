# Task - Define task type (either TemporaryTask or RecurringTask)
from EasyForce.common.utils import initialize_table_names, ask_closed_ended_question, extract_match_from_text
from EasyForce.data_mangement.read_db import display_table

def define_task_type():
    question = "Which task would you like to add?"
    task_types = ["recurring", "temporarily"]
    options = [f"A {task_type} task" for task_type in task_types]
    answer = ask_closed_ended_question(question,options)
    if "recurring" == extract_match_from_text(answer,task_types):
        return "RecurringTask"
    return "TemporaryTask"

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
        elif previous_question and  answer in {'r','R'}:
            return None
        else:
            return answer

def ask_for_name(name):
    question = f"Please enter the {name} name ('R' to return): "
    return ask_open_ended_question(name,question,previous_question=True)
