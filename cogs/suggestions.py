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
        await message.add_reaction("⬆️")
        await message.add_reaction("⬇️")

        acknowledgement = discord.Embed(
            title="Suggestion Submitted",
            description=f"Your suggestion has been submitted. Thank you for your suggestion.",
            colour=self.client.primary_colour,
        )
        await ctx.reply(embed=acknowledgement)
    
    @check.is_staff()
    @commands.command(
        name="replySuggestion",
        description="Approve/deny a suggestion",
        hidden = True,
        alias=["approveSuggestion", "rs", "as", "ds", "denySuggestion"],
        usage=("<suggestion message id> <approve/deny (bool)> <message>"),
    )
    async def replySuggestion(self, ctx, messageID:int, approve:str, *messageToUser):
        messageToUser = " ".join(messageToUser[:])

        channel = self.client.get_channel(865821669730156544)
        message = await channel.fetch_message(messageID)
        if message == None:
            await ctx.reply("No message found!")
            return
        
        # retrieving suggestion and user that submitted it
        user = message.author
        suggestion = ""
        if message.embeds != []:
            for embed in message.embeds:
                if embed.title == "New Suggestion":
                    suggestion = embed.fields[0].value
                    user = int(embed.description.replace("> has submitted a suggestion.", "").replace("<@", "").replace("!", ""))
                    user = self.client.get_user(user)
        else:
            await ctx.reply("Invalid Message")
            return
        if suggestion == "" or user == message.author:
            await ctx.reply("Invalid Message")
            return

        if user == None:
            await ctx.reply("Invalid User")
        
        # send results
        channel2 = self.client.get_channel(882646341799542824)
        await message.delete()
        if approve == "None":
            await channel2.send(embed=discord.Embed(title=f"Suggestion needs clarification.", description=f"Suggestion: {suggestion}", colour=0x0000ff).add_field(name="Admin's message:", value=messageToUser, inline=False).set_footer(text=user.display_name, icon_url=user.avatar_url))
            await user.send(embed=discord.Embed(title=f"Your suggestion needs clarification.", description=f"Suggestion: {suggestion}", colour=0x0000ff).add_field(name="Admin's message:", value=messageToUser, inline=False))
        elif approve == "True":
            await channel2.send(embed=discord.Embed(title=f"Suggestion has been approved.", description=f"Suggestion: {suggestion}", colour=0x00ff00).add_field(name="Admin's message:", value=messageToUser, inline=False).set_footer(text=user.display_name, icon_url=user.avatar_url))
            await user.send(embed=discord.Embed(title=f"Your suggestion has been approved.", description=f"Suggestion: {suggestion}", colour=0x00ff00).add_field(name="Admin's message:", value=messageToUser, inline=False))
        else:
            await channel2.send(embed=discord.Embed(title=f"Suggestion has been denied.", description=f"Suggestion: {suggestion}", colour=0xff0000).add_field(name="Admin's message:", value=messageToUser, inline=False).set_footer(text=user.display_name, icon_url=user.avatar_url))
            await user.send(embed=discord.Embed(title=f"Your suggestion has been denied.", description=f"Suggestion: {suggestion}", colour=0xff0000).add_field(name="Admin's message:", value=messageToUser, inline=False))
        
        await ctx.message.delete()

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
    
    @check.is_staff()
    @commands.command(
        name="replyBugReport",
        description="Approve/deny a bug report",
        hidden = True,
        alias=["approveBugReport", "rbr", "br", "replyBug", "denyBugReport"],
        usage=("<suggestion message id> <approve/deny (bool)> <message>"),
    )
    async def replyBugReport(self, ctx, messageID:int, approve:str, *messageToUser):
        messageToUser = " ".join(messageToUser[:])

        channel = self.client.get_channel(869960880631218196)
        message = await channel.fetch_message(messageID)
        if message == None:
            await ctx.reply("No message found!")
            return
        
        # retrieving report and user that submitted it
        user = message.author
        suggestion = ""
        if message.embeds != []:
            for embed in message.embeds:
                if embed.title == "New Bug":
                    suggestion = embed.fields[0].value
                    user = int(embed.description.replace("> has submitted a bug.", "").replace("<@", "").replace("!", ""))
                    user = self.client.get_user(user)
        else:
            await ctx.reply("Invalid Message")
            return

        if suggestion == "" or user == message.author:
            await ctx.reply("Invalid Message")
            return

        if user == None:
            await ctx.reply("Invalid User")
        
        # send results
        channel2 = self.client.get_channel(882981586818195476)
        await message.delete()
        if approve == "None":
            await channel2.send(embed=discord.Embed(title=f"Bug Report needs clarification.", description=f"Suggestion: {suggestion}", colour=0x0000ff).add_field(name="Admin's message:", value=messageToUser, inline=False).set_footer(text=user.display_name, icon_url=user.avatar_url))
            await user.send(embed=discord.Embed(title=f"Your Bug Report needs clarification.", description=f"Suggestion: {suggestion}", colour=0x0000ff).add_field(name="Admin's message:", value=messageToUser, inline=False))
        elif approve == "True":
            await channel2.send(embed=discord.Embed(title=f"Bug Report has been approved.", description=f"Suggestion: {suggestion}", colour=0x00ff00).add_field(name="Admin's message:", value=messageToUser, inline=False).set_footer(text=user.display_name, icon_url=user.avatar_url))
            await user.send(embed=discord.Embed(title=f"Your Bug Report has been approved.", description=f"Suggestion: {suggestion}", colour=0x00ff00).add_field(name="Admin's message:", value=messageToUser, inline=False))
        else:
            await channel2.send(embed=discord.Embed(title=f"Bug Report has been denied.", description=f"Suggestion: {suggestion}", colour=0xff0000).add_field(name="Admin's message:", value=messageToUser, inline=False).set_footer(text=user.display_name, icon_url=user.avatar_url))
            await user.send(embed=discord.Embed(title=f"Your Bug Report has been denied.", description=f"Suggestion: {suggestion}", colour=0xff0000).add_field(name="Admin's message:", value=messageToUser, inline=False))
        
        await ctx.message.delete()

def setup(client):
    client.add_cog(Suggestions(client))
