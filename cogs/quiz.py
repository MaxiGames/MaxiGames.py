import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import requests
import json

questions = [""]
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# NO NO @nianny go put quiz questions on firebase then retrive them ig
# or use an API 

# hm are there quiz apis :O
# yep just search "trivia APIS"
class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, 5, BucketType.user)
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
            description += f'({alpha[count]}) {i}\n'
            count += 1
        embed = discord.Embed(
            title="TRIVIA",
            description=results["question"].replace("&quot;", '\"').replace("&#039;","\'")+'\n'+description,
        
            colour=self.client.primary_colour
        )
        await ctx.send(embed=embed) 

def setup(client):
    client.add_cog(Quiz(client)) 