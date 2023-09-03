from .processes import synonym_replacement, back_translation
from .text import TextProcessor


textprocessor = TextProcessor()

process_list = [back_translation]

textprocessor.register_processes(process_list)