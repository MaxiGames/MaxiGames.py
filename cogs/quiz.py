import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import requests
import json
import asyncio
import firebase_admin
from firebase_admin import firestore

questions = [""]
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.initation = self.client.get_cog("Initiation")
        self.db = firestore.client()

    # @cooldown(1, 20, BucketType.user)
    @commands.command()
    async def trivia(self, ctx):
        r = {
            "response_code":'value1',
            "results":[
                {
                    "category":'value2',
                    "type":'value3',
                    "difficulty":'value4',
                    "question":'value5',
                    "correct_answer":'value6',
                    "incorrect_answers":'value7'
                }
                ]
            }
        result = json.loads(requests.post("https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple", data=r).text)
        results = result["results"][0]
        
        arr = results["incorrect_answers"]
        arr.append(str(results["correct_answer"])) 
        random.shuffle(arr)
        count = 0
        description=""
        for i in arr:
            description += f'({count+1}) {i}\n'
            count += 1
        embed = discord.Embed(
            title="TRIVIA- You have 10 seconds to answer",
            description=results["question"].replace("&quot;", '\"').replace("&#039;","\'")+'\n'+description,
        
            colour=self.client.primary_colour
        )
        message = await ctx.reply(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        # res = await Bot.wait_for_reaction('3️⃣', message=msg, timeout=15)
        def check(reaction, user):
            return user == ctx.author and reaction.message == message

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title = "You were too slow! Try again next time.",
                description = " ",
                color = self.client.primary_colour
            )
            await ctx.reply(embed=embed)
            
        else:
            #find which option is correct????
            index = None
            if reaction.emoji == '1️⃣':
                index = 0
            elif reaction.emoji == '2️⃣':
                index = 1
            elif reaction.emoji == '3️⃣':
                index = 2
            elif reaction.emoji == '4️⃣':
                index = 3
            else:
                return
            ans = arr[index]
            await self.initation.checkserver(ctx)
            doc_ref = self.db.collection(u'users').document(
                u'{}'.format(str(ctx.author.id)))
            doc = doc_ref.get()
            if doc.exists:
                dict1 = doc.to_dict()
                if ans == str(results["correct_answer"]):
                    dict1["money"] = dict1["money"] + 3
                    embed = discord.Embed(
                        title = "Correct Answer! You win 3 money!",
                        description = "You now have " + str(dict1["money"]) + " money!",
                        color = self.client.primary_colour
                    )
                    await ctx.reply(embed=embed)
                    
                else:
                    
                    dict1["money"] = dict1["money"] - 1
                    embed = discord.Embed(
                        title = "Wrong Answer! You lost 1 money!",
                        description = f"You now have " + str(dict1["money"]) + f" money! The correct answer was {results['correct_answer']} :",
                        color = self.client.primary_colour
                    )
                    await ctx.reply(embed=embed)
                doc_ref.set(dict1)



def setup(client):
    client.add_cog(Quiz(client))

def check(msg, ctx):
        return msg.author == ctx.author and msg.channel == ctx.channel
