import time
import os
from pdf.processing import PdfProcessor
from openai import OpenAI
import json

os.environ["OPENAI_API_KEY"] = "your-key"


max_attempts = 5

prompt_placeholder = '[$$$]'

data_format = [{"page_num": 1, "text": "", "occurrence": 1, "highlight": ""}, {"page_num": 1, "text": "", "occurrence": 1, "highlight": ""}, ...]

command_prompt = 'Point out parts of input that could be enchanced.\n' \
                 'Enhance the input to showcase the relevant education, experience, and skills in a professional manner to effectively demonstrate value to potential employers.\n'

output_commands_prompts = dict()
parsed_data_format = str(data_format).replace('\'', '"')
output_commands_prompts[
    'all'] = f'Return the output as dictionary in the next format {parsed_data_format}. \'text\' is substring of input addressed,\
 \'page_num\' is page number of addressed substring, \'occurence\' is which occurence of this substring it is on this page,\
 \'highlight\' is your comment on what could be improved. Output needs to be directly json parseable.'

input_prompt = f'Input is a text-scrapped PDF file, where each page is separated by string Page i.\n Input: {prompt_placeholder}'


def get_prompt(input_data):
    input_data = str(input_data)

    template = '\n'.join(
        [command_prompt,
          input_prompt.replace(prompt_placeholder, input_data), output_commands_prompts['all']])
    return template



class ChatBot:
    def __init__(self):
        self.client = ""
    def get_highlights(self, resume_text):
        
        i = 0
        while i < max_attempts:
            
          client = OpenAI()

          completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "system", 
                  "content": "You are a professional resume builder and a recruiter."},
              {"role": "user", 
                  "content": get_prompt(resume_text)}
            ]
          )
          # print(completion.choices[0].message.content)
          try:
            response = json.loads(completion.choices[0].message.content)
          except json.JSONDecodeError as e:
             i = i + 1
             continue
          print(f"ChatGPT completed in {i + 1} attempts")
          return response
        print(f"ChatGPT failed miserably")
        return [] 




    # def get_highlights(self, resume_text):
    #     time.sleep(5)
    #     return [
    #         {
    #           'page_num': 1,
    #           'text': 'Zainteresowania',
    #           'occurrence': 1,
    #           'highlight': 'Jakas uwaga'
    #         },
    #         {
    #           'page_num': 1,
    #           'text': 'Anime',
    #           'occurrence': 2,
    #           'highlight': 'Jakas uwaga 2'
    #         },
    #         {
    #           'page_num': 1,
    #           'text': 'Teoria grafów',
    #           'occurrence': 1,
    #           'highlight': 'Jakas uwaga 3'
    #         },
    #         {
    #           'page_num': 2,
    #           'text': 'coś',
    #           'occurrence': 1,
    #           'highlight': 'Jakas uwaga 3'
    #         },
    #         {
    #           'page_num': 2,
    #           'text': 'cośn',
    #           'occurrence': 1,
    #           'highlight': 'Jakas uwaga 3'
    #         },
    #         {
    #           'page_num': 4,
    #           'text': 'Anime',
    #           'occurrence': 1,
    #           'highlight': 'Jakas uwaga 3'
    #         },
    #         {
    #           'page_num': 1,
    #           'text': 'Anime',
    #           'occurrence': 5,
    #           'highlight': 'Jakas uwaga 3'
    #         },
    #     ]