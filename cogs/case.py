import discord
from discord.ext import commands


class Case(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name="snakecase", description="turns a bunch of words into snake case format", usage="snakecase <message>", alias=["sc"])
	async def snakecase(self, ctx, *message):
		message = "_".join(message)
		embed = discord.Embed(title="Snake-Cased your message!", description=message, color=0x00ff00)
		await ctx.reply(embed=embed)

	@commands.command(name="camelcase", description="turns a bunch of words into camel case format", usage="camelcase <message>", alias=["cc"])
	async def camelcase(self, ctx, *message):
		newMesssage = []
		count = 0
		for i in message:
			if count == 0:
				newMesssage.append(i.lower())
				count += 1
				continue
			newMesssage.append(i.title())
			count += 1

		message = "".join(newMesssage)
		embed = discord.Embed(title="camelCased your message!", description=message, color=0x00ff00)
		await ctx.reply(embed=embed)

	@commands.command(name="pascalcase", description="turns a bunch of words into pascal case format", usage="pascalcase <message>", alias=["pc"])
	async def pascalcase(self, ctx, *message):
		newMesssage = []
		count = 0
		for i in message:
			newMesssage.append(i.title())
			count += 1

		message = "".join(newMesssage)
		embed = discord.Embed(title="PascalCased your message!", description=message, color=0x00ff00)
		await ctx.reply(embed=embed)

	@commands.command(name="kebabcase", description="turns a bunch of words into kebab/lisp case format", usage="kebabcase <message>", alias=["kc", "lispcase", "lp"])
	async def kebabcase(self, ctx, *message):
		message = "-".join(message)
		embed = discord.Embed(title="Kebab-Cased your message!", description=message, color=0x00ff00)
		await ctx.reply(embed=embed)

	@commands.command(name="capitalise", description="turns a bunch of words into all capital letters format", usage="capitalise <message>", alias=["cap"])
	async def capitalise(self, ctx, *message):
		newMesssage = []
		count = 0
		for i in message:
			newMesssage.append(i.upper())
			count += 1

		message = " ".join(newMesssage)
		embed = discord.Embed(title="CAPITALISED your message!", description=message, color=0x00ff00)
		await ctx.reply(embed=embed)

	@commands.command(name="lowercase", description="turns a bunch of words into all lower letters format", usage="lowercase <message>", alias=["lower", "lc"])
	async def lowercase(self, ctx, *message):
		newMesssage = []
		count = 0
		for i in message:
			newMesssage.append(i.lower())
			count += 1

		message = " ".join(newMesssage)
		embed = discord.Embed(title="lowercased your message!", description=message, color=0x00ff00)
		await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(Case(client))
