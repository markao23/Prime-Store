import discord
from discord.ext import commands
import json
import os

ARQUIVO_PRODUTOS = "produtos.json"

class EstoqueBaixar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="baixar")
    @commands.has_permissions(administrator=True)
    async def baixar(self, ctx):
        if not os.path.exists(ARQUIVO_PRODUTOS):
            return await ctx.send("❌ Arquivo de produtos não encontrado.")

        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        linhas = []
        for produto in dados["produtos"]:
            linhas.append(
                f"Produto: {produto['nome']}\n"
                f"Preço: R${produto['preco']}\n"
                f"Estoque: {produto['estoque']}\n"
                f"Descrição: {produto['descricao']}\n"
                f"{'-'*30}"
            )

        conteudo = "\n".join(linhas)

        nome_arquivo = "estoque.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

        await ctx.send(
            "📦 Aqui está o estoque atual:",
            file=discord.File(nome_arquivo)
        )

# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(EstoqueBaixar(bot))