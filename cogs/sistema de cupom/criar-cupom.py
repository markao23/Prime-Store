import discord
from discord.ext import commands

class CupomView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Criar Cupom", style=discord.ButtonStyle.green)
    async def criar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "💡 Use:\n`ps!cupom criar CODIGO DESCONTO USOS`",
            ephemeral=True
        )

    @discord.ui.button(label="Listar Cupons", style=discord.ButtonStyle.blurple)
    async def listar(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM cupons")

            if not rows:
                await interaction.response.send_message("❌ Nenhum cupom", ephemeral=True)
                return

            texto = ""
            for r in rows:
                if r['tipo_desconto'] == 'porcentagem':
                    valor_texto = f"{r['valor_desconto']}%"
                else:
                    valor_texto = f"R$ {r['valor_desconto']}"

                texto += f"🎟️ **{r['codigo']}** - {valor_texto} (Usos: {r['usos_atuais']}/{r['usos_maximos']})\n"
            await interaction.response.send_message(
                f"📜 Cupons:\n{texto}",
                ephemeral=True
            )

class Sistema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # MENU
    @commands.group(name="cupom", invoke_without_command=True)
    async def cupom(self, ctx):
        embed = discord.Embed(
            title="🎟️ Sistema de Cupons",
            description="Use os botões abaixo ou comandos",
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed, view=CupomView(self.bot))

    # CRIAR CUPOM
    @cupom.command(name="criar")
    async def cupom_criar(self, ctx, codigo: str, tipo: str, valor: float, usos: int):
        tipo = tipo.lower()

        if tipo not in ['porcentagem', 'fixo']:
            await ctx.send("❌ O tipo de desconto precisa ser `porcentagem` ou `fixo`.")
            return

        async with self.bot.pool.acquire() as conn:
            try:
                await conn.execute(
                    """
                        INSERT INTO cupons
                        (codigo, tipo_desconto, valor_desconto, usos_maximos)
                        VALUES ($1, $2, $3, $4)
                    """,
                    codigo.upper(),
                    tipo,
                    valor,
                    usos,
                )
                await ctx.send(f"✅ Cupom `{codigo.upper()}` criado!")
            except Exception as e:
                print(f"Erro SQL: {e}")
                await ctx.send("❌ Esse cupom já existe!")

    # LISTAR VIA COMANDO
    @cupom.command(name="listar")
    async def cupom_listar(self, ctx):
        async with self.bot.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM cupons")

            if not rows:
                await ctx.send("❌ Nenhum cupom")
                return

            for r in rows:
                if r['tipo_desconto'] == 'porcentagem':
                    valor_texto = f"{r['valor_desconto']}%"
                else:
                    valor_texto = f"R$ {r['valor_desconto']}"

                texto += f"🎟️ **{r['codigo']}** - {valor_texto} (Usos: {r['usos_atuais']}/{r['usos_maximos']})\n"
            await ctx.send(f"📜 Cupons:\n{texto}")

# setup obrigatório
async def setup(bot):
    await bot.add_cog(Sistema(bot))
