from fastapi import (FastAPI, File, HTTPException, UploadFile, WebSocket,WebSocketDisconnect)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging
from contextlib import asynccontextmanager
import traceback
import os
import pandas as pd
from src.bot import CustomChatBot
from random import randint

#INDEX_DATA = bool(int(os.environ["INDEX_DATA"]))
INDEX_DATA = True

# Set up logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager to ensure CustomChatBot is initialized and cleaned up correctly.
    """
    logger.info("Creating instance of custom chatbot.")
    logger.info(f"Index data to vector store: {INDEX_DATA}")
    app.state.chatbot = CustomChatBot(index_data = INDEX_DATA)
    try:
        yield #"Inne halten"
    finally:
        logger.info("Cleaning up chatbot instance.")
        del app.state.chatbot

# Create FastAPI app and configure CORS
app = FastAPI(lifespan = lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # Adjust to restrict domains in production
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class CollectionRequest(BaseModel):
    collection_name: str

# Dateien Hochladen: _________________________________________________________________________
@app.post("/upload_PDF")
async def upload_PDF(file: UploadFile = File(...)):
    upload_dir = "pdfs"
    try:
        os.makedirs(upload_dir, exist_ok = True)

        filename = file.filename or "default.pdf"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        app.state.chatbot.set_vector_db_collection(filename)

        if True:
            logger.debug("Lade Datei in Vector DB...")
            app.state.chatbot.index_file_to_vector_db(file_path)
        return JSONResponse(content={"message": f"Datei '{filename}' erfolgreich hochgeladen!"})
        
        
    except Exception as e:
         return JSONResponse(status_code=500, content={"message": "Fehler beim Hochladen", "error": str(e)})
# __________________________________________________________________________________________

@app.get("/get_collections")
def get_collections():
    collections = app.state.chatbot.get_vector_db_collections()
    return collections


@app.get("/get_current_collection")
def get_current_collection():
    collection = app.state.chatbot.get_current_collection()
    return CollectionRequest(collection_name= collection)


@app.post("/set_collection")
def set_collection(request: CollectionRequest):
    # Setzen der Collection die verwendet werden soll (VectorDB neu initialisieren mit neuer collection)
    collection_name = request.collection_name
    app.state.chatbot.set_vector_db_collection(collection_name)
    return {"message": f"Collection {collection_name} ausgewählt"}

@app.put("/delete_collection")
def delete_collection(collection_name: str):
    result = app.state.chatbot.delete_collection(collection_name)
    return result

# _________________________________________________________________________________________

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that handles communication with the client.
    """
    await websocket.accept()
    logger.info('Client connected.')

    try:
        while True:
            try:
                # Receive input from the WebSocket client
                input_data = await websocket.receive_text()
                logger.info(f"Received input: {input_data}")

                # Process the input using the chatbot's stream_answer method
                async for chunk in app.state.chatbot.astream(input_data):
                    chain_result = chunk
                    logger.info(f"Sending chunk: {chain_result}")
                    # Send the response chunk back to the client
                    await websocket.send_text(chain_result)

            except WebSocketDisconnect:
                # Graceful handling of WebSocket disconnection
                logger.info("Client disconnected.")
                break

            except Exception as e:
                # Handle unexpected errors during input processing
                logger.error(f"Error processing chatbot response: {str(e)}")
                logger.error(traceback.format_exc())
                await websocket.send_text(f"Error: {str(e)}")
                break

    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        logger.info('WebSocket connection closed.')

if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run("main:app", host = "backend", port = 5001, reload = True, log_level = "debug")

@app.get("/Fragen")
def getFrage():
    app.state.chatbot.fragen_erstellen()
    return app.state.chatbot.Fragen

@app.get("/Antwort")
def überprüfeAntwort(antwort:str):
    chunk = app.state.chatbot.Fragen[app.state.chatbot.Fragen['Frage']==lastquestion]['Chunk']
    thema = app.state.chatbot.Fragen[app.state.chatbot.Fragen['Frage']==lastquestion]['Thema']
    überprüfung = app.state.chatbot.antwort_überprüfen(lastquestion,antwort,chunk)
    überprüfung = überprüfung.lower()
    
    if überprüfung=="richtig":
        app.state.chatbot.statistic[app.state.chatbot.statistic['Thema']== thema]['Frage Anzahl'] +=1 
        app.state.chatbot.statistic[app.state.chatbot.statistic['Thema']== thema]['Frage richtig'] +=1 
        return "korrekte Antwort"
    elif überprüfung =="falsch":
        app.state.chatbot.statistic[app.state.chatbot.statistic['Thema']== thema]['Frage Anzahl'] +=1 
        return "falsche Antwort"
    else:
        return "unerwartete Antwort"


lastquestion = ""
@app.get("/nächsteFrage")
def nextQuestion():
    logger.info('nächste Frage wird ausgewählt')
    app.state.chatbot.statistic['richtig Prozent'] = app.state.chatbot.statistic['Frage richtig']/app.state.chatbot.statistic['Frage Anzahl']*100
    thema = app.state.chatbot.statistic[app.state.chatbot.statistic['richtig Prozent'].idxmin()]['thema']
    questions = app.state.chatbot.Fragen[app.state.chatbot.Fragen['Thema']==thema]['Frage']
    question = questions[randint(0,len(questions))]
    lastquestion = question
    return question

@app.get("/Statistik")
def getStatistik():
    return app.state.chatbot.statistic

@app.get("/Zusammenfassung")
def getZusammenfassung():
    zusammenfassung = app.state.chatbot.zusammenfassung_erstellen()
    logger.info("Zusammenfassung erstelllt")
    return zusammenfassung