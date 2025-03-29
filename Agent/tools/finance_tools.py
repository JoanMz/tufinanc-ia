from psycopg import sql

def get_user_spending(user_email, db_connection):
   with db_connection.connection() as conn:
      spending = conn.execute(
         "SELECT amount FROM "
      )
    