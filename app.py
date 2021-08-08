import json
import discord
import os
from client import Client

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from discord_components import DiscordComponents
from discord_slash import SlashCommand
import topgg

print("hallo")
def get_prefix(client, message):
    with open('prefix.json', 'r') as f: 
        prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]

with open("config.json", "r") as file:
    data = json.load(file)
    intents = discord.Intents.default()
    intents.members = True
    client = Client(command_prefix=(get_prefix), intents=intents)
    client.topggpy = topgg.DBLClient(client, data["topggId"], autopost=True)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()



DiscordComponents(client)
slash = SlashCommand(
    client, sync_commands=True, sync_on_cog_reload=True, override_type=True
)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="m!help on " + str(len(client.guilds)) + " servers", type=0
        ),
    )
    print("We have logged in as {0.user}".format(client))

with open("config.json", "r") as file:
    data = json.load(file)
    client.run(data["tokenId"])
