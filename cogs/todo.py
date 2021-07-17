import discord
from discord.ext import commands
import firebase_admin 
from firebase_admin import firestore
from utils import check

class Todo(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.initation = self.client.get_cog("Initiation")
        self.hidden = True
    
    @check.is_staff()
    @commands.command()
    async def todoADD(self, ctx, *msg):
        task = " ".join(msg)
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'servers').document(str(ctx.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()
        try:
          data["todo"].append(task)
        except KeyError:
            data["todo"] = [task]
        doc_ref.set(data)
        await ctx.send("Added")

    @check.is_staff()
    @commands.command()
    async def todo(self, ctx):
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'servers').document(str(ctx.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()
        count = 0
        description = ""
        for i in data["todo"]:
            count += 1
            description += f"({count}) {i} \n"
        embed = discord.Embed(
            title='TODO LIST', description=description, colour=self.client.primary_colour)
        await ctx.send(embed=embed)
    
    @check.is_staff()
    @commands.command()
    async def todoREM(self, ctx, number):
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'servers').document(str(ctx.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()
        try:
          data["todo"].pop(int(number)-1)
        except:
            await ctx.send("Item does not exist. Do note that you are supposed to state the number of the element u want to remove")
            return
        doc_ref.set(data)
        await ctx.send("Successfully removed, run `todo` to check the list")


def setup(client):
    client.add_cog(Todo(client))
