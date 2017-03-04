# VG Module:
# Functions using the VG API. Functions using Discord libraries will be marked by, "!!!DISCORD!!!", in their description.

# IMPORTS
import gamelocker
from gamelocker.strings import pretty
import datetime
import discord
from discord.ext import commands
import TOOL_module as tools

# VG Variables--
keyVG = ""  # VG_API_TOKEN_HERE
apiVG = gamelocker.Gamelocker(keyVG).Vainglory()  # API OBJECT


# Will CHECK if NAME is VALID. Will RETURNS True or False if TYPE = 0, if TYPE = 1 returns ID or False.
def getIDVG(name, type=0):
    name = str(name)  # Convert NAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.datetime.today()
    daterange = str(datenow - datetime.timedelta(days=7)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.datetime.today()) + "T00:00:00Z"  # CURRENT DATE

    try:
        matches = apiVG.matches({"filter[createdAt-start]": "2017-02-16T12:00:00Z", "page[limit]": 2, "filter[playerNames]": name})
        for r in matches[0].rosters:
            for p in r.participants:
                if p.player.name == name:
                    if type == 0:  # Returns TRUE when name is FOUND
                        return True
                    elif type == 1:  # Returns ID when name is FOUND
                        return p.player.id

    except:  # Returns FALSE whenever an ERROR occurs
        return False

# Will get VG GAME MATCHES according to NAME.
def getGameMatchesVG(name):
    name = str(name)  # Converts NAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.datetime.today()
    daterange = str(datenow - datetime.timedelta(days=7)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.datetime.today()) + "T00:00:00Z"  # CURRENT DATE

    try:  # Tries to FIND PLAYER matches in NA servers
        mathes = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]" : 50, "sort" : "createAt", "filter[playerNames]" : name})
    except:
        try:  # Tries to FIND PLAYER matches in EU servers
            matches = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]" : 50, "sort" : "createAt", "filter[playerNames]" : name})
        except:
            print("!!!SOMETHING WENT HORRIBLY WRONG WHILE TRYING TO FETCH VG MATCHES FOR " + name + "!!!")

# GETS a PLAYERS LIFE time INFORMATION with ID. ID = ID or NAME for player, givenname = If True then ID is actually a NAME, server = Server to work with
def getPlayerInfoVG(ID, givenname=False, server="na"):
    ID = str(ID)  # Convert ID to a STRING to prevent errors

    if givenname == True:  # Checks to see if ID is actually a NAME if so then TURN it into a ID
        ID = str(getIDVG(ID, type=1))

    info = apiVG.player(ID)
    return info

