# import sqlite3
# from EasyForce.data_mangement.read_db import get_primary_key_column_names,get_unique_column_name
# from EasyForce.common.config import DB_PATH
#
# def add_record(table, data):
#     """
#     Add a new record to the database and return the primary key columns of the inserted record.
#
#     Steps:
#       1. If 'data' is empty, return None.
#       2. Check if the table has a UNIQUE column:
#          - If yes, and 'data' has a value for that unique column, check if a record already exists with that value.
#          - If a matching record exists, return its primary key (tuple) immediately (no insertion).
#       2.1 If 'data' includes all primary key columns, check if a record already exists with that exact PK combination.
#           - If it exists, return that PK tuple immediately (no insertion).
#       3. If no matching record, proceed with the normal insertion.
#       4. Attempt to retrieve the primary key tuple:
#          - First try 'last_insert_rowid()'.
#          - If that fails (e.g., composite PK table), fall back to selecting the row by all PK columns in 'data'.
#       5. Return the tuple of primary key values for the newly inserted record, or None on failure.
#
#     Args:
#         table (str): The name of the table.
#         data (dict): A dictionary of column names and values to insert.
#
#     Returns:
#         tuple or None:
#             - A tuple containing the primary key column(s) values if inserted successfully
#               or if the record already exists (by unique or full-PK check).
#             - None if the insert failed or if no primary key columns were found.
#     """
#     database_name = DB_PATH
#
#     # 1. If no data is provided, return None
#     if not data:
#         print("No data provided to insert.")
#         print("none1")
#         return None
#
#     # Retrieve the primary key column names for the specified table
#     pk_columns = get_primary_key_column_names(table)
#     if not pk_columns:
#         print(f"No primary key defined or table '{table}' not recognized.")
#         print("none2")
#         return None
#
#     # 2. Check if the table has a UNIQUE column, and if our data includes a value for that column
#     unique_col = get_unique_column_name(table)
#     if unique_col and (unique_col in data):
#         unique_val = data[unique_col]
#         try:
#             # Use a direct query or helper function to see if a row already exists by that UNIQUE column
#             with sqlite3.connect(database_name) as conn:
#                 cursor = conn.cursor()
#
#                 # Build the query to check if there's an existing record with this unique value
#                 pk_col_str = ", ".join(pk_columns)
#                 query = f"SELECT {pk_col_str} FROM {table} WHERE {unique_col} = ?"
#                 cursor.execute(query, (unique_val,))
#                 existing_pk_tuple = cursor.fetchone()
#
#                 if existing_pk_tuple:
#                     # If a record with this unique value already exists,
#                     # return the existing PK tuple without inserting a new record
#                     return existing_pk_tuple
#         except sqlite3.Error as e:
#             print(f"An error occurred while checking unique column existence: {e}")
#             return None
#
#     # 2.1. If data includes all PK columns, check if a record with that exact PK combination already exists
#     all_pk_in_data = all(pk_col in data for pk_col in pk_columns)
#     if all_pk_in_data:
#         try:
#             with sqlite3.connect(database_name) as conn:
#                 cursor = conn.cursor()
#
#                 # Build WHERE clause for all PK columns
#                 pk_col_str = ", ".join(pk_columns)
#                 where_clause = " AND ".join([f"{pk} = ?" for pk in pk_columns])
#                 select_query = f"SELECT {pk_col_str} FROM {table} WHERE {where_clause}"
#                 select_values = tuple(data[pk] for pk in pk_columns)
#
#                 cursor.execute(select_query, select_values)
#                 existing_pk_tuple = cursor.fetchone()
#                 if existing_pk_tuple:
#                     # If that PK combination is already present, return the PK tuple
#                     return existing_pk_tuple
#
#         except sqlite3.Error as e:
#             print(f"An error occurred while checking for existing PK combination: {e}")
#             return None
#
#     # 3. If no matching record (unique or composite PK), proceed with the normal insertion
#     with sqlite3.connect(database_name) as conn:
#         cursor = conn.cursor()
#
#         # Retrieve schema info and maintain the column order
#         cursor.execute(f"PRAGMA table_info({table});")
#         schema_info = cursor.fetchall()
#         column_order = [col_info[1] for col_info in schema_info]
#
#         # Construct the data to insert based on the table schema (in correct column order)
#         ordered_data = {col: data.get(col, None) for col in column_order if col in data}
#
#         # Build the INSERT statement
#         columns = ", ".join(ordered_data.keys())
#         placeholders = ", ".join(["?"] * len(ordered_data))
#         insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
#
#         try:
#             # Execute the INSERT query
#             cursor.execute(insert_query, list(ordered_data.values()))
#             conn.commit()
#
#             # 4. Retrieve the primary key values using last_insert_rowid()
#             #    (This works only if the table has a rowid or single integer PK.)
#             select_pk_query = f"SELECT {', '.join(pk_columns)} FROM {table} WHERE rowid = last_insert_rowid()"
#             cursor.execute(select_pk_query)
#             pk_values = cursor.fetchone()
#
#             # If last_insert_rowid() doesn't work, do a fallback using the PK columns
#             if pk_values is None and all_pk_in_data:
#                 # Build a WHERE clause from the PK columns
#                 where_clause = " AND ".join([f"{pk} = ?" for pk in pk_columns])
#                 fallback_query = f"SELECT {', '.join(pk_columns)} FROM {table} WHERE {where_clause}"
#                 fallback_values = tuple(data[pk] for pk in pk_columns)
#                 cursor.execute(fallback_query, fallback_values)
#                 pk_values = cursor.fetchone()
#
#             if pk_values is not None:
#                 print(f"Record added successfully to table '{table}'. PK: {pk_values}")
#                 return pk_values
#             else:
#                 print("Failed to retrieve primary key after insert.")
#                 print("none3")
#                 return None
#
#         except sqlite3.Error as e:
#             print(f"An error occurred while adding record: {e}")
#             print(f"The problem occurred while inserting into table '{table}'.")
#             print("Before the failure, the table’s data was:")
#             print("none4")
#             return None
#
# def update_record(table, data):
#     """
#     Update an existing record in the database.
#
#     Args:
#         table (str): The name of the table.
#         data (dict): A dictionary of column names and values to update.
#
#     Returns:
#         bool: True if the record was updated successfully, False otherwise.
#     """
#     database_name = 'my_database.db'
#     primary_key_values = {}
#     for key in get_primary_key_column_names(table):
#         primary_key_values[key] = data[key]
#
#     if not data or not primary_key_values:
#         print("No data or primary key values provided to update.")
#         return False
#
#     with sqlite3.connect(database_name) as conn:
#         cursor = conn.cursor()
#
#         # Get column order from the database schema
#         cursor.execute(f"PRAGMA table_info({table});")
#         schema_info = cursor.fetchall()
#         column_order = [column[1] for column in schema_info]
#
#         # Match data to the table schema
#         ordered_data = {col: data.get(col, None) for col in column_order if col in data}
#         ordered_primary_key_values = {col: primary_key_values[col] for col in primary_key_values if col in column_order}
#
#         # Prepare the primary key clause
#         primary_key_clause = ' AND '.join([f"{key} = ?" for key in ordered_primary_key_values.keys()])
#         primary_key_values_list = list(ordered_primary_key_values.values())
#
#         # Prepare the update clause
#         update_clause = ', '.join([f"{key} = ?" for key in ordered_data.keys()])
#         update_values = list(ordered_data.values())
#
#         update_query = f"UPDATE {table} SET {update_clause} WHERE {primary_key_clause}"
#
#         try:
#             cursor.execute(update_query, update_values + primary_key_values_list)
#             conn.commit()
#
#             if cursor.rowcount > 0:
#                 print(f"Record with primary key {primary_key_values_list} updated successfully.")
#                 return True
#             else:
#                 print(f"No record found with primary key {primary_key_values_list}.")
#                 return False
#         except sqlite3.Error as e:
#             print(f"An error occurred while updating record: {e}")
#             return False
#
# def delete_record(table, data):
#     """
#     Delete a record from the database using the primary key.
#
#     Args:
#         table (str): The name of the table.
#         data (dict): A dictionary containing only the primary key columns and their values.
#     """
#     if not data:
#         return
#     primary_key = get_primary_key_column_names(table)
#     with sqlite3.connect('../my_database.db') as conn:
#         cursor = conn.cursor()
#
#         # Build the WHERE clause for the primary key
#         primary_key_clause = ' AND '.join([f"{key} = ?" for key in primary_key])
#         primary_key_values = [data[key] for key in primary_key]
#
#         # Check if the record exists
#         check_query = f"SELECT 1 FROM {table} WHERE {primary_key_clause}"
#         cursor.execute(check_query, primary_key_values)
#         record_exists = cursor.fetchone() is not None
#
#         if record_exists:
#             # If the record exists, delete it
#             delete_query = f"DELETE FROM {table} WHERE {primary_key_clause}"
#             cursor.execute(delete_query, primary_key_values)
#             conn.commit()  # Commit the transaction
#             print(f"Record with primary key {primary_key_values} deleted successfully.")
#         else:
#             # If the record does not exist
#             print(f"Record with primary key {primary_key_values} does not exist in table '{table}'.")