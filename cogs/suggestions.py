import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import os
from utils import check
import asyncio
from firebase_admin import firestore
import asyncio

class Suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.db = firestore.client()

    @check.is_banned()
    @commands.command(
        name="suggest",
        help=(
            "Suggest anything that you want us to know about!!! " +
            "Be it a game that you really want to be implemented, " +
            "or some comments you have on what can be improved :D. " +
            "Do note that if this is a bug, please do `m!bugReport` instead!"
        ),
        usage="suggest <suggestion>",
        aliases=["sug", "suggestadd","suggestion", "newSuggestion", "suggestions"],
    )
    @cooldown(1,60,BucketType.user)
    async def suggest(self, ctx, *msg):
        suggestion = " ".join(msg[:])
        channel = self.client.get_channel(865821669730156544)
        embed = discord.Embed(
            title="New Suggestion",
            description=f"{ctx.author.mention} has submitted a suggestion.",
            colour=self.client.primary_colour,
        )
        embed.add_field(name="Suggestion", value=suggestion, inline=False)
        #! attachments
        if ctx.message.attachments != []:
            for c in ctx.message.attachments:
                embed.set_image(url=c)
        message = await channel.send(embed=embed)

        acknowledgement = discord.Embed(
            title="Suggestion Submitted",
            description=f"Your suggestion has been submitted. Thank you for your suggestion.",
            colour=self.client.primary_colour,
        )
        await ctx.reply(embed=acknowledgement)

    @check.is_banned()
    @commands.command(
        name="bugReport",
        help="Report bugs!",
        usage="bugreport <suggestion>",
        aliases=["report", "br", "bug","reportBug"],
    )
    async def report(self, ctx, *msg):
        suggestion = " ".join(msg[:])
        channel = self.client.get_channel(869960880631218196)

        embed = discord.Embed(
            title="New Bug",
            description=f"{ctx.author.mention} has submitted a bug.",
            colour=self.client.primary_colour,
        )
        embed.add_field(name="Bug report", value=suggestion, inline=False)
        #! attachments
        if ctx.message.attachments != []:
            for c in ctx.message.attachments:
                embed.set_image(url=c)

        message = await channel.send(embed=embed)

        acknowledgement = discord.Embed(
            title="Bug report submitted",
            description=f"Your report has been submitted. Thank you for notifying us of this bug, we will private message you once its fixed/dealt with!",
            colour=self.client.primary_colour,
        )
        await ctx.reply(embed=acknowledgement)
        


def setup(client):
    client.add_cog(Suggestions(client))
