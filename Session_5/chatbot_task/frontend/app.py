import gradio as gr
import websockets
import logging

import pandas as pd
import requests

# Set up logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

base_url = "http://backend:5001/"

current_selected_collection = ""

# PDf hochladen:
def upload_pdf(path: str):
    
    if not path:
        gr.Warning(f"Keine Datei ausgewählt")   

    logger.info(f"Dateipfad: {path}")
    url = base_url + "upload_pdf"

    with open(path, "rb") as f:
        logger.info("Datei geladen")
        files = {"file": f}
        response = requests.post(url, files = files)

    logger.info(response.text)

    if response.status_code == 200:
        bib = get_collections()
        gr.Info(response.json()['message'])
        return  update_dropdown(), gr.List(label = "Die hochgeladenen Dateien sind: ", value = bib)
    else:
        gr.Warning(response.json()['message'])

# Datenabfrage aus ChromaDB
def get_collections():
    """
    Abfragen der Collections 
    die in der ChromaDB gespeichert sind.
    """
    try:
        url = base_url + "get_collections"
        response = requests.get(url)
        response.raise_for_status()

        collections = response.json()
        logger.debug(collections)
        return collections
    
    except Exception as e:
        gr.Warning(f"Fehler beim Collections laden: {e}")

# Aktuellen Datensatz festlegen
def set_collection(selected_collection: str):
    """
    Setzen der Collection, 
    die für die RAG Chain verwendet werden soll.
    """
    try:
        url = base_url + "set_collection"
        data = {"collection_name": selected_collection}

        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info(f"Collection {selected_collection} ausgewählt")
    except:
        gr.Warning(f"Fehler beim Setzen von {selected_collection}")

# WebSocket chat function (asynchronous generator)
async def websocket_chat(message: str):
    uri = "ws://backend:5001/ws"  # Ensure this URI is correct and accessible
    try:
        async with websockets.connect(uri) as websocket:
            logger.info(f"Sending message to WebSocket: {message}")
            await websocket.send(message)

            # Continuously receive and yield chunks until the connection is closed
            while True:
                try:
                    chunk = await websocket.recv()
                    logger.info(f"Received chunk: {chunk}")
                    yield chunk  # Yield each chunk as a separate message
                except websockets.exceptions.ConnectionClosed:
                    logger.info("WebSocket connection closed by the server.")
                    break
                except Exception as e:
                    logger.error(f"Error receiving chunk: {str(e)}")
                    yield f"Error: {str(e)}"
                    break
    except Exception as e:
        logger.error(f"Error during WebSocket communication: {str(e)}")
        yield f"Error: {str(e)}"

# Chat function to update the chatbot message history
async def chat(message: str, history = []):
    if not message.strip():
        yield "Please enter a valid question."
        return

    try:        
        # Stream chunks from WebSocket and append them incrementally
        bot_message = ""
        async for chunk in websocket_chat(message):
            bot_message += str(chunk)  # Accumulate chunks
            yield bot_message  # Yield updated history incrementally for display

    except Exception as e:
        message = f"Error: {e}"
        yield message

# Platzhalter
stats = pd.DataFrame(
  {
    "Bewertung": ["Korrekt", "Falsch"],
    "Anzahl": [80, 47]
  }
)

# Funktion Fragen generieren
def fragen_generieren():
    ...
    return questions()

# Antworten überprüfen
def check_antworten():
    ...
    return ...

# Funktion Generierte Fragen Speichern für Abfrage
def questions():
    ...
    return ...

# Funktion Löschen der Collection
def delete_collection(selected_collection:str):
    try:
        url = base_url + "delete_collection"
        
        data = {"collection_name": selected_collection}

        response = requests.put(url, json = data)
        response.raise_for_status()
        logger.info(f"Collection {selected_collection} gelöscht")
        gr.Info(f"Collection {selected_collection} gelöscht")
        return True
    except:
        gr.Warning(f"Fehler beim Löschen von {selected_collection}")
        return False

# Funktion Update Liste
def update_dropdown(selected_collection = None):
    """
    Aktualisiere das Dropdown-Menü mit neuen Collections und optional einer vorausgewählten Collection.
    """
    if selected_collection == None:
        curr_collection = requests.get(base_url + "get_current_collection")
        name = curr_collection.json()['collection_name']
        selected_collection = name
        
    new_choices = get_collections()
    selected_value = selected_collection if selected_collection else (new_choices[0] if new_choices else None)
    return gr.Dropdown(choices=new_choices, value=selected_value)

# Funktion Zusammenfassung generieren
def zusammenfassung():
    ...
    return ...

# ---------------------------------------------------------------------------------------------------------------------

