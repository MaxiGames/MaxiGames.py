import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import firebase_admin
from firebase_admin import firestore
from utils import check
import random 
import math
import asyncio
import time

mastermind_prefix = "1: :red_circle:  2: :green_circle: 3: :blue_circle: 4: :purple_circle: 5: :brown_circle: 6: :white_circle: 7: :yellow_circle: 8: :orange_circle:\n\n"

class Mastermind(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.initation = self.client.get_cog("Init")
        self.hidden = False

    @commands.command(
        name="mastermind",
        description="Play a game of mastermind :D",
        usage = "mastermind",
        alias = ["mm"]
    )
    #@cooldown(1,120,BucketType.user)
    @cooldown(1,1,BucketType.user)
    async def mastermind(self,ctx):
        player = ctx.author.id
        this_channel = ctx.channel.id
        code = []
        colors = ["red","green","blue","purple","brown","white","yellow","orange"]
        board = "|:negative_squared_cross_mark: :negative_squared_cross_mark: :negative_squared_cross_mark: :negative_squared_cross_mark: :question::question::question::question: :negative_squared_cross_mark: :negative_squared_cross_mark: :negative_squared_cross_mark: :negative_squared_cross_mark:|"
        
        prev_boards = []
        set_of_code = [1,2,3,4,5,6,7,8]
        for i in range(4):
            elem = random.choice(set_of_code)
            code.append(elem)
            set_of_code.remove(elem)
        print(code)
        message = board

        embed = discord.Embed(
            title = mastermind_prefix,
            description=message,
            color = self.client.primary_colour
        )
        await ctx.reply(embed=embed)

        def check(ctx):
            return ctx.author.id == player and this_channel == ctx.channel.id
        guess = ctx
        guesses = 0
        while True:
            
                
            if guesses > 11:
                embed=discord.Embed(
                    title="You used up all your guesses :(",
                    description="You lost the game!",
                    color=0xff0000
                )
                await guess.reply(embed=embed)
                break

            try:
                guess = await self.client.wait_for("message", timeout=90,check=check)
                #check if message contains 4 space-separated 
                #integers between 1 and 8
                choices = guess.content.split(" ")
                print(choices)
                transfer = True
                if len(choices) == 4:
                    try:
                        ok = 1
                        for i in range(4):
                            choices[i] = int(choices[i])
                            transfer = choices[i] >= 1 and choices[i] <= 8
                            if not transfer:
                                embed=discord.Embed(
                                    title="That is not a valid guess! Use integers from 1 to 8!",
                                    description="",
                                    color = 0xff0000
                                )
                                await guess.reply(embed=embed)
                                ok = 0
                                break
                        if ok == 0:
                            continue
                                

                            
                    except ValueError:
                        embed=discord.Embed(
                            title="You need to enter space-separated integers between 1 and 8.",
                            description="",
                            color=0xff0000
                        )
                        await guess.reply(embed=embed)
                        continue

                    
                else:
                    embed=discord.Embed(
                        title="You did not enter the right number of arguments for a guess!",
                        description="You need to input 4 space-separated integers between 1 and 8!",
                        color=0xff0000
                    )
                    await guess.reply(embed=embed)
                    continue
                if transfer:
                    guesses += 1
                    reds = 0
                    whites = 0
                    guess_string = ""
                    for g in range(4):
                        guess_string += ":"
                        guess_string += colors[int(choices[g])-1]
                        guess_string += "_circle: "
                        ref = ["n","n","n","n"]
                        for g in range(4):
                            for j in range(4):
                                if choices[g] == code[j]:
                                    if g == j:
                                        ref[j] = "r"
                                        
                                    else:
                                        if ref[j] != "r":
                                            ref[j] = "w"
                    for col in ref:
                        if col == "r":
                            reds += 1
                        elif col == "w":
                            whites += 1
                    prelimreds = ""
                    
                    for c in range(reds):
                        prelimreds += ":red_square: "
                    for c in range(4-reds):
                        prelimreds += ":negative_squared_cross_mark: "
                    prelimreds = prelimreds[:-1]
                    prelimreds+="|"
                    prelimwhites="|"
                    for c in range(4-whites):
                        prelimwhites += ":negative_squared_cross_mark: "
                    for c in range(whites):
                        prelimwhites += ":white_large_square: "
                    
                    
                    
                    prev_boards.append(prelimwhites + guess_string + prelimreds)
                    print(prev_boards)
            except asyncio.TimeoutError:
                embed=discord.Embed(
                    title="You took too long to respond!",
                    description="Time out!",
                    color = 0xff0000
                )
                await guess.reply(embed=embed)
                break

            message = ""
            for i in prev_boards:
                message += i
                message += "\n"
            embed = discord.Embed(
                title = mastermind_prefix,
                description=message+board,
                color = self.client.primary_colour
            )
            
            await guess.reply(embed=embed)
            correct_guess = True
            for i in range(4):
                if int(choices[i]) != code[i]:
                    correct_guess = False
                    break
            if correct_guess:
                embed=discord.Embed(
                    title="You won the game!",
                    description="You guessed the code! The answer was: "+str(guess.content)+"!",
                    color=self.client.primary_colour
                )
                await ctx.reply(embed=embed)

        
def setup(client):
    client.add_cog(Mastermind(client))