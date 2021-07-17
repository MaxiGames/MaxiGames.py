
from bs4 import BeautifulSoup as soup
import os
from urllib.request import urlopen as uReq
import bs4
import time
import discord
from discord.ext import commands

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
import sys
import time


class Hangman(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = False

    @commands.command()
    async def hangman(self, ctx):
        myList = []
        words = open("../DataBase/words.txt", "r")
        for topic in words:
            myList.append(topic.rstrip("\n"))
        words.close() #can we run it?
    #     while True: 
    #         topic = input(
    #          "Wh
    #          at topic do you want to choose? Type ? for list of topics!")
    #      if topic == "?":
    #          print("----------LIST OF TOPICS AVALIABLE------------")
    #          for word in myList:
    #              print(word)
    #          print("------------------END OF LIST-----------------")
    #      elif topic in myList:
    #          break
    #      else:
    #          Functions.error(
    #              topic,
    #              "Input must be in the list of topics. Input ? for list! (Please check if ur caps differs. It matters!)",
    #          )
      
    #   generatedWord = Functions.generateWord("", topic)
      
    #   shownToUser = []
    #   for i in generatedWord:
    #      shownToUser.append("_")
    #   word = list(generatedWord)
    #   guessedletters = 0  # incldues duplicates
    #   guessedAlph = []
    #   lives = 5
    #   print("You have 6 lives, each incorrect guess is 1 live subtracted")
      
    #   Functions.enumChecker(7)
      
    #   while guessedletters < len(generatedWord):
    #      result = Functions.move(word, guessedAlph, lives, shownToUser)
    #      guessedAlph.append(result[1])
    #      guessedletters += int(result[0])
    #      lives = int(result[2])
      
    #      counter = 0
    #      for i in generatedWord:
    #          if result[1] == i:
    #              shownToUser[counter] = result[1]
    #          counter += 1
      
    #      if lives == 0:
    #          print(
    #              f"Oh no, u have lost all your lives :( THe word was {generatedWord}. Try again next time!"
    #          )
    #          break
    #      if "_" not in shownToUser:
    #          print("You have won! Good job :D")
    #          break
    #      time.sleep(2)
      
    #   Functions.enumChecker(lives + 1)
      
    #   Functions.separationLine()
    #   Functions.separationLine()
      
      
    #   print(
    #      """The word database is taken from enchantedlearning.com.
    #   Hangman ASCII pictures are taken from https://gist.github.com/chrishorton/8510732aa9a80a03c829b09f12e20d9c.
    #   Thanks for playing! More features coming soon!"""
    #   )
      
    #   Functions.separationLine()
      
    #   # --------------------
    #   # end of program
    #   # --------------------
    #   endtime = time.time()
    #   totaltime = startime - endtime
    #   totaltime = str(abs(round(totaltime / 60, 2)))
    #   print(f"You took {totaltime} minutes to complete the Hangman word program!")
    #   time.sleep(10)
      
    #   pass


def setup(client):
    client.add_cog(Hangman(client))


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
#                 os.chdir(str(os.getcwd()) + "../DataBase")
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

