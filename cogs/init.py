import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


class Init(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.hidden = True

    async def initiate(self, ctx):
        self.doc_ref = self.db.collection(u"users").document(
            u"{}".format(str(ctx.author.id))
        )
        self.doc_ref.set(
            {
                u"money": 0,
                u"countingsaves": 0,
                u"name": str(ctx.author.name),
            }
        )
        await self.serverinitiate(ctx)
        embed = discord.Embed(
            title="Account Init",
            description="Your account has been initiated. Now you can start running currency commands :D",
            colour=self.client.primary_colour,
        )
        if isinstance(ctx, discord.Message):
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    async def serverinitiate(self, ctx):
        self.doc_ref = self.db.collection(u"servers").document(
            u"{}".format(str(ctx.guild.id))
        )
        self.doc = self.doc_ref.get()
        self.usr = {}
        if self.doc.exists:
            self.dict2 = self.doc.to_dict()
            self.dict2["users"][u"{}".format(str(ctx.author.id))] = self.usr
            self.doc_ref.set(self.dict2)
        else:
            self.doc_ref.set(
                {
                    u"users": {str(ctx.author.id): self.usr},
                    u"all": {},
                    u"starboard_threshold": 1,
                    u"countingChannels": {
                        "counting": {
                            "name": "counting",
                            "count": 0,
                            "highest_count": 0,
                            "last_user": None,
                        }
                    },
                    u"counting_channels": {
                    },
                    u"name": str(ctx.guild.name),
                }
            )

    async def checkserver(self, ctx, data=None):
        doc_ref = self.db.collection(u"servers").document(
            u"{}".format(str(ctx.guild.id))
        )
        doc = doc_ref.get()
        if doc.exists and (str(ctx.author.id) in doc.to_dict()["users"]):
            if data != None:
                return data
        else:
            await self.serverinitiate(ctx)
            if data != None:
                dat = {}
                docs = self.db.collection(u"servers").stream()
                for doc in docs:
                    dat[doc.id] = doc.to_dict()

                return dat


def setup(client):
    client.add_cog(Init(client))
    # pass
