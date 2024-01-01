
from pdf.processing import PdfProcessor
from pdf.anonymizer import Anonymizer
from chatbot.chatbot import ChatBot

anonymizer = Anonymizer()
chatbot = ChatBot()

direc = "./research/pdfs/"
file_paths = ["samplecv.pdf"]
i = 0

for file_path in file_paths:
    i = i + 1
    processor = PdfProcessor(direc + file_path)
    fText = processor.scrap_text()
    fText = anonymizer.anonymize_text(fText)
    pure_response = chatbot.get_pure(fText)

    with open(f"./research/data/scrap{i}.txt", 'w') as file:
        file.write(fText)
    
    with open(f"./research/data/res{i}.txt", 'w') as file:
        file.write(pure_response)