import discord
from discord.ext import commands
from discord import app_commands

# Simulando um banco de dados (Você substituirá isso pelo seu DB real depois)
db_estoque = [
    {"nome": "Bot de Atendimento (Ticket)", "qtd": 3, "ativo": True, "emoji": "🎫"},
    {"nome": "Bot de Moderação", "qtd": 1, "ativo": True, "emoji": "🛡️"},
    {"nome": "Bot de Vendas Automáticas", "qtd": 0, "ativo": False, "emoji": "🛒"},
    {"nome": "Bot de Economia", "qtd": 5, "ativo": True, "emoji": "💰"},
]


# Função auxiliar para gerar o "container" (Embed) visual
def criar_embed_estoque() -> discord.Embed:
    embed = discord.Embed(
        title="📦 Painel de Estoque",
        description="Confira abaixo a disponibilidade dos nossos sistemas no momento.\n\n",
        color=discord.Color.blurple(),  # Uma cor padrão bonita do Discord
    )

    # Adicionando um container (field) para cada bot
    for bot in db_estoque:
        # Lógica visual para o status
        if bot["ativo"] and bot["qtd"] > 0:
            status_visual = "🟢 **Disponível**"
            cor_qtd = "```yaml\n"  # Truque de formatação do Discord para cor
        else:
            status_visual = "🔴 **Esgotado / Inativo**"
            cor_qtd = "```diff\n-"  # Formatação vermelha

        valor_field = f"> **Status:** {status_visual}\n> **Unidades:** {cor_qtd}{bot['qtd']} em estoque\n```"

        embed.add_field(
            name=f"{bot['emoji']} {bot['nome']}",
            value=valor_field,
            inline=False,  # Coloca um abaixo do outro para parecerem "containers" maiores
        )

    embed.set_footer(text="Estoque atualizado em tempo real.")
    return embed


# Aqui definimos os componentes v2 (Botões, Menus)
class EstoqueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Sem timeout, o botão dura para sempre

        # 1. BOTÃO DE LINK: É adicionado diretamente no __init__
        botao_comprar = discord.ui.Button(
            label="Comprar",
            style=discord.ButtonStyle.link,
            # Coloque apenas a URL pura, sem os colchetes e parênteses do markdown
            url="https://discord.com/channels/1230623705336381490/1450186826412331210",
        )
        self.add_item(botao_comprar)

    # 2. BOTÃO INTERATIVO: Continua usando o decorador normalmente
    @discord.ui.button(
        label="Atualizar",
        style=discord.ButtonStyle.secondary,
        emoji="🔄",
        custom_id="btn_atualizar",
    )
    async def btn_atualizar(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # Aqui você faria a query no seu banco de dados para pegar os dados novos
        novo_embed = criar_embed_estoque()
        await interaction.response.edit_message(embed=novo_embed, view=self)

        # Opcional: Mandar um aviso invisível só pro usuário confirmando
        await interaction.followup.send(
            "Estoque atualizado com sucesso!", ephemeral=True
        )

# A classe principal do Cog
class EstoqueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="estoque",
        description="Mostra os bots disponíveis em nosso estoque com uma UI moderna.",
    )
    async def estoque_cmd(self, interaction: discord.Interaction):
        # Pega a "caixa" visual e os botões
        embed = criar_embed_estoque()
        view = EstoqueView()

        # Envia a resposta combinando ambos
        await interaction.response.send_message(embed=embed, view=view)


# Função obrigatória para o setup_hook conseguir carregar este arquivo
async def setup(bot):
    await bot.add_cog(EstoqueCog(bot))
