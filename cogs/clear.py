import discord
from discord.ext import commands
import typing
import asyncio
from utils import check

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channels = []
        self.hidden = True

    @check.is_admin()
    @commands.group(invoke_without_subcommands=False)
    async def clear(self, ctx, member:typing.Optional[discord.Member]=None, number:typing.Optional[int]=None):  
        if ctx.invoked_subcommand is None:
            if member is None and number is not None:
                if str(ctx.channel.id) in self.channels:
                    await ctx.send("A clear is in progress. Try again later :D")
                    return
                # clear in progress
                self.channels.append(str(ctx.channel.id))
                messages = await ctx.channel.purge(limit=number)
                
                self.channels.remove(str(ctx.channel.id))
                embed = discord.Embed(
                    title=f"Messages deleted :D",
                    description=f"{len(messages)} messages has been deleted from {ctx.channel.name}.",
                    colour = self.client.primary_colour
                )
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(3)
                await msg.delete()
            elif member is not None and number is not None:
                if str(ctx.channel.id) in self.channels:
                    await ctx.send("A clear is in progress. Try again later :D")
                    return
                    # clear in progress
                
                def check(m):
                    return m.author == member and m.channel == ctx.channel
                self.channels.append(str(ctx.channel.id))
                counter = 0
                async for message in ctx.channel.history():
                    if counter >= number:
                        break
                    if message.author == member:
                        counter += 1
                        await message.delete()
                    
                
                self.channels.remove(str(ctx.channel.id))
                embed = discord.Embed(
                    title=f"{counter} messages deleted :D",
                    description=f"{counter} messages by {member.mention} has been deleted from {ctx.channel.name}.",
                    colour = self.client.primary_colour
                )
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(3)
                await msg.delete()
    
    @check.is_staff()
    @clear.command()
    async def all(self, ctx, search: int=100):
        if str(ctx.channel.id) in self.channels:
            await ctx.send("A clear is in progress. Try again later :D")
            return
            # clear in progress
        self.channels.append(str(ctx.channel.id))
        messages = await ctx.channel.purge(limit=search)
        
        self.channels.remove(str(ctx.channel.id))
        embed = discord.Embed(
            title=f"Messages deleted :D",
            description=f"{len(messages)} messages has been deleted from {ctx.channel.name}.",
            colour = self.client.primary_colour
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

    @clear.command()
    async def bot(self, ctx, search: int=100):
        if str(ctx.channel.id) in self.channels:
            await ctx.send("A clear is in progress. Try again later :D")
            return
            # clear in progress
        def check(message):
            return message.author.bot
        self.channels.append(str(ctx.channel.id))
        messages = await ctx.channel.purge(limit=search, check=check)
        
        self.channels.remove(str(ctx.channel.id))
        embed = discord.Embed(
            title=f"Messages deleted :D",
            description=f"{len(messages)} messages has been deleted from {ctx.channel.name}.",
            colour = self.client.primary_colour
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()
    
    @check.is_admin()
    @clear.command()
    async def contains(self, ctx, number:typing.Optional[int]=None, *, substr: str):
        if str(ctx.channel.id) in self.channels:
            await ctx.send("A clear is in progress. Try again later :D")
            return
            # clear in progress
        await ctx.message.delete()
        self.channels.append(str(ctx.channel.id))

        if number is not None:
            counter = 0
            async for message in ctx.channel.history():
                if counter >= number:
                    break
                if substr in message.content:
                    counter += 1
                    await message.delete()
        else:
            def check(m):
                return substr in message.content
            messages = await ctx.channel.purge(check=check)
        
        self.channels.remove(str(ctx.channel.id))
        embed = discord.Embed(
            title=f"Messages deleted :D",
            description=f"{counter} messages that includes {substr} has been deleted from {ctx.channel.name}.",
            colour = self.client.primary_colour
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

def setup(client):
    client.add_cog(Clear(client))
