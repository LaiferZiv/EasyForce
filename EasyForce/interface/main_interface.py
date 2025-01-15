import sys

from EasyForce.common.constants import TEAM_TABLE, SOLDIER_TABLE, ADD, UPDATE, DELETE
from EasyForce.common.utils import questions, extract_match_from_text
from EasyForce.data_mangement.read_db import display_all_tables
from EasyForce.data_processing.schedule_logic import schedule_shifts
from EasyForce.interface.user_questions_management.general_questions import define_task_type, ask_closed_ended_question


def menu():
    """Main menu for the program."""
    while True:
        entities = [TEAM_TABLE,SOLDIER_TABLE,"Task"]
        actions = [ADD,UPDATE,DELETE]
        question = "Main Menu"
        entity_actions = [f"{' / '.join(actions)} a {entity.lower()}" for entity in entities]
        other_options = [
            "Schedule and display shifts",
            "Display any table",
            "Display all tables",
            "Exit"
        ]
        options = entity_actions + other_options
        choice = ask_closed_ended_question(question,options)

        while True:
            if choice in entity_actions:
                entity = extract_match_from_text(choice,entities)
                entity_actions = [f"{action} a {entity.lower()}" for action in actions]
                choice = ask_closed_ended_question("",entity_actions,previous_question=True)
                if choice == "Return":
                    break
                action = extract_match_from_text(choice,actions)
                if entity == "Task":
                    if not questions(define_task_type(),action.lower()):
                        continue
                else:
                    if not questions(entity,action.lower()):
                        continue
            elif choice == "Schedule and display shifts":
                schedule_shifts()
                break
            elif choice == "Display any table":
                if not questions("Display","table"):
                    break
            elif choice == "Display all tables":
                display_all_tables()
                break
            else: # choice == "Exit":
                print("Goodbye!")
                sys.exit(0)