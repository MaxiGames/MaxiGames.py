from bs4 import BeautifulSoup as soup
import os
from urllib.request import urlopen as uReq
import bs4
import random
from discord.ext.commands import cooldown, BucketType
import discord
from discord.ext import commands
import math
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import asyncio
import time
from utils.paginator import Paginator
from utils.leaderboard import leaderboard_generate
from firebase_admin import firestore

alpha = "abcdefghijklmnopqrstuvwxyz"


class Hangman(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.db = firestore.client()
        self.init = self.client.get_cog("Init")
    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def hangmanList(self, ctx):
        dir = os.getcwd() + "/DataBase/words.txt"
        words = open(dir, "r")
        myList = []
        for topic in words:
            myList.append(topic.rstrip("\n"))
        words.close()

        #! PAGES
        pages = []
        page = discord.Embed(
            title="Help",
            description="List of hangman topics",
            colour=self.client.primary_colour,
        )
        page.set_author(
            name=self.client.user.name, icon_url=self.client.user.avatar_url
        )
        page.set_footer(text="Press Next to see the next page of topics")
        pages.append(page)

        length = len(myList)
        total_pages = length // 20 + 1
        count = 0
        count1 = 0
        for i in range(0, total_pages):
            count1 += 1
            string = ""
            for j in range(0, 20):
                count += 1
                if i * 20 + j >= length:
                    break
                curList = myList[i * 20 + j]
                string += f"{count}. `{str(curList)}` \n"
            page = discord.Embed(
                title=str(count1), description=string, colour=self.client.primary_colour
            )
            page.set_author(
                name=self.client.user.name, icon_url=self.client.user.avatar_url
            )
            pages.append(page)
        page_num = 0
        msg = await ctx.send(
            embed=pages[page_num],
        )
        page = Paginator(self.client, ctx, msg, pages, timeout=120)
        await page.start()
    
    @commands.command(name="hangman", description="Play hangman, the classic word-guessing game! Rewards money if you win.", usage="hangman")
    @cooldown(1, 30, BucketType.user)
    async def hangman(self, ctx):
        #! Hangman Firebase Initalisation
        self.init = self.client.get_cog("Init")
        await self.init.checkserver(ctx)
        doc_ref = self.db.collection("users").document(str(ctx.author.id))
        doc = doc_ref.get()
        data = doc.to_dict()

        #! Retriving data
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        dir = os.getcwd() + "/DataBase/words.txt"
        words = open(dir, "r")
        myList = []
        for topic in words:
            myList.append(topic.rstrip("\n"))
        words.close()
        await ctx.reply(
            embed=discord.Embed(
                title="You have **1 minute** to choose one topic. Do `m!hangmanList` to check all the topics.",
                colour=0x00FF00,
            )
        )

        #! Waiting for a reply
        chosenTopic = ""
        while True:
            try:
                message = await self.client.wait_for(
                    "message", timeout=60, check=check
                )
                if (
                    message.content == "m!hangmanList"
                    or message.content == "!hangmanList"
                ):
                    continue
                elif message.content in myList:
                    chosenTopic = message.content
                    await message.reply(
                        embed=discord.Embed(
                            title="You have chosen **" + chosenTopic + "**",
                            colour=0x00FF00,
                        )
                    )
                    break
                else:
                    await message.reply(
                        embed=discord.Embed(
                            title="That is not a valid topic- Spacing, Capitalisation and Spelling are important",
                            colour=0x00FF00,
                        )
                    )

            except asyncio.TimeoutError:
                await ctx.reply(
                    embed=discord.Embed(
                        title="Hangman game aborted due to Timeout",
                        description="",
                        colour=0x00FF00,
                    )
                )
                return

        if chosenTopic == "":
            return

        dir = os.getcwd() + "/DataBase/" + chosenTopic
        specificWords = open(dir, "r")
        wordList = []
        for hangmanWord in specificWords:
            wordList.append(hangmanWord.rstrip("\n"))
        specificWords.close()

        wordChoice = random.choice(wordList)
        wordChoice = wordChoice.lower()
        while True:
            res = True
            for i in wordChoice:
                if i not in alpha:
                    res = False
                    break
            if res:
                break
            else:
                wordChoice = random.choice(wordList)
                wordChoice = wordChoice.lower()
        correctWord = []
        currentGuess = []
        answer = ""
        for i in range(len(wordChoice)):
            correctWord.append(wordChoice[i])
            if wordChoice[i] == " ":
                answer = answer + " "
                currentGuess.append(" ")
            else:

                currentGuess.append("□")
                answer = answer + "□"

        embed = discord.Embed(
            title="Your hangman game: ", description=answer, color=0xFFFF00
        )

        def maxi(a, b):
            if a > b:
                return a
            else:
                return b

        lives = maxi(5, math.floor(len(wordChoice) * 2 / 3))
        word_guessed = 0
        await ctx.reply(embed=embed)
        guessed_letter = []

        #! Main Hangman Portion
        while answer != wordChoice and lives > 0:

            if currentGuess == correctWord:
                break
            try:
                message = await self.client.wait_for("message", timeout=45, check=check)
                messageanswer = message.content.lower()
                if len(str(messageanswer)) == 1:
                    if str(messageanswer) in guessed_letter:
                        embed = discord.Embed(
                            title="You already guessed that letter!",
                            description="Try again!",
                            color=0xFF0000,
                        )
                        await message.reply(embed=embed)
                        continue
                    ok = 0
                    guessed_letter.append(str(messageanswer))

                    answer = ""
                    for i in range(len(correctWord)):
                        if messageanswer == correctWord[i]:
                            currentGuess[i] = correctWord[i]
                            answer += currentGuess[i]
                            ok = 1
                    if ok == 0:
                        lives -= 1
                        embed = discord.Embed(
                            title="Oof... Your guess wasn't correct.",
                            description=f"Try again using individual character or whole word guesses! You have {lives} lives left",
                            color=0xFF0000,
                        )
                    else:
                        embed = discord.Embed(
                            title="Pog! Your guess is correct!",
                            description=f"The word now is {' '.join(currentGuess)}! You have {lives} lives left",
                            color=self.client.primary_colour,
                        )
                    await message.reply(embed=embed)

                else:
                    if messageanswer == wordChoice:
                        add = math.floor((len(wordChoice) * 3.5) + (5*lives))
                        data["money"] += add

                        if "hangmanWins" not in data:
                            data["hangmanWins"] = 0
                        data["hangmanWins"] += 1

                        embed = discord.Embed(
                            title="You won!",
                            description=f"Congratulations, you guessed the word **{wordChoice}** correctly and gained {add} money! You have {data['money']} money now!",
                            color=0x00FF00,
                        )
                        await message.reply(embed=embed)
                        doc_ref.set(data)
                        return
                    else:
                        lives -= 1
                        embed = discord.Embed(
                            title="Your guess was wrong!",
                            description=f"Try again using individual character or whole word guesses! You have {lives} lives left",
                            color=0xFF0000,
                        )
                        await message.reply(embed=embed)
            except asyncio.TimeoutError:
                await ctx.reply(
                    embed=discord.Embed(
                        title="Hangman game aborted due to Timeout",
                        description="",
                        colour=0x00FF00,
                    )
                )
                return
        if lives == 0:
            deduct = random.randint(1, 10)
            data["money"] -= deduct
            if data["money"] < 0:
                data["money"] = 0
            embed = discord.Embed(
                title="You lost!",
                description=f"The word was **{wordChoice}**, {deduct} money was subtracted off your account :(. You currently have {data['money']} money",
                color=0xff0000
            )
            await message.reply(embed=embed)
            doc_ref.set(data)
        elif word_guessed == 0:
            add = math.floor((len(wordChoice) * 3.5) + (5*lives))
            data["money"] += add

            if "hangmanWins" not in data:
                data["hangmanWins"] = 0
            data["hangmanWins"] += 1

            embed = discord.Embed(
                title="You won!",
                description=f"Congratulations, you guessed the word **{wordChoice}** correctly and gained {add} money! You have {data['money']} money now!",
                color=0x00FF00,
            )
            await message.reply(embed=embed)
            doc_ref.set(data)
            
    @commands.command(title="hangmanLB", help="The leaderboard for hangman", aliases=["hangmanleaderboard"])
    @cooldown(1, 15, BucketType.user)
    async def hangmanLB(self, ctx):
        await leaderboard_generate(self, ctx, "hangman")


def setup(client):
    client.add_cog(Hangman(client))


