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
    @cooldown(1,120,BucketType.user)
    async def mastermind(self,ctx):
        player = ctx.author.id
        code = []
        colors = ["red","green","blue","purple","brown","white","yellow","orange"]
        board = "|⬜ ⬜ ⬜ ⬜ :question::question::question::question: 🟥 🟥 🟥 🟥|"
        
        prev_boards = []
        for i in range(4):
            elem = random.choice(colors)
            #no duplicate color in code for now :(
            colors.remove(elem)
            code.append(elem)
    
        message = board

        embed = discord.Embed(
            title = mastermind_prefix,
            description=message,
            color = self.client.primary_colour
        )
        await ctx.reply(embed=embed)

        def check(ctx):
            return ctx.author.id == player

        while True:
            guess = await self.client.wait_for("message", timeout=60,check=check)
            #check if message contains 4 space-separated 
            #integers between 1 and 8

            choices = guess.content.split(" ")
            if len(choices) != 4:
                pass
            


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