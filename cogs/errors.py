import discord
from discord.ext import commands
import traceback

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, bypass=False):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title = "Unauthorised Access",
                description="You are not authorised to use this command.",
                colour = self.client.error_colour
            )
            channel = self.client.get_channel(866526918484164668)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await channel.send(embed = embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description="You do not have permission to run this command. It might be because it is a command only for admins, or because you have been banned.",
                colour = self.client.error_colour
            )
            channel = self.client.get_channel(866526918484164668)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await channel.send(embed = embed)
        
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title = "Command on Cooldown",
                description=f"This command is on cooldown. Try again in {error.retry_after:,.1f} seconds.",
                colour = self.client.primary_colour
            )
            channel = self.client.get_channel(866526918484164668)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await channel.send(embed = embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Incorrect Argument",
                description="There is an error with your command statement. Please check your command syntax through `n!help <command>`.",
                colour=self.client.primary_colour
            )
            channel = self.client.get_channel(866526918484164668)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await channel.send(embed = embed)

        else:
            channel = self.client.get_channel(866526918484164668)
            await channel.send(f"Unknown error: ERROR ({traceback.format_exc()})")
            print(traceback_output)
            print(error)


def setup(client):
    client.add_cog(Errors(client))
    # pass