import discord
from discord.ext import commands
import time

# Importa os seus logs customizados!
from utils import log_ping_start, log_ping_success, log_ping_error


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. Mudamos para @commands.command (formato de prefixo)
    @commands.command(name="ping")
    async def ping(self, ctx):  # 2. Usando ctx em vez de interaction
        # 3. interaction.user vira ctx.author
        log_ping_start(f"Discord API (Usuário: {ctx.author})")

        try:
            # Pega a latência do WebSocket (Comunicação contínua do Bot)
            ws_latency = round(self.bot.latency * 1000)

            # Marca o tempo antes de responder para calcular a latência da API
            start_time = time.time()

            # Cria um Embed bonito pro usuário ver no Discord
            embed = discord.Embed(title="🏓 Pong!", color=discord.Color.brand_green())
            embed.add_field(
                name="📡 Latência do Bot (WS)", value=f"`{ws_latency}ms`", inline=True
            )
            embed.add_field(
                name="⚙️ Latência da API", value="`Calculando...`", inline=True
            )

            # 4. Usamos ctx.send e guardamos a mensagem na variável 'msg'
            msg = await ctx.send(embed=embed)

            # Calcula quanto tempo demorou pra mensagem ir e voltar
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000)

            # Edita a mensagem com a latência real da API
            embed.set_field_at(
                1, name="⚙️ Latência da API", value=f"`{api_latency}ms`", inline=True
            )
            # 5. Editamos a mensagem que guardamos ali em cima
            await msg.edit(embed=embed)

            # Loga o sucesso e os tempos no seu terminal usando o Rich!
            terminal_msg = (
                f"Latência WS: {ws_latency}ms | Latência API: {api_latency}ms"
            )
            log_ping_success("Discord API", terminal_msg)

        except Exception as e:
            # Se der ruim (ex: Discord caiu), loga o erro em vermelho
            log_ping_error("Discord API", str(e))

            # 6. Mensagem de erro simples usando ctx
            await ctx.send("❌ Ocorreu um erro ao calcular o ping.")


# Função obrigatória para o Discord carregar este arquivo
async def setup(bo):
    await bot.add_cog(PingCog(bot))
