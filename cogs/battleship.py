import asyncio
import discord
from utils import check
from discord.ext import commands
import random


class Battleship(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True

    def generateShips(self):
        ships = []
        
        return ships
    
    # @check.is_banned()
    # @commands.command(
    #     name="battleship",
    #     help="Starts a new game of battleship",
    #     usage="",
    #     aliases=["ship", "battle", "bs"],
    # )
    # async def battleship(self, ctx):
    #     message = await ctx.reply(
    #         "React on this message to start a battleship game, another person is needed!"
    #     )
    #     await message.add_reaction("✅")

    #     user1 = ctx.author
    #     user2 = None
    #     def check(reaction, user):
    #         if reaction.message == message and user.id != self.client.user.id and user.id != user1.id:
    #             return True
    #         else:
    #             return False

    #     try:
    #         user2 = await self.client.wait_for(
    #             "reaction_add", timeout=45, check=check
    #         )
    #         await ctx.reply(
    #             f"2 players have joined, battleship game starting... <@{user1.id}>, <@{user2.id}>. This game will be carried out in your DMs to prevent cheating!"
    #         )
    #     except asyncio.TimeoutError:
    #         await ctx.reply("No one else joined, please try again later!")
    #         return




def setup(client):
    client.add_cog(Battleship(client))

