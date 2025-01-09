import sys
from EasyForce.common.utils import questions,display_question_and_get_answer,extract_match_from_text
from EasyForce.data_mangement.read_db import display_all_tables
from EasyForce.data_processing.schedule_logic import schedule_shifts
from EasyForce.interface.user_questions_management.general_questions import define_task_type


def menu():
    """Main menu for the program."""
    while True:
        entities = ["Team","Soldier","Task"]
        actions = ["Add","Update","Delete"]
        question = "Main Menu"
        entity_actions = [f"{' / '.join(actions)} a {entity.lower()}" for entity in entities]
        other_options = [
            "Schedule and display shifts",
            "Display any table",
            "Display all tables",
            "Exit"
        ]
        options = entity_actions + other_options
        choice = display_question_and_get_answer(question,options)

        while True:
            if choice in entity_actions:
                entity = extract_match_from_text(choice,entities)
                entity_actions = [f"{action} a {entity.lower()}" for action in actions]
                other_options = ["Return"]
                options = entity_actions + other_options
                choice = display_question_and_get_answer("",options)
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
            elif choice == "Exit":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")