import discord
import time
from discord.ext import commands
from discord_components import *
import asyncio

from utils.paginator import Paginator


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

    @commands.command()
    async def whoami(self, ctx):
        embed = discord.Embed(
            title="You are " + str(ctx.author) + " :D",
            description="What a pog name!!!",
            color=self.client.primary_colour
        )
        role = ""  # theres probably some way to optimise this...
        for i in ctx.author.roles[::-1]:
            if i.name != "@everyone":
                role += f'{i.mention} '
        embed.add_field(name="Roles", value=role, inline=True)
        embed.add_field(
            name="Created On", value=f'{ctx.author.created_at.strftime("%A, %d %b %Y")} \n {ctx.author.created_at.strftime("%I:%M %p")}', inline=True)
        embed.add_field(
            name="Joined On", value=f'{ctx.author.joined_at.strftime("%A, %d %b %Y")} \n {ctx.author.joined_at.strftime("%I:%M %p")}', inline=True)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def hallolong(self, ctx, num: int): await ctx.send(f'Hall{"o"*num}')

    @commands.command()
    async def servercount(self, ctx):
        embed=discord.Embed(
            title = "I'm in " + str(len(self.client.guilds)) + " servers",
            description = "Invite the bot to your server today using the link from s!invite!",
            color = 0xBB2277
        )
        await ctx.send(embed=embed)

    @commands.command(name="help", description="Shows this help menu or information about a specific command if specified", usage="help")
    async def hallohelp(self, ctx, command: str = None):
        if command:
            command = self.client.get_command(command.lower())
            if not command:
                await ctx.send(
                    embed=discord.Embed(
                        title="Non-existant command",
                        description="This command cannot be found. Please make sure that everything is spelled correctly :D",
                        colour=self.client.primary_colour
                    )
                )
                return
            embed = discord.Embed(
                title=f'Command `{command.name}`',
                description=command.description,
                colour=self.client.primary_colour,
            )
            usage = "\n".join([ctx.prefix + x.strip() for x in command.usage.split('\n')])
            embed.add_field(name="Usage", value=f"```{usage}```", inline=False)
            if len(command.aliases) > 1:
                embed.add_field(name="Aliases", value=f"`{'`, `'.join(command.aliases)}`")
            elif len(command.aliases) > 0:
                embed.add_field(name="Alias", value=f"`{command.aliases[0]}`")
            await ctx.send(embed=embed)
            return
        pages = []
        page=discord.Embed(
            title="Maxi Game",
            description="MaxiGames Help Page! Press Next to see the commands!",
            colour=self.client.primary_colour
        )
        pages.append(page)


        page = discord.Embed(
            title="Commands!!!",
            description="See all commmands that MaxiGame has to offer :D",
            colour=self.client.primary_colour,
        )
        page.set_thumbnail(url=self.client.user.avatar_url)
        for _, cog_name in enumerate(self.client.cogs):
            if cog_name in ["Owner", "Staff", "Ban"]:
                continue
            cog = self.client.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            cmds = "```\n"
            for cmd in cog_commands:
                if cmd.hidden is False:
                    cmds += cmd.name + "\n"
            cmds += "```"
            page.add_field(name=cog_name, value=cmds)
        pages.append(page)

        # await ctx.send(embed=page)


        page_num = 0
        previous_symbol = "⬅️ Previous"
        next_symbol = "Next ➡️"
        msg = await ctx.send(
            embed=pages[page_num],
        )

        page = Paginator(self.client, ctx, msg, pages, timeout=5)
        await page.start()





def setup(client):
    client.add_cog(general(client))
