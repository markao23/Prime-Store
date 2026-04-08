import discord
from discord.ext import commands
from datetime import datetime


class Produto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="produto")
    @commands.has_permissions(administrator=True)  # Apenas admins podem criar produtos
    async def produto(self, ctx, nome: str, preco: str, quantidade: int):

        # 1. Criação da estrutura base do Embed
        embed = discord.Embed(
            title=f"🛒 {nome}",
            description="Temos um novo produto disponível! Confira os detalhes abaixo:",
            color=0x2ECC71,  # Um verde profissional e amigável
            timestamp=datetime.now(),  # Adiciona a hora atual no rodapé
        )

        # 2. Adicionando os campos separados (inline=True deixa eles lado a lado)
        embed.add_field(name="💰 Valor", value=f"**R$ {preco}**", inline=True)
        embed.add_field(
            name="📦 Estoque", value=f"**{quantidade}** unidades", inline=True
        )

        # Opcional: Uma linha extra para dar mais destaque
        embed.add_field(
            name="Como comprar?",
            value="Abra um ticket ou chame a equipe na DM!",
            inline=False,
        )

        # 3. Rodapé com a foto de quem anunciou
        embed.set_footer(
            text=f"Anunciado por {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        # Envia o embed no canal
        await ctx.send(embed=embed)

        # Apaga a mensagem original do "!produto" para deixar o chat limpo
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass  # Ignora caso o bot não tenha permissão de apagar mensagens


# Função obrigatória para carregar a Cog
async def setup(bot):
    await bot.add_cog(Produto(bot))
