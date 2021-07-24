import discord
from discord.ext import commands

class Case(commands.Cog):
		def __init__(self, client):
				self.client = client
				self.hidden = False
				
		@commands.command(name="camelcase", description="Converts a string to camelcase", alias=["cc"], usage="camelcase <string>")
		async def cc(self, ctx, *message):
			count = 0
			newMessage = []
			for i in message:
				if count == 0:
					count+=1
					newMessage.append(i.lower())
					continue

				newMessage.append(i.title())
				count+=1
			await ctx.reply(embed=discord.Embed(title="CamelCase", description=f"{''.join(newMessage)}", color=0x00ff00))

		@commands.command(name="pascalcase", description="Converts a string to pascalcase", alias=["pc"], usage="pascalcase <string>")
		async def pc(self, ctx, *message):
			count = 0
			newMessage = []
			for i in message:
				newMessage.append(i.title())
				count+=1
			await ctx.reply(embed=discord.Embed(title="PascalCase", description=f"{''.join(newMessage)}", color=0x00ff00))
		
		@commands.command(name="snakecase", description="Converts a string to snakecase", alias=["snake"], usage="snakecase <string>")
		async def snake(self, ctx, *message):
			await ctx.reply(embed=discord.Embed(title="SnakeCase", description=f"{'_'.join(message)}", color=0x00ff00))
		
		@commands.command(name="uppercase", description="Converts a string to uppercase", alias=["upper"], usage="uppercase <string>")
		async def upper(self, ctx, *message):
			count = 0
			newMessage = []
			for i in message:
				newMessage.append(i.upper())
				count+=1
			await ctx.reply(embed=discord.Embed(title="UpperCase", description=f"{' '.join(newMessage)}", color=0x00ff00))

		@commands.command(name="lowercase", description="Converts a string to lowercase", alias=["lower"], usage="lowercase <string>")
		async def lower(self, ctx, *message):
			count = 0
			newMessage = []
			for i in message:
				newMessage.append(i.lower())
				count+=1
			await ctx.reply(embed=discord.Embed(title="LowerCase", description=f"{' '.join(newMessage)}", color=0x00ff00))
		
		@commands.command(name = "lispcase", description="Converts a string to lispcase", alias=["lisp"], usage="lispcase <string>")
		async def lisp(self, ctx, *message):
			await ctx.reply(embed=discord.Embed(title="LispCase", description=f"{'-'.join(message)}", color=0x00ff00))

def setup(client):
    client.add_cog(Case(client))