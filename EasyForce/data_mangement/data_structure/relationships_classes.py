"""
relationships_classes.py

Relationship (bridge) tables, also only calling .add(), .delete(), etc. internally.
"""
from typing import Union

from EasyForce.common.constants import PRESENCE_TABLE, TIME_RANGE_TABLE
from EasyForce.data_mangement.data_structure.data_modification import BaseEntity
from EasyForce.data_mangement.data_structure.entities_classes import TimeRange
from EasyForce.data_mangement.read_db import display_table


class Presence(BaseEntity):
    SoldierTeamTaskType: str= None
    SoldierTeamTaskID: int= None
    TimeID: int= None
    isActive: int= None

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
        def get_time_id(start_time,end_time):
            same_time_range = TimeRange.get_all_by_columns_values({"StartDateTime": start_time, "EndDateTime": end_time})
            if same_time_range:
                same_time_range = same_time_range[0].copy()
            else:
                same_time_range = TimeRange(**{"StartDateTime": start_time, "EndDateTime": end_time})
                if start_time < end_time:
                    same_time_range.add()
            return same_time_range.TimeID

        new_time_range = TimeRange.get_by_id({"TimeID": self.TimeID})
        same_entities = Presence.get_all_by_columns_values({"SoldierTeamTaskType":self.SoldierTeamTaskType,"SoldierTeamTaskID":self.SoldierTeamTaskID})
        if not same_entities:
            return super().add()
        tmp = None
        for old_entity in same_entities:
            old_time_range = TimeRange.get_by_id({"TimeID":old_entity.TimeID})
            if not (new_time_range.EndDateTime < old_time_range.StartDateTime or new_time_range.StartDateTime > old_time_range.EndDateTime):  # has blending range
                if self.isActive == old_entity.isActive: #extend range
                    new_start = min(new_time_range.StartDateTime,new_time_range.EndDateTime,old_time_range.StartDateTime,old_time_range.EndDateTime)
                    new_end = max(new_time_range.StartDateTime,new_time_range.EndDateTime,old_time_range.StartDateTime,old_time_range.EndDateTime)
                    self.TimeID = get_time_id(new_start,new_end)
                    old_entity.delete()
                else: #Presence during a time defined as absence, and vice versa
                    print()
                    prev_time_id = get_time_id(old_time_range.StartDateTime,new_time_range.StartDateTime)
                    post_time_id = get_time_id(new_time_range.EndDateTime,old_time_range.EndDateTime)
                    # [new pried], (old period)
                    # [ ( ) ] => [ ]
                    if new_time_range.StartDateTime <= old_time_range.StartDateTime <= old_time_range.EndDateTime <= new_time_range.EndDateTime:
                        old_entity.delete()
                    # ( [ ] ) => ( )[ ]( )
                    elif old_time_range.StartDateTime <= new_time_range.StartDateTime <= new_time_range.EndDateTime <= old_time_range.EndDateTime:
                        prev = old_entity.copy()
                        post = old_entity.copy()
                        prev.TimeID = prev_time_id
                        post.TimeID = post_time_id
                        old_entity.delete()
                        prev.add()
                        post.add()
                    # [ ( ] ) => [ ]( )
                    elif new_time_range.StartDateTime <= old_time_range.StartDateTime <= new_time_range.EndDateTime <= old_time_range.EndDateTime:
                        post = old_entity.copy()
                        post.TimeID = post_time_id
                        old_entity.delete()
                        post.add()
                    else: # ( [ ) ] => ( )[ ]
                        prev = old_entity.copy()
                        prev.TimeID = prev_time_id
                        old_entity.delete()
                        prev.add()
            print("BEFORE:")
            display_table(TIME_RANGE_TABLE)
            display_table(PRESENCE_TABLE)
            print(self)
            tmp = super().add()
            TimeRange.garbage_collector()
            print("AFTER:")
            display_table(TIME_RANGE_TABLE)
            display_table(PRESENCE_TABLE)
        return tmp

class SoldierRole(BaseEntity):
    SoldierID: int= None
    RoleID: int= None

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
    TaskType: str= None
    TaskID: int= None
    SoldierOrRole: str= None
    SoldierOrRoleID: int= None
    MinRequiredCount: int= None
    RoleEnforcementType: int= None

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
    TaskType: str= None
    TaskID: int= None
    SoldierOrTeamType: str= None
    SoldierOrTeamID: int= None
    TimeID: int= None

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
    HistoryID: int= None
    TaskType: str= None
    TaskID: int= None
    SoldierOrTeamType: str= None
    SoldierOrTeamID: int= None
    TaskReputation: str= None
    TimeID: int= None
    CompletionStatus: str= None

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