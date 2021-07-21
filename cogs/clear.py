import discord
from discord.ext import commands
import typing
import asyncio

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channels = []
        self.hidden = True

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
                msg = await ctx.send(f"Deleted {len(messages)} messages")
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
                        message.delete()
                    
                
                self.channels.remove(str(ctx.channel.id))
                msg = await ctx.send(f"Deleted {counter} messages")
                await asyncio.sleep(3)
                await msg.delete()
    
    @clear.command()
    async def all(self, ctx, search: int=100):
        if str(ctx.channel.id) in self.channels:
            await ctx.send("A clear is in progress. Try again later :D")
            return
            # clear in progress
        self.channels.append(str(ctx.channel.id))
        messages = await ctx.channel.purge(limit=search)
        
        self.channels.remove(str(ctx.channel.id))
        msg = await ctx.send(f"Deleted {len(messages)} messages")
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
        msg = await ctx.send(f"Deleted {len(messages)} messages")
        await asyncio.sleep(3)
        await msg.delete()

def setup(client):
    client.add_cog(Clear(client))
