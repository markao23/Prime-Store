import discord
from discord.ext import commands

# --- CLASSE DA INTERAÇÃO (BOTÃO) ---
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Abrir Ticket", 
        style=discord.ButtonStyle.gray, 
        emoji="☁️", 
        custom_id="persistent_view:tkt_nexus" # ID único para salvar no banco do Discord
    )
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Aqui você insere a lógica de criação do canal de ticket
        await interaction.response.send_message("Seu ticket está sendo processado...", ephemeral=True)

# --- CONFIGURAÇÃO DO BOT ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True # Necessário para ler o prefixo !
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Isso faz com que o botão funcione mesmo se o bot cair e voltar
        self.add_view(TicketView())

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot logado como {bot.user.name}')

# --- COMANDO PARA ENVIAR O EMBED ---
@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="🔗 CENTRAL DE ATENDIMENTO",
        description=(
            "Precisa de ajuda, encontrou algum bug ou tem dúvidas sobre os nossos serviços? "
            "Nosso canal de atendimento, estamos prontos para te ajudar! seja para revolver problemas ou esclarecer duvidas\n\n"
            "**O que resolvemos por aqui:**\n"
            "❯ Suporte técnico e dúvidas sobre os sistemas\n"
            "❯ Assuntos financeiros, compras e pagamentos\n"
            "❯ Reportar bugs, erros ou fazer denúncias\n\n"
            "Clique no botão abaixo para abrir um canal de atendimento privado com a gente.\n"
            "🕒 Necessita ter paciencia que nossa equipe responde em breve"
        ),
        color=0x2b2d31 
    )
    
    embed.set_footer(text="VENDAS DE BOTS")
    
    await ctx.send(embed=embed, view=TicketView())
