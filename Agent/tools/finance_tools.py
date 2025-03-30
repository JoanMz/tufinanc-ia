def get_user_spend(user_email: str, db_connection: object) -> float:
   """
   Get the total spending of a user from the database.
   Args:
       user_email (str): The email of the user.
       db_connection: The database connection object.
       Returns:
       float: The total spending of the user.
   """
   with db_connection.connection() as conn:
      spending = conn.execute(
         """
         SELECT 
         u.id AS user_id, 
         u.name_, 
         u.last_name,
         u.email,
         COALESCE(SUM(s.amount), 0) AS total_spent,
         COALESCE(SUM(d.current_payment), 0) AS total_debts_paid,
         COALESCE(SUM(s.amount), 0) + COALESCE(SUM(d.current_payment), 0) AS total_expenses
         FROM financelive.users u
         LEFT JOIN financelive.spendings s ON u.id = s.user_id
         LEFT JOIN financelive.debts d ON u.id = d.user_id
         WHERE u.email = %s
         GROUP BY u.id, u.name_, u.last_name, u.email;
         
         """,
         (user_email, )
      )
      result = spending.fetchone()
      if result:
         total_spent = result[4] or 0
         total_debts_paid = result[5] or 0
         total_expenses = result[6] or 0
         return {
            "total_spent": total_spent,
            "total_debts_paid": total_debts_paid,
            "total_expenses": total_expenses
         }
      else:
         return {
            "total_spent": 0,
            "total_debts_paid": 0,
            "total_expenses": 0
         }
    

