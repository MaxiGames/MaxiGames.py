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
            while True:
                reaction2,user2 = await self.client.wait_for('reaction_add', timeout=45, check=check)
                print(user2.id)
                if user2 == user1:
                    print("attempted to break the system in ttt")
                else:
                    break
            await ctx.reply(f"2 players have joined, tic tac toe game starting... <@{user1.id}>, <@{user2.id}>")
        except asyncio.TimeoutError:
            await ctx.reply("No one joined, please try again later!")
            return
        
        #tic tac toe game
        board = [[" "," "," "],[" "," "," "],[" "," "," "]]
        player1 = user1
        player2 = user2
        turn = 0
        while True:
            if turn == 0:
                await ctx.reply(f"{player1.mention}'s turn!")
                await ctx.reply("Your turn, type a number from 1 to 9 to place a marker on the board")
                while True:
                    try:
                        message = await self.client.wait_for('message', timeout=45, check=lambda m: m.author == player1)
                        if message.content.isdigit() and int(message.content) in range(1,10):
                            board[int(message.content)-1][0] = "X"
                            break
                        else:
                            await ctx.reply("Please enter a valid number from 1 to 9")
                    except asyncio.TimeoutError:
                        await ctx.reply("Please enter a valid number from 1 to 9")
            else:
                await ctx.reply(f"{player2.mention}'s turn!")
                await ctx.reply("Your turn, type a number from 1 to 9 to place a marker on the board")
                while True:
                    try:
                        message = await self.client.wait_for('message', timeout=45, check=lambda m: m.author == player2)
                        if message.content.isdigit() and int(message.content) in range(1,10):
                            board[int(message.content)-1][2] = "O"
                            break
                        else:
                            await ctx.reply("Please enter a valid number from 1 to 9")
                    except asyncio.TimeoutError:
                        await ctx.reply("Please enter a valid number from 1 to 9")



def setup(client):
    client.add_cog(TicTacToe(client))
