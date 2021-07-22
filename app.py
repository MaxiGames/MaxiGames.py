import json
import discord
from discord.ext import commands
import os
import time
from client import Client

# from start import keep_alive
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from discord_components import *
from discord_slash import SlashCommand, SlashContext

with open("config.json", "r") as file:
    data = json.load(file)
    client = Client(command_prefix=[data["prefixBeta"]], help_command=None)

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
    print(client.get_user(782247763542016010))


# keep_alive()

with open("config.json", "r") as file:
    data = json.load(file)
    client.run(data["tokenIdBeta"])
