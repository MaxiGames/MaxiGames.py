
from bs4 import BeautifulSoup as soup
import os
from urllib.request import urlopen as uReq
import bs4
import random
import discord
from discord.ext import commands
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import asyncio
import time

class Hangman(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False

    @commands.command()
    async def hangman(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        dir = os.getcwd() + "/DataBase/words.txt"
        words = open(dir, "r")
        myList = []
        for topic in words:
            myList.append(topic.rstrip("\n"))
        words.close()

        await ctx.reply(embed = discord.Embed(title="Hangman Topics: (you have 45 seconds to choose one)", description=', '.join(myList), colour=0x00ff00))

        chosenTopic = ""
        while True:
            try:
                message = await self.client.wait_for('message', timeout=45, check=check)
                if message.content in myList:
                    chosenTopic = message.content
                    await message.reply(embed = discord.Embed(title="You have chosen **" + chosenTopic + "**", colour=0x00ff00))
                    break
                else:
                    await message.reply(embed = discord.Embed(title="That is not a valid topic- Spacing, Capitalisation and Spelling are important", colour=0x00ff00))

            except asyncio.TimeoutError:
                await ctx.reply(embed = discord.Embed(title="Hangman game aborted due to Timeout", description="", colour=0x00ff00))
                return
        
        if chosenTopic == "":
            return
        
        dir=os.getcwd() + "/DataBase/" + chosenTopic
        specificWords=open(dir, "r")
        wordList = []
        for hangmanWord in specificWords:
            wordList.append(hangmanWord.rstrip("\n"))
        specificWords.close()

        wordChoice = random.choice(wordList)
        while True:
            res = True
            for i in wordChoice:
                res = res and isalpha(i)
            if res:
                break
            else:
                wordChoice = random.choice(wordList)
        correctWord = []
        currentGuess = []
        answer = ""
        for i in range(len(wordChoice)):
            correctWord.append(wordChoice[i])
            print(wordChoice[i])
            currentGuess.append("□")
            answer = answer + "□" + " "
        
        embed = discord.Embed(
            title = "Your hangman game: ",
            description = answer,
            color = 0xffff00
        )
        lives = 5
        await ctx.reply(embed=embed)

        while answer != wordChoice and lives > 0:
            try:
                message = await self.client.wait_for('message', timeout=45, check=check)
                messageanswer = message.content.lower()
                if len(str(messageanswer)) == 1:
                    ok = 0
                    answer = ""
                    for i in range(len(correctWord)):
                        if messageanswer == correctWord[i]:
                            currentGuess[i] = correctWord[i]
                            answer += currentGuess[i]
                            ok = 1
                    if ok == 0:
                        lives -= 1
                        embed = discord.Embed(
                            title = "Oof... Your guess wasn't correct.",
                            description = f"Try again using individual character or whole word guesses! You have {lives} lives left",
                            color = 0xff0000
                        )
                    else:
                        embed = discord.Embed(
                            title = "Pog! Your guess is correct!",
                            description = f"The word now is {' '.join(currentGuess)}! You have {lives} lives left",
                            color = self.client.primary_colour
                        )
                    await ctx.reply(embed=embed)
                    
                else:
                    if messageanswer == wordChoice:
                        embed=discord.Embed(
                            title = "You guessed the word!",
                            description = "The word was " + wordChoice,
                            color = self.client.primary_colour
                        )
                        answer = messageanswer
                        await message.reply(embed=embed)
                    else:
                        lives -= 1
                        embed = discord.Embed(
                            title = "Your guess was wrong!",
                            description = f"Try again using individual character or whole word guesses! You have {lives} lives left",
                            color = 0xff0000
                        )
                        await message.reply(embed=embed)
            except asyncio.TimeoutError:
                await ctx.reply(embed = discord.Embed(title="Hangman game aborted due to Timeout", description="", colour=0x00ff00))
                return
        if lives == 0:
            embed = discord.Embed(
                title = "You lost!",
                description = "The word was " + wordChoice,
                color = 0xff0000
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title = "You won!",
                description = "The word was " + wordChoice,
                color = 0x00ff00
            )
            await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(Hangman(client))

# ! DO NOT DELETE- DATABASE RETRIEVER
# # --------GET HANGMAN FILES------------
# starttime = time.time()

# # --------FIRST PARSE OF LINKS----------
# my_url = "https://www.enchantedlearning.com/wordlist"
# uClient = uReq(my_url)
# page_html = uClient.read()
# uClient.close()

# page = soup(page_html, "html.parser")

# table = page.select(
#     "body > p:nth-child(13) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)"
# )
# tables = page.find_all("td")

# counter = 12
# links = []
# topic = []


# while counter <= 15:
#     container = tables[counter].find_all("a")
#     for label in container:
#         links.append(label.get("href"))
#         topic.append(label.text.replace("/", "").replace('"', ""))
#     counter += 1

# # ---------SECOND PARSE OF WORDS------------
# numberOfWords = 0
# hallo = input(
#     """Do you have a folder named 'Database' with files inside already?
# If yes, input 1(safer option if this is ur first time running this), if not, input anything else
# WARNING: IF THERE IS NO FILES REQUIRED, it might crash!"""
# )

# if hallo == "1":
#     a = input(
#         """Is it alright if we create a few files showing the databank of words for this?
# WARNING: This takes > 3.35 minutes, depending on internet speed and CPU
# If you think you do not have it (checking system to see if u already have it or no coming up), please input 1. Otherwise, input anything. """
#     )

#     if a == "1":
#         while True:
#             try:
#                 os.chdir(str(os.getcwd()) + "/DataBase")
#                 break
#             except:
#                 print("U do not have a Database, creating it now...")
#                 try:
#                     directory = "DataBase"
#                     parent_dir = os.getcwd()
#                     path = os.path.join(parent_dir, directory)
#                     os.mkdir(path)
#                     os.chdir(str(os.getcwd()) + "/DataBase")
#                     break
#                 except:
#                     print("Failed to make database, please report error to github")

#         print("Making files in " + str(os.getcwd()) + " ")

#         counter1 = 0

#         for i in topic:
#             with open(i, "w+") as file1:
#                 website = "https://www.enchantedlearning.com" + links[counter1]
#                 uClient = uReq(website)
#                 page_html = uClient.read()
#                 uClient.close()
#                 page = soup(page_html, "html.parser")
#                 for word in page.find_all("div", {"class": "wordlist-item"}):
#                     file1.write(word.text)
#                     file1.write("\n")
#                     numberOfWords += 1
#             counter1 += 1
#             print(f"Made file with topic {topic[counter1-1]}")

#         endtime = time.time()
#         totaltime = str(abs(round(starttime - endtime, 5) / 60))
#         print(
#             f"It took {totaltime} minutes to run the program! A total of {numberOfWords} words has been added to the database"
#         )
#         os.chdir("..")

