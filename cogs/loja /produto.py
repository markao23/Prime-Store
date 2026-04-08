import discord
from discord.ext import commands
import json

ARQUIVO_PRODUTOS = "produtos.json"

class Produto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="produto", invoke_without_command=True)
    async def produto(self, ctx: commands.Context):
        await ctx.send("Use um subcomando: `editar`, `listar`")

    # Subcomando: !produto editar <nome> <novo_nome> <novo_preco> <nova_descricao>
    @produto.command(name="editar")
    async def produto_editar(self, ctx: commands.Context, nome: str, novo_nome: str, novo_preco: float, *, nova_descricao: str):
        """
        Edita um produto existente no JSON
        Exemplo: 
        !produto edita "Bot Moderador" "Bot Admin" 55 "Bot atualizado com mais comandos"
        """
        # Carrega os produtos
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Procura o produto
        produto = next((p for p in dados["produtos"] if p["nome"].lower() == nome.lower()), None)
        if not produto:
            await ctx.send(f"❌ Produto **{nome}** não encontrado.")
            return

        # Atualiza os dados
        produto["nome"] = novo_nome
        produto["preco"] = novo_preco
        produto["descricao"] = nova_descricao

        # Salva de volta no JSON
        with open(ARQUIVO_PRODUTOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        await ctx.send(
            f"✅ Produto atualizado!\n"
            f"Nome: {novo_nome}\n💰 Preço: R${novo_preco}\n📝 Descrição: {nova_descricao}"
        )

    # Comando extra para listar produtos
    @produto.command(name="listar")
    async def produto_listar(self, ctx: commands.Context):
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if not dados["produtos"]:
            await ctx.send("Não há produtos cadastrados.")
            return

        embed = discord.Embed(title="📦 Produtos", color=discord.Color.green())
        for p in dados["produtos"]:
            embed.add_field(name=p["nome"], value=f"💰 R${p['preco']} | 📝 {p['descricao']}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Produto(bot))