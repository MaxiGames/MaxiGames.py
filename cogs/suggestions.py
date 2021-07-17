import discord
from discord.ext import commands
import os
import firebase_admin
from firebase_admin import firestore
from utils import check


class Suggestions (commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()

    @check.is_banned()
    @commands.command()
    async def suggest(self, ctx, *msg):
        suggestion = " ".join(msg[:])
        channel = self.client.get_channel(865821669730156544)
        embed = discord.Embed(
            title="New Suggestion",
            description=f"{ctx.author.mention} has submitted a suggestion.",
            colour=self.client.primary_colour
        )
        embed.add_field(name="Suggestion", value=suggestion, inline=False)
        await channel.send(embed=embed)
        await ctx.reply("Suggestion acknowledged")



def setup(client):
    client.add_cog(Suggestions(client))

