import discord
from discord.ext import commands
import json
import os


class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def carregar(self):
        # 1. Garante que a pasta existe
        if not os.path.exists("database"):
            os.makedirs("database")

        # 2. Verifica se o arquivo correto existe
        if not os.path.exists("database/dados.json"):
            with open("database/dados.json", "w") as f:
                json.dump({}, f)

        with open("database/dados.json", "r") as f:
            return json.load(f)

    def salvar(self, dados):
        with open("database/dados.json", "w") as f:
            json.dump(dados, f, indent=4)

    # 3. Comandos de barra usam interaction, não ctx
    @commands.command()
    async def saldo(self, interaction: discord.Interaction):
        dados = self.carregar()
        user_id = str(interaction.user.id)

        if user_id not in dados:
            dados[user_id] = {"saldo": 0}
            self.salvar(dados)

        # 4. Acessando o valor 'saldo' dentro do dicionário e respondendo corretamente
        await interaction.response.send_message(
            f"{interaction.user.mention}, seu saldo é de {dados[user_id]['saldo']} moedas."
        )

    # 5. O erro principal estava aqui: discord.Member (com M maiúsculo)
    @commands.command()
    async def add(
        self, interaction: discord.Interaction, membro: discord.Member, valor: int
    ):
        # 6. guild_permissions (com L)
        if interaction.user.guild_permissions.administrator:
            dados = self.carregar()
            user_id = str(membro.id)

            if user_id not in dados:
                dados[user_id] = {"saldo": 0}

            # 7. Somando no lugar certo dentro do dicionário
            dados[user_id]["saldo"] += valor
            self.salvar(dados)

            await interaction.response.send_message(
                f"{valor} moedas adicionadas ao saldo de {membro.mention}."
            )
        else:
            await interaction.response.send_message(
                "Você não tem permissão para usar este comando.", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Economia(bot))
