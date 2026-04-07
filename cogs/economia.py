import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class Econimia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def carregar(self):
        if not os.path.exists("database/dadps.jyson"):
            with open("datbase/dadps.jyson", "w") as f:
                json.dump({}, f)
        
        with open("database/dados.jyson", "r") as f:
            return json.load(f)

    def salvar(self, dados):
        with open("database/dados.jyson", "w") as f:
            json.dump(dados, f, indent=4)
    
    @app_command.command()
    async def saldo(self, ctx):
        dados = self.carregar()
        user = str(ctx.author.id)

        if user not in dados:
            dados[user] = {"saldo": 0}
            self.salvar(dados)

        await ctx.send(f"{ctx.author.mention}, seu saldo é de {dados[user]} moedas.")
    
    @app_command.command()
    async def add(self, ctx, member: discord.member, valor: int):
       if ctx.author.guid_permissions.administrator:
            dados = self.carregar()
            user = str(member.id)
            
            if user not in dados:
                dados[user] = 0
            
            dados[user] += valor
            self.salvar(dados)

            await ctx.send(f" {valor} moedas adicionadas ao saldo de {member.mention}.")

async def setup(bot):
    await bot.add_cog(Econimia(bot))