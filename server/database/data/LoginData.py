# from database.data.BaseData import BaseData
# from datetime import datetime


# class LoginData(BaseData):
#     def __init__(self):
#         self.table_name = 'users'
#         super().__init__()

#     def get_encrypted_password(self, username: str):
#         try:
#             self.cursor.execute(
#                 f"SELECT password FROM {self.table_name} WHERE username = ?", (username,))
#             row = self.cursor.fetchone()
#             if row is not None:
#                 return row['password']
#             return None
#         except Exception as e:
#             raise Exception(
#                 f"Unable to get password for username {username}: {e}")

#     def is_username_available(self, username: str):
#         try:
#             self.cursor.execute(
#                 f"SELECT COUNT(*) FROM {self.table_name} WHERE username = ?", (username,))
#             count = self.cursor.fetchone()[0]
#             return count == 0
#         except Exception as e:
#             raise Exception(
#                 f"Unable to check if username exists: {e}")

#     def create_user(self, username, hashed_password: str):

#         try:
#             current_time_utc = datetime.utcnow().isoformat()
#             self.cursor.execute(f"INSERT INTO {self.table_name} (username, password, created_at_utc, updated_at_utc) VALUES (?, ?, ?, ?)",
#                                 (username, hashed_password, current_time_utc, current_time_utc))
#             self.conn.commit()

#             print("User created successfully")
#         except Exception as e:
#             print("Error:", e)

#     def view_table(self):
#         try:
#             self.cursor.execute(f"SELECT * FROM {self.table_name}")
#             rows = self.cursor.fetchall()
#             return rows
#         except Exception as e:
#             raise Exception(f"Unable to select all users: {e}")
