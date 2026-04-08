import discord
from discord.ext import commands

class Estoque(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Não precisamos mais carregar arquivos JSON aqui!

    # 1. O GRUPO BASE: !estoque
    @commands.group(name="estoque", invoke_without_command=True)
    async def estoque(self, ctx):
        # Pegamos uma conexão do Pool
        async with self.bot.db.acquire() as con:
            # fetch() retorna uma lista com todas as linhas encontradas
            # Filtramos apenas os ativos e ordenamos por nome
            produtos = await con.fetch(
                "SELECT nome, preco_venda, quantidade_estoque FROM produtos WHERE ativo = true ORDER BY nome ASC"
            )

        if not produtos:
            await ctx.send("O estoque da loja está vazio no momento.")
            return

        mensagem = "**📦 Produtos Disponíveis na Loja:**\n\n"
        # O asyncpg retorna registros que funcionam como dicionários
        for p in produtos:
            # Formatamos o preço para ter 2 casas decimais (ex: 15.00)
            mensagem += f"**{p['nome']}** | Preço: `{p['preco_venda']:.2f}` moedas | Quantidade: `{p['quantidade_estoque']}`\n"

        await ctx.send(mensagem)


    # 2. O SUBCOMANDO: !estoque criar <nome> <preco> <quantidade>
    @estoque.command(name="criar")
    @commands.has_permissions(administrator=True)
    # Mudei o preco para float, já que no banco é NUMERIC (aceita centavos)
    async def criar(self, ctx, nome: str, preco: float, quantidade: int = 1):
        nome = nome.capitalize()
        # A tabela exige um SKU único. Vamos gerar um automático (Ex: "Poção de Vida" vira "POÇÃO_DE_VIDA")
        sku = nome.upper().replace(" ", "_")

        async with self.bot.db.acquire() as con:
            # fetchrow() busca apenas 1 registro. Ideal para checar se o produto já existe.
            produto_existente = await con.fetchrow(
                "SELECT quantidade_estoque FROM produtos WHERE sku = $1", 
                sku
            )

            if produto_existente:
                # UPDATE: Soma a quantidade atual com a nova e atualiza o preço
                nova_quantidade = produto_existente['quantidade_estoque'] + quantidade
                
                await con.execute(
                    "UPDATE produtos SET quantidade_estoque = $1, preco_venda = $2 WHERE sku = $3",
                    nova_quantidade, preco, sku
                )
                
                await ctx.send(f"O produto **{nome}** já existia. Estoque atualizado para {nova_quantidade} unidades e preço alterado para `{preco:.2f}`!")
            
            else:
                # INSERT: Cria o produto do zero
                await con.execute(
                    "INSERT INTO produtos (sku, nome, preco_venda, quantidade_estoque) VALUES ($1, $2, $3, $4)",
                    sku, nome, preco, quantidade
                )
                
                await ctx.send(f"Produto **{nome}** criado com sucesso!\nPreço: `{preco:.2f}` moedas | Quantidade inicial: `{quantidade}`")


async def setup(bot):
    await bot.add_cog(Estoque(bot))