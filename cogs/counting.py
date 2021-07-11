import discord
from discord.ext import commands
from firebase_admin import firestore
from utils import check
import time


class Counting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.data = {}
        self.cooldown = {}
        self.initation = self.client.get_cog("Initiation")
        docs = self.db.collection(u'servers').stream()
        for doc in docs:
            self.data[doc.id] = doc.to_dict()
            self.cooldown[doc.id] = {}
            for channel in self.data[doc.id]["countingChannels"]:
                self.cooldown[doc.id][channel] = time.time()-5


    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author == self.client.user:
            return
        if(message.author.bot):
            return
        self.data = await self.initation.checkserver(message, self.data)
        # print(self.data)
        if message.channel.name.lower() in self.data[str(message.guild.id)]["countingChannels"]:
            string = message.content.lower()
            string = string.split(" ")[0]
            string = string.split("_")[0]
            string = string.split("*")[0]
            # print(string)
            if string.isdigit():
                dict2 = self.data[(str(message.guild.id))]
                num = int(string)
                # print(dict2)
                if not (num == dict2["countingChannels"][message.channel.name.lower()]["count"]+1) or (message.author.id == dict2["countingChannels"][message.channel.name.lower()]["last_user"]):
                    wrongCount = not (
                        num == dict2["countingChannels"][message.channel.name.lower()]["count"]+1)
                    previous = dict2["countingChannels"][message.channel.name.lower(
                    )]["count"]
                    dict2["countingChannels"][message.channel.name.lower()
                                              ]["count"] = 0
                    dict2["countingChannels"][message.channel.name.lower()
                                              ]["last_user"] = None
                    self.data[str(message.guild.id)] = dict2
                    await message.add_reaction("❌")
                    if wrongCount:
                        embed = discord.Embed(
                            title="Wrong Count",
                            description=f"{message.author.mention} messed up the count at **{previous}**. The next count for this server is **1**.",
                            colour=self.client.primary_colour
                        )
                    else:
                        embed = discord.Embed(
                            title="You cannot count twice in a row",
                            description=f"{message.author.mention} messed up the count at **{previous}**. The next count for this server is **1**.",
                            colour=self.client.primary_colour
                        )
                    await message.channel.send(embed=embed)

                    self.cooldown[str(message.guild.id)
                                  ][message.channel.name.lower()] = time.time()
                    # await message.channel.edit(topic=f"Count: {dict2['count']}")

                else:
                    if ((time.time()-self.cooldown[str(message.guild.id)][message.channel.name.lower()]) < 2):
                        return
                    if (num > dict2["countingChannels"][message.channel.name.lower()]["highest_count"]):
                        dict2["countingChannels"][message.channel.name.lower()
                                                  ]["highest_count"] = num
                        dict2["countingChannels"][message.channel.name.lower()
                                                  ]["count"] = num
                        dict2["countingChannels"][message.channel.name.lower(
                        )]["last_user"] = message.author.id
                        self.data[str(message.guild.id)] = dict2
                        await message.add_reaction("☑️")
                        # await message.channel.edit(topic=f"Count: {dict2['count']}")
                    else:
                        dict2["countingChannels"][message.channel.name.lower()
                                                  ]["count"] = num
                        dict2["countingChannels"][message.channel.name.lower(
                        )]["last_user"] = message.author.id
                        self.data[str(message.guild.id)] = dict2
                        await message.add_reaction("✅")
                self.db.collection(u'servers').document(
                    str(message.guild.id)).set(dict2)

    @check.is_admin()
    @commands.command(name="Add Channel")
    async def add_counting_channel(self, ctx, name: str = None):
        self.data = await self.initation.checkserver(ctx, self.data)
        if name == None:
            name = ctx.channel.name
        # BUG WARNING
        dict1 = self.data[str(ctx.guild.id)]
        dict1["countingChannels"][name] = {
            "name": name,
            "count": 0,
            "highest_count": 0,
            "last_user": None
        }
        self.data[str(ctx.guild.id)] = dict1
        self.cooldown[str(ctx.guild.id)
                      ][ctx.channel.name.lower()] = time.time()-5
        self.db.collection(u'servers').document(str(ctx.guild.id)).set(dict1)

        embed = discord.Embed(
            title="Counting Channel Added",
            description=f"The channel **{name}** has been added as a counting channel.",
            colour=self.client.primary_colour
        )
        await ctx.send(embed=embed)

    @check.is_admin()
    @commands.command(name="Remove Channel")
    async def remove_counting_channel(self, ctx, name: str = None):
        self.data = await self.initation.checkserver(ctx, self.data)
        if name == None:
            name = ctx.channel.name
        # BUG WARNING
        dict1 = self.data[str(ctx.guild.id)]
        if name not in dict1["countingChannels"]:
            embed = discord.Embed(
                title="Command not in list",
                description="This channel is not originally a counting channel.",
                colour=self.client.error_colour
            )
            await ctx.send(embed=embed)
            return
        dict1["countingChannels"].pop(name)
        self.data[str(ctx.guild.id)] = dict1
        self.db.collection(u'servers').document(str(ctx.guild.id)).set(dict1)

        embed = discord.Embed(
            title="Counting Channel Removed",
            description=f"The channel **{name}** has been removed from being as a counting channel.",
            colour=self.client.primary_colour
        )
        await ctx.send(embed=embed)

    @check.is_staff()
    @commands.command(
        name="Set Count", aliases=["setcount"], description="Sets the current count in the current channel.", usage="setcount <number>", hidden=True
    )
    async def setcurrentcount(self, ctx, num: int):
        self.data = await self.initation.checkserver(ctx, self.data)

        dict2 = self.data[(str(ctx.guild.id))]
        if str(ctx.channel.name.lower()) not in dict2["countingChannels"]:
            embed = discord.Embed(
                title="Channel not a counting channel",
                description="The channel you are in now is not a counting channel. If you want to make this a counting channel, please use the add-counting-channel command.",
                colour=self.client.primary_colour
            )
            await ctx.send(embed=embed)
            return
        dict2["countingChannels"][ctx.channel.name.lower()]["highest_count"] = max(
            dict2["countingChannels"][ctx.channel.name.lower()]["highest_count"], num)
        dict2["countingChannels"][ctx.channel.name.lower()]["count"] = num
        dict2["countingChannels"][ctx.channel.name.lower()]["last_user"] = None
        self.data[str(ctx.guild.id)] = dict2
        self.db.collection(u'servers').document(str(ctx.guild.id)).set(dict2)

        embed = discord.Embed(
            title="Current Count Set",
            description=f"The count in this server has been set by {ctx.author.name} to **{num}**. The next count is **{num+1}**.",
            colour=self.client.primary_colour
        )
        await ctx.send(embed=embed)

    @commands.command(name="Counting Channel Info",
                      description="Returns info about the current channel and counting statistics.",
                      usage="countingchannel", aliases=["csi", "cs", "countingchanne;"]
                      )
    async def channelcountinginfo(self, ctx):
        embed = discord.Embed(
            title=f"Info about the **{ctx.channel.name}** channel",
            description=f"Find all the info you need about this channel you are currently in :D",
            colour=self.client.primary_colour
        )
        embed.add_field(name="Statistics", value=f"""
        Current Count: {self.data[str(ctx.guild.id)]['countingChannels'][ctx.channel.name.lower()]['count']}
        Highest Score: {self.data[str(ctx.guild.id)]['countingChannels'][ctx.channel.name.lower()]['highest_count']}

        Last counted by <@{self.data[str(ctx.guild.id)]['countingChannels'][ctx.channel.name.lower()]['last_user']}>
        """, inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        name="Counting Info",
        description="Shows the statistics of all counting channels in the current server.",
        usage="countinfo", aliases=["ci", "countinfo"]
    )
    async def countinginfo(self, ctx):
        embed = discord.Embed(
            title="Shows the respective counts of the channels :D",
            description="Ever wondered where you could easily keep track of how other counting channels are doing?",
            colour=self.client.primary_colour
        )
        leaderboard = {}
        for i in self.data[str(ctx.guild.id)]["countingChannels"]:
            leaderboard[i] = [self.data[str(ctx.guild.id)]["countingChannels"][i]["count"], self.data[str(
                ctx.guild.id)]["countingChannels"][i]["highest_count"]]
        count = 0
        description = ""
        for i in sorted(leaderboard.items(), key=lambda kv: (kv[1]), reverse=True):
            # embed.add_field(name=)
            embed.add_field(
                name=i[0], value=f"Highest Count: {i[1][1]}\nCount: {i[1][0]}", inline=False)
            count += 1
            if count > 10:
                break

        await ctx.send(embed=embed)

    @commands.command(
        name="Counting Leaderboards",
        description="The very best of all counting channels from all servers.",
        usage="countingl",
        aliases=["cl", "countingl", "cleaderb", "cleaderboards"]
    )
    async def countingleader(self, ctx):
        leaderboard = {}
        for i in self.data:
            highest = 0
            for p in self.data[i]["countingChannels"]:
                highest = max(
                    highest, self.data[i]["countingChannels"][p]["highest_count"])
            leaderboard[self.data[i]["name"]] = highest
        count = 1
        description = ""
        for i in sorted(leaderboard.items(), key=lambda kv: (kv[1]), reverse=True):
            description += (f"{count}. **{i[0]}** - *{i[1]}*" + '\n')
            count += 1
            if count > 10:
                break

        embed = discord.Embed(
            title="Global leaderboard :D",
            description=description,
            colour=self.client.primary_colour
        )
        embed.set_footer(
            text="Find out about the highest and most dedicated servers!!!")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Counting(client))
