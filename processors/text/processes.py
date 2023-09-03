from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
from nltk.corpus import wordnet
import pandas as pd
import numpy as np
import random
import base64
import tempfile
import zipfile
import nltk
import shutil
import os


def augment_text(text, synonym_replacement_prob=0.1):
    words = text.split()
    augmented_words = []

    for word in words:
        if random.random() < synonym_replacement_prob:
            synonyms = wordnet.synsets(word)
            if synonyms:
                synonym = random.choice(synonyms).lemmas()[0].name()
                word = synonym
        augmented_words.append(word)

    augmented_text = " ".join(augmented_words)
    return augmented_text


def synonym_replacement(lines, synonym_replacement_prob=0.1):
    for line in lines:
        synonyms = wordnet.synsets(line)
        if synonyms:
            synonym = random.choice(synonyms).lemmas()[0].name()
            word = synonym


def english_to_german(line):
    # English to German using pipeline and T5
    translator_eng_to_ger = pipeline("translation_en_to_de", model="t5-base")
    eng_to_ger_output = translator_eng_to_ger(line)
    return eng_to_ger_output[0]["translation_text"]


def german_to_english(translated_text):
    # German to English using Bert2Bert model
    tokenizer = AutoTokenizer.from_pretrained(
        "google/bert2bert_L-24_wmt_de_en",
        pad_token="<pad>",
        eos_token="</s>",
        bos_token="<s>",
    )
    model_ger_to_eng = AutoModelForSeq2SeqLM.from_pretrained(
        "google/bert2bert_L-24_wmt_de_en"
    )

    input_ids = tokenizer(
        translated_text, return_tensors="pt", add_special_tokens=False
    ).input_ids
    output_ids = model_ger_to_eng.generate(input_ids)[0]
    return tokenizer.decode(output_ids, skip_special_tokens=True)



def back_translation(
    lines,
    english_to_language_translator=english_to_german,
    language_to_english_translator=german_to_english,
):
    for line in lines:
        translated_text = english_to_language_translator(line)
        augmented_line = language_to_english_translator(translated_text)
        yield line
