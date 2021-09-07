import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import firestore
from utils import check
from discord.ext.commands import cooldown, BucketType
from discord.utils import get


class IdleMiner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.init = self.client.get_cog("Init")
        self.hidden = True  # (whether its hidden from m!help)

    @commands.command(
        name="stats",
        help="Shows the stats of the idle miner",
        alias=[],
        usage="<optional user (ping or id)>",
    )
    @cooldown(1, 2, BucketType.user)
    async def stats(self, ctx, user=None):
        if not user:
            user_requested = ctx.author.id
        else:
            try:
                user_requested = int(user)
            except ValueError:
                try:
                    user_requested = int(user[3:-1])
                except ValueError:
                    embed = discord.Embed(title="Error!", description="Invalid user/id")
                    await ctx.send(embed=embed)
                    return
        doc_ref = self.db.collection("users").document("{}".format(str(user_requested)))
        doc = doc_ref.get()
        if doc.exists:
            dict1 = doc.to_dict()
            embed = discord.Embed(title="Money", description="${:,.2f}".format(dict1["money"]))
            embed.set_author(name="hi",
                             icon_url=ctx.message.author.avatar_url)
            try:
                embed.add_field(name="Mining", value="Level " + str(dict1["mining"]), inline=True)
                embed.add_field(name="Extraction", value="Level " + str(dict1["extraction"]), inline=True)
                embed.add_field(name="Overclock", value="Level " + str(dict1["overclock"]), inline=True)
            except KeyError:
                dict1["mining"] = 0
                dict1["extraction"] = 0
                dict1["overclock"] = 0
                doc_ref.set(dict1)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error!", description="User does not have a profile")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(IdleMiner(client))
