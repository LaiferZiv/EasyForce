import sys
from data_mangement.init_db.init_database import initialize_database
from interface.main_interface import menu

if __name__ == "__main__":
    db = "my_database.db"

    if not initialize_database():
        print("Please ensure the database initialization is completed successfully before using the system.")
        sys.exit(1)
    menu()

    # #check database creation:
    # # with sqlite3.connect(db) as conn:
    #     cursor = conn.cursor()
    #     query = """ SELECT name
    #                 FROM sqlite_master
    #                 WHERE type='table' AND name='Presence';
    #                 """
    #     print(cursor.execute(query))