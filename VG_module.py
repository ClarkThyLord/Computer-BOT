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

# DISCORD EMBED VARIABLES--
botImageDISCORD = "http://i63.tinypic.com/9k6xcj.jpg"  # URL of BOTS IMAGE
signatureDISCORD = "Thanks to SEMC made with love ~ xoxo"  # String used in FOOTER as MESSAGE

# GETS a PLAYERS life time INFORMATION
def getPlayerInfoVG(name, server="", mode="", auto=False):
    ID = str(name)  # Convert ID to a STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=31)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    filterVG = {'filter[createdAt-start]': daterange, 'page[limit]': 1, 'filter[playerNames]': name, "sort": "-createdAt"}  # DEFAULT things to FILTER VG PLAYERS BY

    # FOR DEBUGGING
    print(filterVG)

    if auto == True:

        try:  # TRY to find MATCHES in NA
            matches = apiVG.matches(filterVG, "na")

        except:  # If NOTHING is FOUND then search EU
            try:
                matches = apiVG.matches(filterVG, "eu")

            except:  # If NOTHING is FOUND then search SEA
                try:
                    matches = apiVG.matches(filterVG, "sg")

                except:  # If NOTHING is FOUND then search EA
                    try:
                        matches = apiVG.matches(filterVG, "ea")

                    except:  # If NOTHING is FOUND then search SA
                        try:
                            matches = apiVG.matches(filterVG, "sa")

                        except:
                            return "Couldn't get any matches for **" + str(name) + "** from the past 31 days in any server!"  # RETURN if player MATCHES AREN'T FOUND

    elif auto == False:
        try:  # GIVEN the SERVER try to FIND MATCHES for PLAYER
            matches = apiVG.matches(filterVG, server)

        except:
            return "Couldn't get any matches for **" + str(name) + "** from the past 31 days in " + str(server) + " server!"

    else:
        print("!!!HUGE ERROR!!!")
        return "!!!HUGE ERROR!!!"

    # MATCH VARIABLES
    id = ""
    level = ""
    lifetimeGold = ""
    lossStreak = ""
    played = ""
    winStreak = ""
    wins = ""
    xp = ""
    skillTier = ""
    thumbnail = ""
    karmaLevel = ""

    for match in matches:  # From that MATCH get the VAINGLORY PLAYER ID
        latestmatch = str(match.createdAt)
        gameMode = str(match.gameMode)

        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    matchstats = participant.stats
                    playerstats = participant.player.stats

                    id = str(participant.player.id)
                    level = str(matchstats["level"])
                    lifetimeGold = str(playerstats["lifetimeGold"])
                    lossStreak = str(playerstats["lossStreak"])
                    played = str(playerstats["played"])
                    winStreak = str(playerstats["winStreak"])
                    wins = str(playerstats["wins"])
                    xp = str(playerstats["xp"])

                    skillTier = str(matchstats["skillTier"])
                    thumbnail = giveSkillTierVG(skillTier, 1)
                    karmaLevel = str(matchstats["karmaLevel"])

    # CREATES the STRING for ID
    idString = "\n**ID:** *" + str(id) + "*"

    # CREATES the STRING for LIFETIMEGOLD
    lifetimeGoldString = "\n**Life Time Gold:** *" + str(lifetimeGold) + "*"

    # CREATES the STRING for LOSSSTREAK
    lossStreakString = "\n**Loss Streak:** *" + str(lossStreak) + "*"

    # CREATES the STRING for PLAYED
    playedString = "\n**Played:** *" + str(played) + "*"

    # CREATES the STRING for WINSTREAK
    winStreakString = "\n**Wins Streak:** *" + str(winStreak) + "*"

    # CREATES the STRING for WINS
    winsString = "\n**Wins:** *" + str(wins) + "*"

    # CREATES the STRING for XP
    xpString = "\n**Xp:** *" + str(xp) + "*"

    # CREATES the STRING for LOSE
    loseString = "\n**Lost:** *" + str(int(played) - int(wins)) + "*"

    # CREATES the STRING for
    # String = "\n**:** *" +  + "*"

    # Create the TITLE for EMBED
    title = "Vainglory Career for " + str(name)

    # Create the DESCRIPTION for the EMBED
    description = "**Player:** *" + str(name) + "* **| Lv:** *" + str(level) + "* **| ST:** *" + str(giveSkillTierVG(skillTier)) + "* **| K:** *" + str(giveKarmaVG(karmaLevel)) + "*\n**Last Game Registered:** *" + str(latestmatch) + "* **| Game Type:** *" + str(giveMatchVG(gameMode)) + "*"

    # ASSEMBLE the STATS TOGETHER for EMBED
    staticsOne = str(lifetimeGoldString) + str(winStreakString) + str(lossStreakString) + str(playedString) + str(winsString) + str(loseString) + str(xpString)

    if mode == "dev":
        staticsOne += str(idString)

    # CREATE the EMBED
    embed = discord.Embed(title=title, colour=discord.Colour(0x4e9ff9), description=description,
                          timestamp=datetime.datetime.now())

    # Set the HEADER
    embed.set_author(name="Computer", url="https://github.com/ClarkThyLord/Computer-BOT",
                     icon_url="http://i67.tinypic.com/25738l1.jpg")

    # Set the THUMBNAIL to MOST USED HERO
    try:
        embed.set_thumbnail(url=thumbnail)
    except:  # If THUMBNAIL couldn't be REACHED then MAKE THUMBNAIL the Vainglory logo
        embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    # ADD PART ONE of STATICS to EMBED
    embed.add_field(name="Career:", value=staticsOne)

    # ADD FOOTER of STATICS to EMBED
    embed.set_footer(text=signatureDISCORD, icon_url=botImageDISCORD)

    # SEND the EMBED
    return embed

    # if mode == "" or mode == "user":  # If MODE is DEFAULT or USER SEND regular MESSAGE
    #     return "The player **" + name + "** was found in the Vainglory servers in the past 31 days!"
    # if mode == "dev":  # If MODE is DEV send ID with MESSAGE
    #     return "The player **" + name + "** was found in the Vainglory servers in the past 31 days! ID: " + id


