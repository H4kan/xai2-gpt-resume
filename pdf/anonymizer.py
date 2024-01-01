import spacy
import re

phone_number_regex = r'\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'

class Anonymizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def anonymize_text(self, text):

        doc = self.nlp(text)

        anonymized_text = text
        for ent in doc.ents:
            if not ent.text.startswith("Page "):
                anonymized_text = anonymized_text.replace(ent.text, "(REDACTED)")

        for token in doc:
            if token.like_email:
                anonymized_text = anonymized_text.replace(token.text, "(EMAIL REDACTED)")
            elif token.like_url:
                anonymized_text = anonymized_text.replace(token.text, "(URL REDACTED)")
            elif re.match(phone_number_regex, token.text):
                anonymized_text = anonymized_text.replace(token.text, "(PHONE REDACTED)")

        return anonymized_text
