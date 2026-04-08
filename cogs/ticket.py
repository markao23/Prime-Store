import discord
from discord.ext import commands


# Interface do Botão que aparece abaixo do Embed
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout=None
        )  # timeout=None para o botão não parar de funcionar

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

        # Nome do canal (ex: ticket-usuario)
        channel_name = f"ticket-{user.name}"

        # Verifica se já existe um canal com esse nome para evitar spam (opcional)
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            return await interaction.response.send_message(
                f"Você já tem um ticket aberto em {existing_channel.mention}!",
                ephemeral=True,
            )

        # Permissões do canal: O usuário vê, o resto do @everyone não.
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, attach_files=True
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            ),
        }

        # Cria o canal de ticket
        category = discord.utils.get(
            guild.categories, name="TICKETS"
        )  # Opcional: define uma categoria
        channel = await guild.create_text_channel(
            name=channel_name, overwrites=overwrites, category=category
        )

        await interaction.response.send_message(
            f"Seu ticket foi criado: {channel.mention}", ephemeral=True
        )

        # Mensagem de boas-vindas dentro do ticket
        embed_welcome = discord.Embed(
            title="🎫 Suporte Solicitado",
            description=f"Olá {user.mention}, explique seu problema e aguarde a equipe.\nPara fechar este ticket, um administrador deve deletar o canal.",
            color=discord.Color.blue(),
        )
        await channel.send(embed=embed_welcome)


# Comando de Prefixo Principal
class TicketCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticket")
    @commands.has_permissions(administrator=True)  # Apenas ADMs podem postar o painel
    async def ticket_panel(self, ctx):
        embed = discord.Embed(
            title="✨ Central de Atendimento",
            description=(
                "Precisa de ajuda ou quer realizar uma denúncia?\n\n"
                "**Como funciona?**\n"
                "1️⃣ Clique no botão abaixo.\n"
                "2️⃣ Um canal privado será criado para você.\n"
                "3️⃣ Descreva sua dúvida e aguarde nossa equipe.\n\n"
                "*Horário de atendimento: 09h às 22h.*"
            ),
            color=0x5865F2,  # Azul Blurple do Discord
        )
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(
            text=f"Sistema de Tickets - {ctx.guild.name}",
            icon_url=self.bot.user.avatar.url,
        )

        await ctx.send(embed=embed, view=TicketView())


# Função para adicionar ao bot principal
async def setup(bot):
    await bot.add_cog(TicketCommand(bot))
    