# Get a PLAYERS performance from RANGE of DAYS with the players NAME
def getPlayerPerformanceVG(name, server="", days=7, game="", auto=False):
    name = str(name)  # Convert NAME to STRING to prevent errors
    server = str(server)  # Convert SERVER to STRING to prevent errors
    days = int(days)  # Convert DAYS to INT to prevent errors
    game = str(game)  # Convert GAME to STRING to prevent errors
    auto = bool(auto)  # Convert AUTO to BOOLEAN to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=days)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    filterVG = {"filter[createdAt-start]": daterange, "page[limit]": 50, "filter[playerNames]": name, "sort": "-createdAt"}  # DEFAULT things to FILTER VG MATCHES BY

    if game == "casual":
        filterVG["filter[gameMode]"] = "casual"

    elif game == "rank":
        filterVG["filter[gameMode]"] = "ranked"

    elif game == "royal":
        filterVG["filter[gameMode]"] = "casual_aral"

    elif game == "blitz":
        filterVG["filter[gameMode]"] = "blitz_pvp_ranked"

    # FOR DEBUGGING
    # print(filterVG)

    if auto == True:

        try:  # TRY to find MATCHES in NA
            matches = apiVG.matches(filterVG, "na")  # GET MATCHES from NA

        except:  # If NOTHING is FOUND then search EU
            try:
                matches = apiVG.matches(filterVG, "eu")

            except:  # If NOTHING is FOUND then search SEA
                try:
                    matches = apiVG.matches(filterVG, "sg")

                except:  # If NOTHING is FOUND then search EA
                    try:
                        matches = apiVG.matches(filterVG, "ea")

                    except:  # If NOTHING is FOUND then search SA
                        try:
                            matches = apiVG.matches(filterVG, "sa")

                        except:
                            return "Couldn't get any matches for **" + str(name) + "** from the past " + str(days) + " days in any server!"  # RETURN if player MATCHES AREN'T FOUND

    elif auto == False:
        try:  # GIVEN the SERVER try to FIND MATCHES for PLAYER
            matches = apiVG.matches(filterVG, server)

        except:
            return "Couldn't get any matches for **" + str(name) + "** from the past " + str(days) + "days in the server in " + str(server) + " server!"

    else:
        print("!!!HUGE ERROR!!!")
        return "!!!HUGE ERROR!!!"

    # MATCH VARIABLES
    latestmatch = ""
    gameMode = []
    duration = []

    # Get DATA out of the MATCH OBJECTS
    playerdata = []
    matchNum = 0
    size = len(matches) - 1
    for match in matches:
        if matchNum == size:  # If MATCH is the FIRST MATCH then GET DATA
            latestmatch = str(match.createdAt)

        gameMode.append(str(match.gameMode))
        duration.append(match.duration)
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

    # Go though PLAYERDATA getting DATA needed for building a PROFILE
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

        kills.append(stats["kills"])
        krakenCaptures.append(stats["krakenCaptures"])
        minionKills.append(stats["minionKills"])
        skinKey.append(pretty(stats["skinKey"]))
        turretCaptures.append(stats["turretCaptures"])
        wentAfk.append(stats["wentAfk"])
        winner.append(stats["winner"])

        level = stats["level"]
        karmaLevel = stats["karmaLevel"]
        skillTier = stats["skillTier"]

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
        if len(gamemodes) < 3:  # If LESS then FIVE GAMEMODES were FOUND then set NUM to the GAMEMODES LIST LENGTH
            max = len(gamemodes) - 1

        elif len(gamemodes) >= 3:  # If FIVE or MORE GAMEMODES were FOUND then SET NUM to FIVE
            max = 3

        while num < max:  # NAME POSITIONS of most USED GAMEMODES
            gamemodelistString += "\n**" + str(num + 1) + "** ~ *"

            gamemodelistString += str(giveMatchVG(gamemodes[num])) + "*"

            num += 1

    # CREATING a list(STRING) of the TOP ACTORS used in the past X days
    actors = tools.giveListInOrderTOOL(actor)
    if len(actors) <= 0:  # If NO ACTORS were FOUND then NOTICE USER about it
        actorslistString = "\n**We couldn't get any heroes from your matches!**"

    else:
        actorslistString = "\n**Heroes Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(actors) < 3:  # If LESS then FIVE ACTORS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(actors) - 1

        elif len(actors) >= 3:  # If FIVE or MORE ACTORS were FOUND then SET NUM to FIVE
            max = 3

        while num < max:  # NAME POSITIONS of most USED ACTORS
            actorslistString += "\n**" + str(num + 1) + "** ~ *" + str(actors[num]) + "*"

            if num == 0:  # GETS the THUMBNAIL for MOST USED HERO
                thumbnail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(actors[num]) + ".png"

            num += 1

    # CREATING a list(STRING) of the TOP SKINS used in the past X days
    # skins = tools.giveListInOrderTOOL(skinKey)
    # if len(skins) <= 0:  # If NO SKINS were FOUND then NOTICE USER about it
    #     skinslistString = "\n**We couldn't get any skins from your matches!**"
    #
    # else:
    #     skinslistString = "\n**Skins Used Most:**"  # SET TITLE to INFO
    #
    #     num = 0
    #     if len(skins) < 3:  # If LESS then FIVE SKINS were FOUND then set NUM to the ACTORS LIST LENGTH
    #         max = len(skins) - 1
    #
    #     elif len(skins) >= 3:  # If FIVE or MORE SKINS were FOUND then SET NUM to FIVE
    #         max = 3
    #
    #     while num < max:  # NAME POSITIONS of most USED SKINS
    #         skinslistString += "\n**" + str(num + 1) + "** ~ *" + str(skins[num]) + "*"
    #         num += 1
    #
    # CREATING a list(STRING) of the TOP ITEMS used in the past X days to MSG
    # items = tools.giveListInOrderTOOL(itemslist)
    # if len(items) <= 0:  # If NO ITEMS were FOUND then NOTICE USER about it
    #     itemlistString = "\n**We couldn't get any items from your matches!**"
    #
    # else:
    #     itemlistString = "\n**Items Used Most:**"  # SET TITLE to INFO
    #
    #     num = 0
    #     if len(items) < 3:  # If LESS then FIVE ITEMS were FOUND then set NUM to the ACTORS LIST LENGTH
    #         max = len(items) - 1
    #
    #     elif len(items) >= 3:  # If FIVE or MORE ITEMS were FOUND then SET NUM to FIVE
    #         max = 3
    #
    #     while num < max:  # NAME POSITIONS of most USED ITEMS
    #         itemlistString += "\n**" + str(num + 1) + "** ~ *" + str(items[num]) + "*"
    #         num += 1

    #CREATING DURATION MEAN from the past X days
    durationString = "\n**Average Match Time:** *" + str(round(tools.giveMeanOfList(duration) / 60, 2)) + " minutes*"

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
    crystalmineString = "\n**Average Sentry Captures:** *" + str(round(tools.giveMeanOfList(crystalMineCaptures))) + "*"

    # CREATING LEVEL from the past X days
    # levelString = "\n**Players Level:** *" + str(level) + "*"

    # # CREATING  MEAN from the past X days
    # msg = "\n**** *" + str(round(tools.giveMeanOfList())) + "*"

    if game == "":  # If no specific GAMETYPE was given then set GAME to ANY
        game = "any"

    # Create the TITLE for EMBED
    title = "Match performance from " + str(game) + " matches in the past " + str(days) + " days | Sampled: " + str(size) + " games"

    # Create the DESCRIPTION for the EMBED
    description = "**Player:** *" + str(name) + "* **| Lv:** *" + str(level) + "* **| ST:** *" + str(giveSkillTierVG(skillTier)) + "* **| K:** *" + str(giveKarmaVG(karmaLevel)) + "*\n**Last Game Registered:** *" + str(latestmatch) + "*\n" + str(durationString) + str(gamemodelistString) + "\n" + str(winnerString) + str(wentafkString)

    # ASSEMBLE the TOP LIST TOGETHER for EMBED
    toplist = str(actorslistString)

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
    embed.set_footer(text=signatureDISCORD, icon_url=botImageDISCORD)

    # SEND the EMBED
    return embed

