import firebase_admin
from firebase_admin import firestore

import discord
from discord.ext import commands
from cogs.init import Init

db = firestore.client()


def is_staff():
    async def predicate(ctx):
        doc_ref = db.collection(u"admin").document(u"{}".format("authorised"))
        doc = doc_ref.get()
        people = doc.to_dict()
        allowed = people["owner"] + people["staff"]
        if str(ctx.author.id) not in allowed:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)


def is_owner():
    async def predicate(ctx):
        doc_ref = db.collection(u"admin").document(u"{}".format("authorised"))
        doc = doc_ref.get()
        people = doc.to_dict()
        allowed = people["owner"]
        if str(ctx.author.id) not in allowed:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)


def is_banned():
    async def predicate(ctx):
        doc_ref = db.collection(u"admin").document(u"{}".format("banned"))
        doc = doc_ref.get()
        people = doc.to_dict()
        if str(ctx.author.id) in people:
            raise commands.MissingPermissions([])
        else:
            return True

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        doc_ref = db.collection(u"admin").document(u"{}".format("authorised"))
        doc = doc_ref.get()
        people = doc.to_dict()
        allowed = people["owner"] + people["staff"]
        if (
            str(ctx.author.id) not in allowed
            and not ctx.message.author.guild_permissions.administrator
        ):
            raise commands.MissingPermissions([])
        else:
            return True

    return commands.check(predicate)


async def _isadmin(ctx, pri=True):
    doc_ref = db.collection(u"admin").document(u"{}".format("authorised"))
    doc_ = doc_ref.get()
    if doc_.exists:
        doc = doc_.to_dict()
        if str(ctx.author.id) in doc["owner"] or str(ctx.author.id) in doc["staff"]:
            staff = True
    if ctx.message.author.guild_permissions.administrator or staff:
        if pri:
            await ctx.reply("Of course")
        return True
    else:
        if pri:
            await ctx.reply("What made you think you did...")
        return False
