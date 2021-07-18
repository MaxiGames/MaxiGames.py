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
        
        message = await ctx.reply("React on this message to start a tic tac toe game, 2 people are needed!")
        await message.add_reaction("✅")
        
        def check(reaction, user):
            if reaction.message == message and user.id != 863419048041381920:
                return True
            else: return False

        try:
            reaction1,user1 = await self.client.wait_for('reaction_add', timeout=45, check=check)
            print(user1.id)
            reaction2,user2 = await self.client.wait_for('reaction_add', timeout=45, check=check)
            print(user2.id)
            await ctx.reply(f"2 players have joined, tic tac toe game starting... <@{user1.id}>, <@{user2.id}>")
        except asyncio.TimeoutError:
            await ctx.reply("No one joined, please try again later!")
            return

def setup(client):
    client.add_cog(TicTacToe(client))
