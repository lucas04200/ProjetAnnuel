import numpy as np
import matplotlib.pyplot as plt
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor
import json

class Resumator():
    '''
    Wrapper of image object detectors.

    Args:
        model_name: str, currently only support 'rapid'
        weights_path: str, path to the pre-trained network weights
        model: torch.nn.Module, used only during training
        conf_thres: float, confidence threshold
        input_size: int, input resolution
    '''
    def __init__(self, model_name):
        # post-processing settings
        self.model_name = model_name
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)

    # Passer du json à des phrases concaténées
    def prepare_for_summary(self, conversations):
        prepared_texts = []
        for topic in conversations:
            # Concaténation des commentaires avec des espaces et une ponctuation appropriée.
            concatenated_comments = " ".join(comment for comment in topic["comments"])
            prepared_texts.append(f"{topic['topic']}: {concatenated_comments}")
        return prepared_texts

    def tokenize_text(self, text):
        return self.tokenizer.encode(" " + text, return_tensors="pt", max_length=1024, truncation=True, padding="max_length")
    
    # Tokenizer tous les textes dans un seul return
    def tokenize_func(self, prepared_texts):
        with ThreadPoolExecutor(max_workers=4) as executor:
            tokenized_texts = list(executor.map(self.tokenize_text, prepared_texts))
        return tokenized_texts

    # Générer un summary pour un seul token
    def generate_summary_from_tokens(self, tokenized_input):
        # Détermination du dispositif à utiliser (GPU si disponible, sinon CPU)
        summary_ids = self.model.generate(tokenized_input, max_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary_text = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary_text
    
    # Générer un summary pour tous les tokens et return les summaries
    def generate_summaries(self, tokenized_texts):
        # Génération des résumés à partir des textes tokenisés
        with ThreadPoolExecutor(max_workers=4) as executor:
            summaries = list(executor.map(self.generate_summary_from_tokens, tokenized_texts))
        return summaries

    