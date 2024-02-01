from dotenv import load_dotenv
from src.processings.document_processing import document2text
from src.neuro.gpt import GPT
import os

load_dotenv()

api_key = os.environ['OPENAI_API_KEY']
gpt = GPT(api_key=api_key,
          model="gpt-3.5-turbo")


def summarize_file(filename):
    text = document2text(filename)
    text = text.replace('HYPERLINK', '')
    text = text.replace('_', '')
    text = ' '.join(text.split())
    text = gpt.summarize(text)
    return text
