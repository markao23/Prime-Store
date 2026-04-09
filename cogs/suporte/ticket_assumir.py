import discord
from discord.ext import commands

class TicketSuporte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="assumir")
    # Substitua "Suporte" pelo ID do cargo de suporte (ex: @commands.has_role(1234567890))
    # ou mantenha o nome exato do cargo entre aspas.
    @commands.has_permissions(administrator=True) 
    async def assumir_ticket(self, ctx):
        # 1. Deleta a mensagem original do comando (!assumir) para deixar o chat limpo
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass # Ignora se o bot não tiver permissão para apagar mensagens

        # 2. Monta o Embed profissional
        embed = discord.Embed(
            title="🤝 Atendimento Iniciado",
            description=(
                f"Olá! Meu nome é **{ctx.author.display_name}** e serei o responsável "
                "por ajudar você a partir de agora.\n\n"
                "Por favor, detalhe sua dúvida ou problema abaixo e eu responderei "
                "o mais rápido possível."
            ),
            color=discord.Color.blue()
        )
        
        # Adiciona a foto de perfil do membro do suporte
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        
        # Rodapé com informações de segurança e horário
        embed.set_footer(
            text=f"Atendimento assumido por: {ctx.author.name} • Lembre-se: nossa equipe nunca pedirá sua senha.",
            icon_url=self.bot.user.display_avatar.url # Foto do próprio bot no rodapé
        )

        # 3. Envia o Embed no canal do ticket
        await ctx.send(embed=embed)

        # 4. [Opcional mas Profissional] Renomeia o canal para mostrar que está em atendimento
        # Isso ajuda os outros membros do suporte a verem na lista de canais que este já foi pego.
        try:
            novo_nome = f"atendimento-{ctx.author.name}"
            await ctx.channel.edit(name=novo_nome)
        except discord.HTTPException:
            # O Discord tem limite de quantas vezes você pode renomear um canal rapidamente (rate limit).
            # Esse try/except garante que o bot não trave se atingir o limite.
            pass

    # Tratamento de erro caso alguém sem o cargo tente usar o comando
    @assumir_ticket.error
    async def assumir_ticket_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            erro_embed = discord.Embed(
                description="❌ Você não tem permissão para assumir tickets. Apenas membros da equipe de **Suporte** podem usar este comando.",
                color=discord.Color.red()
            )
            # Manda a mensagem de erro e apaga depois de 5 segundos para não poluir o ticket
            await ctx.send(embed=erro_embed, delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(TicketSuporte(bot))