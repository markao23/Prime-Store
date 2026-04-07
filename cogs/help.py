import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="help", aliases=["ajuda"], description="Mostra o painel de ajuda."
    )
    async def help(self, ctx):
        # 1. Criação do Embed base
        embed = discord.Embed(
            title="🤖 Painel de Comandos",
            description="Aqui estão todos os meus comandos! Lembre-se de usar `!` antes de cada um.",
            color=0x5865F2,  # Cor Blurple (azul/roxo padrão do Discord). Você pode usar 0xFF0000 para vermelho, etc.
        )

        # 2. Adicionando a foto de perfil do bot no canto superior direito
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # 3. Adicionando os campos (Categorias)
        # inline=False faz com que cada categoria fique em uma linha separada
        embed.add_field(
            name="🛠️ **Utilidade**",
            value="`!help` - Mostra esta mensagem.\n`!ping` - Mostra a latência do bot.",
            inline=False,
        )

        embed.add_field(
            name="🎉 **Diversão**",
            value="`!dado` - Rola um dado de 6 lados.\n`!avatar [@usuario]` - Mostra a foto de alguém.",
            inline=False,
        )

        embed.add_field(
            name="🛡️ **Moderação**",
            value="`!limpar [numero]` - Apaga mensagens do chat.\n`!ban [@usuario]` - Bane um membro.",
            inline=False,
        )

        # 4. Rodapé com quem pediu e a hora
        user_avatar = (
            ctx.author.avatar.url
            if ctx.author.avatar
            else ctx.author.default_avatar.url
        )
        embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=user_avatar)

        # Envia o embed no chat onde o comando foi digitado
        await ctx.send(embed=embed)


# Função obrigatória para carregar o Cog no discord.py v2.0+
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
