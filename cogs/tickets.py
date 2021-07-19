from gc import DEBUG_SAVEALL
import discord
from discord.ext import commands


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.messages = {}
        self.count = {}
        self.active_tickets = {}




    @commands.command(name="newticket", description="Creates a new message that responds to ")
    async def newticket(self, ctx):
        embed = discord.Embed(
            title="Get tickets here :D",
            description="To create a ticket react with 🎫 :D",
            colour=self.client.primary_colour
        )
        embed.set_footer(text="MaxiGames - The Best Minigame Bot", icon_url=self.client.user.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎫')
        if str(ctx.guild.id) not in self.messages:
            self.messages[str(ctx.guild.id)] = [msg]
            self.count[str(ctx.guild.id)] = 0
            self.active_tickets[str(ctx.guild.id)] = {}
        else:
            self.messages[str(ctx.guild.id)].append(msg)
        await ctx.message.delete()
        # print(self.messages)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user:
            return
        if str(reaction.message.guild.id) in self.messages:
            if reaction.message in self.messages[str(reaction.message.guild.id)]:
                if reaction.emoji == '🎫':
                    if str(user.id) in self.active_tickets[str(reaction.message.guild.id)]:
                        embed=discord.Embed(
                            title="Ticket Present",
                            description="You can only have 1 ticket open per server. Please close the other ticket before starting a new one :D",
                            colour = self.client.primary_colour
                        )
                        embed.set_footer(text="MaxiGames - The Best Minigame Bot", icon_url=self.client.user.avatar_url)
                        await reaction.message.channel.send(embed=embed)
                        return
                    print('New ticket')
                    found = False
                    for category in reaction.message.guild.categories:
                        if category.name=="open-tickets":
                            overwrites = {
                                reaction.message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                user: discord.PermissionOverwrite(read_messages=True, add_reactions=True, send_messages=True)
                            }
                            self.count[str(reaction.message.guild.id)] += 1
                            self.active_tickets[str(reaction.message.guild.id)][str(user.id)] = self.count[str(reaction.message.guild.id)]
                            channel = await reaction.message.guild.create_text_channel(f'ticket-{self.count[str(reaction.message.guild.id)]}', overwrites=overwrites, category=category)
                            found = True
                            break 
                    
                    if not found:
                        category = await reaction.message.guild.create_category(f'open-tickets', position=0)
                        overwrites = {
                            reaction.message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                            user: discord.PermissionOverwrite(read_messages=True, add_reactions=True, send_messages=True)
                        }
                        self.count[str(reaction.message.guild.id)] += 1
                        channel = await reaction.message.guild.create_text_channel(f'ticket-{self.count[str(reaction.message.guild.id)]}', overwrites=overwrites, category=category)
                    
                    embed=discord.Embed(
                        title="New Ticket",
                        description=f"Welcome {user.mention} to your new ticket.",
                        colour=self.client.primary_colour
                    )
                    embed.set_footer(text="MaxiGames - The Best Minigame Bot", icon_url=self.client.user.avatar_url)
                    startmsg = await channel.send(embed=embed, allowed_mentions = discord.AllowedMentions.all())
                    
                    await reaction.message.remove_reaction('🎫', user)

def setup(client):
    client.add_cog(Ticket(client))
