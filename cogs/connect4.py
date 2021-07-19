import random
import discord
from discord.ext import commands
import sys
import asyncio
import time
alpha = "abcdefghijklmnopqrstuvwxyz"
class Connect4(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False
    @commands.command(name="connect4",description="play connect4 with another player",usage = "connect4")
    async def connect4(self,ctx):
        player1 = ctx.author
        message = await ctx.reply("React on this message to start a Connect 4 game. Another person is needed to start the game!")
        await message.add_reaction("✅")
        
        def check(reaction, user):
            if reaction.message == message and user.id != self.client.user.id:
                return True
            else: return False

        while True:
            try:
                reaction1,user1 = await self.client.wait_for('reaction_add', timeout=45, check=check)
                
                if user1.id == ctx.author.id:
                    embed = discord.Embed(
                        title = "You already joined the game!",
                        description = "Wait for another player.",
                        color = 0xff0000
                    )
                    await ctx.reply(embed=embed)
                else:
                    player2 = user1
                    break
                print(user1.id)
                
                
            except asyncio.TimeoutError:
                await ctx.reply("No one joined, please try again later!")
                return
        
        await ctx.reply(f"2 players have joined, connect4 game starting... <@{player1.id}>, <@{player2.id}>")
        time.sleep(2)
        board = [["□","□","□","□","□","□"],["□","□","□","□","□","□"],["□","□","□","□","□","□"],["□","□","□","□","□","□"],["□","□","□","□","□","□"],["□","□","□","□","□","□"],["□","□","□","□","□","□"]]
        print(board)
        curmax = [0,0,0,0,0,0,0]
        turn = 0
        while True:
            if turn == 0:
                turn = 1
                success = 0
                await ctx.send(f"{player1.mention}'s turn! Type a number from 1 to 7, the column you want to place a marker on!")
                while True:
                    try:
                        message = await self.client.wait_for('message', timeout=30, check=lambda m: m.author == player1)
                        try:
                            selected = int(message.content)-1
                            #restrict number to 1-9
                            if selected < 0 or selected > 6:
                                await message.reply("Invalid number, please try again")
                                continue
                            if curmax[selected]>5:
                                await message.reply("That column is already full! Please try again.")
                                continue
                            board[selected][curmax[selected]] = "o"
                            curmax[selected] += 1
                            print(board)
                            success = 1
                            board_display = "|1 2 3 4 5 6 7"
                            for i in range(6):
                                board_display += "|\n|"
                                for j in range(7):
                                    board_display += board[j][5-i]
                                    board_display += " "
                            board_display += "|"
                                
                            embed=discord.Embed(
                                title = "Successful placement",
                                description = board_display,
                                color = self.client.primary_colour
                            )
                            await message.reply(embed=embed)
                            for i in range(7):
                                
                                for j in range(3):
                                    if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == "o":
                                        embed = discord.Embed(
                                            title = "Game over!",
                                            description =f"{player1.mention} wins!",
                                            color = self.client.primary_colour
                                        )

                                        await message.reply(embed=embed)
                                        return
                            for i in range(6):
                                for j in range(4):
                                    if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == "o":
                                        embed = discord.Embed(
                                            title = "Game over!",
                                            description =f"{player1.mention} wins!",
                                            color = self.client.primary_colour
                                        )
                                        await message.reply(embed=embed)
                                        return
                            
                            break
                        except ValueError:
                            await message.reply("Please enter a number from 1 to 7")
                            continue
                    except asyncio.TimeoutError:
                        await message.reply("Time out")
                        return
                    if success == 1:
                        break
            else:
                turn = 0
                success = 0
                await ctx.send(f"{player2.mention}'s turn! Type a number from 1 to 7, the column you want to place a marker on!")
                while True:
                    try:
                        message = await self.client.wait_for('message', timeout=30, check=lambda m: m.author == player2)
                        try:
                            selected = int(message.content)-1
                            #restrict number to 1-9
                            if selected < 0 or selected > 6:
                                await message.reply("Invalid number, please try again")
                                continue
                            if curmax[selected]>5:
                                await message.reply("That column is already full! Please try again.")
                                continue
                            board[selected][curmax[selected]] = "x"
                            curmax[selected] += 1
                            print(board)
                            success = 1
                            board_display = "|1 2 3 4 5 6 7"
                            for i in range(6):
                                board_display += "|\n|"
                                for j in range(7):
                                    board_display += board[j][5-i]
                                    board_display += " "
                                    print(board_display)
                            board_display += "|"
                            embed=discord.Embed(
                                title = "Successful placement",
                                description = board_display,
                                color = self.client.primary_colour
                            )
                            await message.reply(embed=embed)
                            #diagonal
                            for i in range(4):
                                if board[i][i] == board[i+1][i+1] == board[i+2][i+2] == board[i+3][i+3] == "o":
                                    embed = discord.Embed(
                                        title = "Game over!",
                                        description =f"{player1.mention} wins!",
                                        color = self.client.primary_colour
                                    )
                                    await message.reply(embed=embed)
                                    return
                            #diagonal but other way around
                            for i in range(4):
                                if board[i][i] == board[i+1][i] == board[i+2][i] == board[i+3][i] == "o":
                                    embed = discord.Embed(
                                        title = "Game over!",
                                        description =f"{player1.mention} wins!",
                                        color = self.client.primary_colour
                                    )
                                    await message.reply(embed=embed)
                                    return
                            #horizontal
                            for i in range(7):
                                for j in range(3):
                                    if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == "x":
                                        embed = discord.Embed(
                                            title = "Game over!",
                                            description =f"{player2.mention} wins!",
                                            color = self.client.primary_colour
                                        )

                                        await message.reply(embed=embed)
                                        return
                            #vertical
                            for i in range(6):
                                for j in range(4):
                                    if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == "x":
                                        embed = discord.Embed(
                                            title = "Game over!",
                                            description =f"{player2.mention} wins!",
                                            color = self.client.primary_colour
                                        )
                                        await message.reply(embed=embed)
                                        return
                            break

                        except ValueError:
                            await message.reply("Please enter a number from 1 to 7")
                            continue
                    except asyncio.TimeoutError:
                        await message.reply("Time out")
                        return
                    if success == 1:
                        break
                
def setup(client):
    client.add_cog(Connect4(client))