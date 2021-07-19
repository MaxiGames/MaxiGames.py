import discord
from discord.ext import commands


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.messages = {}

    @commands.command(name="newticket", description="Creates a new message that responds to ")
    async def newticket(self, ctx):
        embed = discord.Embed(
            title="Get tickets here :D",
            description="To create a ticket react with ✔️",
            colour=self.client.primary_colour
        )
        embed.set_footer(text="MaxiGames",
                         icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Ticket(client))
