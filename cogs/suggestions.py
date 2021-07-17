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
        message = await channel.send(embed=embed)
        await ctx.reply("Suggestion acknowledged")
        def check(reaction, user):
            return user == ctx.author and reaction.message == message and reaction.emoji == "❌"
        await message.add_reaction("❌")
        reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
        await message.delete()



def setup(client):
    client.add_cog(Suggestions(client))

