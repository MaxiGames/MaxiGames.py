import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import firestore
class Hacks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.initiation = self.client.get_cog("Initiation")
        self.hidden = False

    def allow_owners(ctx):
        return ctx.message.author.id == 712942935129456671 or ctx.message.author.id == 676748194956181505 or ctx.message.author.id == 782247763542016010
	
    @commands.command()
    @commands.check(allow_owners)
    async def hacks(self, ctx, id, value):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await self.initiation.checkserver(ctx)
        doc_ref = self.db.collection(u'users').document(id)
        doc = doc_ref.get()
        if doc.exists:
            dict1 = doc.to_dict()
            dict1["money"] = value
            doc_ref.set(dict1)
            await ctx.send("Success")
        else:
            await ctx.send("That user doesn't exist!")


def setup(client):
    client.add_cog(Hacks(client))

