# import os

# os.environ["OPENAI_API_KEY"] = "api-key"

# from openai import OpenAI
# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", 
#          "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", 
#          "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)

import time

class ChatBot:
    def __init__(self):
        self.client = ""

    def get_highlights(self, resume_text):
        time.sleep(5)
        return [
            {
              'page_num': 1,
              'text': 'Zainteresowania',
              'occurrence': 1,
              'highlight': 'Jakas uwaga'
            },
            {
              'page_num': 1,
              'text': 'Anime',
              'occurrence': 2,
              'highlight': 'Jakas uwaga 2'
            },
            {
              'page_num': 1,
              'text': 'Teoria grafów',
              'occurrence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 2,
              'text': 'coś',
              'occurrence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 2,
              'text': 'cośn',
              'occurrence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 4,
              'text': 'Anime',
              'occurrence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 1,
              'text': 'Anime',
              'occurrence': 5,
              'highlight': 'Jakas uwaga 3'
            },
        ]