with gr.Blocks() as demo:
    collections = get_collections()

    # State um Collections zu speichern, bei Änderung wird Verwaltung neu gerendert
    collections_state = gr.State(collections) 
    logger.info(f"Collections: {collections}, collection state {collections_state}")


    with gr.Row():      
        with gr.Column(scale = 4):
            head_line = gr.Markdown("# Nova ChatBot")
            auswahl_PDF = gr.Dropdown(label = "PDF Auswahl",
                                      info = "PDF für Kontext auswählen",
                                      choices = collections,
                                      value = collections[0] if collections else None,
                                      interactive = True,
                                      min_width = 50
                                     )
        with gr.Column(scale = 1):
            chatbot_picture = gr.Image(value = "Bilder/HeadPic.jpeg", 
                                       width = 150,
                                       container = False,
                                       show_fullscreen_button = False, 
                                       show_download_button = False
                                      )

    with gr.Row():
        with gr.Column(scale = 6):
        # ChatBot fenster
            with gr.Tab("Chatbot"): 
                gr.ChatInterface(
                                    fn = chat,
                                    chatbot = gr.Chatbot(height = 500),  # Adjusted height for better usability
                                    #textbox = gr.Textbox(placeholder = "Frag mich etwas über dein Script...", container = False, scale = 3),
                                    theme = "soft",
                                    examples = ["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                                )

        # Liste der hochgeladenen PDF Dateien
            with gr.Tab("PDF-Bibliothek"): 
                upload_button = gr.UploadButton("Datei hinzufügen", file_types = [".pdf"], file_count = "single")
                output = gr.List(label = "Die hochgeladenen Dateien sind: ", value = collections)
                upload_button.upload(upload_pdf, inputs = upload_button, outputs = [auswahl_PDF, output])

        # Karteikartenmodus
            with gr.Tab("Karteikarten-Lernen"): 
                chat_fenster = gr.ChatInterface(
                                                    fn = chat,
                                                    chatbot = gr.Chatbot(height = 500),  # Adjusted height for better usability
                                                    retry_btn = None,
                                                    undo_btn = None,
                                                    textbox = gr.Textbox(placeholder = "Wie lautet deine Antwort?", container = False, scale = 3),
                                                    theme = "soft",
                                                )
                
                with gr.Row():
                    butto_generait = gr.Button("Fragen generieren", )
                    button_new = gr.Button("Ein neue Frage stellen")
                    
                    # Button klicken
                    butto_generait.click(fragen_generieren, outputs = [chat_fenster])
                    button_new.click(fragen_generieren, outputs = [chat_fenster])

        # Statistikmodus
            with gr.Tab("Statistik"): 
                with gr.Row():
                    st = gr.BarPlot(
                                        stats, 
                                        x = "Bewertung", 
                                        y = "Anzahl", 
                                        color = "Bewertung",
                                        color_map={"Korrekt": "#75ff33", "Falsch": "#FF5733"}
                                    )
                gr.Button("Statistik laden").click()

        # Verwaltungsmodus
            with gr.Tab("Verwaltung"):
                @gr.render(inputs = collections_state)
                def render_collections(collections):
                    # Für jede Collection wird ein Button erstellt.
                    for collection in collections:
                        with gr.Row():
                            gr.Textbox(f"Collection {collection}", show_label = False, container = False)
                            delete_btn = gr.Button("Löschen", scale = 0, variant = "stop")

                        def delete(collection = collection):       
                            # Überprüfung ob Collection ohne Fehler gelöscht wurde, nur dann werden diese aus der Ansicht entfernen
                            if delete_collection(str(collection)): 
                                # Collection aus State löschen damit neu gerendert wird
                                collections.remove(collection) 

                            # Dropdown aktualiseren
                            dropdown = update_dropdown()    
                            return collections, dropdown
                         
                        delete_btn.click(delete, None, [collections_state, auswahl_PDF])

                with gr.Row():
                    button_delete = gr.Button("Liste löschen")
  
                    # Button Klick
                    button_delete.click(delete_collection)
                
            demo.load(update_dropdown, outputs = auswahl_PDF)
            demo.load(get_collections, outputs = collections_state)
demo.launch(debug = True)

# ---------------------------------------------------------------------------------------------------------------------

# Launch Gradio Chat Interface
"""
gr.ChatInterface(
    fn = chat,
    chatbot = gr.Chatbot(height = 400),  # Adjusted height for better usability
    textbox = gr.Textbox(placeholder = "Ask me questions about your script...", container = False, scale = 7),
    title = "NovaChatbot",
    description = "Ask me questions about your lecture.",
    theme = "soft",
    # Beispiel Fragen:
    examples = ["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
    # Button Fenster bereinigen:
    clear_btn = "Clear"
).launch(debug = True)"""