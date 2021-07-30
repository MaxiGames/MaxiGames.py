import discord
from discord.ext import commands
import os
from utils import check
from firebase_admin import firestore


class Suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.db = firestore.client()

    @check.is_banned()

    @commands.command(
        name="suggestions",
        description="Suggest anything that you want us to know about!!! Be it a game that you really want to be implemented, or some comments you have on what can be improved :D",
        usage="suggest <suggestion>",
        aliases=["suggest", "sug", "s", "suggestadd"],
    )
    async def suggest(self, ctx, *msg):
        suggestion = " ".join(msg[:])
        channel = self.client.get_channel(865821669730156544)
        embed = discord.Embed(
            title="New Suggestion",
            description=f"{ctx.author.mention} has submitted a suggestion.",
            colour=self.client.primary_colour,
        )
        embed.add_field(name="Suggestion", value=suggestion, inline=False)
        message = await channel.send(embed=embed)

        acknowledgement = discord.Embed(
            title="Suggestion Submitted",
            description=f"Your suggestion has been submitted. Thank you for your suggestion.",
            colour=self.client.primary_colour,
        )
        await ctx.reply(embed=acknowledgement)

        def is_staff(ctx1):
            if(str(ctx1.author.id) == "863419048041381920"):
                return False
            doc_ref = self.db.collection(u"admin").document(u"{}".format("authorised"))
            doc = doc_ref.get()
            people = doc.to_dict()
            allowed = people["owner"] + people["staff"]
            if (
                str(ctx.author.id) not in allowed
                and not ctx1.message.author.guild_permissions.administrator
            ):
                raise False
            else:
                return True
            
        def check(reaction, user):
            return (
                is_staff(ctx)
                and reaction.message == message
                and (reaction.emoji == "❌"
                or reaction.emoji == "✅")
            )

        await message.add_reaction("⬆️")
        await message.add_reaction("⬇️")
        await message.add_reaction("❌")
        await message.add_reaction("✅")

        reaction, user = await self.client.wait_for("reaction_add", check=check)
        await message.delete()

        if reaction.emoji == "❌":
            await ctx.author.send(embed=discord.Embed(title="Suggestion declined", description=f"A moderator declined your suggestion {suggestion}", colour=self.client.primary_colour))
            doc_ref = self.db.collection(u"declined_suggestions").document(u"{}".format(ctx.guild.id))
            dictionary = doc_ref.get().to_dict()
            if dictionary == None:
                dictionary = []
            dictionary.append(suggestion)
            doc_ref.set(dictionary)
        elif reaction.emoji == "✅":
            await ctx.author.send(embed=discord.Embed(title="Suggestion accepted", description=f"Thank you for your suggestion {suggestion}, it has been accepted and currently being implemented. Keep a look out for when it releases!", colour=self.client.primary_colour))
            doc_ref = self.db.collection(u"accepted_suggestions").document(u"{}".format(ctx.guild.id))
            dictionary = doc_ref.get().to_dict()
            if dictionary == None:
                dictionary = []
            dictionary.append(suggestion)
            doc_ref.set(dictionary)

def setup(client):
    client.add_cog(Suggestions(client))
