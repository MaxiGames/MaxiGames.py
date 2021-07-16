import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import requests
import json
import asyncio
import firebase_admin
from firebase_admin import firestore
class Hangman(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.initation = self.client.get_cog("Initiation")
        self.db = firestore.client()
def setup(client):
    client.add_cog(Hangman(client))