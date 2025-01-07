import gradio as gr
import websockets
import logging

import os
import pandas as pd
import requests

# Datenabfrage aus ChromaDB
def get_collections():
    p1 = ["Technische Datenerfassung","Technische Informatik","Produktentwicklung"]
    return p1

def chat_great(message):
    return "Hallo"+ message

uploaded_files = []

def upload_file(file):
    # Erstelle einen DataFrame mit den Dateidetails
    filename, file_extension = os.path.splitext(file.name)
    filename = os.path.basename(filename)
    df = pd.DataFrame({'Dateiname': [filename], 'Upload-Datum': [pd.Timestamp.now()]})
    uploaded_files.append(df)

    all_files_df = pd.concat(uploaded_files, ignore_index = True)
    return all_files_df

def set_collection():
    c = 0

# Das Auswahlfenster neu laden:
def update_dropdown(selected_collection = None):
    """
    Aktualisiere das Dropdown-Menü 
    mit neuen Collections und optional 
    einer vorausgewählten Collection.
    """
    if selected_collection == None:
        curr_collection = requests.get("get_current_collection")
        name = curr_collection.json()['collection_name']
        selected_collection = name
        
    new_choices = get_collections()
    selected_value = selected_collection if selected_collection else (new_choices[0] if new_choices else None)
    
    return gr.Dropdown(choices = new_choices, value = selected_value)

#Platzhalter
stats = pd.DataFrame(
  {
    "Bewertung": ["Korrekt", "Falsch"],
    "Anzahl": [80, 47]
  }
)

def fragen_generieren():
    frage = "Wie geht es dir?"
    return frage

def delete_collection(selected_collection:str):
    try:
        #url = base_url + "delete_collection"
        
        data = {"collection_name": selected_collection}

        #response = requests.put(url, json=data)
        #response.raise_for_status()
        #logger.info(f"Collection {selected_collection} gelöscht")
        gr.Info(f"Collection {selected_collection} gelöscht")
        return True
    except:
        gr.Warning(f"Fehler beim Löschen von {selected_collection}")
        return False


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
with gr.Blocks() as demo:
    collections = get_collections()

    collections_state = gr.State(collections) #State um Collections zu speichern, bei Änderung wird Verwaltung neu gerendert
    #logger.info(f"Collections: {collections}, collection state {collections_state}")

    with gr.Row(equal_height = True):
        with gr.Column(scale = 4):
            head_line = gr.Markdown("# Nova ChatBot")
            auswahl_PDF = gr.Dropdown(label = "PDF Auswahl",
                                    info = "PDF für Kontext auswählen",
                                    choices = get_collections(),
                                    #value = collections[0] if collections else None,
                                    interactive = True,
                                    min_width = 1000
                                    )
        with gr.Column(scale = 1):
            chatbot_picture = gr.Image(value = "/workspaces/TeamNovaBot/Session_5/chatbot_task/frontend/Bilder/HeadPic.jpeg", 
                                       width = 150,
                                       container = False,
                                       show_fullscreen_button = False, 
                                       show_download_button = False)

    with gr.Row():
        with gr.Column():
        # ChatBot fenster
            with gr.Tab("Chatbot"): 
                gr.ChatInterface(
                    fn = chat_great,
                    chatbot = gr.Chatbot(height = 500),  # Adjusted height for better usability
                    #textbox = gr.Textbox(placeholder = "Frag mich etwas über dein Script...", container = False, scale = 3),
                    theme = "soft",
                    examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
                )

        # Liste der hochgeladenen PDF Dateien
            with gr.Tab("PDF-Bibliothek"): 
                upload_button = gr.UploadButton("Datei hinzufügen", file_types = [".pdf"], file_count = "single")
                output = gr.List(label = "Hochgeladenen Dateien: ", value = uploaded_files)
                upload_button.upload(upload_file, inputs = upload_button, outputs = output)

        # Karteikartenmodus
            with gr.Tab("Karteikarten-Lernen"): 
                chat_fenster = gr.Chatbot(height = 300) 	                   # Chatfenster für Verlauf
                text_fenster = gr.Textbox(label = "Antwort: ")                 # Textfeld für Antwort
                
                with gr.Row():
                    butto_generait = gr.Button("Fragen generieren", )
                    button_new = gr.Button("Ein neue Frage stellen")
                    
                    # Button klicken
                    butto_generait.click(fragen_generieren, outputs = [chat_fenster])
                    button_new.click(fragen_generieren, outputs = [chat_fenster])

        # Statistikmodus
            with gr.Tab("Statistik"): 
                with gr.Row():
                    st = gr.BarPlot(stats, x = "Bewertung", y = "Anzahl", color = "Bewertung",
                    color_map = {"Korrekt": "#75ff33", "Falsch": "#FF5733"})
                button_stat = gr.Button("Statistik laden")
                button_stat.click()

        # Verwaltungsmodus
            with gr.Tab("Verwaltung"):
                @gr.render(inputs = collections_state)
                def render_collections(collections):
                    for collection in collections: # Für jede Collection wird ein Button erstellt
                
                        with gr.Row():
                            gr.Textbox(f"Collection {collection}", show_label = False, container = False)
                            delete_btn = gr.Button("Löschen", scale = 0, variant = "stop")

                        def delete(collection = collection):       
                            # Überprüfung ob Collection ohne Fehler gelöscht wurde, nur dann diese aus der Ansicht entfernen
                            if delete_collection(str(collection)): 
                                collections.remove(collection) # Collection aus State löschen damit neu gerendert wird

                            dropdown = update_dropdown()    # Dropdown aktualiseren
                            return collections, dropdown
                         
                        delete_btn.click(delete, None, [collections_state, auswahl_PDF])

                with gr.Row():
                    button_delete = gr.Button("Liste löschen")
  
                    # Button Klick
                    button_delete.click(delete_collection)

            
            #demo.load(update_dropdown, outputs = auswahl_PDF)
            #demo.load(get_collections, outputs = collections_state)
    demo.launch(debug = True)