def schedule_shifts():
    return

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