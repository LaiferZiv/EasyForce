import sys
from EasyForce.data_mangement.init_db.init_database import initialize_database
from EasyForce.config import DB_PATH
from interface.main_interface import menu

if __name__ == "__main__":
    if not initialize_database():
        print("Please ensure the database initialization is completed successfully before using the system.")
        sys.exit(1)
    menu()