# Gives KARMA as a TITLE
def giveKarmaVG(karma, mode=0):
    # CHECK that KARMA is VALID
    if tools.isIntTOOL(karma) == False:
        return "Wow that's some crazy karma!"
    karma = int(karma)  # Convert KARMA to INT to prevent ERRORS

    # CHANGE KARMA from a NUMBER to a STRING
    if karma == 0:
        if mode == 1:
            return "http://i66.tinypic.com/2vsmdxi.jpg"

        return "Bad Karma"

    elif karma == 1:
        if mode == 1:
            return "http://i63.tinypic.com/2a9wrr7.jpg"

        return "Good Karma"

    elif karma == 2:
        if mode == 1:
            return "http://i64.tinypic.com/sd1t3b.jpg"

        return "Great Karma"

    else:
        if mode == 1:
            return "http://i63.tinypic.com/9k6xcj.jpg"

        return "Wow that's some crazy karma!"

# GIVES the IGN for MATCH MODE
def giveMatchVG(match, mode=0):
    # Check that MATCH is VALID
    if tools.isIntTOOL(match) == True:
        return "That one match..."
    match = str(match)  # Convert MATCH to STRING to prevent ERRORS

    # SEND the PRETTY version of GAMEMODE
    if match == "blitz_pvp_ranked":
        return "Blitz"

    elif match == "casual_aral":
        return "Battle Royal"

    elif match == "private":
        return "Private Casual"

    elif match == "private_party_draft_match":
        return "Private Draft"

    elif match == "private_party_blitz_match":
        return "Private Blitz"

    elif match == "private_party_aral_match":
        return "Private Battle Royal"

    elif match == "casual":
        return "Casual Match"

    elif match == "ranked":
        return "Rank Match"

    else:  # If NO GAMEMODE was found SEND the RAW GAMEMODE
        return str(match)

