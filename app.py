import os
from src.db_pool import supa_pool
from Agent.finance_agent import run_agent
from Agent.graph import graph
from Agent.tools import finance_tools
from fastapi import (FastAPI,
                     Request,
                     Response,
                     Depends)
from backend.tts.elevenlabs_client import ElevenLabsTTSClient
eleven_client = ElevenLabsTTSClient()
# import backend.


db_url = os.getenv("SUPABASE_CONECTION_URL")
pool = supa_pool(db_url).pool
finance_tools.db_connection = pool
print("Database connection pool created")


app = FastAPI()


@app.get("/")
def alive_check():
    return {"status": "alive"}


@app.post("/spent/voice")
def spent_voice(request: dict) -> bytes:
    email: str = request["email"]
    message: dict = request["message"]
    print("email: ", email)
    print("message: ", message)
    #response = run_agent(message, email).content
    response = call_graph(message, email)["llm_response"]
    print("\n\n\n", response)
    audiob, err = eleven_client.text_to_speech(response, "21m00Tcm4TlvDq8ikWAM", "eleven_multilingual_v2")

    #return Response(content=response, media_type="application/json", status_code=200)
    # return Response(content=audiob.getvalue(), media_type="audio/mpeg", status_code=200)
    if audiob is None:
       return Response(status_code=403)
    return Response(content=audiob.getvalue(), media_type="audio/wav", status_code=200)


@app.post("/month/analysis/voice")
def month_analysis_voice(request: Request):
  pass


def call_graph(messages, email: str):
   response = graph.invoke({"messages": [{"role": "user", "content": messages + f"   user_email:{email} "}], "email": email})
   return response
   