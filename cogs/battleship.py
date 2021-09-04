import asyncio
from discord.ext import commands
from copy import deepcopy

from utils import check
from utils.classesish import gendispatch

# Game logic
# Data... and code
def Pos(x, y):
    def px():
        return x
    def py():
        return y

    return gendispatch(locals())


SHPOHOR = 0
SHPOVER = 1
def Ship(id, length, pos, orient):  # creates a ship
    # id should be unique; will not be checked; make sure it is indeed unique!
    def getid():
        return id
    def getlength():
        return length
    def getpos():
        return pos
    def getori():
        return orient

    return gendispatch(locals())


def Grid(xsz, ysz, data, cnt):  # creates a grid
    # gfill's dimensions will not be checked; make sure they are correct!

    def getxsz():
        return xsz
    def getysz():
        return ysz
    def getdata():
        return data
    def getcnt():
        return cnt

    def putship(shplen, shppos, orient):
        """
        empty cells must be set to None
        does nothing if there's overlap
        """
        d = deepcopy(data)
        if orient == SHPOHOR:
            for i in range(shppos("PX")(), shppos("PX")() + shplen):
                if d[shppos("PY")()][i] != None:
                    return Grid(xsz, ysz, d, cnt)
            for i in range(shppos("PX")(), shppos("PX")() + shplen):
                # This loop must be seperate!
                d[shppos("PY")()][i] = Ship(cnt + 1, shplen, shppos, orient)
        else:
            for i in range(shppos("PY")(), shppos("PY")() + shplen):
                if d[i][shplen("PX")()] != None:
                    return Grid(xsz, ysz, d, cnt)
            for i in range(shppos("PY")(), shppos("PY")() + shplen):
                # This loop must be seperate!
                d[i][shppos("PX")()] = Ship(cnt + 1, shplen, shppos, orient)

        return Grid(xsz, ysz, d, cnt + 1)

    def killcell(cellpos):
        d = deepcopy(data)
        d[cellpos("PY")()][cellpos("PX")()] = None
        return Grid(xsz, ysz, d, cnt)

    return gendispatch(locals())

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
                f"2 players have joined, battleship game starting... <@{user1.id}>, <@{user2.id}>. "
                "This game will be carried out in your DMs to prevent cheating!"
            )
        except asyncio.TimeoutError:
            await ctx.reply("No one else joined, please try again later!")
            return




def setup(client):
    client.add_cog(Battleship(client))

