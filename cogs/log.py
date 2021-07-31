import discord
from discord.ext import commands
from utils import check
import firebase_admin
from firebase_admin import firestore
from discord.ext.commands import cooldown, BucketType

log_events_array = [
		"on_message",
		"on_message_edit",
		"on_reaction_add",
		"on_reaction_remove",
		"on_reaction_clear",
		"on_member_join",
		"on_member_remove",
		"on_member_update",
		"on_server_join",
		"on_server_remove",
		"on_server_update",
		"on_server_role_create",
		"on_server_role_delete",
		"on_server_role_update",
		"on_server_emojis_update",
		"on_voice_state_update",
		"on_member_ban",
		"on_member_unban",
		"on_typing",
		"on_group_join",
		"on_group_remove",
		"on_group_update",
		"on_private_channel_create",
		"on_private_channel_delete",
		"on_private_channel_update",
		"on_private_channel_pins_update",
		"on_webhooks_update",
		"on_message_delete",
		"on_message_edit",
		"on_raw_message_delete",
		"on_raw_message_edit",
		"on_raw_bulk_message_delete",
		"on_raw_bulk_message_edit",
		"on_raw_message_delete_bulk",
		"on_raw_message_edit_bulk",
]


def check_if_log_exists(self, ctx, log_type):
	doc_ref = self.db.collection("logging").document(ctx.guild.id)
	doc = doc_ref.get().to_dict()
	if doc == None:
		return False
	else:
		if log_type in doc:
			return True
		else:
			return False

class Log(commands.Cog):
		def __init__(self, client):
				self.client = client
				self.hidden = False
		
		@commands.command(name='log', description="lists the logs that are present on the server", aliases=['logs'])
		@commands.cooldown(1, 5, commands.BucketType.user)
		@commands.check(check.is_admin)
		async def logs(self, ctx):
				self.db = firestore.client()
				doc_ref = self.db.collection("logging").document(ctx.guild.id)
				doc = doc_ref.get().to_dict()
				if doc == None:
					await ctx.send("No logs active on this server")
				else:
					embed = discord.Embed(title="Logs", description="List of logs", colour=0x00ff00)
					for key, value in doc.items():
						embed.add_field(name=key, value=f"<#{value}>")
					await ctx.send(embed=embed)

		@commands.command(name='addlog', description="adds a log to the server", aliases=['addlogs'])
		@commands.cooldown(1, 5, commands.BucketType.user)
		@commands.check(check.is_admin)
		async def addlog(self, ctx, log_type: str, channel: discord.TextChannel):
			if check_if_log_exists(self, ctx, log_type):
				await ctx.send("Log already exists")
			else:
				if log_type in log_events_array:
					doc_ref = self.db.collection("logging").document(ctx.guild.id)
					doc_ref.set({
						log_type: channel.id
					})
					await ctx.send("Log added")

		#! Log Command Listeners
		@commands.Cog.listener()
		async def on_message_delete(self, ctx):
			if check_if_log_exists(self, ctx, "on_message"):
				doc_ref = self.db.collection("logging").document(ctx.guild.id)
				doc = doc_ref.get().to_dict()
				if "on_message_delete" in doc:
					channel = ctx.get_channel(int(doc["on_message_delete"]))
					if channel != None:
						embed = discord.Embed(title="Message Deleted", description=f"Message by {ctx.mention} was deleted in {ctx.channel.id}", colour=0xff0000)
						embed.add_field(name="Message", value=ctx.message.content)
						await channel.send(embed=embed)
				await ctx.send(f"Logged message: {ctx.content}")

def setup(client):
    client.add_cog(Log(client))
