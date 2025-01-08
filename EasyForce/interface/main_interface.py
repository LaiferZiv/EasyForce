from utils import *

def menu():
    """Main menu for the program."""
    while True:
        print("\nMain Menu")
        print("1. Add/Update/Delete a team")
        print("2. Add/Update/Delete a soldier")
        print("3. Add/Update/Delete a task")
        print("4. Schedule and display shifts")
        print("5. Display any table")
        print("6. Display all tables")
        print("7. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            while True:
                print("1. Add a team")
                print("2. Update a team")
                print("3. Delete a team")
                choice = input("Enter your choice (1-3) or 'R' to return: ").strip()
                if choice == '1':
                    questions("Team","add")
                elif choice == '2':
                    questions("Team","update")
                elif choice == '3':
                    questions("Team","delete")
                elif choice in {'R','r'}:
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '2':
            while True:
                print("1. Add a soldier")
                print("2. Update a soldier")
                print("3. Delete a soldier")
                choice = input("Enter your choice (1-3) or 'R' to return: ").strip()
                if choice == '1':
                    if not questions("Soldier","add",None):
                        break
                elif choice == '2':
                    questions("Soldier","update")
                elif choice == '3':
                    questions("Soldier","delete")
                elif choice in {'R','r'}:
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '3':
            while True:
                print("1. Add a task")
                print("2. Update a task")
                print("3. Delete a task")
                choice = input("Enter your choice (1-3) or 'R' to return: ").strip()
                if choice in {'R','r'}:
                    break
                task_table = questions("TaskType","define")
                if choice == '1':
                    questions(task_table,"add")
                elif choice == '2':
                    questions(task_table,"update")
                elif choice == '3':
                    questions(task_table,"delete")
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '4':
            break
            # while True:
            #     should_break = False
            #     print("When would you like the schedule to start?")
            #     while True:
            #         schedule_start_time = input("Enter 'N' for now, 'R' to return, or enter the time in format: 'YEAR-MONTH-DAY HOUR:MINUTE': ").strip()
            #         if not (schedule_start_time == 'N' or schedule_start_time == 'R' or is_valid_ISO_schedule_time(schedule_start_time) ):
            #             print("Invalid choice. Please try again.")
            #             continue
            #         if schedule_start_time == 'N':
            #             schedule_start_time = datetime.now().isoformat()
            #             break
            #         elif schedule_start_time == 'R':
            #             should_break = True
            #             break
            #     if should_break:
            #         break
            #     print("For how many hours should the shifts be arranged?")
            #     while True:
            #         hours = input("Enter 'D' for a day, 'R' to return, or the number of hours: ")
            #         if not (hours == 'D' or hours == 'R' or isinstance(hours,int) or isinstance(hours,float)):
            #             print("Invalid choice. Please try again.")
            #             continue
            #         if hours == 'R':
            #             break
            #         elif hours == 'D':
            #             hours = DAY
            #             should_break = True
            #             break
            #         else:
            #             should_break = True
            #     if should_break:
            #         schedule_shifts(schedule_start_time,hours)
            #         display_table("CurrentTaskAssignment")
            #         break
        elif choice == '5':
            table_names = initialize_table_names()
            for key in sorted(table_names.keys()):
                print(f"{key}. {table_names[key]}")
            while True:
                choice = input("Enter the table number to display (or 'R' to return)").strip()
                if choice == 'R':
                    break
                elif choice not in table_names.keys():
                    print("Invalid choice. Please try again.")
                    continue
                display_table(table_names[choice])
                break
        elif choice == '6':
            #diplay func
            display_all_tables()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")