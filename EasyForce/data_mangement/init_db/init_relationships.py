import sqlite3
from EasyForce.common.config import DB_PATH

def init_relationships():
    """Initialize the relationships."""
    conn = None
    return_val = True
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON;")

        ##### Create all Relationships tables #####

        # 1) Presence
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Presence (
            SoldierTeamTaskType TEXT NOT NULL CHECK(SoldierTeamTaskType IN ('Soldier', 'Team','RecurringTask','TemporaryTask')),
            SoldierTeamTaskID INTEGER NOT NULL,
            TimeID INTEGER NOT NULL,
            isActive INTEGER NOT NULL DEFAULT 1, -- 1 is presence, 0 is not presence
            PRIMARY KEY (SoldierTeamTaskType, SoldierTeamTaskID, TimeID),
            FOREIGN KEY (TimeID) REFERENCES TimeRange(TimeID) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        # 2) SoldierRole
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SoldierRole(
            SoldierID INTEGER NOT NULL,
            RoleID INTEGER NOT NULL,
            PRIMARY KEY (SoldierID, RoleID),
            FOREIGN KEY (SoldierID) REFERENCES Soldier(SoldierID) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (RoleID) REFERENCES Role(RoleID) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        # 4) TaskRole
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TaskRole(
            TaskType TEXT NOT NULL CHECK(TaskType IN ('TemporaryTask', 'RecurringTask')),
            TaskID INTEGER NOT NULL,
            SoldierOrRole TEXT NOT NULL CHECK(SoldierOrRole IN ('Soldier', 'Role')),
            SoldierOrRoleID INTEGER NOT NULL,
            MinRequiredCount INTEGER NOT NULL,
            RoleEnforcementType INTEGER NOT NULL DEFAULT 1, -- 1 is must be, 0 is can not be
            PRIMARY KEY (TaskType, TaskID,SoldierOrRole, SoldierOrRoleID)        
        );
        """)

        # 5) CurrentTaskAssignment
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CurrentTaskAssignment(
            TaskType TEXT NOT NULL CHECK(TaskType IN ('TemporaryTask', 'RecurringTask')),
            TaskID INTEGER NOT NULL,
            SoldierOrTeamType TEXT NOT NULL CHECK(SoldierOrTeamType IN ('Soldier', 'Team')),
            SoldierOrTeamID INTEGER NOT NULL,
            TimeID INTEGER NOT NULL,
            PRIMARY KEY (TaskType, TaskID, SoldierOrTeamType, SoldierOrTeamID, TimeID),
            FOREIGN KEY (TimeID) REFERENCES TimeRange(TimeID) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        # 6) TaskHistory
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TaskHistory(
            HistoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskType TEXT NOT NULL CHECK(TaskType IN ('TemporaryTask', 'RecurringTask')),
            TaskID INTEGER NOT NULL,
            SoldierOrTeamType TEXT NOT NULL CHECK(SoldierOrTeamType IN ('Soldier', 'Team')),
            SoldierOrTeamID INTEGER NOT NULL,
            TaskReputation TEXT NOT NULL CHECK(TaskReputation IN ('Good', 'Bad', 'None')),
            TimeID INTEGER NOT NULL,
            CompletionStatus TEXT NOT NULL CHECK(CompletionStatus IN ('Canceled', 'Completed', 'Ongoing')),

            UNIQUE (TaskType, TaskID, SoldierOrTeamType, SoldierOrTeamID, TimeID),
            FOREIGN KEY (TimeID) REFERENCES TimeRange(TimeID) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (TaskReputation) REFERENCES TemporaryTask(TaskReputation) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        # Commit relationships
        conn.commit()
        print("All relationships have been initialized successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred during the initialization of relationships tables: {e}")
        return_val = False
    finally:
        if conn:
            conn.close()
            return return_val