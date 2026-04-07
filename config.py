import os 
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("O DISCORD_TOKEN não foi encontrado no arquivo .env!")
