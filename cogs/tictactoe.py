import discord
from discord.ext import commands
# import tictactoe

class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client
	
    @commands.command()
    async def ttt(self, ctx):
	    pass


def setup(client):
    client.add_cog(TicTacToe(client))
