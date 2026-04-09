import discord
from discord.ext import commands


# DICA: Use name="Nome" na classe para definir como a categoria vai aparecer no Embed
class HelpCog(commands.Cog, name="⚙️ Ajuda"):
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
            color=0x5865F2,
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # 2. SISTEMA DINÂMICO DE LEITURA DOS COGS
        # Passa por todos os Cogs que você carregou no main.py
        for cog_name, cog in self.bot.cogs.items():

            # Pega todos os comandos dentro deste Cog
            cog_commands = cog.get_commands()

            # Filtra os comandos para não mostrar os que estão escondidos (hidden=True)
            visible_commands = [cmd for cmd in cog_commands if not cmd.hidden]

            # Se o Cog não tiver comandos visíveis, o bot ignora e pula pro próximo
            if not visible_commands:
                continue

            # Monta o texto com a lista de comandos deste Cog
            command_list = ""
            for cmd in visible_commands:
                # Se o comando não tiver o parâmetro 'description', ele usa um texto padrão
                desc = cmd.description or "Sem descrição configurada."
                command_list += f"`ps!{cmd.name}` - {desc}\n"

            # Adiciona a Categoria e a lista de comandos no Embed
            embed.add_field(name=f"**{cog_name}**", value=command_list, inline=False)

        # 3. Rodapé com quem pediu
        user_avatar = (
            ctx.author.avatar.url
            if ctx.author.avatar
            else ctx.author.default_avatar.url
        )
        embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=user_avatar)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
