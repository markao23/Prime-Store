import discord
from discord.ext import commands
import json
import os


class Estoque(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.arquivo_estoque = "database/estoque.json"

    def carregar_estoque(self):
        # Cria a pasta e o arquivo JSON de estoque se não existirem
        if not os.path.exists("database"):
            os.makedirs("database")
        if not os.path.exists(self.arquivo_estoque):
            with open(self.arquivo_estoque, "w", encoding="utf-8") as f:
                json.dump({}, f)

        with open(self.arquivo_estoque, "r", encoding="utf-8") as f:
            return json.load(f)

    def salvar_estoque(self, dados):
        with open(self.arquivo_estoque, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)

    # 1. O GRUPO BASE: !estoque
    # Se o usuário digitar apenas !estoque, este bloco é executado e lista os itens.
    @commands.group(name="estoque", invoke_without_command=True)
    async def estoque(self, ctx):
        produtos = self.carregar_estoque()

        if not produtos:
            await ctx.send("O estoque da loja está vazio no momento.")
            return

        mensagem = "**📦 Produtos Disponíveis na Loja:**\n\n"
        for nome, info in produtos.items():
            mensagem += f"**{nome}** | Preço: `{info['preco']}` moedas | Quantidade: `{info['quantidade']}`\n"

        await ctx.send(mensagem)

    # 2. O SUBCOMANDO: !estoque criar <nome> <preco> <quantidade>
    # Usamos @estoque.command para vincular ao grupo acima
    @estoque.command(name="criar")
    @commands.has_permissions(administrator=True)  # Apenas admins podem criar produtos
    async def criar(self, ctx, nome: str, preco: int, quantidade: int = 1):
        produtos = self.carregar_estoque()

        # Deixa o nome padronizado (ex: "espada" vira "Espada")
        nome = nome.capitalize()

        if nome in produtos:
            # Se o produto já existe, apenas soma a quantidade e atualiza o preço
            produtos[nome]["quantidade"] += quantidade
            produtos[nome]["preco"] = preco
            self.salvar_estoque(produtos)
            await ctx.send(
                f"O produto **{nome}** já existia. Estoque atualizado para {produtos[nome]['quantidade']} unidades!"
            )
        else:
            # Se não existe, cria do zero
            produtos[nome] = {"preco": preco, "quantidade": quantidade}
            self.salvar_estoque(produtos)
            await ctx.send(
                f"Produto **{nome}** criado com sucesso!\nPreço: `{preco}` moedas | Quantidade inicial: `{quantidade}`"
            )


async def setup(bot):
    await bot.add_cog(Estoque(bot))
