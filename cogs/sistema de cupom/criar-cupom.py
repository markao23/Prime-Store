import discord
from discord.ext import commands
from database import db

class CupomView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Criar Cupom", style=discord.ButtonStyle.green)
    async def criar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Use: `ps!cupom_criar CODIGO DESCONTO USOS`",
            ephemeral=True
        )

    @discord.ui.button(label="Listar Cupons", style=discord.ButtonStyle.blurple)
    async def listar(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM cupons")

            if not rows:
                await interaction.response.send_message("Nenhum cupom", ephemeral=True)
                return

            texto = "\n".join([f"{r['codigo']} - {r['desconto']}%" for r in rows])

            await interaction.response.send_message(
                f"📜 Cupons:\n{texto}",
                ephemeral=True
            )

class Sistema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cupom")
    async def cupom_menu(self, ctx):
        embed = discord.Embed(
            title="🎟️ Sistema de Cupons",
            description="Use os botões abaixo",
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed, view=CupomView())