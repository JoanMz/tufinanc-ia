#from psycopg_pool import ConnectionPool
from psycopg_pool import ConnectionPool

class supa_pool:
    def __init__(self, db_url):
        self.pool = ConnectionPool(db_url, max_size=10)

    def get_spent_by_date(self, user_email, date):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                result = cur.execute(
                    "SELECT * FROM spent WHERE user_email = %s AND date = %s",
                    (user_email, date),
                )
                data = result.fetchall()
                return data
