import discord
from discord.ext import commands
import json
import os
import unicodedata # Biblioteca nativa para lidar com acentos

ARQUIVO_PRODUTOS = "database/produtos.json"

# Função para limpar o texto (tira acentos, espaços extras e deixa minúsculo)
def normalizar_texto(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
    return texto.strip().lower()

class ProdutoInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def produto_info(self, ctx: commands.Context, *, nome: str = None):
        if nome is None:
            await ctx.send("❌ Você precisa informar o nome do produto! Exemplo: `p$info moderacao`")
            return 

        if not os.path.exists(ARQUIVO_PRODUTOS):
            await ctx.send("⚠️ Erro no sistema: O arquivo `produtos.json` não foi encontrado na pasta do bot.")
            return

        try:
            with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("⚠️ Erro no sistema: O arquivo `produtos.json` está corrompido ou vazio.")
            return

        # 1. Normaliza o que o usuário digitou
        termo_busca = normalizar_texto(nome)
        produto_encontrado = None

        # 2. Procura na lista de produtos (aceita nome parcial, sem acento, ou o ID)
        for p in dados.get("produtos", []):
            nome_produto = normalizar_texto(p.get("nome", ""))
            id_produto = normalizar_texto(p.get("id", ""))
            
            # Se a palavra que o usuário digitou estiver no nome OU for o ID exato
            if termo_busca in nome_produto or termo_busca == id_produto:
                produto_encontrado = p
                break # Achou o produto, para de procurar
        
        if not produto_encontrado:
            await ctx.send(f"❌ Produto **{nome}** não encontrado no catálogo da Prime Store.")
            return

        # 3. Monta um Embed super profissional usando a estrutura do novo JSON
        preco_formatado = f"R$ {produto_encontrado['preco']['valor']:.2f}".replace(".", ",")

        embed = discord.Embed(
            title=f"📦 {produto_encontrado['nome']}",
            description=produto_encontrado.get("descricao_curta", "Sem descrição."),
            color=discord.Color.gold(), # Cor premium
        )
        
        embed.add_field(name="💰 Valor", value=f"**{preco_formatado}**", inline=True)
        embed.add_field(name="🏷️ Categoria", value=produto_encontrado.get("categoria", "Geral"), inline=True)
        embed.add_field(name="📌 Status", value=produto_encontrado.get("status", "Disponível"), inline=True)
        
        # Junta a lista de tecnologias em uma string separada por vírgulas
        tecnologias = ", ".join(produto_encontrado.get("tecnologias", []))
        if tecnologias:
            embed.add_field(name="💻 Tecnologias", value=tecnologias, inline=False)
            
        embed.set_footer(text=f"ID do Produto: {produto_encontrado.get('id', 'N/A')}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ProdutoInfo(bot))