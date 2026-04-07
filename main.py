import config
from discord.ext import commands
import discord 

class MeuBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
    
    async def setup_hook(self):
        await self.load_extension("cogs.ping")
        await self.tree.sync()
        print("comandos de barra sincronizados com sucesso")
    
    async def on_ready(self):
        print(f'Bot online e logado como {self.user}')

bot = MeuBot()

if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)