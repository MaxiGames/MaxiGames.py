import discord
from discord.ext import commands
from firebase_admin import firestore
from utils import check
import time
import copy


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.data = {}
        self.cooldown = {}
        self.init = self.client.get_cog("Init")
        self.hidden = False
        docs = self.db.collection("servers").stream()

    @check.is_admin()
    @commands.command(
        name="countingchanneladd",
        description="Sets a counting channel by specifing the channel",
        usage="counting-channel-add <channel-id>",
        aliases=["countca", "counting-channel-add"],
    )
    async def counting_channel_add(self, ctx, channelarg: str = None):
        # sets the key "counting_channel"
        if channelarg == None:
            channelarg = str(ctx.channel.id)

        try:
            t = int("".join(list(filter(str.isdigit, channelarg))))
            channel = t
            data = self.db.collection("servers").document(str(ctx.guild.id)).get().to_dict()

            init_channel_count = {"count": 0, "previous_author": None}

            if "counting_channels" not in data:
                data["counting_channels"] = {}
            
            ##
            chann = discord.utils.get(ctx.guild.channels, id=channel)
            if chann == None or not isinstance(chann, discord.channel.TextChannel):
                await ctx.reply(
                    embed=discord.Embed(
                        title="Error: channel does not exist, or is not a text channel."
                    )
                )
                return
            del chann
        except ValueError:
            await ctx.reply(
                embed=discord.Embed(
                    title="Error: channel does not exist, or is not a text channel."
                )
            )
            return

        if str(ctx.guild.id) in data["counting_channels"]:  # do not merge with and!
            if str(channel) not in data["counting_channels"][str(ctx.guild.id)]:
                data["counting_channels"][str(ctx.guild.id)][str(channel)] = copy.deepcopy(init_channel_count)
                data["counting_channels"][str(ctx.guild.id)]["counterUR"] = {}
                await ctx.reply(embed=discord.Embed(title="Success! Channel Added!"))
            else:
                await ctx.reply(
                    embed=discord.Embed(
                        title="Error: channel is already a counting channel."
                    )
                )

        else:
            data["counting_channels"] = {
                str(ctx.guild.id): {
                    str(channel): copy.deepcopy(init_channel_count),
                    "counterUR": {},
                }
            }
            await ctx.send("OK")

        self.db.collection("servers").document(str(ctx.guild.id)).set(data)

        return

    @check.is_admin()
    @commands.command(
        name="countingchannelrm",
        description="Remove a counting channe by specifying the channel name",
        usage="countingchannelrm <channel>",
        aliases=[
            "countcr",
            "countingchannelremove",
            "counting-channel-remove",
            "counting-channel-rm",
        ],
    )
    async def counting_channel_rm(self, ctx, channel: str = None):
        if channel == None:
            channel = str(ctx.channel.id)
        # sets the key "counting_channel"
        t = "".join(list(filter(str.isdigit, channel)))
        channel = t
        data = self.db.collection("servers").document(str(ctx.guild.id)).get().to_dict()

        if "counting_channels" not in data:
            return  # bruh

        if (
            str(ctx.guild.id) in data["counting_channels"]
            and str(channel) in data["counting_channels"][str(ctx.guild.id)]
        ):
            del data["counting_channels"][str(ctx.guild.id)][str(channel)]
            await ctx.reply(
                embed=discord.Embed(title="Channel is no longer a counting channel.")
            )
        else:
            await ctx.reply(
                embed=discord.Embed(
                    title="Channel never was a counting channel or doesn't exist. "
                )
            )

        self.db.collection("servers").document(str(ctx.guild.id)).set(data)

        return

    @commands.command(
        name="counting-leaderboard-user",
        description="Show the leaderboard for users in this server and your position",
        usage="counting-leaderboard-user",
        aliases=["countlu","countleaderboard"],
    )
    async def counting_leaderboard_user(self, ctx):
        data = self.db.collection("servers").document(str(ctx.guild.id)).get().to_dict()
        sortedUR = list(
            map(
                lambda x: (x[1], x[0]),
                sorted(
                    [(v, k) for k, v in data["counting_channels"][str(ctx.guild.id)]["counterUR"].items()],
                    reverse=True
                )
            )
        )
        if list(filter(lambda x: x[0] == str(ctx.author.id), sortedUR)) == []:
            await ctx.reply(
                embed=discord.Embed(
                    title="You haven't counted yet!",
                )
            )
        else:
            tmp = []
            for i, c in enumerate(sortedUR):
                cmemb = await ctx.guild.fetch_member(c[0])
                cnick = cmemb.nick if cmemb.nick != None else cmemb.name + "#" + cmemb.discriminator
                tmp.append(f"{('**' if int(c[0]) == ctx.author.id else '')}#{i+1}: {cnick} -- {c[1]}{('**' if int(c[0]) == ctx.author.id else '')}\n")

            rank = 0
            for i, c in enumerate(sortedUR):
                if c[0] == str(ctx.author.id):
                    rank = i + 1
                    break

            toprint = []
            if rank < 5 and rank > len(tmp):
                toprint = tmp
            elif rank < 5:
                toprint = tmp[0:rank+5]
            elif rank > len(tmp):
                toprint = tmp[rank-5:len(tmp)-1]

            await ctx.reply(
                embed = discord.Embed(
                    title=f"Your counting userrank is {rank}!",
                    description="".join(toprint)
                )
            )


        return

    @commands.Cog.listener()
    async def on_message(self, msg):
        
        data = self.db.collection("servers").document(str(msg.guild.id)).get().to_dict()
        
        if "counting_channels" not in data:
            return

        # check if things exists; initialise where it makes sense
        if "counterUR" not in data["counting_channels"][str(msg.guild.id)]:
            data["counting_channels"][str(msg.guild.id)]["counterUR"] = {}

        try:
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]
        except KeyError:
            return  # no counting channels set up for this server

        numinter = ""
        for x in msg.content:
            if str.isdigit(x):
                numinter += x
            else:
                break
        if numinter == "":
            return  # no number
        num = int(numinter)

        ccount = data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["count"]
        if (
            num == ccount + 1
            and data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["previous_author"] != msg.author.id
        ):
            await msg.add_reaction("✅")
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)][
                "count"
            ] = num
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)][
                "previous_author"
            ] = msg.author.id
            try:
                # update user's counter userrank
                data["counting_channels"][str(msg.guild.id)]["counterUR"][str(msg.author.id)] += 1
            except KeyError:
                # initialise user's counter userrank
                data["counting_channels"][str(msg.guild.id)]["counterUR"][str(msg.author.id)] = 1
        else:
            await msg.add_reaction("❌")
            if num != ccount + 1:
                await msg.reply(
                    embed=discord.Embed(
                        title="Wrong count",
                        description=f"{msg.author.mention} messed up the count at {ccount}. The next count for this server is 1.",
                    )
                )
            else:
                await msg.reply(
                    embed=discord.Embed(
                        title="You cannot count twice in a row",
                        description=f"{msg.author.mention} messed up the count at {ccount}. The next count for this server is 1.",
                    )
                )

            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["count"] = 0
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["previous_author"] = None

        self.db.collection("servers").document(str(msg.guild.id)).set(data)
        return


def setup(client):
    client.add_cog(Counting(client))
