"""
relationships_classes.py

Contains relationship (bridge) classes that inherit from BaseEntity.
These represent tables linking or relating entities in your schema.
"""

from data_modification import BaseEntity

class Presence(BaseEntity):
    """
    Represents the Presence table:
    - SoldierTeamTaskType (TEXT, part of PK)
    - SoldierTeamTaskID (INTEGER, part of PK)
    - TimeID (INTEGER, part of PK)
    - isActive (INTEGER, default 1 => presence)
    Primary Key: (SoldierTeamTaskType, SoldierTeamTaskID, TimeID)
    """
    @classmethod
    def get_table_name(cls):
        return "Presence"

    @classmethod
    def get_columns(cls):
        return "SoldierTeamTaskType", "SoldierTeamTaskID", "TimeID", "isActive"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "SoldierTeamTaskType", "SoldierTeamTaskID", "TimeID"

    # Not autoincrement since PK is composite and partially text
    @classmethod
    def is_autoincrement(cls):
        return False

    def __repr__(self):
        return (
            f"<Presence(SoldierTeamTaskType={getattr(self, 'SoldierTeamTaskType', None)}, "
            f"SoldierTeamTaskID={getattr(self, 'SoldierTeamTaskID', None)}, "
            f"TimeID={getattr(self, 'TimeID', None)}, "
            f"isActive={getattr(self, 'isActive', None)})>"
        )


class SoldierRole(BaseEntity):
    """
    Represents the SoldierRole table:
    - SoldierID (INTEGER, part of PK)
    - RoleID (INTEGER, part of PK)
    Primary Key: (SoldierID, RoleID)
    """
    @classmethod
    def get_table_name(cls):
        return "SoldierRole"

    @classmethod
    def get_columns(cls):
        return "SoldierID", "RoleID"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "SoldierID", "RoleID"

    @classmethod
    def is_autoincrement(cls):
        return False

    def __repr__(self):
        return (
            f"<SoldierRole(SoldierID={getattr(self, 'SoldierID', None)}, "
            f"RoleID={getattr(self, 'RoleID', None)})>"
        )


class TaskRole(BaseEntity):
    """
    Represents the TaskRole table:
    - TaskType (TEXT, part of PK)
    - TaskID (INTEGER, part of PK)
    - SoldierOrRole (TEXT, part of PK)
    - SoldierOrRoleID (INTEGER, part of PK)
    - MinRequiredCount (INTEGER)
    - RoleEnforcementType (INTEGER, default 1 => must be, 0 => cannot be)
    Primary Key: (TaskType, TaskID, SoldierOrRole, SoldierOrRoleID)
    """
    @classmethod
    def get_table_name(cls):
        return "TaskRole"

    @classmethod
    def get_columns(cls):
        return (
            "TaskType",
            "TaskID",
            "SoldierOrRole",
            "SoldierOrRoleID",
            "MinRequiredCount",
            "RoleEnforcementType",
        )

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TaskType", "TaskID", "SoldierOrRole", "SoldierOrRoleID"

    @classmethod
    def is_autoincrement(cls):
        return False

    def __repr__(self):
        return (
            f"<TaskRole(TaskType={getattr(self, 'TaskType', None)}, "
            f"TaskID={getattr(self, 'TaskID', None)}, "
            f"SoldierOrRole={getattr(self, 'SoldierOrRole', None)}, "
            f"SoldierOrRoleID={getattr(self, 'SoldierOrRoleID', None)}, "
            f"MinRequiredCount={getattr(self, 'MinRequiredCount', None)}, "
            f"RoleEnforcementType={getattr(self, 'RoleEnforcementType', None)})>"
        )


class CurrentTaskAssignment(BaseEntity):
    """
    Represents the CurrentTaskAssignment table:
    - TaskType (TEXT, part of PK)
    - TaskID (INTEGER, part of PK)
    - SoldierOrTeamType (TEXT, part of PK)
    - SoldierOrTeamID (INTEGER, part of PK)
    - TimeID (INTEGER, part of PK)
    Primary Key: (TaskType, TaskID, SoldierOrTeamType, SoldierOrTeamID, TimeID)
    """
    @classmethod
    def get_table_name(cls):
        return "CurrentTaskAssignment"

    @classmethod
    def get_columns(cls):
        return (
            "TaskType",
            "TaskID",
            "SoldierOrTeamType",
            "SoldierOrTeamID",
            "TimeID",
        )

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TaskType", "TaskID", "SoldierOrTeamType", "SoldierOrTeamID", "TimeID"

    @classmethod
    def is_autoincrement(cls):
        return False

    def __repr__(self):
        return (
            f"<CurrentTaskAssignment(TaskType={getattr(self, 'TaskType', None)}, "
            f"TaskID={getattr(self, 'TaskID', None)}, SoldierOrTeamType={getattr(self, 'SoldierOrTeamType', None)}, "
            f"SoldierOrTeamID={getattr(self, 'SoldierOrTeamID', None)}, "
            f"TimeID={getattr(self, 'TimeID', None)})>"
        )


class TaskHistory(BaseEntity):
    """
    Represents the TaskHistory table:
    - HistoryID (INTEGER PRIMARY KEY AUTOINCREMENT)
    - TaskType (TEXT, CHECK constraint)
    - TaskID (INTEGER)
    - SoldierOrTeamType (TEXT, CHECK constraint)
    - SoldierOrTeamID (INTEGER)
    - TaskReputation (TEXT, CHECK constraint)
    - TimeID (INTEGER)
    - CompletionStatus (TEXT, CHECK constraint)
    Primary Key: (HistoryID)
    There's also a UNIQUE constraint on (TaskType, TaskID, SoldierOrTeamType, SoldierOrTeamID, TimeID).
    """
    @classmethod
    def get_table_name(cls):
        return "TaskHistory"

    @classmethod
    def get_columns(cls):
        return (
            "HistoryID",
            "TaskType",
            "TaskID",
            "SoldierOrTeamType",
            "SoldierOrTeamID",
            "TaskReputation",
            "TimeID",
            "CompletionStatus",
        )

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("HistoryID",)

    @classmethod
    def is_autoincrement(cls):
        # HistoryID is AUTOINCREMENT
        return True

    def __repr__(self):
        return (
            f"<TaskHistory(HistoryID={getattr(self, 'HistoryID', None)}, "
            f"TaskType={getattr(self, 'TaskType', None)}, TaskID={getattr(self, 'TaskID', None)}, "
            f"SoldierOrTeamType={getattr(self, 'SoldierOrTeamType', None)}, SoldierOrTeamID={getattr(self, 'SoldierOrTeamID', None)}, "
            f"TaskReputation={getattr(self, 'TaskReputation', None)}, TimeID={getattr(self, 'TimeID', None)}, "
            f"CompletionStatus={getattr(self, 'CompletionStatus', None)})>"
        )