# Get a PLAYERS performance from RANGE of DAYS with the players NAME
def getPlayerPerformanceVG(name, days=7, game=""):
    name = str(name)  # Convert NAME to STRING to prevent errors
    days = int(days)  # Convert DAYS to INT to prevent errors
    game = str(game)  # Convert GAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=days)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    filterVG = {"filter[createdAt-start]": daterange, "page[limit]": 50, "filter[playerNames]": name}  # DEFAULT things to FILTER VG MATCHES BY

    if game == "casual":
        filterVG["filter[gameMode]"] = "casual"

    elif game == "rank":
        filterVG["filter[gameMode]"] = "ranked"

    elif game == "royal":
        filterVG["filter[gameMode]"] = "casual_aral"

    elif game == "blitz":
        filterVG["filter[gameMode]"] = "blitz_pvp_ranked"

    print(filterVG)

    try:  # TRY to find MATCHES in NA
        matches = apiVG.matches(filterVG, "na")  # GET MATCHES from NA

    except:  # If NOTHING is FOUND then search EU
        try:
            matches = apiVG.matches(filterVG, "eu")

        except:  # If NOTHING is FOUND then search SEA
            try:
                matches = apiVG.matches(filterVG, "sea")

            except:  # If NOTHING is FOUND then search EA
                try:
                    matches = apiVG.matches(filterVG, "ea")

                except:  # If NOTHING is FOUND then search SA
                    try:
                        matches = apiVG.matches(filterVG, "sa")

                    except:
                        return "Couldn't get any matches for **" + str(name) + "** from the past " + str(days) + " days in any server!"  # RETURN if player MATCHES AREN'T FOUND

    # Get DATA out of the MATCH OBJECTS
    playerdata = []
    for match in matches:
        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    playerdata.append(participant.to_dict())  # If DATA belongs to PLAYER then KEEP

    # DATA VARIABLES
    size = int(len(playerdata)) - 1  # Get the SIZE of the PLAYERSDATA

    # PROFILE VARIABLES ~ most of this will be USED for MEAN and MODE
    actor = []
    assists = []
    crystalMineCaptures = []
    deaths = []
    farm = []
    goldMineCaptures = []
    itemslist = []
    karmaLevel = []
    kills = []
    krakenCaptures = []
    level = 0
    minionKills = []
    skillTier = []
    skinKey = []
    turretCaptures = []
    wentAfk = []
    winner = []

    num = 0
    # Go though PLAYERDATA getting DATA needed and building a PROFILE
    for data in playerdata:
        attributes = data["attributes"]
        stats = attributes["stats"]

        actor.append(pretty(attributes["actor"]))
        assists.append(stats["assists"])
        crystalMineCaptures.append(stats["crystalMineCaptures"])
        deaths.append(stats["deaths"])
        farm.append(stats["farm"])
        goldMineCaptures.append(stats["goldMineCaptures"])

        for item in stats["items"]:  # LOOPS the ITEMS for EACH MATCH ADDING it to the ITEMSLIST
            itemslist.append(pretty(item))

        karmaLevel.append(stats["karmaLevel"])
        kills.append(stats["kills"])
        krakenCaptures.append(stats["krakenCaptures"])
        minionKills.append(stats["minionKills"])
        skillTier.append(stats["skillTier"])
        skinKey.append(pretty(stats["skinKey"]))
        turretCaptures.append(stats["turretCaptures"])
        wentAfk.append(stats["wentAfk"])
        winner.append(stats["winner"])

        if num == size:
            level = stats["level"]
        num += 1

    print(str(actor) + " | actors")
    print(str(assists) + " | assists")
    print(str(crystalMineCaptures) + " | crystalMineCaptures")
    print(str(deaths) + " | deaths")
    print(str(farm) + " | farm")
    print(str(goldMineCaptures) + " | goldMineCaptures")
    print(str(itemslist) + " | itemslist")
    print(str(karmaLevel) + " | karmaLevel")
    print(str(kills) + " | kills")
    print(str(krakenCaptures) + " | krakenCaptures")
    print(str(level) + " | level")
    print(str(minionKills) + " | minionKills")
    print(str(skillTier) + " | skillTier")
    print(str(skinKey) + " | skinKey")
    print(str(turretCaptures) + " | turretCaptures")
    print(str(wentAfk) + " | wentAfk")
    print(str(winner) + " | winner")

    msg = "__**PERFORMANCE REPORT FOR " + str(name) + " FROM THE PAST " + str(days) + " DAYS"  # BEGINNING of MESSAGE being RETURNED

    if game != "":
        msg += " FROM " + str(game) + " GAMES!"

    msg += "**__"

    # Adding the TOP ACTORS used in the past X days to MSG
    actors = tools.giveListInOrderTOOL(actor)
    if len(actors) <= 0:  # If NO ACTORS were FOUND then NOTICE USER about it
        msg += "\n**We couldn't get any actors from your matches!**"

    else:
        msg += "\n**Actors Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(actors) < 5:  # If LESS then FIVE ACTORS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(actors) - 1

        elif len(actors) >= 5:  # If FIVE or MORE ACTORS were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED ACTORS
            msg += "\n**" + str(num + 1) + "** ~ *" + str(actors[num]) + "*"
            num += 1

    # Adding KILLS MEAN from the past X days to MSG
    msg += "\n**Kills per Game:** *" + str(round(tools.giveMeanOfList(kills), 2)) + "*"

    # Adding ASSISTS MEAN from the past X days to MSG
    msg += "\n**Assists per Game:** *" + str(round(tools.giveMeanOfList(assists), 2)) + "*"

    # Adding DEATHS MEAN from the past X days to MSG
    msg += "\n**Deaths per Game:** *" + str(round(tools.giveMeanOfList(deaths), 2)) + "*"

    # Adding FARM MEAN from the past X days to MSG
    msg += "\n**Farm per Game:** *" + str(round(tools.giveMeanOfList(farm), 2)) + "*"

    # Adding MINIONKILLS MEAN from the past X days to MSG
    msg += "\n**Minions Killed per Game:** *" + str(round(tools.giveMeanOfList(minionKills), 2)) + "*"

    # Adding SKILLTIER MEAN from the past X days to MSG
    msg += "\n**Skill Tier Average Every Game:** *" + str(round(tools.giveMeanOfList(skillTier))) + "*"

    # Adding WINNER MEAN from the past X days to MSG
    msg += "\n**Victory Rate:** *" + str(round(tools.giveMeanOfList(winner))) + "*"

    # Adding WENTAFK MEAN from the past X days to MSG
    msg += "\n**AFK Rate:** *" + str(round(tools.giveMeanOfList(wentAfk))) + "*"

    # Adding TURRETCAPTURES MEAN from the past X days to MSG
    msg += "\n**Turrets Destroyed per Game:** *" + str(round(tools.giveMeanOfList(turretCaptures))) + "*"

    # Adding KRAKEN MEAN from the past X days to MSG
    msg += "\n**Kraken Captures per Game:** *" + str(round(tools.giveMeanOfList(krakenCaptures))) + "*"

    # Adding the TOP SKINS used in the past X days to MSG
    skins = tools.giveListInOrderTOOL(skinKey)
    if len(skins) <= 0:  # If NO SKINS were FOUND then NOTICE USER about it
        msg += "\n**We couldn't get any skins from your matches!**"

    else:
        msg += "\n**Skins Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(skins) < 5:  # If LESS then FIVE SKINS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(skins) - 1

        elif len(skins) >= 5:  # If FIVE or MORE SKINS were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED SKINS
            msg += "\n**" + str(num + 1) + "** ~ *" + str(skins[num]) + "*"
            num += 1

    # Adding  MEAN from the past X days to MSG
    msg += "\n**Average Karma Every Game:** *" + str(round(tools.giveMeanOfList(karmaLevel))) + "*"

    # Adding  MEAN from the past X days to MSG
    msg += "\n**Gold Mine Captures:** *" + str(round(tools.giveMeanOfList(goldMineCaptures))) + "*"

    # Adding  MEAN from the past X days to MSG
    msg += "\n**Crystal Mine Captures:** *" + str(round(tools.giveMeanOfList(crystalMineCaptures))) + "*"

    # Adding the TOP ITEMS used in the past X days to MSG
    items = tools.giveListInOrderTOOL(itemslist)
    if len(items) <= 0:  # If NO ITEMS were FOUND then NOTICE USER about it
        msg += "\n**We couldn't get any items from your matches!**"

    else:
        msg += "\n**Items Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(items) < 5:  # If LESS then FIVE ITEMS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(items) - 1

        elif len(items) >= 5:  # If FIVE or MORE ITEMS were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED ITEMS
            msg += "\n**" + str(num + 1) + "** ~ *" + str(items[num]) + "*"
            num += 1

    # Adding  MEAN from the past X days to MSG
    msg += "\n**Players Level:** *" + str(level) + "*"

    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**** *" + str(round(tools.giveMeanOfList())) + "*"

    msg += ""  # END of MESSAGE BEING SENT
    return msg


