import discord
from discord.ext import commands
import os
import datetime

ARQUIVO_PRODUTOS = "database/produtos.json"

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="backup")
    @commands.has_permissions(administrator=True)
    async def backup(self, ctx):
        if not os.path.exists(ARQUIVO_PRODUTOS):
            return await ctx.send("❌ Arquivo de produtos não encontrado.")

        # Nome do backup com data e hora
        data = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nome_backup = f"backup_produtos_{data}.json"

        # criar o backup
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            conteudo = f.read()

        with open(nome_backup, "w", encoding="utf-8") as f:
            f.write(conteudo)

        # Enviar arquivo
        await ctx.send(
            f"✅ Backup realizado com sucesso!",
            file=discord.File(nome_backup)
        )

# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Backup(bot))