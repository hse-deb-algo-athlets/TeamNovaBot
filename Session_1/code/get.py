from typing import Union 
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

#@app.get("/")
#def read_root():
    #return {"Hello": "World"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
    #return {"item_id": item_id, "q": q}

class Frage(BaseModel):
    frage: str
    thema: str
    antwort: str
    ist_beantwortrt: bool
    antwort_check: bool

@app.get("/fragen/beantworten") # user sicht
def frage_beantworten():
    # Code für Fragenauswahl
    return(Frage.frage)

@app.put("/fragen/beantworten")
def antwort_bekommen(Frage):
    # Code für verarbeitung von Antwort
    return 200

@app.get("/frage/gestellt/")
def frage_gestellt_bekommen():
    # Code für Frage beantworten
    return(Frage.antwort)

@app.get("/statistik/{thema}")
def statistik_all():
    # Code für Statistik
        # allgemein Richtig/Falsch (Kuchendiagramm)
        # themenspezifisch Richtig/Falsch (Liste)
            # welche Fragen wie oft richtig/falsch
    return

@app.get("skript/zusammenfassen/")
def zm_skript():
    # Code für zusammenfassung Skript
    return # ZM-Skript

@app.post("/PDF/Laden/")
async def create_upload_file(file: UploadFile):
    # PDF File Upload
    return {"filename": file.filename}