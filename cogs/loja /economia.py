import discord
from discord.ext import commands
import json
import os


class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def carregar(self):
        # Garante que a pasta e o arquivo existam
        if not os.path.exists("database"):
            os.makedirs("database")
        if not os.path.exists("database/dados.json"):
            with open("database/dados.json", "w") as f:
                json.dump({}, f)

        with open("database/dados.json", "r") as f:
            return json.load(f)

    def salvar(self, dados):
        with open("database/dados.json", "w") as f:
            json.dump(dados, f, indent=4)

    # 1. Mudamos para @commands.command()
    @commands.command(name="saldo")
    # 2. Voltamos a usar ctx em vez de interaction
    async def saldo(self, ctx):
        dados = self.carregar()
        user_id = str(ctx.author.id)

        if user_id not in dados:
            dados[user_id] = {"saldo": 0}
            self.salvar(dados)

        # 3. Voltamos a usar ctx.send para enviar a mensagem
        await ctx.send(
            f"{ctx.author.mention}, seu saldo é de {dados[user_id]['saldo']} moedas."
        )

    @commands.command(name="add")
    async def add(self, ctx, membro: discord.Member, valor: int):
        if ctx.author.guild_permissions.administrator:
            dados = self.carregar()
            user_id = str(membro.id)

            if user_id not in dados:
                dados[user_id] = {"saldo": 0}

            dados[user_id]["saldo"] += valor
            self.salvar(dados)

            await ctx.send(f"{valor} moedas adicionadas ao saldo de {membro.mention}.")
        else:
            await ctx.send("Você não tem permissão para usar este comando.")


async def setup(bot):
    await bot.add_cog(Economia(bot))
