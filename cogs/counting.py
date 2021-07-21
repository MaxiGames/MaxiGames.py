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
        self.init = self.client.get_cog("Init")
        docs = self.db.collection("servers").stream()
        for doc in docs:
            self.data[doc.id] = doc.to_dict()
            self.cooldown[doc.id] = {}
            for channel in self.data[doc.id]["countingChannels"]:
                self.cooldown[doc.id][channel] = time.time() - 5
        self.hidden = False

    @commands.command(
        name="counting-channel",
        description="set a counting channel. NOT NAME BUT ID!",
        usage="m!counting-channel #channel-id",
        aliases=["countc"],
    )
    async def counting_channel(self, ctx, channel: str):
        # sets the key "counting_channel"
        t = "".join(list(filter(str.isdigit, channel)))
        channel = t
        data = self.db.collection("servers").document(str(ctx.guild.id)).get().to_dict()

        if "counting_channels" not in data:
            data["counting_channels"] = {}  # bruh...

        if ctx.guild.id in data["counting_channels"]:  # do not merge with and!
            if channel not in data["counting_channels"][ctx.guild.id]:
                data["counting_channels"][ctx.guild.id][channel] = {
                    "count": 0,
                    "previous-author": None,
                }
                await ctx.send("OK")
            else:
                await ctx.send("Bruh")

        else:
            data["counting_channels"] = {str(ctx.guild.id): {str(channel): {"count": 0}}}
            await ctx.send("OK")

        self.db.collection("servers").document(str(ctx.guild.id)).set(data)

        return

    @commands.Cog.listener()
    async def on_message(self, msg):
        data = self.db.collection("servers").document(str(msg.guild.id)).get().to_dict()

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
            and data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["previous-author"] != msg.author.id
        ):
            await msg.add_reaction("✅")
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["count"] = num
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["previous-author"] = msg.author.id
        else:
            await msg.add_reaction("❌")
            await msg.reply("Oops... resetting counter to 0...")
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["count"] = 0
            data["counting_channels"][str(msg.guild.id)][str(msg.channel.id)]["previous-author"] = None

        self.db.collection("servers").document(str(msg.guild.id)).set(data)

        return


def setup(client):
    client.add_cog(Counting(client))
