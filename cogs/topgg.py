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
            #! is sent by the bo

            # get the id of the user
            content = ctx.content
            userId = int(content.replace("Thank you for the upvote <@", "").replace(">", ""))
            doc_ref = self.db.collection("users").document("{}".format(str(userId)))
            doc = doc_ref.get().to_dict()
            if doc == None:
                doc = {"voteReward": time.time()}
            else:
                doc["voteReward"] = time.time()
            doc_ref.set(doc)

            await ctx.send("Thank you for the upvote <@{}>! You will receive a reward in the next 24 hours!".format(userId))

def setup(client):
    client.add_cog(VoteRewards(client))  
