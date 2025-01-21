"""
data_modification.py

Contains the base class (the "father" class) that provides generic CRUD operations
for any subclass that defines table name, columns, and primary keys.
"""

import sqlite3

class BaseEntity:
    """
    The base class for all entities.
    It assumes that each subclass will:
    1) Define table name through get_table_name().
    2) Define the columns through get_columns().
    3) Define the primary key columns through get_primary_key_columns_names().
    4) Optionally indicate whether the table uses AUTOINCREMENT through is_autoincrement().
    """

    def __init__(self, **kwargs):
        """
        Dynamically set attributes based on provided keyword arguments.
        Subclasses can override or extend this behavior if needed.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_table_name(cls):
        """
        Must be overridden in the subclass to return the table name as a string.
        Example:
            return "TimeRange"
        """
        raise NotImplementedError("Subclasses must define the table name.")

    @classmethod
    def get_columns(cls):
        """
        Must be overridden in the subclass to return a tuple of column names.
        Example:
            return ("TimeID", "StartDateTime", "EndDateTime")
        """
        raise NotImplementedError("Subclasses must define the columns.")

    @classmethod
    def get_primary_key_columns_names(cls):
        """
        Must be overridden in the subclass to return a tuple of the primary key column name(s).
        Example:
            return ("TimeID",)
        """
        raise NotImplementedError("Subclasses must define the primary key columns.")

    @classmethod
    def is_autoincrement(cls):
        """
        Returns True if the table's primary key is AUTOINCREMENT in the schema.
        Defaults to False. Override in the subclass if needed.
        """
        return False

    @classmethod
    def get_by_id(cls, conn, pk_dict):
        """
        Fetches a single record by its primary key(s) and returns an instance of the subclass,
        or None if no matching record is found.

        :param conn: A sqlite3.Connection object.
        :param pk_dict: A dictionary where each key is a primary key column name,
                        and the value is the column's value.

        :raises ValueError: If pk_dict's keys do not match the subclass's primary key definition.

        :return: An instance of the subclass or None.
        """
        table_name = cls.get_table_name()
        columns = cls.get_columns()
        pk_cols = cls.get_primary_key_columns_names()

        # Verify that the provided pk_dict matches the primary key columns
        if set(pk_cols) != set(pk_dict.keys()):
            raise ValueError("Provided keys in pk_dict do not match primary key definition.")

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
    def get_all(cls, conn):
        """
        Fetches all records from the table corresponding to the subclass
        and returns them as a list of instances.

        :param conn: A sqlite3.Connection object.
        :return: A list of subclass instances.
        """
        table_name = cls.get_table_name()
        columns = cls.get_columns()

        cursor = conn.cursor()
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()

        return [cls(**dict(zip(columns, row))) for row in rows]

    def add(self, conn):
        """
        Inserts a new row into the database.
        If the table uses AUTOINCREMENT and has a single primary key column,
        that primary key will be updated with cursor.lastrowid.

        :param conn: A sqlite3.Connection object.
        :return: Self on success, or None on error (e.g. constraint failure).
        """
        pk_cols = self.get_primary_key_columns_names()
        autoincrement = self.is_autoincrement() and (len(pk_cols) == 1)

        # If not autoincrement, check that primary keys are set (not None)
        if not autoincrement:
            for pk_col in pk_cols:
                if getattr(self, pk_col, None) is None:
                    print(f"Add Error: Missing primary key value for '{pk_col}'.")
                    return None

            # Check for duplicate record
            pk_dict = {col: getattr(self, col) for col in pk_cols}
            existing = type(self).get_by_id(conn, pk_dict)
            if existing is not None:
                print("Add Error: A record with these primary key values already exists.")
                return None

        table_name = self.get_table_name()
        columns = self.get_columns()
        values = [getattr(self, col, None) for col in columns]

        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        cursor = conn.cursor()
        try:
            cursor.execute(query, values)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Add Error: {e}")
            return None

        # If autoincrement, update the primary key
        if autoincrement:
            setattr(self, pk_cols[0], cursor.lastrowid)

        return self

    def update(self, conn):
        """
        Updates the existing record in the database.
        Returns self on success, or None on error.

        :param conn: A sqlite3.Connection object.
        """
        pk_cols = self.get_primary_key_columns_names()

        # Check PK is set
        for pk_col in pk_cols:
            if getattr(self, pk_col, None) is None:
                print(f"Update Error: Missing primary key value for '{pk_col}'.")
                return None

        # Check if record exists
        pk_dict = {col: getattr(self, col) for col in pk_cols}
        existing = type(self).get_by_id(conn, pk_dict)
        if existing is None:
            print("Update Error: No existing record found with these primary key values.")
            return None

        table_name = self.get_table_name()
        columns = self.get_columns()
        cursor = conn.cursor()

        set_clause = ", ".join([f"{col} = ?" for col in columns if col not in pk_cols])
        where_clause = " AND ".join([f"{col} = ?" for col in pk_cols])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        non_pk_values = [getattr(self, col) for col in columns if col not in pk_cols]
        pk_values = [getattr(self, col) for col in pk_cols]

        try:
            cursor.execute(query, non_pk_values + pk_values)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Update Error: {e}")
            return None

        return self

    def delete(self, conn):
        """
        Deletes the record from the database based on the primary key.
        Returns self on success, or None on error.

        :param conn: A sqlite3.Connection object.
        """
        pk_cols = self.get_primary_key_columns_names()
        pk_values = [getattr(self, col, None) for col in pk_cols]

        # If any PK is None, cannot delete
        if any(val is None for val in pk_values):
            print("Delete Error: Missing primary key value(s).")
            return None

        table_name = self.get_table_name()
        cursor = conn.cursor()
        where_clause = " AND ".join([f"{col} = ?" for col in pk_cols])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"

        try:
            cursor.execute(query, pk_values)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Delete Error: {e}")
            return None

        return self