# Gives SKILL TIER as a TITLE
def giveSkillTierVG(tier, mode=0):
    if tools.isIntTOOL(tier) == False:
        return "Unreal Rank"

    tier = int(tier)  # Convert to INT to prevent ERRORS

    if tier == -1:
        if mode == 1:
            return "http://i64.tinypic.com/30veur5.jpg"

        return "Un-Ranked"

    elif tier == 0:
        if mode == 1:
            return "http://i66.tinypic.com/spj77t.jpg"

        return "Just Beginning - B"

    elif tier == 1:
        if mode == 1:
            return "http://i67.tinypic.com/24ct7qu.jpg"

        return "Just Beginning - S"

    elif tier == 2:
        if mode == 1:
            return "http://i63.tinypic.com/14kytzl.jpg"

        return "Just Beginning - G"

    elif tier == 3:
        if mode == 1:
            return "http://i66.tinypic.com/w8x5ci.jpg"

        return "Getting There - B"

    elif tier == 4:
        if mode == 1:
            return "http://i65.tinypic.com/2rc3f39.jpg"

        return "Getting There - S"

    elif tier == 5:
        if mode == 1:
            return "http://i66.tinypic.com/15guo43.jpg"

        return "Getting There - G"

    elif tier == 6:
        if mode == 1:
            return "http://i63.tinypic.com/10zbkuw.jpg"

        return "Rock Solid - B"

    elif tier == 7:
        if mode == 1:
            return "http://i64.tinypic.com/2igmao7.jpg"

        return "Rock Solid - S"

    elif tier == 8:
        if mode == 1:
            return "http://i64.tinypic.com/m9ngpc.jpg"

        return "Rock Solid - G"

    elif tier == 9:
        if mode == 1:
            return "http://i63.tinypic.com/99jgg4.jpg"

        return "Worthy Foe - B"

    elif tier == 10:
        if mode == 1:
            return "http://i64.tinypic.com/nnksv9.jpg"

        return "Worthy Foe - S"

    elif tier == 11:
        if mode == 1:
            return "http://i68.tinypic.com/120kpk9.jpg"

        return "Worthy Foe - G"

    elif tier == 12:
        if mode == 1:
            return "http://i64.tinypic.com/4rxoid.jpg"

        return "Got Swagger - B"

    elif tier == 13:
        if mode == 1:
            return "http://i68.tinypic.com/2lnib61.jpg"

        return "Got Swagger - S"

    elif tier == 14:
        if mode == 1:
            return "http://i63.tinypic.com/oqjgau.jpg"

        return "Got Swagger - G"

    elif tier == 15:
        if mode == 1:
            return "http://i65.tinypic.com/dphenn.jpg"

        return "Credible Threat - B"

    elif tier == 16:
        if mode == 1:
            return "http://i66.tinypic.com/2dr9law.jpg"

        return "Credible Threat - S"

    elif tier == 17:
        if mode == 1:
            return "http://i65.tinypic.com/20h6cti.jpg"

        return "Credible Threat - G"

    elif tier == 18:
        if mode == 1:
            return "http://i65.tinypic.com/288vxuc.jpg"

        return "The Hotness - B"

    elif tier == 19:
        if mode == 1:
            return "http://i68.tinypic.com/2e3rby8.jpg"

        return "The Hotness - S"

    elif tier == 20:
        if mode == 1:
            return "http://i68.tinypic.com/dq3meg.jpg"

        return "The Hotness - G"

    elif tier == 21:
        if mode == 1:
            return "http://i65.tinypic.com/2hpm0d3.jpg"

        return "Simply Amazing - B"

    elif tier == 22:
        if mode == 1:
            return "http://i66.tinypic.com/2b19ap.jpg"

        return "Simply Amazing - S"

    elif tier == 23:
        if mode == 1:
            return "http://i65.tinypic.com/im5f13.jpg"

        return "Simply Amazing - G"

    elif tier == 24:
        if mode == 1:
            return "http://i65.tinypic.com/vp8f8l.jpg"

        return "Pinnacle of Awesome - B"

    elif tier == 25:
        if mode == 1:
            return "http://i68.tinypic.com/5wjhvs.jpg"

        return "Pinnacle of Awesome - S"

    elif tier == 26:
        if mode == 1:
            return "http://i65.tinypic.com/10r7rrs.jpg"

        return "Pinnacle of Awesome- G"

    elif tier == 27:
        if mode == 1:
            return "http://i68.tinypic.com/27y8mdw.jpg"

        return "Vainglorious - B"

    elif tier == 28:
        if mode == 1:
            return "http://i64.tinypic.com/1znqsds.jpg"

        return "Vainglorious - S"

    elif tier == 29:
        if mode == 1:
            return "http://i65.tinypic.com/e6x74n.jpg"

        return "Vainglorious - G"

