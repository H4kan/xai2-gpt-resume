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


class ChatBot:
    def __init__(self):
        self.client = ""

    def get_highlights(self, resume_text):
        return [
            {
              'page_num': 0,
              'text': 'Zainteresowania',
              'occurence': 1,
              'highlight': 'Jakas uwaga'
            },
            {
              'page_num': 0,
              'text': 'Anime',
              'occurence': 2,
              'highlight': 'Jakas uwaga 2'
            },
            {
              'page_num': 0,
              'text': 'Teoria grafów',
              'occurence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 1,
              'text': 'coś',
              'occurence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 1,
              'text': 'cośn',
              'occurence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 3,
              'text': 'Anime',
              'occurence': 1,
              'highlight': 'Jakas uwaga 3'
            },
            {
              'page_num': 0,
              'text': 'Anime',
              'occurence': 5,
              'highlight': 'Jakas uwaga 3'
            },
        ]