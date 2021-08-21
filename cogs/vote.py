import discord
from discord.ext import commands

class Vote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='didivote')
    async def didvote(self, ctx):
        print(await self.client.topggpy.get_user_vote(ctx.author.id))


def setup(client):
    client.add_cog(Vote(client))