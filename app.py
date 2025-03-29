import os

from src.db_pool import supa_pool 

from fastapi import FastAPI
 


def lifespan(app: FastAPI):
    db_url = os.getenv("DATABASE_URL")
    pool = supa_pool(db_url)
    yield pool
    pool.close()


pool = 

app = FastAPI()