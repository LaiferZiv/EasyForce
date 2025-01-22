"""
data_modification.py

Contains the base class (the "father" class) that provides generic CRUD operations
for any subclass that defines table name, columns, and primary keys.

All database connections are opened internally, so no external 'conn' is passed around.
"""

import sqlite3
from typing import Optional, Dict, Any, Union
from EasyForce.common.config import DB_PATH


class BaseEntity:
    """
    The base class for all entities.
    It assumes that each subclass will:
    1) Define table name through get_table_name().
    2) Define the columns through get_columns().
    3) Define the primary key columns through get_primary_key_columns_names().
    4) Optionally indicate whether the table uses AUTOINCREMENT through is_autoincrement().
    """

    def __init__(self, **kwargs: Any):
        """
        Dynamically set attributes based on provided keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def _get_connection(cls):
        """
        Internal helper: opens a connection to DB_PATH.
        All class methods will call this instead of receiving a conn param.
        """
        return sqlite3.connect(DB_PATH)

    @classmethod
    def get_table_name(cls) -> str:
        raise NotImplementedError("Subclasses must define the table name.")

    @classmethod
    def get_columns(cls):
        """
        Returns a tuple of column names WITHOUT parentheses:
        e.g., return "TimeID", "StartDateTime", "EndDateTime"
        """
        raise NotImplementedError("Subclasses must define the columns.")

    @classmethod
    def get_primary_key_columns_names(cls):
        """
        Returns the PK column names as a tuple WITHOUT parentheses:
        e.g., return "TimeID",
        or return "SoldierTeamTaskType", "SoldierTeamTaskID", "TimeID"
        """
        raise NotImplementedError("Subclasses must define the primary key columns.")

    @classmethod
    def is_autoincrement(cls) -> bool:
        """
        Override in subclass if the table uses AUTOINCREMENT on a single PK column.
        """
        return False

    @classmethod
    def get_by_id(cls, pk_dict: Dict[str, Any]) -> Optional["BaseEntity"]:
        """
        Fetches a single record by its primary key(s) and returns an instance of the subclass,
        or None if no matching record is found.

        Because we don't pass conn, we open it internally.
        """
        table_name = cls.get_table_name()
        columns = cls.get_columns()
        pk_cols = cls.get_primary_key_columns_names()

        if set(pk_cols) != set(pk_dict.keys()):
            raise ValueError("Provided keys do not match primary key definition.")

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            where_clause = " AND ".join([f"{col} = ?" for col in pk_cols])
            query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {where_clause}"
            pk_values_ordered = [pk_dict[col] for col in pk_cols]
            cursor.execute(query, pk_values_ordered)
            row = cursor.fetchone()

        if row:
            data_dict = dict(zip(columns, row))
            return cls(**data_dict)
        return None

    @classmethod
    def get_all(cls) -> list:
        """
        Fetches all records from the table and returns them as a list of subclass instances.
        Opens the DB internally.
        """
        table_name = cls.get_table_name()
        columns = cls.get_columns()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()

        return [cls(**dict(zip(columns, row))) for row in rows]

    @classmethod
    def get_column_values(cls, column_name: str) -> Optional[list]:
        """
        Retrieves all values from a specified column in the table.

        Args:
            column_name (str): The name of the column to retrieve values from.

        Returns:
            list: A list of values from the specified column if it exists and contains values.
            None: If the column doesn't exist or contains no values.
        """
        table_name = cls.get_table_name()
        columns = cls.get_columns()

        # Check if the column exists in the table
        if column_name not in columns:
            print(f"Error: Column '{column_name}' does not exist in table '{table_name}'.")
            return None

        with cls._get_connection() as conn:
            cursor = conn.cursor()

            try:
                # Query to fetch all values from the specified column
                query = f"SELECT {column_name} FROM {table_name}"
                cursor.execute(query)
                rows = cursor.fetchall()

                if rows:
                    # Return a flat list of values
                    return [row[0] for row in rows]
                else:
                    print(f"No values found in column '{column_name}' of table '{table_name}'.")
                    return None
            except sqlite3.Error as e:
                print(f"Database error while retrieving column '{column_name}': {e}")
                return None

    def add(self) -> Union["BaseEntity", None]:
        """
        Inserts a new row into the database.
        If autoincrement and single PK, updates self.pk_col with cursor.lastrowid.
        """
        pk_cols = self.get_primary_key_columns_names()
        autoincrement = self.is_autoincrement() and (len(pk_cols) == 1)

        # If not autoincrement, ensure PK is set
        if not autoincrement:
            for pk_col in pk_cols:
                if getattr(self, pk_col, None) is None:
                    print(f"Add Error: Missing primary key value for '{pk_col}'.")
                    return None
            # Check duplicates by PK
            pk_dict = {col: getattr(self, col) for col in pk_cols}
            existing = type(self).get_by_id(pk_dict)
            if existing is not None:
                print("Add Error: A record with these primary key values already exists.")
                return None

        table_name = self.get_table_name()
        columns = self.get_columns()
        values = [getattr(self, col, None) for col in columns]

        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                if autoincrement:
                    setattr(self, pk_cols[0], cursor.lastrowid)
            return self
        except sqlite3.Error as e:
            print(f"Add Error: {e}")
            return None

    def update(self) -> Union["BaseEntity", None]:
        """
        Updates the existing record in the database.
        """
        pk_cols = self.get_primary_key_columns_names()
        for pk_col in pk_cols:
            if getattr(self, pk_col, None) is None:
                print(f"Update Error: Missing primary key value for '{pk_col}'.")
                return None

        # Check if record exists
        pk_dict = {col: getattr(self, col) for col in pk_cols}
        existing = type(self).get_by_id(pk_dict)
        if existing is None:
            print("Update Error: No existing record found with these primary key values.")
            return None

        table_name = self.get_table_name()
        columns = self.get_columns()

        set_clause = ", ".join([f"{col} = ?" for col in columns if col not in pk_cols])
        where_clause = " AND ".join([f"{col} = ?" for col in pk_cols])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        non_pk_values = [getattr(self, col) for col in columns if col not in pk_cols]
        pk_values = [getattr(self, col) for col in pk_cols]

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, non_pk_values + pk_values)
                conn.commit()
            return self
        except sqlite3.Error as e:
            print(f"Update Error: {e}")
            return None

    def delete(self) -> Union["BaseEntity", None]:
        """
        Deletes the record from the database based on the primary key.
        """
        pk_cols = self.get_primary_key_columns_names()
        pk_values = [getattr(self, col, None) for col in pk_cols]
        if any(val is None for val in pk_values):
            print("Delete Error: Missing primary key value(s).")
            return None

        table_name = self.get_table_name()
        where_clause = " AND ".join([f"{col} = ?" for col in pk_cols])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, pk_values)
                conn.commit()
            return self
        except sqlite3.Error as e:
            print(f"Delete Error: {e}")
            return None