from gc import DEBUG_SAVEALL
import discord
from discord.ext import commands
from discord_components import ButtonStyle, Button, InteractionType, message
from utils import check
import firebase_admin
from firebase_admin import firestore


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.db = firestore.client()
        doc_ref = self.db.collection("tickets").document("ticket-ref")
        doc = doc_ref.get()
        if doc.exists:
            self.messages = doc.to_dict()["messages"]
            self.count = doc.to_dict()["count"]
            self.active_tickets = doc.to_dict()["active_tickets"]
        else:
            self.messages = {}
            self.count = {}
            self.active_tickets = {}
        print(self.messages)
    

    @commands.command(
        name="newticket", description="Creates a new message that responds to "
    )
    async def newticket(self, ctx):
        embed = discord.Embed(
            title="Get tickets here :D",
            description="To create a ticket react with 🎫 :D",
            colour=self.client.primary_colour,
        )
        embed.set_footer(
            text="MaxiGames - The Best Minigame Bot",
            icon_url=self.client.user.avatar_url,
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎫")
        if str(ctx.guild.id) not in self.messages:
            self.messages[str(ctx.guild.id)] = [str(msg.id)]
            self.count[str(ctx.guild.id)] = 0
            self.active_tickets[str(ctx.guild.id)] = {}
        else:
            self.messages[str(ctx.guild.id)].append(str(msg.id))
        doc_ref = self.db.collection(u'tickets').document('ticket-ref')
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data["messages"] = self.messages
            data["count"] = self.count
            data["active_tickets"] = self.active_tickets
        else:
            data = {
                'active_tickets': self.active_tickets,
                'messages': self.messages,
                'count': self.count
            }
        doc_ref.set(data)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.client.user.id:
            return
        print(payload.guild_id)
        print(payload.message_id)
        reaction_guild = self.client.get_guild(payload.guild_id)
        reaction_channel = self.client.get_channel(payload.channel_id)
        reaction_message = await reaction_channel.fetch_message(payload.message_id)
        if str(payload.guild_id) in self.messages:
            
            if str(payload.message_id) in self.messages[str(payload.guild_id)]:
                if payload.emoji.name == '🎫':
                    if str(payload.user_id) in self.active_tickets[str(payload.guild_id)]:
                        embed=discord.Embed(
                            title="Ticket Present",
                            description="You can only have 1 ticket open per server. Please close the other ticket before starting a new one :D",
                            colour=self.client.primary_colour,
                        )
                        embed.set_footer(
                            text="MaxiGames - The Best Minigame Bot",
                            icon_url=self.client.user.avatar_url,
                        )
                        await reaction_channel.send(embed=embed)
                        return
                    print("New ticket")
                    found = False
                    for category in reaction_guild.categories:
                        if category.name == "open-tickets":
                            found = True
                            break

                    if not found:
                        category = await reaction_guild.create_category(
                            f"open-tickets", position=0
                        )
                    overwrites = {
                        reaction_guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        payload.member: discord.PermissionOverwrite(read_messages=True, add_reactions=True, send_messages=True)
                    }
                    self.count[str(payload.guild_id)] += 1
                    self.active_tickets[str(payload.guild_id)][str(payload.user_id)] = self.count[str(payload.guild_id)]
                    channel = await reaction_guild.create_text_channel(f'ticket-{self.count[str(payload.guild_id)]}', overwrites=overwrites, category=category)
                    
                    embed=discord.Embed(
                        title="New Ticket",
                        description=f"Welcome {payload.member.mention} to your new ticket.",
                        colour=self.client.primary_colour
                    )
                    embed.set_footer(text="MaxiGames - The Best Minigame Bot", icon_url=self.client.user.avatar_url)
                    startmsg = await channel.send(embed=embed, components=[[Button(style=ButtonStyle.grey, label="🔒 Close")]], allowed_mentions = discord.AllowedMentions.all())
                    await reaction_message.remove_reaction('🎫', payload.member)

                    doc_ref = self.db.collection("tickets").document("ticket-ref")
                    data = {
                        "active_tickets": self.active_tickets,
                        "messages": self.messages,
                        "count": self.count,
                    }
                    doc_ref.set(data)

                    while True:

                        def check(interaction):
                            return interaction.user == payload.member and interaction.message.channel == channel and interaction.component.label == "🔒 Close"
                        res = await self.client.wait_for("button_click", check = check)
                        await res.respond(
                            type=InteractionType.DeferredUpdateMessage  # , content=f"{res.component.label} pressed"
                        )

                        confirmation = discord.Embed(
                            title="Confirm closing of ticket",
                            description=f"Please confirm that you want to delete this ticket. This is not reversible.",
                            colour=self.client.primary_colour,
                        )
                        embed.set_footer(text="MaxiGames - The Best Minigame Bot", icon_url=self.client.user.avatar_url)
                        confirm = await channel.send(embed=confirmation, components=[[Button(style=ButtonStyle.red, label="Close"), Button(style=ButtonStyle.grey, label="Cancel")]])

                        def check(interaction):
                            return interaction.user == payload.member and interaction.message.channel == channel
                        
                        res = await self.client.wait_for("button_click", check = check)
                        await res.respond(
                            type=InteractionType.DeferredUpdateMessage  # , content=f"{res.component.label} pressed"
                        )
                        if res.component.label == "Close":
                            await channel.delete()
                            # self.messages[str(reaction.message.guild.id)].remove(str(reaction.message.id))
                            self.active_tickets[str(payload.guild_id)].pop(str(payload.user_id))
                            doc_ref = self.db.collection(u'tickets').document('ticket-ref')
                            data = {
                                 'active_tickets': self.active_tickets,
                                 'messages': self.messages,
                                 'count': self.count
                            }
                            doc_ref.set(data)
                            break
                        else:
                            await confirm.delete()
    @check.is_staff()
    @commands.command()
    async def deletechannel(self, ctx):
        await ctx.channel.delete()


def setup(client):
    client.add_cog(Ticket(client))