# CLASS containing ALL COMMANDS for THIS MODULE
class Vg():
    """All the commands in relation to Vainglory.

            Made with love and some Vainglory api, python - gamelocker.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vgperformance(self, player_name="", days="7", game_type=""):
        """Gets a players performance in the past days.

                >vgperformance (player_name) (days) (game_type)
            player_name   ~   name of player to search for
            days          ~   day range to search from
            game_type     ~   game type you would like performance check   ~   casual, ranked, royal, blitz

        """

        if player_name == "":  # MESSAGE the USER if NO NAME was GIVEN
            await self.bot.say("You need to give a players name at least...")
            return

        if len(str(player_name)) < 3:  # MESSAGE the USER if NAME GIVEN is TOO SHORT
            await self.bot.say("That isn't a valid name... :sweat_smile:")
            return

        if tools.isIntTOOL(player_name) == True:  # MESSAGE the USER if a NUMBER was GIVEN
            await self.bot.say(str(player_name) + " isn't a valid name... :sweat_smile:")
            return

        notice = "Looking for match results for " + str(player_name)

        if days != "" and tools.isIntTOOL(days) == True:  # CHECK DAYS to be a VALID NUMBER
            days = int(days)  # Convert DAYS to INT to prevent ERRORS

            if days > 93:
                days = 93  # MAKE DAYS a VALID RANGE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

            elif days <= 0:
                days = 1  # MAKE DAYS a VALID RANGE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE
            else:
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

        if days != "" and tools.isIntTOOL(days) == False:  # CHECKS if DATE is INVALID if so THEN MESSAGE USER
            await self.bot.say("Sorry but " + str(days) + " isn't a valid number... :sweat_smile:")  # If DAYS is an INVALID number TELL USER
            return

        if game_type != "" and tools.isIntTOOL(game_type) == False:

            if game_type == "casual" or game_type == "rank" or game_type == "royal" or game_type == "blitz":
                notice += " from " + game_type

            else:
                await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
                return

        if game_type != "" and tools.isIntTOOL(game_type) == True:
            await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
            return

        notice += "... :eyes:"

        msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
        await self.bot.edit_message(msg, str(getPlayerPerformanceVG(player_name, days, game_type)))  # RUNS PERFORMANCE FETCH and UPDATES MESSAGE once DONE

    @commands.command()
    async def vgcheckplayer(self, player_name=""):
        """Checks if player exist in vainglory.

                >vgcheckplayer (player_name)
            player_name   ~   name of player to check for

        """

        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        elif tools.isIntTOOL(player_name) == False:
            player_name = str(player_name)  # Convert PLAYER_NAME to STRING to prevent errors

            notice = "Looking for " + player_name + "... :eyes:"  # DEFAULT NOTICE SENT to USER!

            msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
            await self.bot.edit_message(msg, str(getIDVG(player_name)))  # RUNS ID TEST

        else:
            await self.bot.say("Sorry but " + str(player_name) + " isn't a valid name... :sweat_smile:")
            return


def setup(bot):
    bot.add_cog(Vg(bot))