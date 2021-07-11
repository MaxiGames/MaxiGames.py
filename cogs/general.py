import discord
import time
from discord.ext import commands


class general(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dates = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

    @commands.command()
    async def hallo(self, ctx):
        await ctx.send("Hallo")

    @commands.command()
    async def current(self, ctx):
        result = time.localtime(time.time())
        embed = discord.Embed(
            title="Current Date and Time",
            description=f'Find the current date and time below :D',
            colour=self.client.primary_colour
        )

        embed.add_field(
            name="Date", value=f'{result.tm_mday}/{result.tm_mon}/{result.tm_year}', inline=True)
        embed.add_field(
            name="Day", value=self.dates[result.tm_wday], inline=True)
        embed.add_field(
            name="Time", value=f'{result.tm_hour}:{result.tm_min}:{result.tm_sec}', inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def seconds(self, ctx):
        await ctx.send(str(round(time.time())) + " seconds have passed since the epoch!")

    @commands.command()
    async def ns(self, ctx, num: int):
        if num < 1 or num > 50:
            await ctx.send("That is not a valid value for this command!:thinking:")
        else:
            answer = ""
            n = 1
            while n <= num:

                poop = n
                while poop > 0:
                    answer = answer + "^"
                    poop -= 1
                answer = answer + "\n"

                n += 1
            await ctx.send(answer)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite Link to invite the bot",
                              description="https://discord.com/api/oauth2/authorize?client_id=863419048041381920&permissions=8&scope=bot", color=self.client.primary_colour)
        await ctx.send(embed=embed)

    @commands.command()
    async def official(self, ctx):
        embed = discord.Embed(
            title="Join our official server today!",
            description="https://discord.gg/nGWhxNG2sf",
            colour=self.client.primary_colour)
        await ctx.send(embed=embed)

    @commands.command()
    async def whoami(self, ctx):
        embed = discord.Embed(
            title="You are " + str(ctx.author) + " :D",
            description="What a pog name!!!",
            color=self.client.primary_colour
        )
        role = "" #theres probably some way to optimise this...
        for i in ctx.author.roles[::-1]:
            if i.name != "@everyone":
                role += f'{i.mention} '
        embed.add_field(name="Roles", value=role, inline=True)
        embed.add_field(name="Created On",value=f'{ctx.author.created_at.strftime("%A, %d %b %Y")} \n {ctx.author.created_at.strftime("%I:%M %p")}',inline=True)
        embed.add_field(name="Joined On",value=f'{ctx.author.joined_at.strftime("%A, %d %b %Y")} \n {ctx.author.joined_at.strftime("%I:%M %p")}',inline=True)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def hallolong(self,ctx,num:int): await ctx.send(f'Hall{"o"*num}')
    
    @commands.command()
    async def servercount(self,ctx):
        await ctx.send(str(len(self.bot.servers)))
    @commands.command()
    async def help(self,ctx,which:str):
        if which == "general":
            embed=discord.Embed(title = "A list of all the current commands!",
            description = " ",color=0x12A366)
        #this is initial help command. Soon i will push another version that has different categories and is less messy.

            embed.add_field(name="help",value="Brings you to this page",inline=True)
            embed.add_field(name="invite",value="Creates a link that lets you invite the bot to any server that you are an admin in.",inline=True)
        
            embed.add_field(name="official",value="Generates an invite to Stonks Bot and MaxiGames' official server!",inline=True)
        elif which == "currency":
            embed=discord.Embed(title="Currency commands",description="commands that are related to the bot's currency system.",color=self.client.primary_colour)
            embed.add_field(name="initiate",value="Makes an account for you if you don't already have one.",inline=True)
            embed.add_field(name="money",value="Gives you one money for using this command!",inline=True)
            embed.add_field(name="h hallo",value="Hourly command that gives you some money for saying hallo",inline=True)
            embed.add_field(name="bal",value="Shows you how much money you have!",inline=True) 
        elif which == "fun":  
            embed=discord.Embed(title="Fun commands",description="random commands which are for the user's enjoyment.",color=self.client.primary_colour)    
            embed.add_field(name="hallolong",value="Prints out hallo with the number of letter o that you specify!",inline=True)
            
            embed.add_field(name="ns",value="prints out a descending right angled triangle of ^ characters of your specified size",inline=True)
        elif which == "others":
            embed=discord.Embed(title="Other commands",description="The other commands that do not fall into any of the other categories.",color=self.client.primary_colour)
            embed.add_field(name="current",value="Returns the current date and time",inline=True)
            embed.add_field(name="seconds",value="returns the number of seconds that have passed since 1 Jan 1970. No one knows what this date means.",inline=True)

            embed.add_field(name="whoami",value="Gives you some personal information about yourself!",inline=True)
        else:
            embed=discord.Embed(title="Invalid category.",description="The categories are general, currency, fun and others",color=self.client.primary_colour)
        
        
        
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(general(client))