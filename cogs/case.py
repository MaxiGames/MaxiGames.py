import discord
from discord.ext import commands

class Case(commands.Cog):
		def __init__(self, client):
				self.client = client
				self.hidden = False
				
		@commands.command(name="camelcase", description="Converts a string to camelcase", alias=["cc"], usage="camelcase <string>")
		async def cc(self, ctx, *message):
			count = 0
			for i in message:
				if count == 0:
					count+=1
					continue
				i = i.title()
				count+=1
			await ctx.reply(embed=discord.Embed(title="CamelCase", description=f"{' '.join(message)}", color=0x00ff00))

			@commands.command(name="pascalcase", description="Converts a string to pascalcase", alias=["pc"], usage="pascalcase <string>")
			async def pc(self, ctx, *message):
				for i in message:
					i = i.title()
				await ctx.reply(embed=discord.Embed(title="PascalCase", description=f"{' '.join(message)}", color=0x00ff00))
			
			@commands.command(name="snakecase", description="Converts a string to snakecase", alias=["snake"], usage="snakecase <string>")
			async def snake(self, ctx, *message):
				for i in message:
					i = i.lower()
				await ctx.reply(embed=discord.Embed(title="SnakeCase", description=f"{' '.join(message)}", color=0x00ff00))
			
			@commands.command(name="uppercase", description="Converts a string to uppercase", alias=["upper"], usage="uppercase <string>")
			async def upper(self, ctx, *message):
				for i in message:
					i = i.upper()
				await ctx.reply(embed=discord.Embed(title="UpperCase", description=f"{' '.join(message)}", color=0x00ff00))
				

def setup(client):
    client.add_cog(Case(client))