import asyncio
import discord
from utils import check
from discord.ext import commands
import random

# Game logic
# Data
PX = 0
PY = 1
def Pos(x, y):
    def dispatch(n):
        return x if n == 0 else y
    return dispatch


SHPID = 0
SHPLEN = 1
SHPPOS = 2
SHPORI = 3

SHPOHOR = 0
SHPOVER = 1
def Ship(id, length, pos, orient):  # creates a ship
    # id should be unique; will not be checked; make sure it is indeeed unique!
    def dispatch(n):
        if n == 0:
            return id
        elif n == 1:
            return length
        elif n == 2:
            return pos
        else:
            return orient
    return dispatch


GRIDX = 0
GRIDY = 1
GRIDDATA = 2
GRIDCNT = 3  # for internal state
def Grid(xsz, ysz, gfill, cnt):  # creates a grid
    # gfill's dimensions will not be checked; make sure they are correct!
    def dispatch(n):
        if n == 0:
            return xsz
        elif n == 1:
            return ysz
        elif n == 2:
            return gfill
        else:
            return cnt
    return dispatch

# Data done
def grid_putship(shplen, shppos, orient, oldgrid):
    """
    empty cells must be set to None
    does nothing if there's overlap
    """
    d = oldgrid(GRIDDATA)
    if orient == SHPOHOR:
        for i in range(shppos(PX), shppos(PX) + shplen):
            if d[shppos(PY)][i] != None:
                return oldgrid
        for i in range(shppos(PX), shppos(PX) + shplen):
            # This loop must be seperate!
            d[shppos(PY)][i] = Ship(oldgrid(GRIDCNT) + 1, shplen, shppos, orient)
    else:
        for i in range(shppos(PY), shppos(PY) + shplen):
            if d[i][shplen(PX)] != None:
                return oldgrid
        for i in range(shppos(PY), shppos(PY) + shplen):
            # This loop must be seperate!
            d[i][shppos(PX)] = Ship(oldgrid(GRIDCNT) + 1, shplen, shppos, orient)
    return Grid(oldgrid(GRIDX), oldgrid(GRIDY), d, oldgrid(GRIDCNT) + 1)


# The cog

class Battleship(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True

    def generateShips(self):
        ships = []
        return ships
    
    @check.is_banned()
    @commands.command(
        name="battleship",
        help="Starts a new game of battleship",
        usage="",
        aliases=["ship", "battle", "bs"],
    )
    async def battleship(self, ctx):
        message = await ctx.reply(
            "React on this message to start a battleship game, another person is needed!"
        )
        await message.add_reaction("✅")

        user1 = ctx.author
        user2 = None
        def check(reaction, user):
            if reaction.message == message and user.id != self.client.user.id and user.id != user1.id:
                return True
            else:
                return False

        try:
            user2 = await self.client.wait_for(
                "reaction_add", timeout=45, check=check
            )
            await ctx.reply(
                f"2 players have joined, battleship game starting... <@{user1.id}>, <@{user2.id}>. This game will be carried out in your DMs to prevent cheating!"
            )
        except asyncio.TimeoutError:
            await ctx.reply("No one else joined, please try again later!")
            return




def setup(client):
    client.add_cog(Battleship(client))

