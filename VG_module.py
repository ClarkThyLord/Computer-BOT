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

# GETS a PLAYERS life time INFORMATION
def getPlayerInfoVG(name, mode=""):
    ID = str(name)  # Convert ID to a STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=31)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    filterVG = {'filter[createdAt-start]': daterange, 'page[limit]': 1, 'filter[playerNames]': name}  # DEFAULT things to FILTER VG PLAYERS BY

    # FOR DEBUGGING
    # print(filterVG)

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
                        return "Couldn't find anyone named **" + str(name) + "** in the Vainglory servers from the past 31 days!"  # RETURN if player MATCHES AREN'T FOUND

    for match in matches:  # From that MATCH get the VAINGLORY PLAYER ID
        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    playerID = participant.player.id

    if mode == "" or mode == "user":  # If MODE is DEFAULT or USER SEND regular MESSAGE
        return "The player **" + name + "** was found in the Vainglory servers in the past 31 days!"
    if mode == "dev":  # If MODE is DEV send ID with MESSAGE
        return "The player **" + name + "** was found in the Vainglory servers in the past 31 days! ID: " + playerID


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

    # print(filterVG)

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

    # MATCH VARIABLES
    latestmatch = ""
    gameMode = []

    # Get DATA out of the MATCH OBJECTS
    playerdata = []
    matchNum = 0
    size = len(matches) - 1
    for match in matches:
        if matchNum == size:  # If MATCH is the FIRST MATCH then GET DATA
            latestmatch = str(match.createdAt)

        gameMode.append(str(match.gameMode))
        matchNum += 1

        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    playerdata.append(participant.to_dict())  # If DATA belongs to PLAYER then KEEP

    # FOR DEBUGGING
    # print(str(latestmatch) + " | latestmatch")
    # print(str(gameMode) + " | gameMode")

    # DATA VARIABLES
    size = str(len(playerdata))  # Get the SIZE of the PLAYERSDATA

    # PROFILE VARIABLES ~ most of this will be USED for MEAN and MODE
    actor = []
    assists = []
    crystalMineCaptures = []
    deaths = []
    farm = []
    goldMineCaptures = []
    itemslist = []
    karmaLevel = ""
    kills = []
    krakenCaptures = []
    level = ""
    minionKills = []
    skillTier = ""
    skinKey = []
    turretCaptures = []
    wentAfk = []
    winner = []

    num = 0
    # Go though PLAYERDATA getting DATA needed for building a PROFILE
    for data in playerdata:
        attributes = data["attributes"]
        stats = attributes["stats"]

        if num == 0:  # Gets the DATA from the LATEST MATCH
            level = stats["level"]
            karmaLevel = stats["karmaLevel"]
            skillTier = stats["skillTier"]

        actor.append(pretty(attributes["actor"]))
        assists.append(stats["assists"])
        crystalMineCaptures.append(stats["crystalMineCaptures"])
        deaths.append(stats["deaths"])
        farm.append(stats["farm"])
        goldMineCaptures.append(stats["goldMineCaptures"])

        for item in stats["items"]:  # LOOPS the ITEMS for EACH MATCH ADDING it to the ITEMSLIST
            itemslist.append(pretty(item))

        kills.append(stats["kills"])
        krakenCaptures.append(stats["krakenCaptures"])
        minionKills.append(stats["minionKills"])
        skinKey.append(pretty(stats["skinKey"]))
        turretCaptures.append(stats["turretCaptures"])
        wentAfk.append(stats["wentAfk"])
        winner.append(stats["winner"])

        num += 1

    # FOR DEBUGGING
    # print(str(actor) + " | actors")
    # print(str(assists) + " | assists")
    # print(str(crystalMineCaptures) + " | crystalMineCaptures")
    # print(str(deaths) + " | deaths")
    # print(str(farm) + " | farm")
    # print(str(goldMineCaptures) + " | goldMineCaptures")
    # print(str(itemslist) + " | itemslist")
    # print(str(karmaLevel) + " | karmaLevel")
    # print(str(kills) + " | kills")
    # print(str(krakenCaptures) + " | krakenCaptures")
    # print(str(level) + " | level")
    # print(str(minionKills) + " | minionKills")
    # print(str(skillTier) + " | skillTier")
    # print(str(skinKey) + " | skinKey")
    # print(str(turretCaptures) + " | turretCaptures")
    # print(str(wentAfk) + " | wentAfk")
    # print(tools.giveMeanOfList(wentAfk))
    # print(str(winner) + " | winner")
    # print(tools.giveMeanOfList(winner))

    # CREATING a list(STRING) of the TOP GAMEMODES in the past X days
    gamemodes = tools.giveListInOrderTOOL(gameMode)
    if len(gamemodes) <= 0:  # If NO GAMEMODES were FOUND then NOTICE USER about it
        gamemodelistString = "\n**We couldn't get any game modes from your matches!**"

    elif game != "":
        gamemodelistString = "\n**This is performance from " + str(game) + " games only...**"

    else:
        gamemodelistString = "\n**Game Modes Played Most:**"  # SET TITLE to INFO

        num = 0
        if len(gamemodes) < 5:  # If LESS then FIVE GAMEMODES were FOUND then set NUM to the GAMEMODES LIST LENGTH
            max = len(gamemodes) - 1

        elif len(gamemodes) >= 5:  # If FIVE or MORE GAMEMODES were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED GAMEMODES
            gamemodelistString += "\n**" + str(num + 1) + "** ~ *"

            if str(gamemodes[num]) == "casual":
                gamemodelistString += "Casual*"

            elif str(gamemodes[num]) == "ranked":
                gamemodelistString += "Ranked*"

            elif str(gamemodes[num]) == "casual_aral":
                gamemodelistString += "Royal*"

            elif str(gamemodes[num]) == "blitz_pvp_ranked":
                gamemodelistString += "Blitz*"

            elif str(gamemodes[num]) == "private":
                gamemodelistString += "Private*"

            else:
                gamemodelistString += "Unknown Game Mode"

            num += 1

    # CREATING a list(STRING) of the TOP ACTORS used in the past X days
    actors = tools.giveListInOrderTOOL(actor)
    if len(actors) <= 0:  # If NO ACTORS were FOUND then NOTICE USER about it
        actorslistString = "\n**We couldn't get any actors from your matches!**"

    else:
        actorslistString = "\n**Actors Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(actors) < 5:  # If LESS then FIVE ACTORS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(actors) - 1

        elif len(actors) >= 5:  # If FIVE or MORE ACTORS were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED ACTORS
            actorslistString += "\n**" + str(num + 1) + "** ~ *" + str(actors[num]) + "*"

            if num == 0:  # GETS the THUMBNAIL for MOST USED HERO
                thumbnail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(actors[num]) + ".png"

            num += 1

    # CREATING a list(STRING) of the TOP SKINS used in the past X days
    skins = tools.giveListInOrderTOOL(skinKey)
    if len(skins) <= 0:  # If NO SKINS were FOUND then NOTICE USER about it
        skinslistString = "\n**We couldn't get any skins from your matches!**"

    else:
        skinslistString = "\n**Skins Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(skins) < 5:  # If LESS then FIVE SKINS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(skins) - 1

        elif len(skins) >= 5:  # If FIVE or MORE SKINS were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED SKINS
            skinslistString += "\n**" + str(num + 1) + "** ~ *" + str(skins[num]) + "*"
            num += 1

    # CREATING a list(STRING) of the TOP ITEMS used in the past X days to MSG
    items = tools.giveListInOrderTOOL(itemslist)
    if len(items) <= 0:  # If NO ITEMS were FOUND then NOTICE USER about it
        itemlistString = "\n**We couldn't get any items from your matches!**"

    else:
        itemlistString = "\n**Items Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(items) < 5:  # If LESS then FIVE ITEMS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(items) - 1

        elif len(items) >= 5:  # If FIVE or MORE ITEMS were FOUND then SET NUM to FIVE
            max = 5

        while num < max:  # NAME POSITIONS of most USED ITEMS
            itemlistString += "\n**" + str(num + 1) + "** ~ *" + str(items[num]) + "*"
            num += 1

    # CREATING KILLS MEAN from the past X days
    killsString = "\n**Average Kills:** *" + str(round(tools.giveMeanOfList(kills), 2)) + "*"

    # CREATING ASSISTS MEAN from the past X days
    assistsString = "\n**Average Assists:** *" + str(round(tools.giveMeanOfList(assists), 2)) + "*"

    # CREATING DEATHS MEAN from the past X days
    deathString = "\n**Average Deaths:** *" + str(round(tools.giveMeanOfList(deaths), 2)) + "*"

    # CREATING FARM MEAN from the past X days
    farmString = "\n**Average Farm:** *" + str(round(tools.giveMeanOfList(farm), 2)) + "*"

    # CREATING MINIONKILLS MEAN from the past X days
    minionkillsString = "\n**Average Minion Kills:** *" + str(round(tools.giveMeanOfList(minionKills), 2)) + "*"

    # CREATING WINNER MEAN from the past X days
    winnerString = "\n**Victory Rate:** *" + str(round(tools.giveMeanOfList(winner) * 100)) + "%*"

    # CREATING WENTAFK MEAN from the past X days
    wentafkString = "\n**AFK Rate:** *" + str(round(tools.giveMeanOfList(wentAfk) * 100)) + "%*"

    # CREATING TURRETCAPTURES MEAN from the past X days
    turrentcapturesString = "\n**Average Turrets Destroyed:** *" + str(round(tools.giveMeanOfList(turretCaptures))) + "*"

    # CREATING KRAKEN MEAN from the past X days
    krakenString = "\n**Average Kraken Captures:** *" + str(round(tools.giveMeanOfList(krakenCaptures))) + "*"

    # CREATING MEAN GOLDMINECAPTURES from the past X days
    goldmineString = "\n**Average Gold Mine Captures:** *" + str(round(tools.giveMeanOfList(goldMineCaptures))) + "*"

    # CREATING MEAN CRYSTALMINECAPTURES from the past X days
    crystalmineString = "\n**Average Crystal Mine Captures:** *" + str(round(tools.giveMeanOfList(crystalMineCaptures))) + "*"

    # CREATING LEVEL from the past X days
    # levelString = "\n**Players Level:** *" + str(level) + "*"

    # CHANGE KARMA from a NUMBER to a STRING
    if karmaLevel == 0:
        karmaLevel = "Bad Karma"

    elif karmaLevel == 1:
        karmaLevel = "Good Karma"

    elif karmaLevel == 2:
        karmaLevel = "Great Karma"

    else:
        karmaLevel = "Wow that's some crazy karma!"

    # # CREATING  MEAN from the past X days
    # msg = "\n**** *" + str(round(tools.giveMeanOfList())) + "*"

    if game == "":  # If no specific GAMETYPE was given then set GAME to ANY
        game = "any"

    # Create the TITLE for EMBED
    title = "Match performance from " + str(game) + " matches in the past " + str(days) + " days | Sampled: " + str(size) + " games"

    # Create the DESCRIPTION for the EMBED
    description = "**Player:** *" + str(name) + "* **| Lv:** *" + str(level) + "* **| ST:** *" + str(skillTier) + "* **| K:** *" + str(karmaLevel) + "*\n**Last Game Registered:** *" + str(latestmatch) + "*\n" + str(gamemodelistString) + "\n" + str(winnerString) + str(wentafkString)

    # ASSEMBLE the TOP LIST TOGETHER for EMBED
    toplist = str(actorslistString) + str(skinslistString) + str(itemlistString)

    # ASSEMBLE the STATS TOGETHER for EMBED
    staticsOne = str(killsString) + str(assistsString) + str(deathString) + str(farmString) +  str(minionkillsString) + str(turrentcapturesString) +  str(crystalmineString) + str(goldmineString) + str(krakenString)

    # CREATE the EMBED
    embed = discord.Embed(title=title, colour=discord.Colour(0x4e9ff9), description=description, timestamp=datetime.datetime.now())

    # Set the HEADER
    embed.set_author(name="Computer", url="https://github.com/ClarkThyLord/Computer-BOT", icon_url="http://i67.tinypic.com/25738l1.jpg")

    # Set the THUMBNAIL to MOST USED HERO
    try:
        embed.set_thumbnail(url=thumbnail)
    except:  # If THUMBNAIL couldn't be REACHED then MAKE THUMBNAIL the Vainglory logo
        embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    # ADD TOP LIST to the EMBED
    embed.add_field(name="Top Elements:", value=toplist)

    # ADD PART ONE of STATICS to EMBED
    embed.add_field(name="Overall Match Stats:", value=staticsOne)

    # ADD FOOTER of STATICS to EMBED
    embed.set_footer(text="made with love and vg api ~ xoxo", icon_url="http://i63.tinypic.com/9k6xcj.jpg")

    # SEND the EMBED
    return embed


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
            days          ~   day range to search from                     ~   default: 7, requirements: maximum: 93, minimum: 1
            game_type     ~   game type you would like performance check   ~   options: casual, ranked, royal, blitz

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
        await self.bot.edit_message(msg, embed=getPlayerPerformanceVG(player_name, days, game_type))  # RUNS PERFORMANCE FETCH and UPDATES MESSAGE once DONE

    @commands.command()
    async def vgcheckplayer(self, player_name="", mode=""):
        """Checks if player exist in vainglory.

                >vgcheckplayer (player_name) (mode)
            player_name   ~   name of player to check for
            mode          ~   user or dev mode              ~   default: user, options: user, dev

        """

        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        if mode != "" and tools.isIntTOOL(mode) == False:
            if mode == "user" or mode == "dev":
                pass
            else:
                await self.bot.say(str(mode) + " isn't a possible mode... :sweat_smile:")

        if mode != "" and tools.isIntTOOL(mode) == True:
            await self.bot.say(str(mode) + " isn't a possible mode... :sweat_smile:")
            return

        elif tools.isIntTOOL(player_name) == False:
            player_name = str(player_name)  # Convert PLAYER_NAME to STRING to prevent errors

            notice = "Looking for " + player_name + "... :eyes:"  # DEFAULT NOTICE SENT to USER!

            msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
            await self.bot.edit_message(msg, str(getPlayerInfoVG(player_name, mode)))  # RUNS ID TEST

        else:
            await self.bot.say("Sorry but " + str(player_name) + " isn't a valid name... :sweat_smile:")
            return


def setup(bot):
    bot.add_cog(Vg(bot))
