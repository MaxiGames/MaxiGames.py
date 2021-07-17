import discord
from discord.ext import commands

class Hacks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
	
    @commands.command()
    async def hacks(self, ctx):
	    pass


def setup(client):
    client.add_cog(Hacks(client))
