import sqlite3
from EasyForce.common.config import DB_PATH

def init_triggers():
    """Initialize the triggers."""
    conn = None
    return_val = True

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON;")

        ##### Create all Triggers tables #####

        # 1) Check_time_range_validity
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS check_time_range_validity_insert
        BEFORE INSERT ON TimeRange
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.EndDateTime <= NEW.StartDateTime THEN
                    RAISE(ABORT, 'EndDateTime must be after StartDateTime')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS check_time_range_validity_update
        BEFORE UPDATE ON TimeRange
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.EndDateTime <= NEW.StartDateTime THEN
                    RAISE(ABORT, 'EndDateTime must be after StartDateTime')
            END;
        END;
        """)

        # 2) Ensure_positive_required_personnel
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS ensure_positive_required_personnel_insert
        BEFORE INSERT ON RecurringTask
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.RequiredPersonnel < 0 THEN
                    RAISE(ABORT, 'RequiredPersonnel cannot be negative')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS ensure_positive_required_personnel_update
        BEFORE UPDATE ON RecurringTask
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.RequiredPersonnel < 0 THEN
                    RAISE(ABORT, 'RequiredPersonnel cannot be negative')
            END;
        END;
        """)

        # 3) Validate Presence References
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_presence_reference_insert
        BEFORE INSERT ON Presence
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.SoldierOrTeamType = 'Soldier'
                     AND (SELECT COUNT(*) FROM Soldier WHERE SoldierID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Soldier table')
                WHEN NEW.SoldierOrTeamType = 'Team'
                     AND (SELECT COUNT(*) FROM Team WHERE TeamID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Team table')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_presence_reference_update
        BEFORE UPDATE ON Presence
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.SoldierOrTeamType = 'Soldier'
                     AND (SELECT COUNT(*) FROM Soldier WHERE SoldierID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Soldier table')
                WHEN NEW.SoldierOrTeamType = 'Team'
                     AND (SELECT COUNT(*) FROM Team WHERE TeamID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Team table')
            END;
        END;
        """)

        # 4) Validate TaskPeriod References
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_taskperiod_reference_insert
        BEFORE INSERT ON TaskPeriod
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_taskperiod_reference_update
        BEFORE UPDATE ON TaskPeriod
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;
        END;
        """)

        # 5) Validate TaskRole References
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_taskrole_reference_insert
        BEFORE INSERT ON TaskRole
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_taskrole_reference_update
        BEFORE UPDATE ON TaskRole
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;
        END;
        """)

        # 6) Validate CurrentTaskAssignment References
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_currenttaskassignment_reference_insert
        BEFORE INSERT ON CurrentTaskAssignment
        FOR EACH ROW
        BEGIN
            -- First check the Task part
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;

            -- Then check the SoldierOrTeam part
            SELECT CASE
                WHEN NEW.SoldierOrTeamType = 'Soldier'
                     AND (SELECT COUNT(*) FROM Soldier WHERE SoldierID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Soldier table')
                WHEN NEW.SoldierOrTeamType = 'Team'
                     AND (SELECT COUNT(*) FROM Team WHERE TeamID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Team table')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_currenttaskassignment_reference_update
        BEFORE UPDATE ON CurrentTaskAssignment
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;

            SELECT CASE
                WHEN NEW.SoldierOrTeamType = 'Soldier'
                     AND (SELECT COUNT(*) FROM Soldier WHERE SoldierID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Soldier table')
                WHEN NEW.SoldierOrTeamType = 'Team'
                     AND (SELECT COUNT(*) FROM Team WHERE TeamID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Team table')
            END;
        END;
        """)

        # 7) Validate TaskHistory References
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_taskhistory_reference_insert
        BEFORE INSERT ON TaskHistory
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;

            SELECT CASE
                WHEN NEW.SoldierOrTeamType = 'Soldier'
                     AND (SELECT COUNT(*) FROM Soldier WHERE SoldierID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Soldier table')
                WHEN NEW.SoldierOrTeamType = 'Team'
                     AND (SELECT COUNT(*) FROM Team WHERE TeamID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Team table')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_taskhistory_reference_update
        BEFORE UPDATE ON TaskHistory
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.TaskType = 'TemporaryTask'
                     AND (SELECT COUNT(*) FROM TemporaryTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in TemporaryTask table')
                WHEN NEW.TaskType = 'RecurringTask'
                     AND (SELECT COUNT(*) FROM RecurringTask WHERE TaskID = NEW.TaskID) = 0 THEN
                    RAISE(ABORT, 'TaskID does not exist in RecurringTask table')
            END;

            SELECT CASE
                WHEN NEW.SoldierOrTeamType = 'Soldier'
                     AND (SELECT COUNT(*) FROM Soldier WHERE SoldierID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Soldier table')
                WHEN NEW.SoldierOrTeamType = 'Team'
                     AND (SELECT COUNT(*) FROM Team WHERE TeamID = NEW.SoldierOrTeamID) = 0 THEN
                    RAISE(ABORT, 'SoldierOrTeamID does not exist in Team table')
            END;
        END;
        """)

        # 8) Validate unique TeamName in Team table
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_team_name_uniqueness_insert
        BEFORE INSERT ON Team
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM Team
                    WHERE TeamName = NEW.TeamName
                      AND TeamID != NEW.TeamID
                ) > 0 THEN
                    RAISE(ABORT, 'The team name already exists. Please use a unique name')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_team_name_uniqueness_update
        BEFORE UPDATE ON Team
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM Team
                    WHERE TeamName = NEW.TeamName
                      AND TeamID != NEW.TeamID
                ) > 0 THEN
                    RAISE(ABORT, 'The team name already exists. Please use a unique name')
            END;
        END;
        """)

        # 9) Validate unique RoleName in Role table
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_role_name_uniqueness_insert
        BEFORE INSERT ON Role
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM Role
                    WHERE RoleName = NEW.RoleName
                      AND RoleID != NEW.RoleID
                ) > 0 THEN
                    RAISE(ABORT, 'The role name already exists. Please use a unique name')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_role_name_uniqueness_update
        BEFORE UPDATE ON Role
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM Role
                    WHERE RoleName = NEW.RoleName
                      AND RoleID != NEW.RoleID
                ) > 0 THEN
                    RAISE(ABORT, 'The role name already exists. Please use a unique name')
            END;
        END;
        """)

        # 10) Validate unique TaskName in TemporaryTask
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_temporary_task_name_uniqueness_insert
        BEFORE INSERT ON TemporaryTask
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM TemporaryTask
                    WHERE TaskName = NEW.TaskName
                      AND TaskID != NEW.TaskID
                ) > 0 THEN
                    RAISE(ABORT, 'The temporary task name already exists. Please use a unique name')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_temporary_task_name_uniqueness_update
        BEFORE UPDATE ON TemporaryTask
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM TemporaryTask
                    WHERE TaskName = NEW.TaskName
                      AND TaskID != NEW.TaskID
                ) > 0 THEN
                    RAISE(ABORT, 'The temporary task name already exists. Please use a unique name')
            END;
        END;
        """)

        # 11) Validate unique TaskName in RecurringTask
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_recurring_task_name_uniqueness_insert
        BEFORE INSERT ON RecurringTask
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM RecurringTask
                    WHERE TaskName = NEW.TaskName
                      AND TaskID != NEW.TaskID
                ) > 0 THEN
                    RAISE(ABORT, 'The recurring task name already exists. Please use a unique name')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS validate_recurring_task_name_uniqueness_update
        BEFORE UPDATE ON RecurringTask
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN (
                    SELECT COUNT(*)
                    FROM RecurringTask
                    WHERE TaskName = NEW.TaskName
                      AND TaskID != NEW.TaskID
                ) > 0 THEN
                    RAISE(ABORT, 'The recurring task name already exists. Please use a unique name')
            END;
        END;
        """)

        # Commit triggers
        conn.commit()
        print("All triggers have been initialized successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred during the initialization of triggers tables: {e}")
        return_val = False
    finally:
        if conn:
            conn.close()
            return return_val