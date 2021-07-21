import discord
import time
from discord.ext import commands
from discord_components import *
import asyncio
import math
import random
from discord_slash import cog_ext, SlashContext
from utils.paginator import Paginator
from utils import check
from firebase_admin import firestore

class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dates = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        self.hidden = False
        self.client = client
        self.db = firestore.client()
        self.init = self.client.get_cog("Init")

    @commands.command()
    async def hallo(self, ctx):
        await ctx.send("Hallo")

    @commands.command()
    async def current(self, ctx):
        result = time.localtime(time.time())
        embed = discord.Embed(
            title="Current Date and Time",
            description=f"Find the current date and time below :D",
            colour=self.client.primary_colour,
        )

        embed.add_field(
            name="Date",
            value=f"{result.tm_mday}/{result.tm_mon}/{result.tm_year}",
            inline=True,
        )
        embed.add_field(name="Day", value=self.dates[result.tm_wday], inline=True)
        embed.add_field(
            name="Time",
            value=f"{result.tm_hour}:{result.tm_min}:{result.tm_sec}",
            inline=True,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def seconds(self, ctx):
        await ctx.send(
            str(round(time.time())) + " seconds have passed since the epoch!"
        )

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
        embed = discord.Embed(
            title="Invite Link to invite the bot",
            description="https://discord.com/api/oauth2/authorize?client_id=863419048041381920&permissions=8&scope=bot",
            color=self.client.primary_colour,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def official(self, ctx):
        embed = discord.Embed(
            title="Join our official server today!",
            description="https://discord.gg/nGWhxNG2sf",
            colour=self.client.primary_colour,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def whoami(self, ctx):
        embed = discord.Embed(
            title="You are " + str(ctx.author) + " :D",
            description="What a pog name!!!",
            color=self.client.primary_colour,
        )
        role = ""  # theres probably some way to optimise this...
        for i in ctx.author.roles[::-1]:
            if i.name != "@everyone":
                role += f"{i.mention} "
        embed.add_field(name="Roles", value=role, inline=True)
        embed.add_field(
            name="Created On",
            value=f'{ctx.author.created_at.strftime("%A, %d %b %Y")} \n {ctx.author.created_at.strftime("%I:%M %p")}',
            inline=True,
        )
        embed.add_field(
            name="Joined On",
            value=f'{ctx.author.joined_at.strftime("%A, %d %b %Y")} \n {ctx.author.joined_at.strftime("%I:%M %p")}',
            inline=True,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def hallolong(self, ctx, num: int):
        await ctx.send(f'Hall{"o"*num}')

    @commands.command()
    async def servercount(self, ctx):
        embed = discord.Embed(
            title="I'm in " + str(len(self.client.guilds)) + " servers",
            description="Invite the bot to your server today using the link from s!invite!",
            color=0xBB2277,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="help",
        description="Shows this help menu or information about a specific command if specified",
        usage="help <command (optional)> ",
    )
    async def help(self, ctx, *cmd):
        if len(cmd) > 0:
            command = " ".join(cmd)
            command = self.client.get_command(command.lower())
            if not command:
                await ctx.send(
                    embed=discord.Embed(
                        title="Non-existant command",
                        description="This command cannot be found. Please make sure that everything is spelled correctly :D",
                        colour=self.client.primary_colour,
                    )
                )
                return
            embed = discord.Embed(
                title=f"Command `{command.name}`",
                description=command.description,
                colour=self.client.primary_colour,
            )
            usage = "\n".join(
                [ctx.prefix + x.strip() for x in command.usage.split("\n")]
            )
            embed.add_field(name="Usage", value=f"```{usage}```", inline=False)
            if len(command.aliases) > 1:
                embed.add_field(
                    name="Aliases", value=f"`{'`, `'.join(command.aliases)}`"
                )
            elif len(command.aliases) > 0:
                embed.add_field(name="Alias", value=f"`{command.aliases[0]}`")
            await ctx.send(embed=embed)
            return
        pages = []
        page = discord.Embed(
            title="Help",
            description="""Halloooo and thank you for using Maxigames, a fun, random, cheerful and gambling-addiction-curbing bot developed as part of an initiative to curb gambling addiction and fill everyones' lives with bad puns, minigames and happiness!!!

            Feel free to invite this bot to your own server from the link below, or even join our support server, if you have any questions or suggestions :D""",
            colour=self.client.primary_colour,
        )
        page.set_author(
            name=self.client.user.name, icon_url=self.client.user.avatar_url
        )
        page.set_footer(text="Press Next to see the commands :D")
        pages.append(page)

        page = discord.Embed(
            title="Commands!!!",
            description="See all commmands that MaxiGame has to offer :D",
            colour=self.client.primary_colour,
        )
        page.set_thumbnail(url=self.client.user.avatar_url)
        for _, cog_name in enumerate(self.client.cogs):
            cog = self.client.get_cog(cog_name)
            if cog.hidden is True:
                continue
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
        buttons = [
            [
                Button(
                    style=ButtonStyle.URL,
                    label="Invite :D",
                    url="https://discord.com/api/oauth2/authorize?client_id=863419048041381920&permissions=8&scope=bot%20applications.commands",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Support Server!!!",
                    url="https://discord.gg/BNm87Cvdx3",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Vote :)",
                    url="https://top.gg/bot/863419048041381920",
                ),
            ]
        ]
        page = Paginator(self.client, ctx, msg, pages, buttons=buttons, timeout=60)
        await page.start()

    @cog_ext.cog_slash(name="help", description="Shows the help menu :D")
    async def help_command(self, ctx: SlashContext):
        await self.help(ctx)

    @commands.command(
        name="randnum",
        description="Gives you a random number between the two numbers you specified.",
        usage="randnum <minimum number> <maximum number>",
    )
    async def randnum(self, ctx, start: int, end: int):
        answer = random.randint(start, end)
        await ctx.reply("Your number was " + str(answer))

    @commands.command()
    async def empty(self, ctx):
        await ctx.reply("‎")

    @commands.command(
        name="fibo",
        description="Returns the nth fibonacci number, where n is the number you input.",
        usage="fibo <number>",
    )
    async def fibo(self, ctx, num: int):
        if num <= 0:
            embed = discord.Embed(
                title="Bruh. Don't be stupid.", description="", color=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif num == 1:
            embed = discord.Embed(
                title="The 1st fibonacci number is 1!",
                description="",
                color=self.client.primary_colour,
            )
            await ctx.reply(embed=embed)
        elif num == 2:
            embed = discord.Embed(
                title="The 2nd fibonacci number is 1!",
                description="",
                color=self.client.primary_colour,
            )
            await ctx.reply(embed=embed)
        elif num <= 1000:
            fibo1 = 1
            fibo2 = 2
            for i in range(num - 3):
                currfibo1 = fibo1
                fibo1 = fibo2
                fibo2 += currfibo1
            embed = discord.Embed(
                title="The " + str(num) + "th fibonacci number is " + str(fibo2) + "!",
                description="",
                color=self.client.primary_colour,
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Make it smaller, stop trying to break me.",
                description="",
                color=0xFF0000,
            )
            await ctx.reply(embed=embed)

    @commands.command(
        name="bigdice",
        description="rolls a specified number of dice with a specified number of faces that you can specify.",
        usage="bigdice <number of faces for each dice> <number of dice>",
    )
    async def bigdice(self, ctx, sides: int, num: int):
        curr = ""
        if sides <= 0:
            embed = discord.Embed(
                title="What kind of dice is this?", description="", color=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif sides == 1:
            embed = discord.Embed(
                title="What's the point of rolling a die if it's always gonna come out on the same side?",
                description="",
                color=0xFF0000,
            )
            await ctx.reply(embed=embed)
        elif sides >= 1000:
            embed = discord.Embed(
                title=str(sides)
                + " sides?!?! Come back to me when you make this die. Seriously why.",
                description="Bruh",
                color=0xFF0000,
            )
            await ctx.reply(embed=embed)

        elif num <= 0:
            embed = discord.Embed(
                title="Don't be stupid. Honestly.", description="", color=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif num <= 100:
            for i in range(num):
                curr += str(random.randint(1, sides))
                curr += " "
            embed = discord.Embed(
                title="Your dice roll results came out!",
                description=curr,
                color=self.client.primary_colour,
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Don't be stupid. Honestly.", description="", color=0xFF0000
            )
            await ctx.reply(embed=embed)

    @commands.command(
        name="dice",
        description="rolls the number of dice you specify.",
        usage="dice <number of dice>",
    )
    async def dice(self, ctx, num: int):
        curr = ""
        if num <= 0:
            embed = discord.Embed(
                title="Don't be stupid. Honestly.", description="", color=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif num <= 100:
            for i in range(num):
                curr += str(random.randint(1, 6))
                curr += " "
            embed = discord.Embed(
                title="Your dice roll results came out!",
                description=curr,
                color=self.client.primary_colour,
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Don't be stupid. Honestly.", description="", color=0xFF0000
            )
            await ctx.reply(embed=embed)

    @commands.command(
        name="numprop",
        description="tells you the property of a number you specify!",
        usage="numprop <number>",
    )
    async def numprop(self, ctx, num: int):

        if num > 1000000000000:
            embed = discord.Embed(
                title="Bruh. I'm not going to waste my time trying to find out more about that big guy.",
                description="",
                color=0xFF0000,
            )
            await ctx.reply(embed=embed)
            return
        elif num < 0:
            embed = discord.Embed(
                title="Hey. I won't evaluate negative numbers for you.",
                description="",
                color=0xFF0000,
            )
            await ctx.reply(embed=embed)
            return
        embed = discord.Embed(
            title="Thinking... :thinking::thinking::thinking:",
            description="",
            color=0xFFFF00,
        )
        message = await ctx.reply(embed=embed)
        embed = discord.Embed(
            title="The number ", description="", color=self.client.primary_colour
        )
        if num == 0:
            embed.add_field(
                name="This number, when added to anything, gives the thing you added it to!",
                value="HoW iNtErEsTiNg!",
                inline=True,
            )
        root = math.sqrt(num)
        if int(root + 0.5) ** 2 == num:
            embed.add_field(name="Perfect Square!", value="Fascinating.", inline=True)
        if num % 2 == 0:
            embed.add_field(
                name="Even!", value="Also known as a multiple of 2!", inline=True
            )
        else:
            embed.add_field(
                name="Odd!", value="It is not a multiple of 2!", inline=True
            )
        flag = False
        if num > 1:
            # check for factors
            for i in range(2, math.ceil(root) + 1):
                if i != num:
                    if (num % i) == 0:
                        flag = True
                        break

        if not flag and num == 1:
            embed.add_field(
                name="Not prime and not composite!",
                value="That's special!",
                inline=True,
            )
        elif not flag and num == 0:
            embed.add_field(
                name="Not prime and not composite!",
                value="That's special!",
                inline=True,
            )
        elif flag:
            embed.add_field(
                name="Composite!",
                value="That means that it has more than 2 factors!",
                inline=True,
            )
        else:
            embed.add_field(name="Prime!", value="Ooh!", inline=True)
        if "69420" in str(num):
            embed.add_field(
                name="VERRRRYYYYYYY SUSSSSSS!!!",
                value="That's because it contains :six::nine::four::two::zero: in it!!!!!!",
                inline=True,
            )
        elif "69" in str(num):
            embed.add_field(name="SUS!", value="because it contains 69!!!", inline=True)
        elif "420" in str(num):
            embed.add_field(
                name="SUS!", value="because it contains 420!!!", inline=True
            )
        res = str(num) == str(num)[::-1]
        if res:
            embed.add_field(
                name="Palindrome!",
                value="Reads same forwards and backwards!",
                inline=True,
            )
        time.sleep(1)
        await message.edit(embed=embed)

    @commands.command(
        name="lmgtfy",
        description="Command that creats a Let Me Google That For You link for all your queries!",
        usage="lmgtfy",
    )
    async def lmgtfy(self, ctx, *quer: str):
        curr_url = "https://lmgtfy.app/?q="
        query = " ".join(quer)
        query = query.replace(" ", "+")
        curr_url += query
        embed = discord.Embed(
            title=curr_url,
            description="Let Me Google That For You!",
            color=self.client.primary_colour,
        )
        await ctx.reply(embed=embed)

    @commands.command(
        name="choose",
        description="Chooses a random choice from the set of words given",
        usage="choose <choices space-separated>",
    )
    async def choose(self, ctx, *choices: str):
        chosen = random.choice(choices)
        embed = discord.Embed(
            title=chosen + " was chosen!",
            description="Poggers!",
            color=self.client.primary_colour,
        )
        await ctx.reply(embed=embed)

    @commands.command(
        name="kawaii",
        description="Makes what you say kawaii <3",
        usage="kawaii <message>",
    )
    async def kawaii(self, ctx, *msg: str):
        words = " ".join(msg)
        final = ""
        previous_char = ""
        for i in words:
            if i == "s" == previous_char:
                continue
            elif i == "h" and previous_char == "s":
                continue
            elif i == "z" == previous_char:
                continue
            elif i == "h" and previous_char == "z":
                continue
            else:
                final += i
                previous_char = i
        new = final
        first_time = 1 
        while new != final or first_time == 1:
            first_time = 0
            final = new
            new = final.replace("zz","z").replace("ss","s")
        final = new
        final = (
            final.replace("sh","s")
            .replace("zh","z")
            .replace("s", "sh")
            .replace("z", "zh")
            .replace("rr", "ww")
            .replace("nine", "9")
            .replace("four", "4")
            .replace("one", "1")
        )
        if final[-1] == "y":
            final = final[:-1] + "ie"

        await ctx.reply(final)

    @commands.command(
        name="getsettings",
        description="Views current MaxiGames settings :D",
        usage="getsettings",
        aliases=["gs", "tux"],
    )
    @check.is_staff()
    async def getsettings(self, ctx):
        self.init = self.client.get_cog("Init")
        await self.init.checkserver(ctx)
        doc_ref = self.db.collection("servers").document(str(ctx.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()

        m = ""
        for k, v in data.items():
            m += (f"\n**{k}**:\n {v}\n")

        await ctx.send(m)


def setup(client):
    client.add_cog(General(client))
