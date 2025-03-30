import os
from contextlib import contextmanager
from src.db_pool import supa_pool
from Agent.finance_agent import FinanceAgent
from fastapi import (FastAPI,
                     Request,
                     Response,
                     Depends)



@contextmanager
def lifespan(app: FastAPI):
    db_url = os.getenv("DATABASE_URL")
    app.state.pool = supa_pool(db_url)
    print("Database connection pool created")
    yield 
    app.state.pool.close()

def get_pool():
    """
    Get the database connection pool from the FastAPI app state.
    Returns:
        object: The database connection pool.
    """
    return app.state.pool

app = FastAPI(lifespan=lifespan)
finance_agent = FinanceAgent(get_pool())


@app.get("/")
def alive_check():
    return {"status": "alive"}


@app.post("/spent/voice")
def spent_voice(request: Request):
    form = request.form()
    email = form.get("email")
    message = form.get("message")
    response = finance_agent.run_agent(message, email)
    print(response)
    return Response(content=response, media_type="application/json", status_code=200)



