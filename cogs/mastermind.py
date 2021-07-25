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
        board = "|⬜ ⬜ ⬜ ⬜ :question::question::question::question: 🟥 🟥 🟥 🟥|"
        
        prev_boards = []
        for i in range(4):
            elem = random.randint(1,8)
            code.append(elem)
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

        while True:
            guess = await self.client.wait_for("message", timeout=60,check=check)
            #check if message contains 4 space-separated 
            #integers between 1 and 8
            choices = guess.content.split(" ")
            print(choices)
            if len(choices) == 4:
                try:
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
                            break
                        else:
                            guess_string = ""
                            for g in range(4):
                                guess_string += ":"
                                guess_string += colors[int(choices[g])-1]
                                guess_string += "_circle: "
                            await guess.reply(guess_string)
                            
                        
                except ValueError:
                    embed=discord.Embed(
                        title="You need to enter space-separated integers between 1 and 8.",
                        description="",
                        color=0xff0000
                    )
                    await guess.reply(embed=embed)

                
            else:
                embed=discord.Embed(
                    title="You did not enter the right number of arguments for a guess!",
                    description="You need to input 4 space-separated integers between 1 and 8!",
                    color=0xff0000
                )
                await guess.reply(embed=embed)
            


            message = ""
            for i in prev_boards:
                message += i
                message += "\n"
            message += board
            embed = discord.Embed(
                title = mastermind_prefix,
                description=message,
                color = self.client.primary_colour
            )
            await guess.reply(embed=embed)
            

        
def setup(client):
    client.add_cog(Mastermind(client))