
from typing import Union

from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Frage(BaseModel):
    frage: str
    thema: str
    antwort: str
    ist_beantwortet: bool
    antwort_richtig: bool



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/fragen/beantworten")
def fragen_beantworten():
    #code für Frage auswahl
    return {Frage.frage}

@app.put("fragen/beantworten")
def antwort_bekommen(Frage):
    #code für Antwort verarbeiten
    return 200

@app.get("/frage/stellen")
def frage_stellen():
    #
    return Frage.antwort

@app.get("/statistik/{thema}")
def get_statistik():
    #
    return {}

@app.get("/skript/zusammenfassen")
def skript_zusammenfassen():
    #Zusammenfassen
    return "zusammenfassung"

@app.post("/uploadfile")
async def create_upload_file(UploadFile):
    #File upload
    return 200
    


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run("chatbot:app", host="0.0.0.0", port=5001, reload=True, log_level="debug")


