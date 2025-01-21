"""
entities_classes.py

Contains classes representing the main entity tables, each inheriting from BaseEntity.
"""

from data_modification import BaseEntity

class TimeRange(BaseEntity):
    """
    Represents the TimeRange table:
    - TimeID (INTEGER PRIMARY KEY AUTOINCREMENT)
    - StartDateTime (TEXT NOT NULL)
    - EndDateTime (TEXT NOT NULL)
    """
    @classmethod
    def get_table_name(cls):
        return "TimeRange"

    @classmethod
    def get_columns(cls):
        return "TimeID", "StartDateTime", "EndDateTime"

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("TimeID",)

    @classmethod
    def is_autoincrement(cls):
        return True

    def __repr__(self):
        return (
            f"<TimeRange(TimeID={getattr(self, 'TimeID', None)}, "
            f"StartDateTime={getattr(self, 'StartDateTime', None)}, "
            f"EndDateTime={getattr(self, 'EndDateTime', None)})>"
        )


class Team(BaseEntity):
    """
    Represents the Team table:
    - TeamID (INTEGER PRIMARY KEY AUTOINCREMENT)
    - TeamName (TEXT NOT NULL UNIQUE)
    """
    @classmethod
    def get_table_name(cls):
        return "Team"

    @classmethod
    def get_columns(cls):
        return "TeamID", "TeamName"

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("TeamID",)

    @classmethod
    def is_autoincrement(cls):
        return True

    def __repr__(self):
        return (
            f"<Team(TeamID={getattr(self, 'TeamID', None)}, "
            f"TeamName={getattr(self, 'TeamName', None)})>"
        )


class Soldier(BaseEntity):
    """
    Represents the Soldier table:
    - SoldierID (INTEGER PRIMARY KEY)  (NOT AUTOINCREMENT)
    - FullName (TEXT NOT NULL)
    - TeamID (INTEGER NOT NULL, references Team(TeamID))
    """
    @classmethod
    def get_table_name(cls):
        return "Soldier"

    @classmethod
    def get_columns(cls):
        return "SoldierID", "FullName", "TeamID"

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("SoldierID",)

    @classmethod
    def is_autoincrement(cls):
        # SoldierID is not AUTOINCREMENT
        return False

    def __repr__(self):
        return (
            f"<Soldier(SoldierID={getattr(self, 'SoldierID', None)}, "
            f"FullName={getattr(self, 'FullName', None)}, "
            f"TeamID={getattr(self, 'TeamID', None)})>"
        )


class Role(BaseEntity):
    """
    Represents the Role table:
    - RoleID (INTEGER PRIMARY KEY AUTOINCREMENT)
    - RoleName (TEXT NOT NULL UNIQUE)
    """
    @classmethod
    def get_table_name(cls):
        return "Role"

    @classmethod
    def get_columns(cls):
        return "RoleID", "RoleName"

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("RoleID",)

    @classmethod
    def is_autoincrement(cls):
        return True

    def __repr__(self):
        return (
            f"<Role(RoleID={getattr(self, 'RoleID', None)}, "
            f"RoleName={getattr(self, 'RoleName', None)})>"
        )


class TemporaryTask(BaseEntity):
    """
    Represents the TemporaryTask table:
    - TaskID (INTEGER PRIMARY KEY AUTOINCREMENT)
    - TaskName (TEXT NOT NULL UNIQUE)
    - TaskReputation (TEXT NOT NULL CHECK(TaskReputation IN ('Good', 'Bad', 'None')))
    """
    @classmethod
    def get_table_name(cls):
        return "TemporaryTask"

    @classmethod
    def get_columns(cls):
        return "TaskID", "TaskName", "TaskReputation"

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("TaskID",)

    @classmethod
    def is_autoincrement(cls):
        return True

    def __repr__(self):
        return (
            f"<TemporaryTask(TaskID={getattr(self, 'TaskID', None)}, "
            f"TaskName={getattr(self, 'TaskName', None)}, "
            f"TaskReputation={getattr(self, 'TaskReputation', None)})>"
        )


class RecurringTask(BaseEntity):
    """
    Represents the RecurringTask table:
    - TaskID (INTEGER PRIMARY KEY AUTOINCREMENT)
    - TaskName (TEXT NOT NULL UNIQUE)
    - ShiftDurationInMinutes (INTEGER NOT NULL)
    - EveryDayStartTime (TEXT NOT NULL)
    - EveryDayEndTime (TEXT NOT NULL)
    - RequiredPersonnel (INTEGER NOT NULL)
    """
    @classmethod
    def get_table_name(cls):
        return "RecurringTask"

    @classmethod
    def get_columns(cls):
        return (
            "TaskID",
            "TaskName",
            "ShiftDurationInMinutes",
            "EveryDayStartTime",
            "EveryDayEndTime",
            "RequiredPersonnel",
        )

    @classmethod
    def get_primary_key_columns_names(cls):
        return ("TaskID",)

    @classmethod
    def is_autoincrement(cls):
        return True

    def __repr__(self):
        return (
            f"<RecurringTask(TaskID={getattr(self, 'TaskID', None)}, "
            f"TaskName={getattr(self, 'TaskName', None)}, "
            f"ShiftDurationInMinutes={getattr(self, 'ShiftDurationInMinutes', None)}, "
            f"EveryDayStartTime={getattr(self, 'EveryDayStartTime', None)}, "
            f"EveryDayEndTime={getattr(self, 'EveryDayEndTime', None)}, "
            f"RequiredPersonnel={getattr(self, 'RequiredPersonnel', None)})>"
        )