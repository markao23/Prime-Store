import discord
from discord.ext import commands

class VendaBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vender")
    @commands.has_permissions(administrator=True)
    async def vender(self, ctx, *, nome_produto: str):
        # Acessa o pool de conexões do PostgreSQL (ajuste caso sua variável tenha outro nome)
        pool = self.bot.db 

        async with pool.acquire() as conn:
            # 1. Busca o produto pelo nome (ignorando maiúsculas/minúsculas usando ILIKE)
            produto = await conn.fetchrow(
                "SELECT * FROM produtos WHERE nome ILIKE $1", 
                nome_produto
            )

            # Validações iniciais
            if not produto:
                return await ctx.send(f"❌ Produto `{nome_produto}` não encontrado no banco de dados.")

            if produto['quantidade_estoque'] <= 0:
                return await ctx.send(f"⚠️ O bot **{produto['nome']}** já está com o estoque zerado!")

            # 2. Efetua a baixa reduzindo 1 do estoque e atualizando a data
        if produto['quantidade_estoque'] == 1:
            linha_apagada = await conn.fetchrow(
                "DELETE FROM produtos WHERE id = $1 RETURNING *",
                produto['id']
            )
            produto_atualizado = dict(linha_apagada)
            produto_atualizado['quantidade_estoque'] = 0
            aviso_estoque = "\n🛑 **Estoque Esgotado!** O bot foi removido da tabela."
            cor_embed = discord.Color.red()
        else:
            produto_atualizado = await conn.fetchrow(
                """
                UPDATE produtos 
                SET quantidade_estoque = quantidade_estoque - 1, 
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = $1 
                RETURNING *
                """, 
                produto['id']
            )
            aviso_estoque = ""
            cor_embed = discord.Color.green()

        # 3. Monta o Embed com todos os detalhes da tabela
        embed = discord.Embed(
            title="✅ Venda e Baixa Efetuada!",
            description=f"O bot **{produto_atualizado['nome']}** foi vendido com sucesso.",
            color=discord.Color.green()
        )

        embed.add_field(name="📦 SKU", value=produto_atualizado['sku'] or "N/A", inline=True)
        embed.add_field(name="🏷️ Cód. Barras", value=produto_atualizado['codigo_barras'] or "N/A", inline=True)
        embed.add_field(name="💰 Preço Venda", value=f"R$ {produto_atualizado['preco_venda']:.2f}", inline=True)
        
        # Formata o custo apenas se ele existir na tabela
        custo = f"R$ {produto_atualizado['preco_custo']:.2f}" if produto_atualizado['preco_custo'] else "N/A"
        embed.add_field(name="📉 Preço Custo", value=custo, inline=True)
        
        embed.add_field(name="📊 Estoque Restante", value=f"{produto_atualizado['quantidade_estoque']} unidades", inline=True)
        
        status = "🟢 Ativo" if produto_atualizado['ativo'] else "🔴 Inativo"
        embed.add_field(name="⚙️ Status", value=status, inline=True)

        if produto_atualizado['descricao']:
            embed.add_field(name="📝 Descrição", value=produto_atualizado['descricao'], inline=False)

        embed.set_footer(text=f"ID do Produto: {produto_atualizado['id']} | Autorizado por: {ctx.author.name}")

        # 4. Envia o comprovante no chat
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(VendaBot(bot))