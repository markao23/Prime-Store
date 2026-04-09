import discord
from discord.ext import commands

class ProdutoSelect(discord.ui.Select):
    def __init__(self, produtos):
        options = [
            discord.SelectOption(
                label=p["nome"],
                description=f"R${p['preco']}"
            )
            for p in produtos
        ]

        super().__init__(placeholder="Escolha um produto...", options=options)

    async def callback(self, interaction: discord.Interaction):
        produto = self.values[0]

        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO carrinho (user_id, produto) VALUES ($1, $2)",
                interaction.user.id, produto
            )

        await interaction.response.send_message(
            f"🛒 {produto} adicionado ao carrinho!",
            ephemeral=True
        )


class ComprarView(discord.ui.View):
    def __init__(self, produtos):
        super().__init__(timeout=60)
        self.add_item(ProdutoSelect(produtos))


class Comprar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comprar")
    async def comprar(self, ctx):
        async with self.bot.pool.acquire() as conn:
            rows = await conn.fetch("SELECT nome, preco FROM produtos")

        if not rows:
            await ctx.send("❌ Nenhum produto disponível")
            return

        produtos = [{"nome": r["nome"], "preco": r["preco"]} for r in rows]

        embed = discord.Embed(
            title="🛍️ Loja",
            description="Escolha um produto abaixo",
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed, view=ComprarView(produtos))


async def setup(bot):
    await bot.add_cog(Comprar(bot))