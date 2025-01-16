import sqlite3
from EasyForce.common.config import DB_PATH

def init_entities():
    """Initialize the entities."""
    conn = None
    return_val = True
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON;")

        ##### Create all Entities tables #####

        # 1) TimeRange
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TimeRange (
            TimeID INTEGER PRIMARY KEY AUTOINCREMENT,
            StartDateTime TEXT NOT NULL,
            EndDateTime TEXT NOT NULL
        );
        """)

        # 2) Team
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Team (
            TeamID INTEGER PRIMARY KEY AUTOINCREMENT,
            TeamName TEXT NOT NULL UNIQUE
        );
        """)

        # 3) Soldier
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Soldier (
            SoldierID INTEGER PRIMARY KEY,
            FullName TEXT NOT NULL,
            TeamID INTEGER NOT NULL,
            FOREIGN KEY (TeamID) REFERENCES Team(TeamID) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        # 4) Role
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Role (
            RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
            RoleName TEXT NOT NULL UNIQUE
        );
        """)

        # 5) TemporaryTask
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TemporaryTask(
            TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskName TEXT NOT NULL UNIQUE,
            TaskReputation TEXT NOT NULL CHECK(TaskReputation IN ('Good', 'Bad', 'None'))
        );
        """)

        # 6) RecurringTask
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS RecurringTask(
            TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskName TEXT NOT NULL UNIQUE,
            ShiftDurationInMinutes INTEGER NOT NULL,
            EveryDayStartTime TEXT NOT NULL,
            EveryDayEndTime TEXT NOT NULL,
            RequiredPersonnel INTEGER NOT NULL
        );
        """)

        # Commit everything
        conn.commit()
        print("All entities have been initialized successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred during the initialization of entity tables: {e}")
        return_val = False
    finally:
        if conn:
            conn.close()
            return return_val