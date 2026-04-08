import discord
from discord.ext import commands
import json

ARQUIVO_PRODUTOS = "produtos.json"

class Produto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="produto", invoke_without_command=True)
    async def produto(self, ctx):
        await ctx.send("Use um subcomando: `info`, `editar`, `listar`")

    # Comando: !produto info <nome>
    @produto.command(name="info")
    async def produto_info(self, ctx: commands.Context, *, nome: str):
        # Carrega os produtos do JSON
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        produto = next((p for p in dados["produtos"] if p["nome"].lower() == nome.lower()), None)
        if not produto:
            await ctx.send(f"❌ Produto **{nome}** não encontrado.")
            return

        # Cria embed com os detalhes do produto
        embed = discord.Embed(
            title=f"📦 {produto['nome']}",
            description=produto["descricao"],
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Preço", value=f"R${produto['preco']}", inline=False)

        await ctx.send(embed=embed)
