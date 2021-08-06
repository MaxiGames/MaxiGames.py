import discord
from discord.ext import commands
import topgg

class Topgg(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)

def setup(client):
    client.add_cog(Topgg(client))  