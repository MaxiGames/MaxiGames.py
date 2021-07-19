import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import firebase_admin
from firebase_admin import firestore
from utils import check
import random
import math
import time
from discord_slash import SlashContext, cog_ext


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.initation = self.client.get_cog("Initiation")
        self.hidden = False

    # Curb gambling addiction
    @check.is_banned()
    @cooldown(1, 5, BucketType.user)
    @commands.command(name="Coinflip", aliases=["coinflip", "cf", "kymchi"])
    async def _coinflip(self, ctx, choice: str, amount: int = 1):
        self.initation = self.client.get_cog("Initiation")
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'users').document(
            u'{}'.format(str(ctx.author.id)))
        doc = doc_ref.get()
        if doc.exists:
            dict1 = doc.to_dict()
            if dict1['money'] < amount:
                embed = discord.Embed(
                    title="Amount in bank too low",
                    description="The amount that you want to gamble is more than what you have in your bank.",
                    color=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
            if amount <= 0:
                doc_ref = self.db.collection(u'users').document(
                    u'{}'.format(str(ctx.author.id)))
                doc = doc_ref.get()
                if doc.exists:
                    dict1 = doc.to_dict()
                    dict1['money'] = -1
                    doc_ref.set(dict1)
                embed = discord.Embed(
                    title="Amount gambled unacceptable",
                    description="It appears that you have been attempting to exploit the system and this is very bad!!! Therefore, your balance will be set to negative 1.",
                    color=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)

            side = 0
            if choice == "head" or choice == "heads":
                side = 0
            elif choice == "tail" or choice == "tails":
                side = 1
            else:
                raise discord.ext.commands.errors.MissingRequiredArgument

            result = (random.randint(0, 100) >= 40)
            if result:
                embed = discord.Embed(
                    title="Coinflip results",
                    description=f"Welp, the coin flipped to **{'tails' if not side else 'heads'}**. You lost {amount} points to coinflipping :(",
                    colour=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                dict1['money'] -= amount
                # await ctx.send(f"Welp you lost {amount} points to coinflipping :(")
                ctx.send
            else:
                dict1['money'] += amount
                # await ctx.send(f"Oh wow, you won {amount} points to coinflipping :O")
                embed = discord.Embed(
                    title="Coinflip results",
                    description=f"Oh wow, the coin flipped to **{'tails' if side else 'heads'}**. You won {amount} points from the coin flip :O",
                    colour=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
            doc_ref.set(dict1)
        else:
            await self.initation.initiate(ctx)

    @commands.command(name="Gamble", description="Gamble all the money you want until you're happy. Remember, theres a jackpot :D", aliases=['g', 'gamble', 'gg'], usage="gamble <amount>")
    async def _gamble(self, ctx, amount: int = 5):
        self.initation = self.client.get_cog("Initiation")
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'users').document(
            u'{}'.format(str(ctx.author.id)))
        doc = doc_ref.get()
        if doc.exists:
            dict1 = doc.to_dict()
            if dict1['money'] < amount:
                embed = discord.Embed(
                    title="Amount in bank too low",
                    description="The amount that you want to gamble is more than what you have in your bank.",
                    color=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
            if amount <= 0:
                doc_ref = self.db.collection(u'users').document(
                    u'{}'.format(str(ctx.author.id)))
                doc = doc_ref.get()
                if doc.exists:
                    dict1 = doc.to_dict()
                    dict1['money'] = -1
                    doc_ref.set(dict1)
                embed = discord.Embed(
                    title="Amount gambled unacceptable",
                    description="It appears that you have been attempting to exploit the system and this is very bad!!! Therefore, your balance will be set to negative 1.",
                    color=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
            #chance = (math.log10(amount)-0.95) / \
                #(100+100*max(10, math.log2(amount)))
            #print(chance)
            botnum = random.randint(1,12)
            yournum = random.randint(1,14)
            if yournum >= 13:
                yournum = random.randint(1,6)
            if yournum > botnum:
                dict1['money'] += amount
                embed = discord.Embed(
                    title="Gambling results",
                    description="Bot rolled: " + str(botnum) + "\nYou rolled: " + str(yournum) + 
                    "\nYou won! Congrats. You now have " + str(dict1['money']) + " money",
                    colour=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        

                await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
                doc_ref.set(dict1)
            elif yournum == botnum:
                dict1['money'] -= math.ceil(amount/2)
                embed = discord.Embed(
                    title="Gambling results",
                    description="Bot rolled: " + str(botnum) + "\nYou rolled: " + str(yournum) + 
                    "\nYou drawed and lost half of your bet.\nYou now have " + str(dict1['money']) + " money.",

                    colour=0xffff00
                )
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                        

                await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
                doc_ref.set(dict1)
            else:
                dict1['money'] -= amount
                embed = discord.Embed(
                    title = "Gambling results",
                    description="Bot rolled: " + str(botnum) + "\nYou rolled: " + str(yournum) + 
                    "\nYou lost your whole bet.\nYou now have " + str(dict1['money']) + " money.",
                    colour=0xff0000
                )
                await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
        else:
            await check.initiate(ctx)

    @check.is_banned()
    @commands.command(
        name="Money",
        description="Allows you to get a source of unlimited points :O",
        usage="money",
        aliases=["money", "m"]
    )
    @cooldown(1, 5, BucketType.user)
    async def _money(self, ctx):
        self.initation = self.client.get_cog("Initiation")
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'users').document(
            u'{}'.format(str(ctx.author.id)))
        doc = doc_ref.get()
        if doc.exists:
            dict1 = doc.to_dict()
            dict1["money"] = dict1["money"] + 1
            doc_ref.set(dict1)
            embed = discord.Embed(
                title="Money added",
                description="Money has been added to your bank. ",
                colour=self.client.primary_colour
            )
            embed.set_author(name=ctx.author.display_name,
                             url="https://google.com", icon_url=ctx.author.avatar_url)
            embed.add_field(name="New Balance",
                            value=f'{dict1["money"]}', inline=True)
            embed.set_footer(
                text="Find our more about how to use other currency functions by typing 'n!help currency' :D")
            await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
        else:
            await self.initation.initiate(ctx)
            # await ctx.send("Now you can start running currency commands :D")

    @check.is_banned()
    @commands.command()
    async def bal(self, ctx):
        self.initation = self.client.get_cog("Initiation")
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection(u'users').document(
            u'{}'.format(str(ctx.author.id)))
        doc = doc_ref.get()
        if doc.exists:
            embed = discord.Embed(
                title="Current Amount",
                description="How much money do you have in your bank?",
                colour=self.client.primary_colour
            )
            embed.set_author(name=ctx.author.display_name,
                             url="https://google.com", icon_url=ctx.author.avatar_url)
            embed.add_field(
                name="Balance", value=f'{doc.to_dict()["money"]}', inline=True)
            await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
        else:
            await self.initation.initiate(ctx)
            # return False

    @commands.command(
        name="Leaderboard",
        description="Shows you the richest and most wealthy people in the server you are in :O",
        usage="leaderboard",
        aliases=["leaderboard", "l", "rich", "r", " l"]
    )
    async def _leaderboard(self, ctx):
        self.initation = self.client.get_cog("Initiation")
        await self.initation.checkserver(ctx)

        doc_ref = self.db.collection(u'servers').document(
            u'{}'.format(str(ctx.guild.id)))
        doc = doc_ref.get()
        dict2 = doc.to_dict()["users"]
        dict3 = {}
        for i in dict2.keys():
            doc_ref = self.db.collection(u'users').document(u'{}'.format(i))
            doc = doc_ref.get()
            dict1 = doc.to_dict()
            dict3[i] = dict1['money']
        descriptio = ""
        count = 1
        for i in sorted(dict3.items(), key=lambda kv: (kv[1]), reverse=True):
            user = self.client.get_user(int(i[0]))
            descriptio += f'{count}) {user.mention} - {i[1]} points\n'
            count += 1
            if count > 10:
                break
        embed = discord.Embed(
            title=f"Leaderboard in {ctx.message.guild.name}:",
            description=descriptio,
            colour=self.client.primary_colour
        )
        embed.set_author(name="Hallo Bot",
                         icon_url='https://cdn.discordapp.com/attachments/797393542251151380/839131666483511336/476ffc83637891f004e1ba6e1ca63e6c.jpg')
        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="Hourly", description="Hourly points for saying hallo :D", usage="hourly hallo", aliases=["h", "hourly", " h", " hourly"])
    @cooldown(1, 3600, BucketType.user)
    async def _hourly(self, ctx, string: str = ""):
        self.initation = self.client.get_cog("Initiation")
        if string.lower() == "hallo":
            await self.initation.checkserver(ctx)
            doc_ref = self.db.collection(u'users').document(
                u'{}'.format(str(ctx.author.id)))
            doc = doc_ref.get()
            booster = 1
            if doc.exists:
                dict1 = doc.to_dict()
                # value = int(doc.to_dict()['money'])
                dict1["money"] = dict1["money"] + \
                    booster * (random.randint(20, 50))
                doc_ref.set(dict1)
                embed = discord.Embed(
                    title="Hourly claimed :D",
                    description="Money gained from saying \"hallo\" has been added to your bank. ",
                    colour=self.client.primary_colour
                )
                embed.set_author(name=ctx.author.display_name,
                                 url="https://google.com", icon_url=ctx.author.avatar_url)
                embed.add_field(name="New Balance",
                                value=f'{dict1["money"]}', inline=True)
                embed.set_footer(
                    text="Find our more about how to use other currency functions by typing 'n!help currency' :D")
                await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
            else:
                await self.initation.initiate(ctx)
    
    @cog_ext.cog_slash(name="hourly", description="Claim your hourly money here :D")
    async def _hourly_cog(self, ctx):
        await self._hourly(ctx, "hallo")

    @check.is_staff()
    @commands.command(
        name="Set Money",
        description="Sets the amount of money of a person.",
        usage="setmoney <user>",
        aliases=["sm", "setmoney", "setm"],
        hidden=True
    )
    async def _setmoney(self, ctx, amount: int, name: discord.Member = None):
        if name == None:
            uid = str(ctx.author.id)
        else:
            uid = str(name.id)

        doc_ref = self.db.collection(u'users').document(u'{}'.format(uid))
        doc = doc_ref.get()
        if doc.exists:
            dict2 = doc.to_dict()
            dict2["money"] = amount
            doc_ref.set(dict2)
            embed = discord.Embed(
                title="User amount set",
                description=f"Amount of <@{uid}> has been set to {amount}.",
                colour=self.client.primary_colour
            )
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="User not initiated",
                description="This user is not initiated. Please make sure that the person has used hallo bot before :D",
                color=self.client.primary_colour
            )
            await ctx.send(embed=embed)

    
        
        
    

def setup(client):
    client.add_cog(Economy(client))
