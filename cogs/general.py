import discord
import time
from discord.ext import commands
from discord_components import *
import asyncio
import math
import random
from discord_slash import cog_ext, SlashContext
from discord.ext.commands import cooldown, BucketType
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
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        doc_ref = self.db.collection(u'servers').document(str(guild.id))
        data = {
            u"users": {},
            u"all": {},
            u"starboard_threshold": 1,
            u"counting_channels": {},
            u"name": str(guild.name),
            u"prefix": [self.client.primary_prefix],
            u'autoresponses': {}
        }
        doc_ref.set(data)
        await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="m!help on " + str(len(self.client.guilds)) + " servers", type=0
        ),
    )
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        doc_ref = self.db.collection(u'servers').document(str(guild.id))
        doc_ref.delete()
        await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="m!help on " + str(len(self.client.guilds)) + " servers", type=0
        ),
    )
        

    @commands.command()
    @cooldown(1, 60, BucketType.user)
    async def hallo(self, ctx):
        await ctx.send("Hallo!")

    @commands.command()
    @cooldown(1, 60, BucketType.user)
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
    @cooldown(1, 100, BucketType.user)
    async def seconds(self, ctx):
        await ctx.send(
            str(round(time.time())) + " seconds have passed since the epoch!"
        )
    @commands.command(
        name="ns",
        description="Makes an intriguing triangle made of ^ symbols.",
        usage = "",
        aliases = ["triangle","notstonks"]
    )
    @cooldown(1, 15, BucketType.user)
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
    @commands.command(
        name="invite",
        description="Gives you a link for you to invite the bot to your server!",
        usage=""
    )
    @cooldown(1, 20, BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite Link to invite the bot",
            description="https://discord.com/api/oauth2/authorize?client_id=863419048041381920&permissions=261188091120&scope=bot%20applications.commands",
            color=self.client.primary_colour,
        )
        await ctx.send(embed=embed)
    @commands.command(
        name="official",
        description="Gives you a discord invite link to the bot's official server!",
        usage = ""
    )
    @cooldown(1, 20, BucketType.user)
    async def official(self, ctx):
        embed = discord.Embed(
            title="Join our official server today!",
            description="https://discord.gg/nGWhxNG2sf",
            colour=self.client.primary_colour,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="whoami",
        description="Gives a bit of information about you",
        usage=""
    )
    @cooldown(1, 60, BucketType.user)
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
    @cooldown(1, 15, BucketType.user)
    async def hallolong(self, ctx, num: int):
        if num > 1996:
            await ctx.send(f'Too long!')
        await ctx.send(f'Hall{"o"*num}')

    @commands.command(
        name="servercount",
        description="Shows how many servers the bot is in :D",
        usage = ""
    )
    @cooldown(1, 60, BucketType.user)
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
    @cooldown(1, 5, BucketType.user)
    async def help(self, ctx, *cmd):
        if len(cmd) > 0:
            command = " ".join(cmd)
            print(command)
            command = self.client.get_command(command.lower())
            if not command:
                # ! Specified command not found
                await ctx.send(
                    embed=discord.Embed(
                        title="Non-existant command",
                        description="This command cannot be found. Please make sure that everything is spelled correctly :D",
                        colour=self.client.primary_colour,
                    )
                )
                return
            #! Command found 

            if (isinstance(command, commands.Group)):
                print(command.name)
                print(command.commands)
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
        #! No command specified, thus giving a list of all the commands
        pages = []
        page = discord.Embed(
            title="Help",
            description="""Hallo! Thank you for using Maxigames, a fun, random, cheerful and gambling-addiction-curbing bot developed as part of an initiative to curb gambling addiction and fill everyones' lives with bad puns, minigames and happiness!!!

            Feel free to invite this bot to your own server from the link below, or even join our support server, if you have any questions or suggestions :D""",
            colour=self.client.primary_colour,
        )
        page.set_author(
            name=self.client.user.name, icon_url=self.client.user.avatar_url
        )
        page.set_footer(text="Press Next to see the commands")
        pages.append(page)

        page = discord.Embed(
            title="Commands",
            description="See all commmands that MaxiGame has to offer",
            colour=self.client.primary_colour,
        )
        page.set_thumbnail(url=self.client.user.avatar_url)

        totalCount = 0
        for _, cog_name in enumerate(self.client.cogs):
            cog = self.client.get_cog(cog_name)
            if cog.hidden is True:
                continue
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            count  = 0
            cmds = "```\n"
            for cmd in cog_commands:
                # print(type(cmd))
                count += 1
                if cmd.hidden is False:
                    cmds += cmd.name + "\n"
            cmds += "```"

            print(cog_name)
            if count > 20:
                #! if amount of commands on its own is too much to fit in one page, have its own page
                pages.append(page)
                # give it its on page
                page = discord.Embed(
                    title="Commands",
                    description="See all commands that MaxiGame has to offer",
                    colour=self.client.primary_colour,
                )
                page.add_field(name=cog_name, value=cmds)
                page.set_thumbnail(url=self.client.user.avatar_url)
                pages.append(page)
                
                # reset page
                page = discord.Embed(
                    title="Commands",
                    description="See all commands that MaxiGame has to offer",
                    colour=self.client.primary_colour,
                )
                page.set_thumbnail(url=self.client.user.avatar_url)
                totalCount = 0
            elif totalCount + count > 20:
                #! if amount of commands is too much to fit in one page, make a new page
                pages.append(page)
                totalCount = count
                page = discord.Embed(
                    title="Commands",
                    description="See all commands that MaxiGame has to offer",
                    colour=self.client.primary_colour,
                )
                page.add_field(name=cog_name, value=cmds)
                page.set_thumbnail(url=self.client.user.avatar_url)
            else:
                page.add_field(name=cog_name, value=cmds)
                totalCount += count

        pages.append(page)
        page_num = 0
        msg = await ctx.send(
            embed=pages[page_num],
        )
        buttons = [
            [
                Button(
                    style=ButtonStyle.URL,
                    label="Invite the bot!",
                    url="https://discord.com/api/oauth2/authorize?client_id=863419048041381920&permissions=261188091120&scope=bot%20applications.commands",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Join support server!",
                    url="https://discord.gg/BNm87Cvdx3",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Vote for us!",
                    url="https://top.gg/bot/863419048041381920",
                ),
            ]
        ]
        page = Paginator(self.client, ctx, msg, pages, buttons=buttons, timeout=60)
        await page.start()

    @commands.command(
        name="randnum",
        help="Gives you a random number between the two numbers you specified.",
        usage="<minimum number> <maximum number>",
    )
    @cooldown(1, 5, BucketType.user)
    async def randnum(self, ctx, start: int, end: int):
        answer = random.randint(start, end)
        await ctx.reply("Your number was " + str(answer))

    @commands.command(
        name = "empty",
        help = "Gives you an empty unicode character.",
        usage = ""
    )
    @cooldown(1, 5, BucketType.user)
    async def empty(self, ctx):
        await ctx.reply("‎")

    @commands.command(
        name="fibo",
        help="Returns the nth fibonacci number, where n is the number you input.",
        usage="<number>",
    )
    @cooldown(1, 5, BucketType.user)
    async def fibo(self, ctx, num: int):
        if num <= 0:
            embed = discord.Embed(
                title="Bruh. Don't be stupid.", 
                description="", 
                color = 0xff0000
            )
            await ctx.reply(embed=embed)
        elif num == 1:
            embed = discord.Embed(
                title="The 1st fibonacci number is 1!",
                description="",
                color=discord.Color.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
            )
            await ctx.reply(embed=embed)
        elif num == 2:
            embed = discord.Embed(
                title="The 2nd fibonacci number is 1!",
                description="",
                color=discord.Color.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
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
                title="That number is too big!",
                description="",
                color=0xFF0000,
            )
            await ctx.reply(embed=embed)

    @commands.command(
        name="bigdice",
        help="rolls a specified number of dice with a specified number of faces that you can specify.",
        usage="<number of faces for each dice> <number of dice>",
    )
    @cooldown(1, 10, BucketType.user)
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
                title="That's too many sides for a die!",
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
        help="rolls the number of dice you specify.",
        usage="<number of dice>",
    )
    @cooldown(1, 10, BucketType.user)
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
        help="tells you the property of a number you specify!",
        usage="<number>",
    )
    @cooldown(1, 5, BucketType.user)
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
        help="Command that creats a Let Me Google That For You link for all your queries!",
        usage="",
    )
    @cooldown(1, 30, BucketType.user)
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
        help="Chooses a random choice from the set of words given",
        usage="<choices space-separated>",
    )
    @cooldown(1, 5, BucketType.user)
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
        help="Makes what you say kawaii <3",
        usage="<message>",
    )
    @cooldown(1, 10, BucketType.user)
    async def kawaii(self, ctx, *msg: str):
        words = " ".join(msg)
        upper_or_lower = []
        
        final = ""
        previous_char = ""
        for i in words:
            i = i.lower()

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
        help="Views current MaxiGames settings :D",
        usage="",
        aliases=["gs", "tux"],
    )
    @check.is_staff()
    @cooldown(1, 30, BucketType.user)
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

    @commands.command(
        name="randcol",
        help = "Gives you an embed with a random color :D",
        usage = "",
        aliases=["randomcol","randomcolor","randomcolour","randcolour","randcolor"]
    )
    @cooldown(1,15,BucketType.user)
    async def randcol(self,ctx):
        embed = discord.Embed(title="Random Color!",description="",color=discord.Colour.random())
        await ctx.reply(embed=embed)
    @cooldown(1,10,BucketType.user)
    @commands.command(
        name="ship",
        help="How well do two things (names, objects, discord tags etc.) fit together based on complements, similarity and length difference",
        usage="[name1] [name2]",
        aliases=["matchmake","matchmaking","match"]
    )
    async def ship(self,ctx,fne:str,sne:str):
        
        fn=""
        sn=""
        alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
        for i in fne:
            if i not in "abcdefghijklmnopqrstuvwxyz0123456789":
                i = alpha[ord(i)%36]
                
            fn += i
        for i in sne:
            if i not in "abcdefghijklmnopqrstuvwxyz0123456789":
                i = alpha[ord(i)%36]
                
            sn += i
        total_mismatch = 0
        length_to_do = min(len(fn),len(sn))
        for i in range(length_to_do):
            alpha_index = alpha.index(fn[i])
            distance = min(alpha.index(sn[i])-alpha_index,abs(35-alpha.index(sn[i])-alpha_index))
            total_mismatch += distance
        percentage_match = round((35*length_to_do - total_mismatch)/(35*length_to_do)*100*min(len(fn),len(sn))/max(len(fn),len(sn)))
        
        embed=discord.Embed(
            title="Ship results",
            description="Ship between " + str(fne) + " and " + str(sne) + ":\n**" + str(percentage_match) + "%**!",
            color=self.client.primary_colour
        )
        await ctx.reply(embed=embed)

    @commands.command(
        name="vote",
        help="Voting link to vote the bot",
        usage="",
        aliases=["v","upvote"]
    )
    @cooldown(1, 10, BucketType.user)
    async def vote(self, ctx):
        await ctx.send(
            "**Vote**\n"
            "https://top.gg/bot/863419048041381920/vote"
        )
def setup(client):
    client.add_cog(General(client))
