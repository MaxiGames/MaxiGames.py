import asyncio
from discord.ext import commands
from copy import deepcopy

from utils import check
from utils.classesish import gendispatch
""" 
# Game logic
# Data... and code
def Pos(x, y):
    return gendispatch(Pos, locals())


SHPOHOR = 0
SHPOVER = 1
def Ship(id, length, pos, orient):  # creates a ship
    # id should be unique; will not be checked; make sure it is indeed unique!
    return gendispatch(Ship, locals())


def Grid(xsz, ysz, data):  # creates a grid
    # gfill's dimensions will not be checked; make sure they are correct!

    def putship(shplen, shppos, orient):
        empty cells must be set to None
        does nothing if there's overlap
        d = deepcopy(data)
        if orient == SHPOHOR:
            for i in range(shppos("_x")(), shppos("_x")() + shplen):
                if d[shppos("_y")()][i] != None:
                    return Grid(xsz, ysz, d)
            for i in range(shppos("_x")(), shppos("_x")() + shplen):
                # This loop must be seperate!
                d[shppos("_y")()][i] = Ship(
                    2 ** shppos("_x")() * 3 ** shppos("_y")(),  # reverse prime factoring :)
                    shplen,
                    shppos,
                    orient
                )
        else:
            for i in range(shppos("_y")(), shppos("_y")() + shplen):
                if d[i][shppos("_x")()] != None:
                    return Grid(xsz, ysz, d)
            for i in range(shppos("_y")(), shppos("_y")() + shplen):
                # This loop must be seperate!
                d[i][shppos("_x")()] = Ship(
                    2 ** shppos("_x")() * 3 ** shppos("_y")(),  # reverse prime factoring :)
                    shplen,
                    shppos,
                    orient
                )

        return Grid(xsz, ysz, d)

    def killcell(cellpos):
        d = deepcopy(data)
        d[cellpos("_y")()][cellpos("_x")()] = None
        return Grid(xsz, ysz, d)

    return gendispatch(Grid, locals())

"""

class Battleship(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hidden = True

    @check.is_banned()
    @commands.command(
        name="battleship",
        help="Starts a new game of battleship",
        usage="",
        aliases=["battle", "bs", "battleships"],
    )
    async def battleship(self, ctx):
        message = await ctx.reply(
            "React on this message to start a battleship game, another person is needed for this game to start!"
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
            reaction, user2 = await self.client.wait_for(
                "reaction_add", timeout=45, check=check
            )
            await ctx.reply(embed=discord.Embed(title = 
                f"2 players have joined, battleship game starting... <@{user1.id}>, <@{user2.id}>.", 
                description = "This game will be carried out in your DMs to prevent cheating!",
                color = self.client.primary_colour
            ).add_field(name="Player 1", value=f"{user1.mention}", inline=False))
            .add_filed(name="Player 2", value=f"{user2.mention}", inline=False))
            .add_field(name="Battleship sizes", value="1, 2, 3, 4, 5"))

            #! Players have joined, initalising board
            board = []
            for i in range(8):
                board.append([])
                for j in range(8):
                    board[i].append("O")
            
            battleshipSizes = [1, 2, 3, 4, 5]
            ships = []
            for i in battleshipSizes:


        except asyncio.TimeoutError:
            await ctx.reply("No one else joined, please try again later!")
            return 
        


def setup(client):
    client.add_cog(Battleship(client))
