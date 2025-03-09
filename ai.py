from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv('BASE_URL')
api_key = os.getenv('OPENAI_API_KEY') 



client = OpenAI(
  base_url = base_url,
 api_key = api_key
)



