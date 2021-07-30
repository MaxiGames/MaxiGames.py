import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import firestore
from utils import check


class Starboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.db = firestore.client()
        self.init = self.client.get_cog("Init")

    @check.is_admin()
    @commands.command(
        name="starboard-threshold",
        description="Starts a starboard",
        usage="m!starboard #starboard",
        aliases=["starthresh", "starcount"]
    )
    async def starboard_threshold(self, ctx, thresh: int = None):
        self.initation = self.client.get_cog("Init")
        await self.initation.checkserver(ctx)
        doc_ref = self.db.collection("servers").document(str(ctx.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()

        if thresh == None:
            data["starboard_threshold"] = 5
            await ctx.reply("Reset starboard threshold to 5.")
        elif type(thresh) != int or thresh < 1:
            await ctx.reply("Must set to a positive integer!")
        else:
            data["starboard_threshold"] = thresh
            await ctx.reply(f"Starboard threshold has been set to {thresh}!")

        doc_ref.set(data)

    @check.is_admin()
    @commands.command(
        name="starboard",
        description="Starts a starboard",
        usage="m!starboard #starboard",
    )
    async def starboard(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.reply("You need to specify a channel")
            return
        try:
            self.initation = self.client.get_cog("Init")
            await self.initation.checkserver(ctx)
            doc_ref = self.db.collection("servers").document(str(ctx.guild.id))
            doc = doc_ref.get()
            data = doc.to_dict()
            data["starboard"] = {"channel": channel.id}
            data["starboard_threshold"] = 5
            doc_ref.set(data)
            await ctx.reply(f"Starboard channel has been set to {channel}!")
        except:
            await ctx.reply("That channel does not exist")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.init = self.client.get_cog("Init")
        doc_ref = self.db.collection("servers").document(str(reaction.message.guild.id))
        doc = doc_ref.get()
        data = doc.to_dict()
        if "starboard" not in data:
            return
        channel = self.client.get_channel(int(data["starboard"]["channel"]))
        await self.init.checkserver(reaction.message)

        if "starboard" not in data:
            print("b")
            return
        if channel is None:
            print("a")
            return

        if reaction.count >= data["starboard_threshold"] and reaction.emoji == "⭐":
            try:
                msg = await channel.fetch_message(
                    data["starboard"][str(reaction.message.id)]
                )
                await msg.edit(
                    embed=discord.Embed(
                        title=f"Starboard: {reaction.count}",
                        description=reaction.message.content,
                        color=0x00FF00,
                    )
                    .set_footer(text=f"React with {'🌟'} to star this message")
                    .set_author(
                        name=reaction.message.author.name,
                        icon_url=reaction.message.author.avatar_url,
                    )
                )
                doc_ref.set(data)
            except KeyError:
                message = await channel.send(
                    embed=discord.Embed(
                        title=f"Starboard: {reaction.count}",
                        description=reaction.message.content,
                        color=0x00FF00,
                    )
                    .set_footer(text=f"React with {'🌟'} to star this message")
                    .set_author(
                        name=reaction.message.author.name,
                        icon_url=reaction.message.author.avatar_url,
                    )
                )
                data["starboard"][str(reaction.message.id)] = message.id
                doc_ref.set(data)


def setup(client):
    client.add_cog(Starboard(client))
