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



with gr.Blocks() as demo:
    #collections = get_collections()
    with gr.Row(equal_height = True):
        with gr.Column(scale = 4):
            head_line = gr.Markdown("# Nova ChatBot")
            auswahl_PDF = gr.Dropdown(label = "PDF Auswahl",
                                    info = "PDF für Kontext auswählen",
                                    choices = ["Hallo", "Bye"],
                                    #value = collections[0] if collections else None,
                                    interactive = True,
                                    min_width = 1000
                                    )
        with gr.Column(scale = 1):
            chatbot_picture = gr.Image(value = "/workspaces/TeamNovaBot/Session_5/chatbot_task/frontend/Bilder/HeadPic.jpeg", 
                                       width = 150,
                                       #container = False,
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
                chat_fenster = gr.Chatbot(height = 300)
                text_fenster = gr.Textbox()
                with gr.Row():
                    butto_generait = gr.Button("Fragen generieren", )
                    button_new = gr.Button("Ein neue Frage stellen")
                    
                    # Button klicken
                    butto_generait.click()
                    button_new.click()

        # Statistikmodus
            with gr.Tab("Statistik"): 
                with gr.Row():
                    st = gr.BarPlot(stats, x = "Bewertung", y = "Anzahl", color = "Bewertung",
                    color_map = {"Korrekt": "#75ff33", "Falsch": "#FF5733"})
                button_stat = gr.Button("Statistik laden")
                button_stat.click()

        # Verwaltungsmodus
            with gr.Tab("Verwaltung"):
                with gr.Row():
                    button_delete = gr.Button("Liste löschen")
                    button_del_one = gr.Button("Einfach Löschen")
                    output = gr.List(label = "Hochgeladenen Dateien: ", value = uploaded_files)

                    # Button Klick
                    button_delete.click()
                    button_del_one.click()
            
            #demo.load(update_dropdown, outputs = auswahl_PDF)
    demo.launch(debug = True)