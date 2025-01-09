# Task - Define task type (either TemporaryTask or RecurringTask)
from EasyForce.common.utils import initialize_table_names, display_question_and_get_answer, extract_match_from_text
from EasyForce.data_mangement.read_db import display_table

def define_task_type():
    question = "Which task would you like to add?"
    task_types = ["recurring", "temporarily"]
    options = [f"A {task_type} task" for task_type in task_types]
    answer = display_question_and_get_answer(question,options)
    if "recurring" == extract_match_from_text(answer,task_types):
        return "RecurringTask"
    return "TemporaryTask"

def display_table_questions():
    question = "Please select the number of the table you would like to display:"
    options = [table_name for table_name in initialize_table_names().values()]
    options.append("Return")
    table_name = display_question_and_get_answer(question,options)
    if table_name == "Return":
        return False
    display_table(table_name)
    return True