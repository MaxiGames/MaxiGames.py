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
				self.initiation = self.client.get_cog("Initiation")

		@check.is_admin()
		@commands.command(name="starboard", description="Starts a starboard", usage="m!starboard #starboard")
		async def starboard(self, ctx, channel: discord.TextChannel):
			try:
				self.initation = self.client.get_cog("Initiation")
				await self.initation.checkserver(ctx)
				doc_ref = self.db.collection(u'servers').document(str(ctx.guild.id))
				doc = doc_ref.get()
				data = doc.to_dict()
				data["starboard"] = {"channel": channel.id,"messages":[]}
				doc_ref.set(data)
			except:
				await ctx.send("That channel does not exist")

		@commands.Cog.listener()
		async def on_reaction_add(self, reaction, user):
				self.initation = self.client.get_cog("Initiation")
				await self.initation.checkserver(reaction.message)
				doc_ref = self.db.collection(u'servers').document(str(reaction.message.guild.id))
				doc = doc_ref.get()
				data = doc.to_dict()
				if "starboard" not in data:
					return
				channel = self.client.get_channel(int(data["starboard"]["channel"]))
				if channel is None:
					return
			#TODO: MAKE THIS CORRECT
				if reaction.emoji == "🌟":
					if reaction.message.id in data["starboard"]["messages"]:
						await reaction.message.edit(content=discord.Embed(title=f"Starboard: {reaction.count}", description=reaction.message.content, color=0x00ff00).set_footer(text=f"React with {'🌟'} to star this message").set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url).set_image(url=reaction.message.attachments[0].url).set_thumbnail(url=reaction.message.author.avatar_url))
					else:
						message = await reaction.message.send(content=discord.Embed(title=f"Starboard: {reaction.count}", description=reaction.message.content, color=0x00ff00).set_footer(text=f"React with {'🌟'} to star this message").set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url).set_image(url=reaction.message.attachments[0].url).set_thumbnail(url=reaction.message.author.avatar_url))
						data["starboard"]["messages"].append(message.id)
						doc_ref.set(data)


def setup(client):
    client.add_cog(Starboard(client))
