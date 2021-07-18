import discord
from discord.ext import commands
from discord import DMChannel
from discord.mentions import AllowedMentions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from utils import check
import asyncio

class Ban (commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.cred = credentials.Certificate("serviceAccountKey.json")
        # firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.hidden = True
        # self.uid = 0
        # self.doc_ref = ""
        # self.doc = {}
    @check.is_owner()
    @commands.command(
        name="ban",
        description = "This commands bans people!!!",
        usage = "ban <person> <reason>",
        hidden = True
    )
    async def ban(self, ctx, user: discord.Member, *reason: str):
        self.uid = str(user.id)
        self.banlist_ref = self.db.collection(u'admin').document(u'{}'.format("banned"))
        self.banlist_ = self.banlist_ref.get()
        if not self.banlist_.exists:
            self.banlist = {}
        self.banlist = self.banlist_.to_dict()
        self.banlist[self.uid] = " ".join(reason[:])
        self.banlist_ref.set(self.banlist)
        embed = discord.Embed(
            title="User Banned",
            description=f"{user.mention} has been banned for {self.banlist[self.uid]}"
,
            colour=self.client.primary_colour
        )
        await ctx.send(embed=embed)
        embed.title="Account Banned"
        embed.description=f"Your account has been banned from Hallo Bot for {self.banlist[self.uid]}."
        await DMChannel.send(user, embed=embed)

    @check.is_owner()
    @commands.command(
        name="unban",
        aliases=[],
        description="Unbans people when they are good again :D",
        hidden=True

    )
    async def unban(self, ctx, user:discord.Member):
        self.uid = str(user.id)
        self.banlist_ref = self.db.collection(u'admin').document(u'{}'.format("banned"))
        self.banlist_ = self.banlist_ref.get()
        self.banlist = self.banlist_.to_dict()
        self.banlist.pop(self.uid)
        self.banlist_ref.set(self.banlist)

        embed = discord.Embed(
            title="User Unbanned",
            description=f"{user.mention} has been unbanned."
            ,
            colour=self.client.primary_colour
        )
        await ctx.send(embed=embed)
        embed.title="Unbanned"
        embed.description="Your discord account has been unbanned from Hallo Bot."
        await DMChannel.send(user, embed=embed)
    
    @check.is_staff()
    @commands.command(
        name="banlist",description="Shows the list of people who have been banned",hidden=True, aliases=[]
    )
    async def ban_list(self, ctx):
        self.banlist_ref = self.db.collection(u'admin').document(u'{}'.format("banned"))
        self.banlist_ = self.banlist_ref.get()
        self.banlist = self.banlist_.to_dict()
        self.users = ""
        for i in self.banlist:
            self.users = self.users + str(self.client.get_user(int(i)).mention) + '\n'
        embed = discord.Embed(
            title= "Banned List",
            description=self.users,
            colour = self.client.primary_colour
        )
        embed.set_author(name="Hallo Bot", icon_url=self.client.icon_url)
        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.all())
    
    # @check.is_owner()
    # @commands.command()
    # async def mention(self, ctx, user: discord.Member, times:int):
    #     for i in range(times):
    #         for p in range(10):
    #             await ctx.send(user.mention)
    #         await asyncio.sleep(3)





def setup(client):
    client.add_cog(Ban(client))