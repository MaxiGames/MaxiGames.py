import discord
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.messages = []
    
    @commands.command(name="newticket", description="Creates a new message that responds to ")
    async def newticket(self, ctx):
        

def setup(client):
    client.add_cog(Ticket(client))