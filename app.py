from _typeshed import HasFileno
import json
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=["m!"], help_command=None)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('m!help'))
    print("We have logged in as {0.user}".format(client))

 
client.run(json.load(open('config.json',))) 