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
            if reaction.message == message and user.id != self.client.user.id:
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
                turn = 1
                await ctx.send(f"{player1.mention}'s turn! Type a number from 1 to 9 to place a marker on the board")
                while True:
                    try:
                        
                        message = await self.client.wait_for('message', timeout=45, check=lambda m: m.author == player1)
                        
                        if int(message.content) and int(message.content) in range(1,10):
                            selected = int(message.content)-1
                            board[int(selected/3)][int(selected%3)] = "X"
                            break
                        else:
                            await message.reply("Please enter a valid number from 1 to 9")
                    except asyncio.TimeoutError:
                        await message.reply("Timeout")
            else:
                turn = 0 
                await ctx.send(f"{player2.mention}'s turn! Type a number from 1 to 9 to place a marker on the board")
                while True:
                    try:
                        message = await self.client.wait_for('message', timeout=45, check=lambda m: m.author == player2)
                        if int(message.content) and int(message.content) in range(1,10):
                            selected = int(message.content)-1
                            board[int(selected/3)][int(selected%3)] = "O"
                            break
                        else:
                            await message.reply("Please enter a valid number from 1 to 9")
                    except asyncio.TimeoutError:
                        await message.reply("Timeout")
            string = ""
            for i in board:
                for j in i:
                    toAdd = ""
                    if j == " ":
                        toAdd = "□ "
                    else:
                        toAdd = j + " "
                    string += toAdd
                string += "\n"
            embed = discord.Embed(title="Tic Tac Toe", description=string, color=0x00ff00)
            await message.reply(embed=embed)
            if board[0][0] == board[1][1] == board[2][2] == "X" or board[0][0] == board[1][1] == board[2][2] == "O": #diagonals
                if board[0][0] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            elif board[0][2] == board[1][1] == board[2][0] == "X" or board[0][2] == board[1][1] == board[2][0] == "O":
                if board[0][2] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            #horizontal
            elif board[0][0] == board[0][1] == board[0][2] == "X" or board[0][0] == board[0][1] == board[0][2] == "O":
                if board[0][0] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            elif board[1][0] == board[1][1] == board[1][2] == "X" or board[1][0] == board[1][1] == board[1][2] == "O":
                if board[1][0] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            elif board[2][0] == board[2][1] == board[2][2] == "X" or board[2][0] == board[2][1] == board[2][2] == "O":
                if board[2][0] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            #vertical
            elif board[0][0] == board[1][0] == board[2][0] == "X" or board[0][0] == board[1][0] == board[2][0] == "O":
                if board[0][0] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            elif board[0][1] == board[1][1] == board[2][1] == "X" or board[0][1] == board[1][1] == board[2][1] == "O":
                if board[0][1] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            elif board[0][2] == board[1][2] == board[2][2] == "X" or board[0][2] == board[1][2] == board[2][2] == "O":
                if board[0][2] == "X":
                    await ctx.reply(f"{player1.mention} wins!")
                else:
                    await ctx.reply(f"{player2.mention} wins!")
                break
            elif " " not in board[0] and " " not in board[1] and " " not in board[2]:
                await ctx.reply("Draw!")
                break
        await ctx.send("Game over, please start a new game!")
                    

def setup(client):
    client.add_cog(TicTacToe(client))
