
from pdf.processing import PdfProcessor
from pdf.anonymizer import Anonymizer
from chatbot.chatbot import ChatBot
import os

anonymizer = Anonymizer()
chatbot = ChatBot()

direc = "./research/pdfs/"
i = 0

for file_path in os.listdir(direc):
    if file_path.endswith('.pdf'):
        i = i + 1
        processor = PdfProcessor(direc + file_path)
        fText = processor.scrap_text()
        fText = anonymizer.anonymize_text(fText)
        pure_response = chatbot.get_pure(fText)

        with open(f"./research/data/scrap{i}.txt", 'w', encoding='utf-8') as file:
            file.write(fText)
        
        with open(f"./research/data/res{i}.txt", 'w', encoding='utf-8') as file:
            file.write(pure_response)

        print(f"Finished itertation {i}")