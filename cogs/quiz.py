import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import requests
import json
import asyncio
import firebase_admin
from firebase_admin import firestore
import os
import copy

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.initiation = self.client.get_cog("Initiation")
        self.db = firestore.client()
        self.hidden = False

    # @cooldown(1, 20, BucketType.user)
    @commands.command(name="trivia", description="Answer a trivia question using reactions! Provide a number from 1 to 3 specifying the difficulty of the trivia question you want.", usage="trivia <difficulty>")
    async def trivia(self, ctx, difficulty=100000000000):
        word = "hard"
        moneyToAdd = 0
        if(difficulty == 1):
            word = "easy"
            moneyToAdd = 2
        elif(difficulty == 2):
            word = "medium"
            moneyToAdd = 5
        elif(difficulty == 3):
            word = "hard"
            moneyToAdd = 10
        else:
            await ctx.reply(embed=discord.Embed(title="Error", description="A difficulty level of 1, 2 or 3 is needed! Note that the harder the question is, the more points you will get if u get it right!", colour=self.client.primary_colour))
            return
        r = {
            "response_code": 'value1',
            "results": [
                {
                    "category": 'value2',
                    "type": 'value3',
                    "difficulty": 'value4',
                    "question": 'value5',
                    "correct_answer": 'value6',
                    "incorrect_answers": 'value7'
                }
            ]
        }
        result = json.loads(requests.post(
            f"https://opentdb.com/api.php?amount=1&difficulty={word}&type=multiple", data=r).text)
        results = result["results"][0]

        arr = results["incorrect_answers"]
        arr.append(str(results["correct_answer"]))
        random.shuffle(arr)
        count = 0
        description = ""
        for i in arr:
            description += f'({count+1}) {i}\n'
            count += 1
        embed = discord.Embed(
            title=f"TRIVIA- You have 10 seconds to answer ({word})",
            description=results["question"].replace(
                "&quot;", '\"').replace("&#039;", "\'")+'\n'+description,

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
                title="You were too slow! Try again next time.",
                description=" ",
                color=self.client.primary_colour
            )
            await ctx.reply(embed=embed)

        else:
            # find which option is correct????
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
            await self.initiation.checkserver(ctx)
            doc_ref = self.db.collection(u'users').document(
                u'{}'.format(str(ctx.author.id)))
            doc = doc_ref.get()
            if doc.exists:
                dict1 = doc.to_dict()
                if ans == str(results["correct_answer"]):
                    dict1["money"] = dict1["money"] + \
                        random.randint(0, moneyToAdd)
                    embed = discord.Embed(
                        title="Correct Answer! You win 3 money!",
                        description="You now have " +
                        str(dict1["money"]) + " money!",
                        color=self.client.primary_colour
                    )
                    await ctx.reply(embed=embed)

                else:

                    dict1["money"] = dict1["money"] - \
                        int(random.randint(0, moneyToAdd)/3)
                    embed = discord.Embed(
                        title="Wrong Answer! You lost 1 money!",
                        description=f"You now have " +
                        str(dict1["money"]) +
                        f" money! The correct answer was {results['correct_answer']} :",
                        color=self.client.primary_colour
                    )
                    await ctx.reply(embed=embed)
                doc_ref.set(dict1)

    @commands.command(name="math", description="Answer a math question correctly to gain coins. If you don't get it correct you lose coins!", usage="math")
    async def math(self, ctx):
        first = random.randint(1, 100)
        second = random.randint(1, 100)
        operandation = random.randint(1, 100)
        oper = "+"
        if operandation < 9:
            oper = "*"
            theanswer = str(first*second)
            timehehe = 10 + (first+second-69)/20
        elif operandation < 40:
            oper = "-"
            theanswer = str(first-second)
            timehehe = 6 + (first+second-49)/30
        else:
            timehehe = 4 + (first+second-69)/60
            theanswer = str(first+second)
        timehehe = int(timehehe)

        question_ask = "What is " + str(first) + oper + str(second) + "?"

        embed = discord.Embed(
            title=question_ask,

            description="You have " +
            str(timehehe) + " seconds to answer! You only have one chance.",
            color=self.client.primary_colour
        )
        await ctx.reply(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            messageanswer = await self.client.wait_for('message', timeout=timehehe, check=check)
            msgcontent = messageanswer.content

            await self.initiation.checkserver(ctx)
            doc_ref = self.db.collection(u'users').document(
                u'{}'.format(str(ctx.author.id)))
            doc = doc_ref.get()
            if doc.exists == False:
                print("Nonexistant database")
                return
            dict1 = doc.to_dict()
            if msgcontent == theanswer:
                added = random.randint(1, 3)
                embed = discord.Embed(
                    title="Your answer " + theanswer + " was correct!",
                    description=f"You are veery beeg brain! U gained {added}",
                    color=self.client.primary_colour
                )
                dict1["money"] += added
                await ctx.reply(embed=embed)

            else:
                embed = discord.Embed(
                    title="Your answer was wrong! The correct answer was " + theanswer,
                    description=f"Not beeg brain :'( U lost 1 money!",
                    color=self.client.primary_colour
                )
                dict1["money"] -= 1
                if dict1["money"] < 0:
                    dict1["money"] = 0
                await ctx.reply(embed=embed)
            doc_ref.set(dict1)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="You took too long. You math noob.",
                description="How saddening",
                color=self.client.primary_colour
            )
            await ctx.reply(embed=embed)

    @commands.command(name="scramble", description="Try to unscramble a word!", usage="scramble")
    async def scramble(self, ctx):
        wordCount = 5
        chosenWords = []
        correctWords = []
        with open(file=str(os.getcwd()) + "/cogs/word.txt", mode="r") as f:
            wordDict = f.read().split('\n')
            for i in range(wordCount):
                firstWord = list(random.choice(wordDict))
                word = copy.copy(firstWord)
                random.shuffle(firstWord) 
                newWord = ''.join(word)
                newStartWord = ''.join(firstWord)
                chosenWords.append(newStartWord)
                correctWords.append(newWord)
        print(correctWords)
        embed = discord.Embed(
            title="Scrambled words",
            description=f"The words you have to unscramble are: {', '.join(chosenWords)}",
            color=self.client.primary_colour
        )
        await ctx.reply(embed=embed)
        await ctx.send("You have 1 minute to unscramble the word. Everytime u send a message and it contains a correct word, the timer will reset")

        # firebase 
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        await self.initiation.checkserver(ctx)
        doc_ref = self.db.collection(u'users').document(u'{}'.format(str(ctx.author.id)))
        doc = doc_ref.get()
        if doc.exists == False:
            print("Nonexistant database")
            return
        dict1 = doc.to_dict()

        while True:
            try:
                messageanswer = await self.client.wait_for('message', timeout=60, check=check)
                msgcontent = messageanswer.content
                if msgcontent in correctWords:
                    toAdd = len(msgcontent)
                    dict1["money"] += toAdd
                    moneynow = dict1["money"]
                    embed = discord.Embed(
                        title="Correct answer",
                        description=f"The word was {msgcontent}, you gained {toAdd} money! You now have {moneynow} money! :D",
                        color=self.client.primary_colour
                    )
                    await messageanswer.reply(embed=embed)
                    correctWords.remove(msgcontent)
                    if len(chosenWords) == 0:
                        embed = discord.Embed(
                            title="You won!",
                            description="You have won the game!",
                            color=self.client.primary_colour
                        )
                        await messageanswer.reply(embed=embed)
                        break
                else:
                    embed = discord.Embed(
                        title="Wrong answer",
                        description="Continue guessing. Oof. Oof. Oof.",
                        color=0xff0000
                    )
                    await messageanswer.reply(embed=embed)

            except asyncio.TimeoutError:
                lost = random.randint(1, 10)
                dict1["money"] -= lost
                embed = discord.Embed(
                    title="Time has run out...",
                    description=f"How saddening, you lost {lost} money, you currently have {dict1['money']}",
                    color=self.client.primary_colour
                )
                await ctx.reply(embed=embed)
                break
        doc_ref.set(dict1)

    
def setup(client):
    client.add_cog(Quiz(client))


def check(msg, ctx):
    return msg.author == ctx.author and msg.channel == ctx.channel
