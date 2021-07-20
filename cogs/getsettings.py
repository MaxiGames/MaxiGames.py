import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import firestore
from utils import check


class GetSettings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.db = firestore.client()
        self.initiation = self.client.get_cog("Initiation")

    @commands.command(
        name="getsettings",
        description="Views current MaxiGames settings :D",
        usage="getsettings",
        aliases=["gs", "tux"]
    )
    async def getsettings(self, ctx):
        self.initation = self.client.get_cog("Initiation")
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection("servers").document(str(ctx.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()

        m = ""
        for k, v in data.items():
            m += (f"\n**{k}**:\n {v}\n")

        await ctx.send(m)


def setup(client):
    client.add_cog(Starboard(client))
