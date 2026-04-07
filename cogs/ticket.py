import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout None mantém o botão ativo após reiniciar

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.gray, emoji="☁️", custom_id="abrir_ticket")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.send_message("Criando seu ticket...", ephemeral=True)

@bot.command()
async def setup_suporte(ctx):
    # Criando o Embed
    embed = discord.Embed(
        title="🔗 CENTRAL DE ATENDIMENTO",
        description=(
            "Precisa de ajuda, encontrou algum bug ou tem dúvidas sobre os nossos serviços? "
            "Nossa equipe da Staff está pronta para te auxiliar o mais rápido possível.\n\n"
            "**O que resolvemos por aqui:**\n"
            "❯ Suporte técnico e dúvidas sobre os sistemas\n"
            "❯ Assuntos financeiros, compras e pagamentos\n"
            "❯ Reportar bugs, erros ou fazer denúncias\n\n"
            "Clique no botão abaixo para abrir um canal de atendimento privado com a gente.\n"
            "🕒 Necessita ter paciencia que nossa equipe responde em breve"
        ),
        color=discord.Color.dark_grey() # Cor aproximada da imagem
    )
    
    # Rodapé (Footer)
    embed.set_footer(text="🛠️ Nexus Studios • Sistema de Suporte")

    # Enviando a mensagem com o botão
    await ctx.send(embed=embed, view=TicketView())
