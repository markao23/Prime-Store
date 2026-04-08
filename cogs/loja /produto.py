import discord
from discord.ext import commands
import json

ARQUIVO_PRODUTOS = "produtos.json"


class SistemaProduto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 1. Mudei para "produtos" (no plural) para acabar com o erro de conflito de nome
    @commands.group(name="produtos", invoke_without_command=True)
    async def produto(self, ctx: commands.Context):
        await ctx.send("Use um subcomando: `!produtos editar` ou `!produtos listar`")

    # 2. Em vez de @commands.command, usamos @produto.command para ligar este comando ao grupo acima!
    @produto.command(name="editar")
    async def produto_editar(
        self,
        ctx: commands.Context,
        nome: str,
        novo_nome: str,
        novo_preco: float,
        *,
        nova_descricao: str,
    ):
        """
        Edita um produto existente no JSON
        Exemplo:
        !produtos editar "Bot Moderador" "Bot Admin" 55 "Bot atualizado com mais comandos"
        """
        # Carrega os produtos
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Procura o produto
        produto_encontrado = next(
            (p for p in dados["produtos"] if p["nome"].lower() == nome.lower()), None
        )
        if not produto_encontrado:
            await ctx.send(f"❌ Produto **{nome}** não encontrado.")
            return

        # Atualiza os dados
        produto_encontrado["nome"] = novo_nome
        produto_encontrado["preco"] = novo_preco
        produto_encontrado["descricao"] = nova_descricao

        # Salva de volta no JSON
        with open(ARQUIVO_PRODUTOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        await ctx.send(
            f"✅ Produto atualizado!\n"
            f"Nome: {novo_nome}\n💰 Preço: R${novo_preco}\n📝 Descrição: {nova_descricao}"
        )

    # 3. Aqui também usamos @produto.command
    @produto.command(name="listar")
    async def produto_listar(self, ctx: commands.Context):
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if not dados["produtos"]:
            await ctx.send("Não há produtos cadastrados.")
            return

        embed = discord.Embed(title="📦 Produtos", color=discord.Color.green())
        for p in dados["produtos"]:
            embed.add_field(
                name=p["nome"],
                value=f"💰 R${p['preco']} | 📝 {p['descricao']}",
                inline=False,
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SistemaProduto(bot))
