import discord
from discord.ext import commands
from firebase_admin import firestore
import threading
import time

class VoteRewards(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.autoresponse = {}
        self.db = firestore.client()
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot and ctx.channel.id == 879697234340491274:
            #! is sent by the bot

            # get the id of the user
            content = ctx.content
            print(content)
            userId = int(content.replace("Thank you for the upvote <@", "").replace(">", ""))
            doc_ref = self.db.collection("users").document("{}".format(str(userId)))
            doc = doc_ref.get().to_dict()
            if doc == None:
                doc = {"voteReward": time.time()}
            else:
                doc["voteReward"] = time.time()
                if "money" in doc.keys():
                    doc["money"] += 500
                else:
                    doc["money"] = 500
                num = doc["money"]
            doc_ref.set(doc)

def setup(client):
    client.add_cog(VoteRewards(client))  
