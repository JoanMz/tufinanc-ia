#from psycopg_pool import ConnectionPool
from supabase import create_client
from psycopg_pool import ConnectionPool

class supa_pool:
    def __init__(self, db_url):
        self.pool = ConnectionPool(db_url, max_size=10)

