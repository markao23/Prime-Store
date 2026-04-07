import discord
from discord.ext import commands
import time

# Importa os seus logs customizados!
from utils import log_ping_start, log_ping_success, log_ping_error


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Isso cria o Slash Command (/ping) com a v2 do Discord
    @commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        # 1. Loga no seu terminal que alguém usou o comando
        log_ping_start(f"Discord API (Usuário: {interaction.user})")

        try:
            # 2. Pega a latência do WebSocket (Comunicação contínua do Bot)
            ws_latency = round(self.bot.latency * 1000)

            # 3. Marca o tempo antes de responder para calcular a latência da API
            start_time = time.time()

            # Cria um Embed bonito pro usuário ver no Discord
            embed = discord.Embed(title="🏓 Pong!", color=discord.Color.brand_green())
            embed.add_field(
                name="📡 Latência do Bot (WS)", value=f"`{ws_latency}ms`", inline=True
            )
            embed.add_field(
                name="⚙️ Latência da API", value="`Calculando...`", inline=True
            )

            # 4. Responde o usuário (isso bate na API do Discord)
            await interaction.response.send_message(embed=embed)

            # 5. Calcula quanto tempo demorou pra mensagem ir e voltar
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000)

            # 6. Edita a mensagem com a latência real da API
            embed.set_field_at(
                1, name="⚙️ Latência da API", value=f"`{api_latency}ms`", inline=True
            )
            await interaction.edit_original_response(embed=embed)

            # 7. Loga o sucesso e os tempos no seu terminal usando o Rich!
            terminal_msg = (
                f"Latência WS: {ws_latency}ms | Latência API: {api_latency}ms"
            )
            log_ping_success("Discord API", terminal_msg)

        except Exception as e:
            # Se der ruim (ex: Discord caiu), loga o erro em vermelho
            log_ping_error("Discord API", str(e))

            # Tenta avisar o usuário, mas só ele vê a mensagem (ephemeral)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ Ocorreu um erro ao calcular o ping.", ephemeral=True
                )


# Função obrigatória para o Discord carregar este arquivo
async def setup(bot):
    await bot.add_cog(PingCog(bot))
