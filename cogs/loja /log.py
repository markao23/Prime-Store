import discord
from discord.ext import commands
import json
import os

ARQUIVO_CONFIG = "config.json"

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="config", invoke_without_command=True)
    async def config(self, ctx):
        await ctx.send("Use: `ps!config logs #canal`")

    @config.command(name="logs")
    @commands.has_permissions(administrator=True)
    async def config_logs(self, ctx, canal: discord.TextChannel):
        # Criar arquivo se não existir
        if not os.path.exists(ARQUIVO_CONFIG):
            with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
                json.dump({"pix": "", "canal_logs": 0}, f, indent=4)

        # Carregar config
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Atualizar canal de logs
        dados["canal_logs"] = canal.id

        # Salvar
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        await ctx.send(f"✅ Canal de logs definido para {canal.mention}")

# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Config(bot))