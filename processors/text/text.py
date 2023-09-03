"""
Text Augmentation
"""
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


class FileErrorException(Exception):
    pass

class TextFileContent:

    def __init__(self):
        self.is_writeable = True
        self.content = []

    def add_content(self, line):
        self.content.append(line)

    def write_to_file(self, filename):
        self.filename = filename
        with open(filename, 'w') as textfile:
            for line in self.content:
                textfile.writeline(line)

    def get_download_link(self):
         return f'<a href="data:text/plain;charset=utf-8,{self.filename}" download="augmented_text.txt">Click here to download</a>'

class TextProcessGenerator:
    def __init__(self):
        self.generators = []

    def add(self, text_generator):
        self.generators.append(text_generator)

    def __iter__(self):
        return (gen for gen in self.generators)


class TextProcessor:


    def __init__(self, uploaded_file=None, augmented_text_path="augmented_text.txt"):
        self.text_file = uploaded_file
        self.processes = TextProcessGenerator()
        self.destination = augmented_text_path

    @property
    def lines(self):
        if self.text_file == None:
            raise FileErrorException(
                "TextProcessor has no `text_file` attribute, use the add_file to add a text file"
            )
        for line in self.text_file.read().decode('utf-8'):
            yield line

    def add_process(self, process):
        self.processes.add(process(self.lines))
    
    def register_processes(self, processes):
        for process in processes:
            self.add_process(process)
   

    def add_file(self, text_file):
        self.text_file = text_file

    def run_augmentation(self):
        result = TextFileContent()
        for line_generator in self.processes:
            for line in line_generator:
                result.add_content(line)
        result.write_to_file(self.destination)
        return result
