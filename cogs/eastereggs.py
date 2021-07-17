import discord
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions
# import tictactoe

class EasterEggs(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
	
    @commands.command(hidden=True)
    async def whoru(self, ctx):
        embed = discord.Embed(title = "Hey! Looks like you found this easter egg!",description = "Nice.",color = self.client.primary_colour)
        embed.add_field(
            name = "Whoami?",
            value = "I am Maxigames! The creation of amateur bot devs <@!712942935129456671>, <@!676748194956181505> and <@!782247763542016010>",
            inline = False
        )
        embed.add_field(
            name = "Are there more easter eggs?",
            value = "Yes ofc.",
            inline = False
        )
        await ctx.author.send(embed=embed)
    @commands.command(hidden=True)
    async def whoareu(self, ctx):
        embed = discord.Embed(title = "Hey! Looks like you found this easter egg!",description = "Nice.",color = self.client.primary_colour)
        embed.add_field(
            name = "Whoami?",
            value = "I am Maxigames! The creation of amateur bot devs <@!712942935129456671>, <@!676748194956181505> and <@!782247763542016010>",
            inline = False
        )
        embed.add_field(
            name = "Are there more easter eggs?",
            value = "Yes ofc.",
            inline = False
        )
        await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(EasterEggs(client))
