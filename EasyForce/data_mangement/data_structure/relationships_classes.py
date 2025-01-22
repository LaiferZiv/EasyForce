"""
relationships_classes.py

Relationship (bridge) tables, also only calling .add(), .delete(), etc. internally.
"""
from typing import Union
from datetime import datetime

from EasyForce.data_mangement.data_structure.data_modification import BaseEntity
from EasyForce.data_mangement.data_structure.entities_classes import TimeRange


class Presence(BaseEntity):
    SoldierTeamTaskType: str
    SoldierTeamTaskID: int
    TimeID: int
    isActive: int

    @classmethod
    def get_table_name(cls) -> str:
        return "Presence"

    @classmethod
    def get_columns(cls):
        return "SoldierTeamTaskType", "SoldierTeamTaskID", "TimeID", "isActive"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "SoldierTeamTaskType", "SoldierTeamTaskID", "TimeID"

    @classmethod
    def is_autoincrement(cls) -> bool:
        return False

    def __repr__(self):
        return (
            f"<Presence(SoldierTeamTaskType={getattr(self, 'SoldierTeamTaskType', None)}, "
            f"SoldierTeamTaskID={getattr(self, 'SoldierTeamTaskID', None)}, "
            f"TimeID={getattr(self, 'TimeID', None)}, "
            f"isActive={getattr(self, 'isActive', None)})>"
        )

    def add(self) -> Union["BaseEntity", None]:
        new_time_range = TimeRange.get_by_id({"TimeID": self.TimeID})
        same_entities = Presence.get_all_by_columns_values({"SoldierTeamTaskType":self.SoldierTeamTaskType,"SoldierTeamTaskID":self.SoldierTeamTaskID})
        if not same_entities:
            return super().add()
        tmp = None
        for old_entity in same_entities:
            old_time_range = TimeRange.get_by_id({"TimeID":old_entity.TimeID})
            if self.isActive == old_entity.isActive:
                if new_time_range.EndDateTime < old_time_range.StartDateTime or \
                   new_time_range.StartDateTime > old_time_range.EndDateTime: #No blending range
                    tmp = super().add()
                else:
                    new_start = min(new_time_range.StartDateTime,new_time_range.EndDateTime,old_time_range.StartDateTime,old_time_range.EndDateTime)
                    new_end = max(new_time_range.StartDateTime,new_time_range.EndDateTime,old_time_range.StartDateTime,old_time_range.EndDateTime)
                    new_time_range = TimeRange(**{"StartDateTime": new_start, "EndDateTime": new_end}).add()
                    self.TimeID = new_time_range.TimeID
                    old_entity.delete()
                    tmp = super().add()
        return tmp

class SoldierRole(BaseEntity):
    SoldierID: int
    RoleID: int

    @classmethod
    def get_table_name(cls) -> str:
        return "SoldierRole"

    @classmethod
    def get_columns(cls):
        return "SoldierID", "RoleID"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "SoldierID", "RoleID"

    @classmethod
    def is_autoincrement(cls) -> bool:
        return False

    def __repr__(self):
        return (
            f"<SoldierRole(SoldierID={getattr(self, 'SoldierID', None)}, "
            f"RoleID={getattr(self, 'RoleID', None)})>"
        )

class TaskRole(BaseEntity):
    TaskType: str
    TaskID: int
    SoldierOrRole: str
    SoldierOrRoleID: int
    MinRequiredCount: int
    RoleEnforcementType: int

    @classmethod
    def get_table_name(cls) -> str:
        return "TaskRole"

    @classmethod
    def get_columns(cls):
        return "TaskType", "TaskID", "SoldierOrRole", "SoldierOrRoleID", "MinRequiredCount", "RoleEnforcementType"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TaskType", "TaskID", "SoldierOrRole", "SoldierOrRoleID"

    @classmethod
    def is_autoincrement(cls) -> bool:
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
    TaskType: str
    TaskID: int
    SoldierOrTeamType: str
    SoldierOrTeamID: int
    TimeID: int

    @classmethod
    def get_table_name(cls) -> str:
        return "CurrentTaskAssignment"

    @classmethod
    def get_columns(cls):
        return "TaskType", "TaskID", "SoldierOrTeamType", "SoldierOrTeamID", "TimeID"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "TaskType", "TaskID", "SoldierOrTeamType", "SoldierOrTeamID", "TimeID"

    @classmethod
    def is_autoincrement(cls) -> bool:
        return False

    def __repr__(self):
        return (
            f"<CurrentTaskAssignment(TaskType={getattr(self, 'TaskType', None)}, "
            f"TaskID={getattr(self, 'TaskID', None)}, SoldierOrTeamType={getattr(self, 'SoldierOrTeamType', None)}, "
            f"SoldierOrTeamID={getattr(self, 'SoldierOrTeamID', None)}, "
            f"TimeID={getattr(self, 'TimeID', None)})>"
        )

class TaskHistory(BaseEntity):
    HistoryID: int
    TaskType: str
    TaskID: int
    SoldierOrTeamType: str
    SoldierOrTeamID: int
    TaskReputation: str
    TimeID: int
    CompletionStatus: str

    @classmethod
    def get_table_name(cls) -> str:
        return "TaskHistory"

    @classmethod
    def get_columns(cls):
        return "HistoryID", "TaskType", "TaskID", "SoldierOrTeamType", "SoldierOrTeamID", "TaskReputation", "TimeID", "CompletionStatus"

    @classmethod
    def get_primary_key_columns_names(cls):
        return "HistoryID",

    @classmethod
    def is_autoincrement(cls) -> bool:
        return True

    def __repr__(self):
        return (
            f"<TaskHistory(HistoryID={getattr(self, 'HistoryID', None)}, "
            f"TaskType={getattr(self, 'TaskType', None)}, TaskID={getattr(self, 'TaskID', None)}, "
            f"SoldierOrTeamType={getattr(self, 'SoldierOrTeamType', None)}, SoldierOrTeamID={getattr(self, 'SoldierOrTeamID', None)}, "
            f"TaskReputation={getattr(self, 'TaskReputation', None)}, TimeID={getattr(self, 'TimeID', None)}, "
            f"CompletionStatus={getattr(self, 'CompletionStatus', None)})>"
        )