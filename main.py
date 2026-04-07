import config
from discord.ext import commands
import discord 

class MeuBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
    
    async def setup_hook(self)