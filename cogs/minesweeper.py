import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import requests
import math
import json
import asyncio
import firebase_admin
from firebase_admin import firestore
from utils.paginator import Paginator
import os
import copy
from utils import check
from utils.leaderboard import leaderboard_generate

class Minesweeper(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
    @commands.command(
        name="minesweeper",
        description="Play minesweeper :D",
        usage="minesweeper",
        aliases=["mines"]
    )
    @cooldown(1,90,BucketType.user)
    async def minesweeper(self,ctx):
        player = ctx.author
        board=[]
        empty_mastermind="o"
        empty_squares=[]
        for i in range(9):
            blank=[]
            for j in range(9):
                blank.append(empty_mastermind)
            board.append(blank)
        
        for i in range(64):
            empty_squares.append(i)
        mines = []
        for i in range(10):
            mine_add = random.choice(empty_squares)
            empty_squares.remove(mine_add)
            mines.append(mine_add)
            print(mine_add)
            board[int((mine_add-(mine_add%8))/8)][mine_add%8] = "x"
        msg = ""
        for i in board:
            for j in i:
                msg += j 
                msg += " "
            msg += "\n"
        await ctx.reply(msg)

def setup(client):
    client.add_cog(Minesweeper(client))