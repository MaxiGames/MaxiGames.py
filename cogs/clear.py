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
        # print(member)
        # print(type(member))
        # print(number)
        # print(type(number))
        print("hallo")
    
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
