"""
entities_classes.py

Contains classes representing the main entity tables, each inheriting from BaseEntity,
with typed attributes and without parentheses when returning tuples.
"""
from datetime import datetime,timedelta

from EasyForce.common.constants import UNNECESSARILY_TIME_RANGE
from EasyForce.data_management.data_structure.data_modification import BaseEntity

class TimeRange(BaseEntity):
    TimeID: int = None
    StartDateTime: str = None
    EndDateTime: str = None

    @classmethod
    def get_table_name(cls) -> str:
        return "TimeRange"

    @classmethod
    def get_columns(cls):
        return "TimeID", "StartDateTime", "EndDateTime"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TimeID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return True
    @classmethod
    def garbage_collector(cls):
        from EasyForce.data_management.data_structure.relationships_classes import Presence, CurrentTaskAssignment, TaskHistory

        presence_table_time_ids = Presence.get_column_values("TimeID")
        current_task_assignment_table_time_ids = CurrentTaskAssignment.get_column_values("TimeID")
        task_history_table_time_ids = TaskHistory.get_column_values("TimeID")
        unified_time_ids = set(presence_table_time_ids) | set(current_task_assignment_table_time_ids) | set(task_history_table_time_ids)
        time_range_rows = TimeRange.get_all()
        for row in time_range_rows:
            if (row.TimeID not in unified_time_ids or
                    (datetime.fromisoformat(row.EndDateTime).replace(microsecond=0) -
                     datetime.fromisoformat(row.StartDateTime).replace(microsecond=0)) <
                     timedelta(minutes=UNNECESSARILY_TIME_RANGE)):
                row.delete()

    def __repr__(self):
        return (
            f"<TimeRange(TimeID={getattr(self, 'TimeID', None)}, "
            f"StartDateTime={getattr(self, 'StartDateTime', None)}, "
            f"EndDateTime={getattr(self, 'EndDateTime', None)})>"
        )


class Team(BaseEntity):
    TeamID: int = None
    TeamName: str = None

    @classmethod
    def get_table_name(cls) -> str:
        return "Team"

    @classmethod
    def get_columns(cls):
        return "TeamID", "TeamName"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TeamID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return True

    @classmethod
    def get_by_unique_name(cls, team_name: str):
        """
        Fetches a Team by its unique TeamName.
        Returns a Team instance if found, or None if no match.
        """
        columns = cls.get_columns()
        table_name = cls.get_table_name()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE TeamName = ?"
            cursor.execute(query, (team_name,))
            row = cursor.fetchone()

        if row:
            data_dict = dict(zip(columns, row))
            return cls(**data_dict)
        return None

    def __repr__(self):
        return (
            f"<Team(TeamID={getattr(self, 'TeamID', None)}, "
            f"TeamName={getattr(self, 'TeamName', None)})>"
        )


class Soldier(BaseEntity):
    SoldierID: int = None
    FullName: str= None
    TeamID: int= None

    @classmethod
    def get_table_name(cls) -> str:
        return "Soldier"

    @classmethod
    def get_columns(cls):
        return "SoldierID", "FullName", "TeamID"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "SoldierID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return False

    def __repr__(self):
        return (
            f"<Soldier(SoldierID={getattr(self, 'SoldierID', None)}, "
            f"FullName={getattr(self, 'FullName', None)}, "
            f"TeamID={getattr(self, 'TeamID', None)})>"
        )


class Role(BaseEntity):
    RoleID: int= None
    RoleName: str= None

    @classmethod
    def get_table_name(cls) -> str:
        return "Role"

    @classmethod
    def get_columns(cls):
        return "RoleID", "RoleName"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "RoleID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return True

    @classmethod
    def get_by_unique_name(cls, role_name: str):
        """
        Fetches a Role by its unique RoleName.
        Returns a Role instance if found, or None if no match.
        """
        columns = cls.get_columns()
        table_name = cls.get_table_name()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE RoleName = ?"
            cursor.execute(query, (role_name,))
            row = cursor.fetchone()

        if row:
            data_dict = dict(zip(columns, row))
            return cls(**data_dict)
        return None

    def __repr__(self):
        return (
            f"<Role(RoleID={getattr(self, 'RoleID', None)}, "
            f"RoleName={getattr(self, 'RoleName', None)})>"
        )


class TemporaryTask(BaseEntity):
    TaskID: int= None
    TaskName: str= None
    TaskReputation: str= None

    @classmethod
    def get_table_name(cls) -> str:
        return "TemporaryTask"

    @classmethod
    def get_columns(cls):
        return "TaskID", "TaskName", "TaskReputation"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TaskID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return True

    @classmethod
    def get_by_unique_name(cls, task_name: str) :
        """
        Fetches a TemporaryTask by its unique TaskName.
        Returns a TemporaryTask instance if found, or None if no match.
        """
        columns = cls.get_columns()
        table_name = cls.get_table_name()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE TaskName = ?"
            cursor.execute(query, (task_name,))
            row = cursor.fetchone()

        if row:
            data_dict = dict(zip(columns, row))
            return cls(**data_dict)
        return None

    def __repr__(self):
        return (
            f"<TemporaryTask(TaskID={getattr(self, 'TaskID', None)}, "
            f"TaskName={getattr(self, 'TaskName', None)}, "
            f"TaskReputation={getattr(self, 'TaskReputation', None)})>"
        )


class RecurringTask(BaseEntity):
    TaskID: int= None
    TaskName: str= None
    ShiftDurationInMinutes: int= None
    EveryDayStartTime: str= None
    EveryDayEndTime: str= None
    RequiredPersonnel: int= None

    @classmethod
    def get_table_name(cls) -> str:
        return "RecurringTask"

    @classmethod
    def get_columns(cls):
        return "TaskID", "TaskName", "ShiftDurationInMinutes", "EveryDayStartTime", "EveryDayEndTime", "RequiredPersonnel"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TaskID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return True

    @classmethod
    def get_by_unique_name(cls, task_name: str):
        """
        Fetches a RecurringTask by its unique TaskName.
        Returns a RecurringTask instance if found, or None if no match.
        """
        columns = cls.get_columns()
        table_name = cls.get_table_name()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE TaskName = ?"
            cursor.execute(query, (task_name,))
            row = cursor.fetchone()

        if row:
            data_dict = dict(zip(columns, row))
            return cls(**data_dict)
        return None

    def __repr__(self):
        return (
            f"<RecurringTask(TaskID={getattr(self, 'TaskID', None)}, "
            f"TaskName={getattr(self, 'TaskName', None)}, "
            f"ShiftDurationInMinutes={getattr(self, 'ShiftDurationInMinutes', None)}, "
            f"EveryDayStartTime={getattr(self, 'EveryDayStartTime', None)}, "
            f"EveryDayEndTime={getattr(self, 'EveryDayEndTime', None)}, "
            f"RequiredPersonnel={getattr(self, 'RequiredPersonnel', None)})>"
        )