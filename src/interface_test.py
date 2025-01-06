import gradio as gr
import websockets
import logging

import pandas as pd
import requests

# Datenabfrage aus ChromaDB
def get_collections():
    p1 = ["Technische Datenerfassung","Technische Informatik","Produktentwicklung"]
    return p1

def chat_great(message):
    return "Hallo"+ message

def pdf_upload():
    s = 0

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


with gr.Blocks() as demo:
    #collections = get_collections()
    skalierung = 150
    
    with gr.Row(equal_height = True):
        with gr.Column(scale = 1):
            chatbot_picture = gr.Image(value = "/workspaces/TeamNovaBot/Session_5/chatbot_task/frontend/Bilder/HeadPic.jpeg", 
                                       height = skalierung, 
                                       width = skalierung,
                                       container = False,
                                       show_fullscreen_button = False, 
                                       show_download_button = False)
        
        with gr.Column(scale = 1):
            head_line = gr.Markdown("# Nova ChatBot", height = "500px")
        
        with gr.Column(scale = 1):
            auswahl_PDF = gr.Dropdown(label = "PDF Bibliothek",
                                    info = "PDF für Kontext auswählen",
                                    choices = get_collections(),
                                    #value = collections[0] if collections else None,
                                    interactive = True,
                                    min_width = 50)

    with gr.Row():
        with gr.Column(scale = 6):
            with gr.Tab("Chatbot"): # ChatBot fenster
                chatbot = gr.Chatbot(height = 500)
                msg     = gr.Textbox(placeholder = "Frag mich etwas über dein Script...")
                clear   = gr.ClearButton([msg, chatbot])

                def respond(message, chat_history):
                    bot_message = chat_great(chat_history)
                    chat_history.append((message, bot_message))
                    return "", chat_history
                msg.submit(respond, [msg, chatbot], [msg, chatbot])

            with gr.Tab("PDF-Bibliothek"): # Liste der hochgeladenen PDF Dateien
                #liste = gr.List(value = get_collections)
                dropdown = gr.Dropdown(label = "PDF Bibliothek",
                            info = "PDF für Kontext auswählen",
                            choices = get_collections(),
                            #value = collections[0] if collections else None,
                            interactive = True)
                upload_button = gr.UploadButton("Datei hinzufügen", file_types = [".pdf"], file_count = "single")
        
                upload_button.upload(pdf_upload, inputs = upload_button, outputs = dropdown)
                dropdown.change(set_collection, inputs = dropdown)
            
            with gr.Tab("Karteikarten-Lernen"): # Karteikartenmodus
                with gr.Row():
                    butto_generait = gr.Button("Fragen generieren")
                    button_new = gr.Button("Ein neue Frage stellen")

            with gr.Tab("Statistik"): # Statistikmodus
                with gr.Row():
                    st = gr.BarPlot(stats, x = "Bewertung", y = "Anzahl", color = "Bewertung",
                    color_map={"Korrekt": "#75ff33", "Falsch": "#FF5733"})
                gr.Button("Statistik laden")

            with gr.Tab("Verwaltung"):  # Verwaltungsmodus
                gr.Button("Liste löschen")  
            
            demo.load(update_dropdown, outputs = dropdown)
    demo.launch(debug = True)