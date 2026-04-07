import discord
from discord.ext import commands


# 1. A View (Botões) permanece fora da classe ou dentro, mas sem depender de 'bot' global
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Abrir Ticket",
        style=discord.ButtonStyle.primary,
        emoji="🎫",
        custom_id="persistent_view:ticket",
    )
    async def create_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        guild = interaction.guild
        user = interaction.user

        channel_name = f"ticket-{user.name}".lower()
        existing_channel = discord.utils.get(guild.channels, name=channel_name)

        if existing_channel:
            return await interaction.response.send_message(
                f"Você já tem um ticket aberto em {existing_channel.mention}!",
                ephemeral=True,
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, attach_files=True
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            ),
        }

        # Tenta encontrar a categoria 'TICKETS', se não existir, cria na raiz
        category = discord.utils.get(guild.categories, name="TICKETS")
        channel = await guild.create_text_channel(
            name=channel_name, overwrites=overwrites, category=category
        )

        await interaction.response.send_message(
            f"Seu ticket foi criado: {channel.mention}", ephemeral=True
        )

        embed_welcome = discord.Embed(
            title="🎫 Suporte Solicitado",
            description=f"Olá {user.mention}, explique seu problema e aguarde a equipe.",
            color=discord.Color.blue(),
        )
        await channel.send(embed=embed_welcome)


# 2. A Classe da Cog (Onde o erro estava acontecendo)
class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # EM COGS, USAMOS @commands.command() e adicionamos 'self' nos argumentos
    @commands.command(name="ticket")
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx):
        embed = discord.Embed(
            title="✨ Central de Atendimento",
            description=(
                "Precisa de ajuda ou quer realizar uma denúncia?\n\n"
                "**Como funciona?**\n"
                "1️⃣ Clique no botão abaixo.\n"
                "2️⃣ Um canal privado será criado para você.\n"
                "3️⃣ Descreva sua dúvida e aguarde nossa equipe."
            ),
            color=0x5865F2,
        )
        # 'self.bot' é usado aqui para pegar o avatar do bot
        embed.set_footer(
            text=f"Sistema de Tickets - {ctx.guild.name}",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None,
        )

        await ctx.send(embed=embed, view=TicketView())


# 3. Função obrigatória para carregar a Cog
async def setup(bot):
    await bot.add_cog(Ticket(bot))
