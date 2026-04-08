import config
from discord.ext import commands
import discord
import traceback
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True


class MeuBot(commands.Bot):
    def __init__(self):
        # Aqui definimos o prefixo que o bot vai ouvir. Neste caso, o "!"
        super().__init__(command_prefix="ps!", intents=intents, help_command=None)

    async def setup_hook(self):
        cogs_dir = Path("cogs")

        for file in cogs_dir.rglob("*.py"):
            if file.name == "__init__.py":
                continue

            module_name = ".".join(file.with_suffix("").parts)

            try:
                await self.load_extension(module_name)
                print(f"[+] Extensão carregada: {module_name}")
            except Exception as e:
                print(f"[-] Erro ao carregar a extensão {module_name}: {e}")
                traceback.print_exc()

        # Removemos toda a parte de self.tree.sync(). Não é mais necessário!
        print("Cogs carregados. Pronto para receber comandos de prefixo!")

    async def on_ready(self):
        print(f"Bot online e logado como {self.user}")
        await self.change_presence(activity=discord.Game(name="!help"))



bot = MeuBot()

if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
