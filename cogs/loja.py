import discord
from discord.ext import commands

class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="100 moedas - R$5", style=discord.ButtonStyle.green)
    async def comprar_100(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "💳 Você escolheu 100 moedas!\nFale com o admin para pagar via PIX.",
            ephemeral=True
        )

    @discord.ui.button(label="500 moedas - R$20", style=discord.ButtonStyle.blurple)
    async def comprar_500(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "💳 Você escolheu 500 moedas!\nFale com o admin.",
            ephemeral=True
        )

    @discord.ui.button(label="1000 moedas - R$35", style=discord.ButtonStyle.red)
    async def comprar_1000(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "💳 Você escolheu 1000 moedas!\nFale com o admin.",
            ephemeral=True
        )


class Loja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def loja(self, ctx):
        embed = discord.Embed(
            title="🛒 Loja de Moedas",
            description="Escolha um pacote abaixo:",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=LojaView())


async def setup(bot):
    await bot.add_cog(Loja(bot))