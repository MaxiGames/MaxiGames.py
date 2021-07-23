import discord
from discord.ext import commands
from firebase_admin import firestore
import threading
import json
from utils import check

class Autoresponse(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.autoresponse = {}
        self.db = firestore.client()
        self.init = self.client.get_cog("Init")
        docs = self.db.collection(u'servers').stream()
        for doc in docs:
            data = doc.to_dict()["autoresponses"]
            self.autoresponse[str(doc.id)] = data
        
        callback_done = threading.Event()

        # Create a callback on_snapshot function to capture changes
        def on_snapshot(col_snapshot, changes, read_time):
            for change in changes:
                self.autoresponse[str(change.document.id)] = change.document.to_dict()["autoresponses"]
            callback_done.set()

        col_query = self.db.collection(u'servers')
        query_watch = col_query.on_snapshot(on_snapshot)

    @check.is_admin()
    @commands.group(name="autoresponse", invoke_without_command=True)
    async def auto_response(self, ctx):
        responses = self.autoresponse[str(ctx.guild.id)]
        description = ""
        if len(responses) == 0:
            description="This server has no autoresponses."
        else:
            for i, cur in enumerate(responses):
                description += f"{i+1}. {cur}\n"
        embed = discord.Embed(title="Autoresponses", description=description, colour=self.client.primary_colour)

        await ctx.send(embed=embed)
    
    @check.is_admin()
    @auto_response.command(name="add")
    async def add_subcommand(self, ctx, trigger: str, *, response: str):
        self.init = self.client.get_cog("Init")
        self.init.checkserver(ctx)
        doc_ref = self.db.collection("servers").document(str(ctx.guild.id))
        data = doc_ref.get().to_dict()
        data["autoresponses"][trigger] = response
        doc_ref.update(data)

        



def setup(client):
    client.add_cog(Autoresponse(client))