def getLatestMatchVG(name, server, game, auto):
    name = str(name)  # Convert to STRING prevent ERRORS
    server = str(server)  # Convert to STRING prevent ERRORS
    game = str(game)  # Convert to STRING prevent ERRORS
    auto = bool(auto)  # Convert to STRING prevent ERRORS

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=31)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    filterVG = {'filter[createdAt-start]': daterange, 'page[limit]': 1, 'filter[playerNames]': name, "sort": "-createdAt"}  # DEFAULT things to FILTER VG PLAYERS BY

    if game == "casual":
        filterVG["filter[gameMode]"] = "casual"

    elif game == "rank":
        filterVG["filter[gameMode]"] = "ranked"

    elif game == "royal":
        filterVG["filter[gameMode]"] = "casual_aral"

    elif game == "blitz":
        filterVG["filter[gameMode]"] = "blitz_pvp_ranked"


    # FOR DEBUGGING
    # print(filterVG)

    if auto == True:

        try:  # TRY to find MATCHES in NA
            matches = apiVG.matches(filterVG, "na")

        except:  # If NOTHING is FOUND then search EU
            try:
                matches = apiVG.matches(filterVG, "eu")

            except:  # If NOTHING is FOUND then search SEA
                try:
                    matches = apiVG.matches(filterVG, "sg")

                except:  # If NOTHING is FOUND then search EA
                    try:
                        matches = apiVG.matches(filterVG, "ea")

                    except:  # If NOTHING is FOUND then search SA
                        try:
                            matches = apiVG.matches(filterVG, "sa")

                        except:
                            return "Couldn't get any matches for **" + str(name) + "** from the past 31 days in any server!"  # RETURN if player MATCHES AREN'T FOUND

    elif auto == False:
        try:  # GIVEN the SERVER try to FIND MATCHES for PLAYER
            matches = apiVG.matches(filterVG, server)

        except:
            return "Couldn't get any matches for **" + str(name) + "** from the past 31 days in " + str(server) + " server!"

    else:
        print("!!!HUGE ERROR!!!")
        return "!!!HUGE ERROR!!!"

    # MATCH VARIABLES
    latestmatch = ""
    gameMode = ""
    winner = ""
    heroKillsA = ""
    goldA = ""
    acesEarnedA = ""
    krakenCapturesA = ""
    turretKillsA = ""
    turretsRemainingA = ""
    heroKillsB = ""
    goldB = ""
    acesEarnedB = ""
    krakenCapturesB = ""
    turretKillsB = ""
    turretsRemainingB = ""
    player1 = {}
    player2 = {}
    player3 = {}
    player4 = {}
    player5 = {}
    player6 = {}

    roasternum = 0
    playernum = 0
    for match in matches:  # From that MATCH get the VAINGLORY PLAYER ID
        latestmatch = str(match.createdAt)
        gameMode = str(match.gameMode)

        for roaster in match.rosters:
            roasterdata = roaster.to_dict()
            roasterattributes = roasterdata["attributes"]
            roasterstats = roasterattributes["stats"]
            print(str(roasterdata) + " | RoasterData")
            print(str(roasterattributes) + " | RoastersAttributes")
            print(str(roasterstats) + " | RoasterStats")

            if roasternum == 0:
                heroKillsA = roasterstats["heroKills"]
                goldA = roasterstats["gold"]
                acesEarnedA = roasterstats["acesEarned"]
                krakenCapturesA = roasterstats["krakenCaptures"]
                turretKillsA = roasterstats["turretKills"]
                turretsRemainingA = roasterstats["turretsRemaining"]

            elif roasternum == 1:
                heroKillsB = roasterstats["heroKills"]
                goldB = roasterstats["gold"]
                acesEarnedB = roasterstats["acesEarned"]
                krakenCapturesB = roasterstats["krakenCaptures"]
                turretKillsB = roasterstats["turretKills"]
                turretsRemainingB = roasterstats["turretsRemaining"]

            roasternum += 1

            for participant in roaster.participants:
                matchstats = participant.stats  # INFORMATION belonging to the MATCH about CURRENT PLAYER
                playerstats = participant.player.stats  # INFORMATION belonging to the PLAYER about CURRENT PLAYER
                print(str(matchstats) + " | MatchStats")
                print(str(playerstats) + " | PlayerStats")

                if participant.player.name == name:
                    thumbnail = str(giveKarmaVG(matchstats["karmaLevel"], 1))

                if playernum == 0:
                    if str(matchstats["winner"]) == "True":
                        winner = "Team A"

                    player1["name"] = str(participant.player.name)
                    player1["level"] = str(playerstats["level"])
                    player1["karmaLevel"] = str(matchstats["karmaLevel"])
                    player1["skillTier"] = str(matchstats["skillTier"])

                    player1["actor"] = str(pretty(participant.actor))
                    player1["kills"] = str(matchstats["kills"])
                    player1["assists"] = str(matchstats["assists"])
                    player1["deaths"] = str(matchstats["deaths"])
                    player1["farm"] = str(matchstats["farm"])

                elif playernum == 1:
                    player2["name"] = str(participant.player.name)
                    player2["level"] = str(playerstats["level"])
                    player2["karmaLevel"] = str(matchstats["karmaLevel"])
                    player2["skillTier"] = str(matchstats["skillTier"])

                    player2["actor"] = str(pretty(participant.actor))
                    player2["kills"] = str(matchstats["kills"])
                    player2["assists"] = str(matchstats["assists"])
                    player2["deaths"] = str(matchstats["deaths"])
                    player2["farm"] = str(matchstats["farm"])

                elif playernum == 2:
                    player3["name"] = str(participant.player.name)
                    player3["level"] = str(playerstats["level"])
                    player3["karmaLevel"] = str(matchstats["karmaLevel"])
                    player3["skillTier"] = str(matchstats["skillTier"])

                    player3["actor"] = str(pretty(participant.actor))
                    player3["kills"] = str(matchstats["kills"])
                    player3["assists"] = str(matchstats["assists"])
                    player3["deaths"] = str(matchstats["deaths"])
                    player3["farm"] = str(matchstats["farm"])

                elif playernum == 3:
                    if str(matchstats["winner"]) == "True":
                        winner = "Team B"

                    player4["name"] = str(participant.player.name)
                    player4["level"] = str(playerstats["level"])
                    player4["karmaLevel"] = str(matchstats["karmaLevel"])
                    player4["skillTier"] = str(matchstats["skillTier"])

                    player4["actor"] = str(pretty(participant.actor))
                    player4["kills"] = str(matchstats["kills"])
                    player4["assists"] = str(matchstats["assists"])
                    player4["deaths"] = str(matchstats["deaths"])
                    player4["farm"] = str(matchstats["farm"])

                elif playernum == 4:
                    player5["name"] = str(participant.player.name)
                    player5["level"] = str(playerstats["level"])
                    player5["karmaLevel"] = str(matchstats["karmaLevel"])
                    player5["skillTier"] = str(matchstats["skillTier"])

                    player5["actor"] = str(pretty(participant.actor))
                    player5["kills"] = str(matchstats["kills"])
                    player5["assists"] = str(matchstats["assists"])
                    player5["deaths"] = str(matchstats["deaths"])
                    player5["farm"] = str(matchstats["farm"])

                elif playernum == 5:
                    player6["name"] = str(participant.player.name)
                    player6["level"] = str(playerstats["level"])
                    player6["karmaLevel"] = str(matchstats["karmaLevel"])
                    player6["skillTier"] = str(matchstats["skillTier"])

                    player6["actor"] = str(pretty(participant.actor))
                    player6["kills"] = str(matchstats["kills"])
                    player6["assists"] = str(matchstats["assists"])
                    player6["deaths"] = str(matchstats["deaths"])
                    player6["farm"] = str(matchstats["farm"])

                playernum += 1

    print(str(player1) + " | player1")
    print(str(player2) + " | player2")
    print(str(player3) + " | player3")
    print(str(player4) + " | player4")
    print(str(player5) + " | player5")
    print(str(player6) + " | player6")

    # Create STRING for TEAMA
    teamAString = "**Kills:** *" + str(heroKillsA) + "* **| Deaths:** *" + str(heroKillsB) + "* **| Aces:** *" + str(acesEarnedA) + "* **| Kraken Captures:** *" + str(krakenCapturesA) + "* **| Gold:** *" + str(goldA) + "* **| Turrets Destroyed:** *" + str(turretKillsA) + "* **| Turrets Left:**" + str(turretsRemainingA) + "*"

    # Create STRING for PLAYER1
    player1String = "\n\n**Player:** *" + str(player1["name"]) + "* **| Lv:** *" + str(player1["level"]) + "* **ST:** *" + str(giveSkillTierVG(player1["skillTier"])) + "* **K:** *" + str(giveKarmaVG(player1["karmaLevel"])) + "*\n**Actor:** *" + str(player1["actor"]) + "* **| Kills:** *" + str(player1["kills"]) + "* **| Assists:** *" + player1["assists"] + "* **| Deaths:** *" + player1["deaths"] + "* **| Grind:** *" + player1["farm"] + "*"

    # Create STRING for PLAYER2
    player2String = "\n\n**Player:** *" + str(player2["name"]) + "* **| Lv:** *" + str(player2["level"]) + "* **ST:** *" + str(giveSkillTierVG(player2["skillTier"])) + "* **K:** *" + str(giveKarmaVG(player2["karmaLevel"])) + "*\n**Actor:** *" + str(player2["actor"]) + "* **| Kills:** *" + str(player2["kills"]) + "* **| Assists:** *" + player2["assists"] + "* **| Deaths:** *" + player2["deaths"] + "* **| Grind:** *" + player2["farm"] + "*"

    # Create STRING for PLAYER3
    player3String = "\n\n**Player:** *" + str(player3["name"]) + "* **| Lv:** *" + str(player3["level"]) + "* **ST:** *" + str(giveSkillTierVG(player3["skillTier"])) + "* **K:** *" + str(giveKarmaVG(player3["karmaLevel"])) + "*\n**Actor:** *" + str(player3["actor"]) + "* **| Kills:** *" + str(player3["kills"]) + "* **| Assists:** *" + player3["assists"] + "* **| Deaths:** *" + player3["deaths"] + "* **| Grind:** *" + player3["farm"] + "*"

    # Create STRING for TEAMB
    teamBString = "**Kills:** *" + str(heroKillsB) + "* **| Deaths:** *" + str(heroKillsA) + "* **| Aces:** *" + str(acesEarnedB) + "* **| Kraken Captures:** *" + str(krakenCapturesB) + "* **| Gold:** *" + str(goldB) + "* **| Turrets Destroyed:** *" + str(turretKillsB) + "* **| Turrets Left:**" + str(turretsRemainingB) + "*"

    # Create STRING for PLAYER4
    player4String = "\n\n**Player:** *" + str(player4["name"]) + "* **| Lv:** *" + str(player4["level"]) + "* **ST:** *" + str(giveSkillTierVG(player4["skillTier"])) + "* **K:** *" + str(giveKarmaVG(player4["karmaLevel"])) + "*\n**Actor:** *" + str(player4["actor"]) + "* **| Kills:** *" + str(player4["kills"]) + "* **| Assists:** *" + player4["assists"] + "* **| Deaths:** *" + player4["deaths"] + "* **| Grind:** *" + player4["farm"] + "*"

    # Create STRING for PLAYER5
    player5String = "\n\n**Player:** *" + str(player5["name"]) + "* **| Lv:** *" + str(player5["level"]) + "* **ST:** *" + str(giveSkillTierVG(player5["skillTier"])) + "* **K:** *" + str(giveKarmaVG(player5["karmaLevel"])) + "*\n**Actor:** *" + str(player5["actor"]) + "* **| Kills:** *" + str(player5["kills"]) + "* **| Assists:** *" + player5["assists"] + "* **| Deaths:** *" + player5["deaths"] + "* **| Grind:** *" + player5["farm"] + "*"

    # Create STRING for PLAYER6
    player6String = "\n\n**Player:** *" + str(player6["name"]) + "* **| Lv:** *" + str(player6["level"]) + "* **ST:** *" + str(giveSkillTierVG(player6["skillTier"])) + "* **K:** *" + str(giveKarmaVG(player6["karmaLevel"])) + "*\n**Actor:** *" + str(player6["actor"]) + "* **| Kills:** *" + str(player6["kills"]) + "* **| Assists:** *" + player6["assists"] + "* **| Deaths:** *" + player6["deaths"] + "* **| Grind:** *" + player6["farm"] + "*"

    # Create the TITLE for EMBED
    title = "Latest match from " + str(name) + " in the past 31 days | Game Type: " + str(giveMatchVG(gameMode)) + " | Date: " + str(latestmatch)

    # Create the DESCRIPTION for the EMBED
    description = "**Match Winner:** *" + str(winner) + "*"

    # ASSEMBLE the TOP LIST TOGETHER for EMBED
    teamAINFO = str(teamAString) + str(player1String) + str(player2String) + str(player3String)

    # ASSEMBLE the STATS TOGETHER for EMBED
    teamBINFO = str(teamBString) + str(player4String) + str(player5String) + str(player6String)

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
    embed.add_field(name="Team A:", value=teamAINFO)

    # ADD PART ONE of STATICS to EMBED
    embed.add_field(name="Team B:", value=teamBINFO)

    # ADD FOOTER of STATICS to EMBED
    embed.set_footer(text=signatureDISCORD, icon_url=botImageDISCORD)

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
    async def stats(self, player_name="", server="na", days="7", game_type="any", auto="False"):
        """Gets a players performance in the past days.

                >stats (player_name) (server) (days) (game_type)
            player_name   ~   name of player to search for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sg, ea, sa
            days          ~   day range to search from                     ~   default: 7, requirements: maximum: 93, minimum: 1
            game_type     ~   game type you would like performance check   ~   default: any, options: any, casual, ranked, royal, blitz

            example:
                >stats player1 na 10 casual

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # MESSAGE the USER if NO NAME was GIVEN
        if player_name == "":
            await self.bot.say("You need to give a players name at least...")
            return

        # MESSAGE the USER if NAME GIVEN is TOO SHORT
        if len(str(player_name)) < 3:
            await self.bot.say("That isn't a valid name... :sweat_smile:")
            return

        # MESSAGE the USER if a NUMBER was GIVEN
        if tools.isIntTOOL(player_name) == True:
            await self.bot.say(str(player_name) + " isn't a valid name... :sweat_smile:")
            return

        notice = "Looking at matches for " + str(player_name)

        # Check that SERVER is VALID
        if server == "na" or server == "eu" or server == "sg" or server == "ea" or server == "sa":
            notice += " in " + str(server) + " servers"

        else:
            await self.bot.say(str(server) + " isn't a valid server name... :sweat_smile:")
            return

        # CHECK DAYS to be a VALID NUMBER
        if tools.isIntTOOL(days) == True:
            days = int(days)  # Convert DAYS to INT to prevent ERRORS

            if days > 93:
                days = 93  # MAKE DAYS a VALID RANGE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

            elif days <= 0:
                days = 1  # MAKE DAYS a VALID RANGE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

            else:  # LEAVE DAYS ALONE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

        else:  # DATE is INVALID so THEN MESSAGE USER
            await self.bot.say("Sorry but " + str(days) + " isn't a valid number... :sweat_smile:")  # If DAYS is an INVALID number TELL USER
            return

        # Check that GAMETYPE is VALID
        if game_type != "" and tools.isIntTOOL(game_type) == False:

            if game_type == "any" or game_type == "casual" or game_type == "rank" or game_type == "royal" or game_type == "blitz":  # GAMETYPE is VALID
                notice += " from " + game_type + " games"

                # If GAMETYPE is ANY turn to BLANK
                if game_type == "any":
                    game_type = ""

            else:  # GAMETYPE isn't VALID
                await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
                return

        # If GAMETYPE is VALID then MESSAGE user
        if game_type != "" and tools.isIntTOOL(game_type) == True:
            await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
            return

        # END of NOTICE
        notice += "... :eyes:"

        # Converts AUTO to it's proper BOOLEAN
        if auto == "False" or auto == "false":
            auto = False
        elif auto == "True" or auto == "true":
            auto = True
            notice += " - AUTO: True"

        else:
            await self.bot.say("That isn't a valid secret!")
            return

        # NOTICE USER that THEIR COMMAND is being PROCESSED
        msg = await self.bot.say(notice)
        # RUNS PERFORMANCE FETCH and UPDATES MESSAGE once DONE
        await self.bot.edit_message(msg, embed=getPlayerPerformanceVG(player_name, server, days, game_type, auto))

    @commands.command()
    async def player(self, player_name="", server="na", mode="user", auto="False"):
        """Checks if player exist in vainglory.

                >player (player_name) (server) (mode)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sg, ea, sa
            mode          ~   user or dev mode                             ~   default: user, options: user, dev

            Example:
                >player player1 na user

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        notice = "Looking for "  # DEFAULT NOTICE SENT to USER!

        # Check that a NAME was GIVEN
        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        # Check that NAME is VALID
        if tools.isIntTOOL(player_name) == True or len(player_name) < 3:
            await self.bot.say(str(player_name) + " isn't a valid name!")

        notice += str(player_name)

        # Check that SERVER is VALID
        if server == "na" or server == "eu" or server == "sg" or server == "ea" or server == "sa":
            notice += " in " + str(server) + " servers"

        else:
            await self.bot.say(str(server) + " isn't a valid server name... :sweat_smile:")
            return

        notice += "... :eyes:"

        # Check that MODE is VALID
        if mode == "user" or mode == "dev":
            pass

        else:
            await self.bot.say(str(mode) + " isn't a valid mode... :sweat_smile:")
            return


        # Converts AUTO to it's proper BOOLEAN
        if auto == "False" or auto == "false":
            auto = False

        elif auto == "True" or auto == "true":
            auto = True

            notice += " - AUTO: True"

        else:
            await self.bot.say("That isn't a valid secret!")
            return

        player_name = str(player_name)  # Convert PLAYER_NAME to STRING to prevent errors

        msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
        await self.bot.edit_message(msg, embed=getPlayerInfoVG(player_name, server, mode, auto))  # RUNS ID TEST


    @commands.command()
    async def match(self, player_name="", server="na", game_type="any", auto="False"):
        """Fetched the latest Vainglory match.

                >player (player_name) (server) (game_type)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sg, ea, sa
            game_type     ~   game type you would like performance check   ~   default: any, options: any, casual, ranked, royal, blitz

            Example:
                >match player1 na casual

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        notice = "Looking for the latest match of "  # DEFAULT NOTICE SENT to USER!

        # Check that a NAME was GIVEN
        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        # Check that NAME is VALID
        if tools.isIntTOOL(player_name) == True or len(player_name) < 3:
            await self.bot.say(str(player_name) + " isn't a valid name!")

        notice += str(player_name)

        # Check that SERVER is VALID
        if server == "na" or server == "eu" or server == "sg" or server == "ea" or server == "sa":
            notice += " in " + str(server) + " servers"

        else:
            await self.bot.say(str(server) + " isn't a valid server name... :sweat_smile:")
            return

        # Check that GAMETYPE is VALID
        if game_type != "" and tools.isIntTOOL(game_type) == False:

            if game_type == "any" or game_type == "casual" or game_type == "rank" or game_type == "royal" or game_type == "blitz":  # GAMETYPE is VALID
                notice += " from " + game_type + " games"

                # If GAMETYPE is ANY turn to BLANK
                if game_type == "any":
                    game_type = ""

            else:  # GAMETYPE isn't VALID
                await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
                return

            # Converts AUTO to it's proper BOOLEAN
            if auto == "False" or auto == "false":
                auto = False
            elif auto == "True" or auto == "true":
                auto = True
                notice += " - AUTO: True"

            else:
                await self.bot.say("That isn't a valid secret!")
                return

            notice += "... :eyes:"

            msg = await self.bot.say(notice)
            await self.bot.edit_message(msg, embed=getLatestMatchVG(player_name, server, game_type, auto))

def setup(bot):
    bot.add_cog(Vg(bot))
