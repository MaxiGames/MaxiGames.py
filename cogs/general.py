import discord
import time
from discord.ext import commands


class general(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dates = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

    @commands.command()
    async def hallo(self, ctx):
        await ctx.send("Hallo")

    @commands.command()
    async def current(self, ctx):
        result = time.localtime(time.time())
        embed = discord.Embed(
            title="Current Date and Time",
            description=f'Find the current date and time below :D',
            colour=self.client.primary_colour
        )

        embed.add_field(
            name="Date", value=f'{result.tm_mday}/{result.tm_mon}/{result.tm_year}', inline=True)
        embed.add_field(
            name="Day", value=self.dates[result.tm_wday], inline=True)
        embed.add_field(
            name="Time", value=f'{result.tm_hour}:{result.tm_min}:{result.tm_sec}', inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def seconds(self, ctx):
        await ctx.send(str(round(time.time())) + " seconds have passed since the epoch!")

    @commands.command()
    async def ns(self, ctx, num: int):
        if num < 1 or num > 50:
            await ctx.send("That is not a valid value for this command!:thinking:")
        else:
            answer = ""
            n = 1
            while n <= num:

                poop = n
                while poop > 0:
                    answer = answer + "^"
                    poop -= 1
                answer = answer + "\n"

                n += 1
            await ctx.send(answer)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite Link to invite the bot",
                              description="https://discord.com/api/oauth2/authorize?client_id=863419048041381920&permissions=8&scope=bot", color=self.client.primary_colour)
        await ctx.send(embed=embed)

    @commands.command()
    async def official(self, ctx):
        embed = discord.Embed(
            title="Join our official server today!",
            description="https://discord.gg/nGWhxNG2sf",
            colour=self.client.primary_colour)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(general(client))
