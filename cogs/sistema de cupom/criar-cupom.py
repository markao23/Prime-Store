import discord
from discord.ext import commands
from database import db

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
        async with db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM cupons")

            if not rows:
                await interaction.response.send_message("❌ Nenhum cupom", ephemeral=True)
                return

            texto = "\n".join([f"🎟️ {r['codigo']} - {r['desconto']}%" for r in rows])

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

        await ctx.send(embed=embed, view=CupomView())

    # CRIAR CUPOM
    @cupom.command(name="criar")
    async def cupom_criar(self, ctx, codigo: str, desconto: int, usos: int):
        async with db.pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO cupons (codigo, desconto, usos) VALUES ($1, $2, $3)",
                    codigo, desconto, usos
                )
                await ctx.send(f"✅ Cupom `{codigo}` criado!")
            except:
                await ctx.send("❌ Esse cupom já existe!")

    # LISTAR VIA COMANDO
    @cupom.command(name="listar")
    async def cupom_listar(self, ctx):
        async with db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM cupons")

            if not rows:
                await ctx.send("❌ Nenhum cupom")
                return

            texto = "\n".join([f"{r['codigo']} - {r['desconto']}%" for r in rows])
            await ctx.send(f"📜 Cupons:\n{texto}")

# setup obrigatório
async def setup(bot):
    await bot.add_cog(Sistema(bot))