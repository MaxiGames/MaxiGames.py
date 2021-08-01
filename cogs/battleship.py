import discord
from discord.ext import commands

class Battleship(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True


def setup(client):
    client.add_cog(Battleship(client))