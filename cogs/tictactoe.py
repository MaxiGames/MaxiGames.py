import discord
from discord.ext import commands
import asyncio

class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
	
    @commands.command(name="ttt", description="tic tac toe game u can play with your friend!")
    async def ttt(self, ctx):
        player1 = ""
        player2 = ""
        def check(msg):
            if msg.channel == ctx.channel:
                msg.author.id = player1
                return True
            else: return False

        def check2(msg):
            if msg.channel == ctx.channel and msg.author.id != player1:
                msg.author.id = player2
                return True
            else: return False
        
        message = await ctx.reply("React on this message to start a tic tac toe game, 2 people are needed!")
        await message.add_reaction("✅")

        try:
            reaction1 = await self.client.wait_for('reaction', timeout=45, check=check)
            reaction2 = await self.client.wait_for('reaction', timeout=45, check=check2)

            await ctx.reply("2 players have join, tic tac toe game starting...")
        except asyncio.TimeoutError:
            await ctx.reply("No one joined, please try again later!")
            return

def setup(client):
    client.add_cog(TicTacToe(client))
