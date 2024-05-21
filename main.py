from services.html_parser import parse_html_to_text
from services.conv_to_resume import Resumator
import numpy as np
import matplotlib.pyplot as plt
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import json
import os

def single_conversation(file_path):
        file = open(file_path)
        conversation = json.load(file)
        return conversation

def seq_conversations(folder_path):
    conversations = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # Vérifier si le fichier est un fichier JSON
            file_path = os.path.join(folder_path, filename)  # Construire le chemin complet du fichier
            # Ouvrir et lire le fichier JSON
            with open(file_path) as file:
                conversations.append(json.load(file))
                # Traitement de l'objet JSON ici
    return conversations

def main():
    resumator = Resumator(model_name="facebook/bart-large-cnn")

    html_file_path = "conversations/ExploDeDonnee.html"
    formatted_conversation = parse_html_to_text(html_file_path)

    # Écrire la sortie dans un fichier texte
    output_file_path = "prepa-text/text.json"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(formatted_conversation)

    # print(f"Le résultat a été écrit dans le fichier '{output_file_path}'")
    text_json = seq_conversations("./prepa-text/")
    prepared_text = resumator.prepare_for_summary(text_json)
    tokenized_text = resumator.tokenize_func(prepared_text)
    summaries = resumator.generate_summaries(tokenized_text)
    print(summaries)

if __name__ == "__main__":
    main()
 