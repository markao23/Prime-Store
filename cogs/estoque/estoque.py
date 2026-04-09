import discord
from discord.ext import commands
import asyncpg 

async def criar_embed_estoque(bot) -> discord.Embed:
    embed = discord.Embed(
        title="📦 Painel de Estoque",
        description="Confira abaixo a disponibilidade dos nossos sistemas no momento.\n\n",
        color=discord.Color.blurple(),
    )

    query = """
        SELECT sku, codigo_barras, nome, descricao, preco_custo, preco_venda, quantidade_estoque, ativo 
        FROM produtos
    """
    
    # Certifique-se de que o nome aqui (db ou db_pool) bate com o que você colocou no main.py
    async with bot.db.acquire() as conn:
        registros = await conn.fetch(query)

    for linha in registros:
        sku = linha['sku']
        codigo_barras = linha['codigo_barras'] or "Null"
        nome = linha['nome'] or "Null"
        descricao = linha['descricao'] or "Null"
        preco_custo = linha['preco_custo'] or "Null"
        preco_venda = linha['preco_venda'] or "Null"
        qtd = linha['quantidade_estoque'] or 0
        ativo = linha['ativo']

        if ativo and qtd > 0:
            status_visual = "🟢 **Disponível**"
            cor_qtd = "```yaml\n"
        else:
            status_visual = "🔴 **Esgotado / Inativo**"
            cor_qtd = "```diff\n-"

        valor_field = (
            f"> **Status:** {status_visual}\n"
            f"> **SKU:** {sku} | **Cód. Barra:** {codigo_barras}\n"
            f"> **Descrição:** {descricao}\n"
            f"> **Custo:** R$ {preco_custo} | **Venda:** R$ {preco_venda}\n"
            f"> **Unidades:** {cor_qtd}{qtd} em estoque\n```"
        )

        embed.add_field(
            name=f"📦 {nome}",
            value=valor_field,
            inline=False,
        )

    embed.set_footer(text="Estoque atualizado em tempo real.")
    return embed


class EstoqueView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot 
        
        # O BOTÃO DE URL FOI TOTALMENTE REMOVIDO DAQUI

    @discord.ui.button(
        label="Atualizar",
        style=discord.ButtonStyle.secondary,
        emoji="🔄",
        custom_id="btn_atualizar",
    )
    async def btn_atualizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        novo_embed = await criar_embed_estoque(self.bot)
        await interaction.response.edit_message(embed=novo_embed, view=self)

        await interaction.followup.send(
            "Estoque atualizado com sucesso do Banco de Dados!", ephemeral=True
        )


class EstoqueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="criar_estoque",
        help="Mostra os bots disponíveis em nosso estoque."
    )
    async def estoque_cmd(self, ctx: commands.Context):
        async with ctx.typing():
            embed = await criar_embed_estoque(self.bot)
            view = EstoqueView(self.bot)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(EstoqueCog(bot))