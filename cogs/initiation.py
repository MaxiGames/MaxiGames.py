import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

class Initiation (commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()

    @commands.command(aliases=["init", "Init", "Initiate"])
    async def initiate(self, ctx):
        self.doc_ref = self.db.collection(u'users').document(u'{}'.format(str(ctx.author.id)))
        self.doc_ref.set({
            u'money': 0,
            u'countingsaves': 0
        })
        await self.serverinitiate(ctx)
        embed = discord.Embed(
            title="Account Initiation",
            description="Your account has been initiated. Now you can start running currency commands :D",
            colour=discord.Colour.orange()
        )
        embed.set_author(name=ctx.author.display_name, url="https://google.com", icon_url=ctx.author.avatar_url)
        if isinstance(ctx, discord.Message):
            await ctx.channel.send(embed)
        else:
            await ctx.send(embed=embed)

    async def serverinitiate(self,ctx):
        self.doc_ref = self.db.collection(u'servers').document(u'{}'.format(str(ctx.guild.id)))
        self.doc = self.doc_ref.get()
        self.usr = {}
        if self.doc.exists:
            self.dict2 = self.doc.to_dict()
            self.dict2["users"][u'{}'.format(str(ctx.author.id))] = self.usr
            self.doc_ref.set(self.dict2)
        else:
            self.doc_ref.set({
                u'users':{
                    str(ctx.author.id): self.usr
                },
                u'all': {},
                u'countingChannels': {
                    "counting": {
                        "name": "counting",
                        "count": 0,
                        "highest_count": 0,
                        "last_user": None
                    }
                },
                u'name': str(ctx.guild.name)
            })
    
    async def checkserver(self, ctx, data=None):
        doc_ref = self.db.collection(u'servers').document(u'{}'.format(str(ctx.guild.id)))
        doc = doc_ref.get()
        if doc.exists and (str(ctx.author.id) in doc.to_dict()["users"]):
            if data != None:
                return data
        else:
            await self.initiate(ctx)
            if data != None:
                dat = {}
                docs = self.db.collection(u'servers').stream()
                for doc in docs:
                    dat[doc.id] = doc.to_dict()
                
                return dat

def setup(client):
    client.add_cog(Initiation(client))
    # pass