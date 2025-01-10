import sqlite3

from EasyForce.common.config import DB_PATH
from EasyForce.common.utils import initialize_table_names

def display_table(table_name):
    """Display the contents of a specified table, printing first the tuple of column names
    in their creation order, then each row in that same order."""

    database_name = 'my_database.db'
    conn = None
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Execute a query to select all columns
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names in the order they were defined
        column_names = [desc[0] for desc in cursor.description]

        # Print the table name
        print(f"\n{table_name} table :")

        # Print the tuple of column names
        print(tuple(column_names))

        # Print each row in the same order
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def display_all_tables():
    tables = initialize_table_names()
    for t in tables.values():
        display_table(t)

def get_primary_key_val_by_unique_column_val(table, unique_text_value):
    """
    Retrieve the primary key of a record based on a unique text column value.

    Args:
        table (str): The name of the table.
        unique_text_value (str): The unique text value.

    Returns:
        int or None: The primary key of the record if found, or None if no matching record exists.
    """
    database_name = 'my_database.db'

    # Get the primary key column(s) and unique column name
    primary_key_column = get_primary_key_column_names(table)
    text_column = get_unique_column_name(table)

    # Convert tuple to string for SQL query
    primary_key_column_str = ", ".join(primary_key_column) if primary_key_column else None

    if not text_column or not primary_key_column_str:
        print(f"Invalid table or columns: table={table}, unique_column={text_column}, primary_key={primary_key_column}")
        return None

    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()

            # Query to find the primary key based on the unique text column
            query = f"""
            SELECT {primary_key_column_str}
            FROM {table}
            WHERE {text_column} = ?;
            """
            cursor.execute(query, (unique_text_value,))
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                print(f"No record found in table '{table}' with {text_column} = '{unique_text_value}'.")
                return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def get_column_value_by_primary_key(table, column, primary_key_columns, primary_key_values):
    """
    Retrieve the value of a specific column in a table based on one or more primary key columns.

    Args:
        table (str): The name of the table.
        column (str): The name of the column whose value you want to retrieve.
        primary_key_columns (tuple): A tuple of the primary key column names.
        primary_key_values (tuple): A tuple of the corresponding primary key values
                                    in the same order as primary_key_columns.

    Returns:
        The value of the specified column if found, or None if no matching record exists.
    """
    database_name = DB_PATH
    if len(primary_key_columns) != len(primary_key_values):
        print("Error: The number of PK columns does not match the number of PK values.")
        return None

    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()

            # Build the WHERE clause dynamically based on the tuple of PK columns
            where_clause = " AND ".join([f"{col} = ?" for col in primary_key_columns])

            # Construct the SQL query
            query = f"""
            SELECT {column}
            FROM {table}
            WHERE {where_clause};
            """

            cursor.execute(query, primary_key_values)
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                print(
                    f"No record found in table '{table}' "
                    f"with PK columns {primary_key_columns} = {primary_key_values}."
                )
                return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def get_unique_column_name(table):
    """
    Returns the name of the column that is defined as UNIQUE in the specified table.
    If no UNIQUE column is found or the table does not exist, returns None.
    """

    # If the table has only a composite key (like SoldierRole),
    # and no single unique column, just return None immediately.
    if table in ("SoldierRole", "Presence", "TaskRole"):
        return None

    database_name = 'my_database.db'
    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()

            # 1) Ensure the table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (table,)
            )
            if not cursor.fetchone():
                print(f"Table '{table}' does not exist in the database.")
                return None

            # 2) Retrieve all indexes on the table
            cursor.execute(f"PRAGMA index_list({table});")
            indexes = cursor.fetchall()

            # 3) Search for an index that is marked as unique
            for idx in indexes:
                index_name = idx[1]
                is_unique = idx[2]
                if is_unique == 1:
                    # 4) Retrieve the columns of that unique index
                    cursor.execute(f"PRAGMA index_info({index_name});")
                    index_info = cursor.fetchall()
                    if index_info:
                        # 5) Return the first column name from that unique index
                        return index_info[0][2]

            return None

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def get_column_values(table, column):
    """
    Retrieve all values from a specific column in a table.

    Args:
        table (str): The name of the table.
        column (str): The name of the column to retrieve values from.

    Returns:
        list: A list of values from the specified column, or None if an error occurs or no values exist.
    """
    database_name = DB_PATH
    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()

            # Construct the SQL query
            query = f"SELECT {column} FROM {table};"
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                # Extract the first element from each row to return a flat list
                return [row[0] for row in results]
            else:
                print(f"No records found in table '{table}' for column '{column}'.")
                return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

################ need to rewrite it ################################
def get_primary_key_column_names(table):
    """
    Get the primary key column names for a specified table.

    Args:
        table (str): The name of the table.

    Returns:
        tuple or None: A tuple of primary key column names if the table exists in the mapping,
        otherwise None.
    """
    primary_keys = {
        "TimeRange": ("TimeID",),
        "Team": ("TeamID",),
        "Soldier": ("SoldierID",),
        "Role": ("RoleID",),
        "TemporaryTask": ("TaskID",),
        "RecurringTask": ("TaskID",),
        "Presence": ("SoldierTeamTaskType", "SoldierTeamTaskID", "TimeID"),
        "SoldierRole": ("SoldierID", "RoleID"),
        "TaskRole": ("TaskType", "TaskID", "RoleID"),
        "CurrentTaskAssignment": ("TaskType", "TaskID", "SoldierOrTeamType", "SoldierOrTeamID", "TimeID"),
        "TaskHistory": ("HistoryID",),
    }
    return primary_keys[table] if table in primary_keys else None
