from gc import DEBUG_SAVEALL
import discord
from discord.ext import commands
from discord_components import ButtonStyle, Button, InteractionType
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
        await ctx.message.delete()
        # print(self.messages)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user:
            return
        if str(reaction.message.guild.id) in self.messages:
            if (
                str(reaction.message.id)
                in self.messages[str(reaction.message.guild.id)]
            ):
                if reaction.emoji == "🎫":
                    if (
                        str(user.id)
                        in self.active_tickets[str(reaction.message.guild.id)]
                    ):
                        embed = discord.Embed(
                            title="Ticket Present",
                            description="You can only have 1 ticket open per server. Please close the other ticket before starting a new one :D",
                            colour=self.client.primary_colour,
                        )
                        embed.set_footer(
                            text="MaxiGames - The Best Minigame Bot",
                            icon_url=self.client.user.avatar_url,
                        )
                        await reaction.message.channel.send(embed=embed)
                        return
                    print("New ticket")
                    found = False
                    for category in reaction.message.guild.categories:
                        if category.name == "open-tickets":
                            found = True
                            break

                    if not found:
                        category = await reaction.message.guild.create_category(
                            f"open-tickets", position=0
                        )
                    overwrites = {
                        reaction.message.guild.default_role: discord.PermissionOverwrite(
                            view_channel=False
                        ),
                        user: discord.PermissionOverwrite(
                            read_messages=True, add_reactions=True, send_messages=True
                        ),
                    }
                    self.count[str(reaction.message.guild.id)] += 1
                    self.active_tickets[str(reaction.message.guild.id)][
                        str(user.id)
                    ] = self.count[str(reaction.message.guild.id)]
                    channel = await reaction.message.guild.create_text_channel(
                        f"ticket-{self.count[str(reaction.message.guild.id)]}",
                        overwrites=overwrites,
                        category=category,
                    )

                    embed = discord.Embed(
                        title="New Ticket",
                        description=f"Welcome {user.mention} to your new ticket.",
                        colour=self.client.primary_colour,
                    )
                    embed.set_footer(
                        text="MaxiGames - The Best Minigame Bot",
                        icon_url=self.client.user.avatar_url,
                    )
                    startmsg = await channel.send(
                        embed=embed,
                        components=[[Button(style=ButtonStyle.grey, label="🔒 Close")]],
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                    await reaction.message.remove_reaction("🎫", user)

                    doc_ref = self.db.collection("tickets").document("ticket-ref")
                    data = {
                        "active_tickets": self.active_tickets,
                        "messages": self.messages,
                        "count": self.count,
                    }
                    doc_ref.set(data)

                    while True:

                        def check(interaction):
                            return (
                                interaction.user == user
                                and interaction.message.channel == channel
                                and interaction.component.label == "🔒 Close"
                            )

                        res = await self.client.wait_for("button_click", check=check)
                        await res.respond(
                            type=InteractionType.DeferredUpdateMessage  # , content=f"{res.component.label} pressed"
                        )

                        confirmation = discord.Embed(
                            title="Confirm closing of ticket",
                            description=f"Please confirm that you want to delete this ticket. This is not reversible.",
                            colour=self.client.primary_colour,
                        )
                        embed.set_footer(
                            text="MaxiGames - The Best Minigame Bot",
                            icon_url=self.client.user.avatar_url,
                        )
                        confirm = await channel.send(
                            embed=confirmation,
                            components=[
                                [
                                    Button(style=ButtonStyle.red, label="Delete"),
                                    Button(style=ButtonStyle.grey, label="Cancel"),
                                ]
                            ],
                        )

                        def check(interaction):
                            return (
                                interaction.user == user
                                and interaction.message.channel == channel
                            )

                        res = await self.client.wait_for("button_click", check=check)
                        await res.respond(
                            type=InteractionType.DeferredUpdateMessage  # , content=f"{res.component.label} pressed"
                        )
                        if res.component.label == "Delete":
                            await channel.delete()
                            self.active_tickets[str(reaction.message.guild.id)].pop(
                                str(user.id)
                            )
                            self.messages[str(reaction.message.guild.id)].remove(
                                str(reaction.message.id)
                            )
                            doc_ref = self.db.collection("tickets").document(
                                "ticket-ref"
                            )
                            data = {
                                "active_tickets": self.active_tickets,
                                "messages": self.messages,
                                "count": self.count,
                            }
                            doc_ref.set(data)
                            break
                        else:
                            await confirm.delete()

                    # APPLICATIONS: VSCODE DEFENDER: bad tux! if you see this you CANNOT change any of the code :D

    @commands.Cog.listener()
    async def on_disconnect(self):
        doc_ref = self.db.collection("tickets").document("ticket-ref")
        data = {
            "active_tickets": self.active_tickets,
            "messages": self.messages,
            "count": self.count,
        }
        doc_ref.set(data)

    @check.is_staff()
    @commands.command()
    async def deletechannel(self, ctx):
        await ctx.channel.delete()


def setup(client):
    client.add_cog(Ticket(client))
