import discord
from discord.ext import commands
import os
from utils import check


class Suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False

    @check.is_banned()

    @commands.command(
        name="suggestions",
        description="Suggest anything that you want us to know about!!! Be it a game that you really want to be implemented, or some comments you have on what can be improved :D",
        usage="suggest <suggestion>",
        aliases=["suggest", "sug", "s", "suggestadd"],
    )
    async def suggest(self, ctx, *msg):
        suggestion = " ".join(msg[:])
        channel = self.client.get_channel(865821669730156544)
        embed = discord.Embed(
            title="New Suggestion",
            description=f"{ctx.author.mention} has submitted a suggestion.",
            colour=self.client.primary_colour,
        )
        embed.add_field(name="Suggestion", value=suggestion, inline=False)
        message = await channel.send(embed=embed)

        acknowledgement = discord.Embed(
            title="Suggestion Submitted",
            description=f"Your suggestion has been submitted. Thank you for your suggestion.",
            colour=self.client.primary_colour,
        )
        await ctx.reply(embed=acknowledgement)

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message == message
                and reaction.emoji == "❌"
            )

        await message.add_reaction("⬆️")
        await message.add_reaction("⬇️")
        await message.add_reaction("❌")
        reaction, user = await self.client.wait_for("reaction_add", check=check)
        await message.delete()

        delete_channel = self.client.get_channel(866339642075775058)
        await delete_channel.send(embed=embed)


def setup(client):
    client.add_cog(Suggestions(client))
