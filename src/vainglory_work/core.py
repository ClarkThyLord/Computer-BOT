import discord
import gamelocker
import config
import datetime
import dateutil.parser
import threading
from src.extra import tools as extraTools
from src.vainglory_work import tools, languages, leaderboards, drafting
from src.mongo_work import core as db
from random import randrange
import json

api = gamelocker.Vainglory(config.VG_KEY)


def getPlayer(player_id, region):
    """Gives you a dict of player's data. Use this function whenever you want this data it works with db to make calling more efficient!"""

    data = api.player(player_id, region)

    # Save the new data fetched from the api
    if "error" not in data:
        threading.Thread(target=processPlayers, args=[data, region]).start()

    return data


def processPlayer(data, region):
    """Save and process players data.

    :param data: Players data.
    :param region: Region of the players.
    :return: Doesn't return anything

    """

    db.updateVgPlayerData(data["name"], region, data)

    # Update players verify data
    db.updateDiscordUserWith({"vaingloryRelated.verifiedName": data["name"], "vaingloryRelated.verifiedRegion": region, "vaingloryRelated.playerProfile": {"$ne": {}}}, {"vaingloryRelated.playerProfile.player": data}, safe=False)


def getPlayers(igns, region):
    """Gives you a list of players data. Use this function whenever you want this data it works with db to make calling more efficient!

    :parameter igns: Igns of the players; no spaces and seperated by ",".
    :parameter region: Regions of players.
    :returns: The data asked for.

    """

    # Filter used to get a players latest data
    args = {'filter[playerNames]': igns}

    # FOR DEBUGGING
    # print("PLAYER ARGS:   " + str(args))

    data = api.players(args, region)

    # Data wasn't fetched from api
    if "error" in data:
        newData = []
        for ign in str(igns).split(","):
            result = db.vgPlayerDataDictionary(str(ign), region)
            if result != False:
                newData.append(result["data"])

        # Check if something was found in the db
        if newData != []:
            data = newData

    else:  # New data was fetched from the api
        threading.Thread(target=processPlayers, args=[data, region]).start()

    return data


def processPlayers(data, region):
    """Save and process players data.

    :param data: Players data.
    :param region: Region of the players.
    :return: Doesn't return anything

    """

    # FOR DEBUGGING
    # print("PLAYERS DATA: " + str(data))

    for player in data:
        # Update the players data in the db
        db.updateVgPlayerData(player["name"], region, player)


def getMatch(match_id, region):
    """Gives you a dict of a match's data. Use this function whenever you want this data it works with db to make calling more efficient!"""

    data = api.match(match_id, region)

    return data


def getMatches(ign, region, gameMode="any"):
    """Gives you a list of matches data. Use this function whenever you want this data it works with db to make calling more efficient!"""

    result = db.checkVgMatchData(ign, region, gameMode, 4)

    #FOR DEBUGGING
    # print("DB RESULT:   " + str(result))

    # Data requested wasn't found in our db
    if result["found"] == False:
        # FOR DEBUGGING
        # print("!!!FETCHING FROM API!!!")

        # Filter used to get a players latest data
        # createdAt-end   ~ the earliest data can be ~ default: now or 3 hours depends on api; max: 28 days
        # createdAt-start ~ the latest data can be   ~ default: 28 days back from now; max: 28 days
        args = {"sort": "-createdAt", 'page[limit]': 50, 'filter[playerNames]': ign}

        if gameMode == "any" or gameMode == "":
            pass

        else:
            args["filter[gameMode]"] = tools.giveGameModeVG(gameMode, 1)

        # FOR DEBUGGING
        # print("PLAYER ARGS:   " + str(args))

        data = api.matches(args, region)

        # FOR DEBUGGING
        # print("!!!FETCHED FROM API!!!\nFETCHED API DATA:   " + str(data))

        # Check if data is useful and should be processed
        if "error" not in data:
            # FOR DEBUGGING
            # print("!!!UNLESS DATA!!!")
            threading.Thread(target=processMatches, args=[data, ign, region, gameMode]).start()

    # Data requested is found in db but isn't valid
    elif result["found"] == True and result["valid"] == False:
        # FOR DEBUGGING
        # print("!!!FETCHING FROM API!!!")

        # Filter used to get a players latest data
        # createdAt-end   ~ the earliest data can be ~ default: now or 3 hours depends on api; max: 28 days
        # createdAt-start ~ the latest data can be   ~ default: 28 days back from now; max: 28 days
        args = {"sort": "-createdAt", 'page[limit]': 50, 'filter[playerNames]': ign}

        if gameMode == "any" or gameMode == "":
            pass

        else:
            args["filter[gameMode]"] = tools.giveGameModeVG(gameMode, 1)

        # FOR DEBUGGING
        # print("PLAYER ARGS:   " + str(args))

        data = api.matches(args, region)

        # FOR DEBUGGING
        # print("!!!FETCHED FROM API!!!\nFETCHED API DATA:   " + str(data))

        if "error" in data:
            # FOR DEBUGGING
            # print("!!!MATCHES DATA ERROR FETCHING FROM DB!!!\n" + str(data))

            data = result["data"]

            # FOR DEBUGGING
            # print("!!!FETCHED FROM DB!!!\nFETCHED DB DATA:   " + str(data))

        else:
            threading.Thread(target=processMatches, args=[data, ign, region, gameMode]).start()

    # Data requested is found in our db and is valid
    else:
        # FOR DEBUGGING
        # print("!!!FETCHING FROM DB!!!")

        data = result["data"]

        # FOR DEBUGGING
        # print("!!!FETCHED FROM DB!!!\nFETCHED DB DATA:   " + str(data))

    return data


def processMatches(data, ign, region, gameMode):
    """Save and process matches data.

    :param data: Matches data.
    :param ign: Players in-game name.
    :param region: Region of the player.
    :param gameMode: Game mode of the matches.
    :return: Doesn't return anything.

    """

    try:

        # FOR DEBUGGING
        # print("!!!MATCHES BEING PROCESSED!!!")
        # print("DATA:\n" + str(data) + "\nIGN:   " + ign + " |REGION:   " + region + " |GAME MODE:   " + gameMode)

        currentMatch = data[0]["createdAt"]

        # FOR DEBUGGING
        # print("LATEST MATCH: " + str(currentMatch))

        lastRegistered = db.vgMatchDataDictionary(ign, region, gameMode)
        if lastRegistered != False:
            lastRegistered = lastRegistered["lastUpdateApi"]

        # FOR DEBUGGING
        # print("LAST REGISTERED MATCH: " + str(lastRegistered))

        if currentMatch == lastRegistered:
            # FOR DEBUGGING
            # print("!!!DONE DATA!!!")

            return

        else:
            # FOR DEBUGGING
            # print("!!!UPDATING MATCHES DB!!!")

            # Update the players match data in the db
            db.updateVgMatchData(ign, region, gameMode, data)

            # FOR DEBUGGING
            # print("!!!UPDATED MATCHES DB!!!")

            for match in data:
                # FOR DEBUGGING
                # print("CHECKED MATCH AT: " + str(match["createdAt"]))

                if match["createdAt"] == lastRegistered:
                    # FOR DEBUGGING
                    # print("BREAK AT: " + str(match["createdAt"]))

                    break

                # SEND TO LEADER BOARD
                leaderboards.processMatch(match, ign, region)

                # Fast but intense
                # threading.Thread(target=leaderboards.processMatch, args=[match, ign, region]).start()

                # SEND TO DRAFTING
                drafting.processMatch(match)

                # Fast but intense
                # threading.Thread(target=drafting.processMatch, args=[match]).start()

                # SEND TO HERO
                # TODO CREATE HERO STUFF

                # FOR DEBUGGING
                # print("PROCESSED MATCH AT: " + str(match["createdAt"]))

        # FOR DEBUGGING
        # print("!!!MATCHES HAVE BEEN PROCESSED!!!")

    except Exception as e:
        print("!!!AN ERROR OCCURRED IN MATCH PROCESS!!!\n" + str(e))


def getTelemetry(url):
    """Gives you a list of a match's telemetry data. Use this function whenever you want this data it works with db to make calling more efficient!"""

    return api.telemetry(url)


def playerEmbed(ign, region, emojis=True, language="english", ad=""):
    """

    :param ign: In-game name of VainGlory player.
    :param region: Region of the player.
    :param language: Language embed should show in.
    :param ad: Text ad added to the end of footer.
    :return: Returns a embed discord object.

    """

    # Get the player's `latest match data
    data = getMatches(ign, region)

    # FOR DEBUGGING
    # print("PLAYER DATA BEFORE:   " + str(data))

    if "error" in data:
        return False

    data = data[0]

    # FOR DEBUGGING
    # print("PLAYER DATA AFTER:   " + str(data))

    # Retrieve player's data from match data
    for roster in data["rosters"]:
        for participant in roster["participants"]:
            if participant["player"]["name"] == ign:
                playerData = participant["player"]

                # When this data was updated
                playerData["createdAt"] = str((dateutil.parser.parse(str(data["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"

                # We got what we wanted so break
                break

    # FOR DEBUGGING
    # print("PLAYER DATA AFTER:   " + str(playerData))

    embed = discord.Embed(
        title=ign + " |LV: " + str(playerData["level"]) + " |K: " + tools.giveFormat(playerData["karmaLevel"], "karma", emojis),
        url="https://vgpro.gg/players//" + region + "/" + ign,
        description=languages.playerDescription(language, playerData["name"], playerData["createdAt"])
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url=tools.giveSkillTierVG(playerData["skillTier"], 1))

    # FOR DEBUGGING
    # print("WIN RATE:   " + str(abs(playerData["wins"] / playerData["played"]) * 100))

    try:

        winRate = str(round(abs(playerData["wins"] / playerData["played"]) * 100)) + "%"

    except:
        winRate = "0%"

    embed.add_field(name=languages.playerEmbedFieldOneTitle(language), value=languages.playerEmbedFieldOne(language, winRate, str(playerData["wins"]), str(int(abs(playerData["played"] - playerData["wins"]))), str(playerData["played"]), str(playerData["winStreak"]), str(playerData["lossStreak"]), str(round(playerData["lifetimeGold"], 2))))

    msg = ""
    if playerData["elo_earned_season_1"] != 0:
        msg += "**Season 1:** *" + str(round(playerData["elo_earned_season_1"], 2)) + "*\n"

    if playerData["elo_earned_season_2"] != 0:
        msg += "**Season 2:** *" + str(round(playerData["elo_earned_season_2"], 2)) + "*\n"

    if playerData["elo_earned_season_3"] != 0:
        msg += "**Season 3:** *" + str(round(playerData["elo_earned_season_3"], 2)) + "*\n"

    if playerData["elo_earned_season_4"] != 0:
        msg += "**Season 4:** *" + str(round(playerData["elo_earned_season_4"], 2)) + "*\n"

    if playerData["elo_earned_season_5"] != 0:
        msg += "**Season 5:** *" + str(round(playerData["elo_earned_season_5"], 2)) + "*\n"

    if playerData["elo_earned_season_6"] != 0:
        msg += "**Season 6:** *" + str(round(playerData["elo_earned_season_6"], 2)) + "*\n"

    if playerData["elo_earned_season_7"] != 0:
        msg += "**Season 7:** *" + str(round(playerData["elo_earned_season_7"], 2)) + "*\n"

    if msg != "":
        embed.add_field(name=languages.playerEmbedFieldTwoTitle(language), value=msg)

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def comparePlayersEmbed(igns, region, language="english", ad=""):
    """

    :param igns: A string of players VainGlory separated by , all from the same region
    :param region: Region of all players.
    :param language: Language embed should show in.
    :param ad: Text ad added to the footer of embed.
    :return: Embed discord object of player.

    """

    # Get the player's latest match data
    data = getPlayers(igns, region)

    # FOR DEBUGGING
    # print("PLAYERS DATA:   " + str(data))

    if "error" in data:
        return False

    # DATA
    levels = {}
    # xp = {}
    golds = {}
    winRates = {}
    wins = {}
    losses = {}
    # winStreaks = {}
    # lossStreaks = {}

    for player in data:
        levels[player["name"]] = player["level"]
        # xp[player["name"]] = player["xp"]
        golds[player["name"]] = round(player["lifetimeGold"], 2)
        winRates[player["name"]] = round(abs(player["wins"] / player["played"]) * 100)
        wins[player["name"]] = player["wins"]
        losses[player["name"]] = int(abs(player["played"] - player["wins"]))
        # winStreaks[player["name"]] = player["winStreak"]
        # lossStreaks[player["name"]] = player["lossStreak"]

    levelsList = extraTools.giveDictInOrder(levels, 1)
    # xpList = extraTools.giveDictInOrder(xp, 1)
    goldList = extraTools.giveDictInOrder(golds, 1)
    winRatesList = extraTools.giveDictInOrder(winRates, 1)
    winsList = extraTools.giveDictInOrder(wins, 1)
    lossesList = extraTools.giveDictInOrder(losses, 1)
    # winStreaksList = extraTools.giveDictInOrder(winStreaks, 1)
    # lossStreaksList = extraTools.giveDictInOrder(lossStreaks, 1)

    levelsString = ""
    for name in levelsList:
        levelsString += "**" + str(name) + " | " + str(levels[name]) + "**\n"

    # FOR DEBUGGING
    # print("LEVEL STRING:   " + levelsString)

    # xpString = ""
    # for name in xpList:
    #     xpString += "**" + str(name) + " | " + str(xp[name]) + "**\n"
    #
    # # FOR DEBUGGING
    # print("XP STRING:   " + xpString)

    goldsString = ""
    for name in goldList:
        goldsString += "**" + str(name) + " | " + str(golds[name]) + "**\n"

    # FOR DEBUGGING
    # print("GOLD STRING:   " + goldsString)

    winRatesString = ""
    for name in winRatesList:
        winRatesString += "**" + str(name) + " | " + str(winRates[name]) + "**\n"

    # FOR DEBUGGING
    # print("WIN RATES STRING:   " + winRatesString)

    winsString = ""
    for name in winsList:
        winsString += "**" + str(name) + " | " + str(wins[name]) + "**\n"

    # FOR DEBUGGING
    # print("WINS STRING:   " + winsString)

    lossesString = ""
    for name in lossesList:
        lossesString += "**" + str(name) + " | " + str(losses[name]) + "**\n"

    # FOR DEBUGGING
    # print("LOSSES STRING:   " + lossesString)

    # winStreaksString = ""
    # for name in winStreaksList:
    #     winStreaksString += "**" + str(name) + " | " + str(winStreaks[name]) + "**\n"
    #
    # # FOR DEBUGGING
    # print("WIN STREAK STRING STRING:   " + winStreaksString)
    #
    # lossStreaksString = ""
    # for name in lossStreaksList:
    #     lossStreaksString += "**" + str(name) + " | " + str(lossStreaks[name]) + "**\n"
    #
    # # FOR DEBUGGING
    # print("LOSS STREAK STRING STRING:   " + lossStreaksString)

    embed = discord.Embed(
        title=igns,
        url=config.bot_server,
        description=languages.comparePlayersDescription(language, str(len(levelsList)), region)
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    embed.add_field(name=languages.comparePlayersFieldOneTitle(language), value=levelsString)

    # embed.add_field(name=languages.comparePlayersFieldTwoTitle(language), value=xpString)

    embed.add_field(name=languages.comparePlayersFieldThreeTitle(language), value=goldsString)

    embed.add_field(name=languages.comparePlayersFieldFourTitle(language), value=winRatesString)

    embed.add_field(name=languages.comparePlayersFieldFiveTitle(language), value=winsString)

    embed.add_field(name=languages.comparePlayersFieldSixTitle(language), value=lossesString)

    # embed.add_field(name=languages.comparePlayersFieldSevenTitle(language), value=winStreaksString)
    #
    # embed.add_field(name=languages.comparePlayersFieldEightTitle(language), value=lossStreaksString)

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def compareUniquePlayersEmbed(ignOne, ignTwo, regionOne, regionTwo, emojis=True, language="english", ad=""):
    """

    :param ignOne: In-game name of a VainGlory player.
    :param ignTwo: Different in-game name of a VainGlory player.
    :param regionOne: Region of the first player.
    :param regionTwo: Region of the second player.
    :return: Returns a embed discord object.

    """

    # FOR DEBUGGING
    # print("IGN ONE:   " + str(ignOne) + " |REGION ONE:   " + str(regionOne) + "\nIGN TWO:   " + str(ignTwo) + " |REGION TWO:   " + str(regionTwo))

    # DATA
    rankTiers = {}
    # karmas = {}
    levels = {}
    # xp = {}
    golds = {}
    winRates = {}
    wins = {}
    losses = {}
    # winStreaks = {}
    # lossStreaks = {}

    data = getMatches(ignOne, regionOne)

    # FOR DEBUGGING
    # print("PLAYER ONE DATA BEFORE:   " + str(data))

    # Returns the ign for the player whose data gave error
    if "error" in data:
        return ignOne

    data = data[0]

    # FOR DEBUGGING
    # print("PLAYER ONE DATA AFTER:   " + str(data))

    for roster in data["rosters"]:
        for participant in roster["participants"]:
            if participant["player"]["name"] == ignOne:
                rankTiers[ignOne] = participant["skillTier"]
                # karmas[ignOne] = participant["karmaLevel"]
                levels[ignOne] = participant["player"]["level"]
                # xp[ignOne] = participant["player"]["xp"]
                golds[ignOne] = round(participant["player"]["lifetimeGold"], 2)
                winRates[ignOne] = round(abs(participant["player"]["wins"] / participant["player"]["played"] * 100))
                wins[ignOne] = participant["player"]["wins"]
                losses[ignOne] = int(abs(participant["player"]["played"] - participant["player"]["wins"]))
                # winStreaks[ignOne] = participant["player"]["winSteak"]
                # lossStreaks[ignOne] = participant["player"]["lossStreak"]

                break

    data = getMatches(ignTwo, regionTwo)

    # FOR DEBUGGING
    # print("PLAYER TWO DATA BEFORE:   " + str(data))

    # Returns the ign fo the player whose data gave error
    if "error" in data:
        return ignTwo

    data = data[0]

    # FOR DEBUGGING
    # print("PLAYER TWO DATA AFTER:   " + str(data))

    for roster in data["rosters"]:
        for participant in roster["participants"]:
            if participant["player"]["name"] == ignTwo:
                rankTiers[ignTwo] = participant["skillTier"]
                # karmas[ignTwo] = participant["karmaLevel"]
                levels[ignTwo] = participant["player"]["level"]
                # xp[ignTwo] = participant["player"]["xp"]
                golds[ignTwo] = round(participant["player"]["lifetimeGold"], 2)
                winRates[ignTwo] = round(abs(participant["player"]["wins"] / participant["player"]["played"] * 100))
                wins[ignTwo] = participant["player"]["wins"]
                losses[ignTwo] = int(abs(participant["player"]["played"] - participant["player"]["wins"]))
                # winStreaks[ignTwo] = participant["player"]["winSteak"]
                # lossStreaks[ignTwo] = participant["player"]["lossStreak"]

                break

    rankTiersList = extraTools.giveDictInOrder(rankTiers, 1)
    # karmaList = extraTools.giveDictInOrder(karmas, 1)
    levelsList = extraTools.giveDictInOrder(levels, 1)
    # xpList = extraTools.giveDictInOrder(xp, 1)
    goldList = extraTools.giveDictInOrder(golds, 1)
    winRatesList = extraTools.giveDictInOrder(winRates, 1)
    winsList = extraTools.giveDictInOrder(wins, 1)
    lossesList = extraTools.giveDictInOrder(losses, 1)
    # winStreaksList = extraTools.giveDictInOrder(winStreaks, 1)
    # lossStreaksList = extraTools.giveDictInOrder(lossStreaks, 1)

    rankTierString = ""
    for name in rankTiersList:
        rankTierString += "**" + str(name) + " | " + str(tools.giveFormat(rankTiers[name], "skillTier", emojis)) + "**\n"

    # FOR DEBUGGING
    # print("RANK TIER STRING:   " + rankTierString)

    # karmaString = ""
    # for name in karmaList:
    #     karmaString += "**" + str(name) + " | " + str(tools.giveFormat(karmas[name], "karma", emojis)) + "**\n"
    #
    # # FOR DEBUGGING
    # print("KARMA STRING:   " + karmaString)

    levelsString = ""
    for name in levelsList:
        levelsString += "**" + str(name) + " | " + str(levels[name]) + "**\n"

    # FOR DEBUGGING
    # print("LEVEL STRING:   " + levelsString)

    # xpString = ""
    # for name in xpList:
    #     xpString += "**" + str(name) + " | " + str(xp[name]) + "**\n"
    #
    # # FOR DEBUGGING
    # print("XP STRING:   " + xpString)

    goldsString = ""
    for name in goldList:
        goldsString += "**" + str(name) + " | " + str(golds[name]) + "**\n"

    # FOR DEBUGGING
    # print("GOLD STRING:   " + goldsString)

    winRatesString = ""
    for name in winRatesList:
        winRatesString += "**" + str(name) + " | " + str(winRates[name]) + "**\n"

    # FOR DEBUGGING
    # print("WIN RATES STRING:   " + winRatesString)

    winsString = ""
    for name in winsList:
        winsString += "**" + str(name) + " | " + str(wins[name]) + "**\n"

    # FOR DEBUGGING
    # print("WINS STRING:   " + winsString)

    lossesString = ""
    for name in lossesList:
        lossesString += "**" + str(name) + " | " + str(losses[name]) + "**\n"

    # FOR DEBUGGING
    # print("LOSSES STRING:   " + lossesString)

    # winStreaksString = ""
    # for name in winStreaksList:
    #     winStreaksString += "**" + str(name) + " | " + str(winStreaks[name]) + "**\n"
    #
    # # FOR DEBUGGING
    # print("WIN STREAK STRING STRING:   " + winStreaksString)
    #
    # lossStreaksString = ""
    # for name in lossStreaksList:
    #     lossStreaksString += "**" + str(name) + " | " + str(lossStreaks[name]) + "**\n"
    #
    # # FOR DEBUGGING
    # print("LOSS STREAK STRING STRING:   " + lossStreaksString)

    embed = discord.Embed(
        title=ignOne + " & " + ignTwo,
        url="https://vgpro.gg/players//" + regionOne + "/" + ignOne,
        description=languages.compareUniquePlayersDescription(language, str(len(levelsList)), regionOne, regionTwo)
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    embed.add_field(name=languages.compareUniquePlayersFieldOneTitle(language), value=rankTierString)

    # embed.add_field(name=languages.compareUniquePlayersFieldTwoTitle(language), value=karmaString)

    embed.add_field(name=languages.compareUniquePlayersFieldThreeTitle(language), value=levelsString)

    # embed.add_field(name=languages.compareUniquePlayersFieldFourTitle(language), value=xpString)

    embed.add_field(name=languages.compareUniquePlayersFieldFiveTitle(language), value=goldsString)

    embed.add_field(name=languages.compareUniquePlayersFieldSixTitle(language), value=winRatesString)

    embed.add_field(name=languages.compareUniquePlayersFieldSevenTitle(language), value=winsString)

    embed.add_field(name=languages.compareUniquePlayersFieldEightTitle(language), value=lossesString)

    # embed.add_field(name=languages.compareUniquePlayersFieldNineTitle(language), value=winStreaksString)

    # embed.add_field(name=languages.compareUniquePlayersFieldTenTitle(language), value=lossStreaksString)

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def statsEmbed(ign, region="na", gameMode="any", days=28, compact=False, emojis=True, language="english", ad=""):
    """

    :param ign: In-game name of a VainGlory player.
    :param region: Region of player.
    :param gameMode: Game mode to sample stats from.
    :param days: Days to sample stats from.
    :param compact: If the content should be compact.
    :param language: Language to display embed in.
    :param ad: Ad to display at the end of footer.
    :return: Discord embed object.

    """

    # FOR DEBUGGING
    # print("STATS EMBED INPUT:\nIGN :   " + str(ign) + " |REGION :   " + str(region) + " |GAMEMODE:   " + str(days))

    data = getMatches(ign, region, gameMode)

    if "error" in data:
        return False

    # DATA
    # Get a time stamp for a date range to fetch data from
    dateRange = (datetime.datetime.today() - datetime.timedelta(days=days)).replace(tzinfo=None)

    # FOR DEBUGGING
    # print("DATE RANGE: " + str(dateRange))

    # latestSkillTier = ""
    # latestKarmaLevel = ""
    latestMatchDate = ""
    latestMatchGameMode = ""

    gameModes = []
    outcomes = []
    afks = []

    skillTiers = []
    karmaLevels = []

    kills = []
    assists = []
    deaths = []
    minionKills = []

    golds = []
    farms = []

    turrets = []
    crystalMiners = []
    goldMiners = []
    krakenCaptures = []

    actors = []
    # skins = []

    # items = []
    # itemUses = {}

    num = 0
    sampleSize = 0
    for match in data:
        # FOR DEBUGGING
        # print("DATE RANGE: " + str(dateRange) + " |MATCH DATE: " + str((dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None)))
        # if dateRange < (dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None):
        #     # FOR DEBUGGING
        #     print("NEWER")
        #
        # # Check if current match is out of date range if so break
        # elif dateRange > (dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None):
        #     # FOR DEBUGGING
        #     print("OLDER")
        #
        #     break

        if dateRange > (dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None):
            # FOR DEBUGGING
            # print("OLDER")

            break

        for roster in match["rosters"]:
            for participant in roster["participants"]:
                if participant["player"]["name"] == ign:

                    gameModes.append(tools.giveGameModeVG(match["gameMode"]))
                    outcomes.append(participant["winner"])
                    afks.append(participant["wentAfk"])

                    skillTiers.append(participant["skillTier"])
                    karmaLevels.append(participant["karmaLevel"])

                    kills.append(participant["kills"])
                    assists.append(participant["assists"])
                    deaths.append(participant["deaths"])
                    minionKills.append(participant["minionKills"])

                    golds.append(participant["gold"])
                    farms.append(participant["farm"])

                    turrets.append(participant["turretCaptures"])
                    crystalMiners.append(participant["crystalMineCaptures"])
                    goldMiners.append(participant["goldMineCaptures"])
                    krakenCaptures.append(participant["krakenCaptures"])

                    actors.append(tools.giveFormat(participant["actor"], "hero", emojis))
                    # skins.append(participant["skinKey"])
                    #
                    # # Get each item and place it in the items list
                    # for item in participant["items"]:
                    #     items.append(tools.clearItemNameVG(item))
                    #
                    # # Get each item and value and place it in the itemUses list
                    # for item, value in dict(participant["itemUses"]).items():
                    #     if item in itemUses:
                    #         itemUses[tools.clearItemNameVG(item)] += value
                    #
                    #     else:
                    #         itemUses[tools.clearItemNameVG(item)] = value

                    if num == 0:
                        latestMatchDate = str((dateutil.parser.parse(str(match["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"
                        latestMatchGameMode = str(match["gameMode"])
                        # latestSkillTier = tools.giveFormat(participant["skillTier"], "skillTier", emojis)
                        # latestKarmaLevel = tools.giveFormat(participant["karmaLevel"], "karma", emojis)

                    # We got what we needed continue on to next match
                    continue

        sampleSize += 1

    # FOR DEBUGGING
    # print("gameModes:   " + str(gameModes))
    # print("outcomes:   " + str(outcomes))
    # print("afks:    " + str(afks))
    #
    # print("skillTiers:   " + str(skillTiers))
    # print("karmaLevel:   " + str(karmaLevels))
    #
    # print("kills:   " + str(kills))
    # print("assists:   " + str(assists))
    # print("deaths:   " + str(deaths))
    # print("minion kills:   " + str(minionKills))
    #
    # print("golds:   " + str(golds))
    # print("farms:   " + str(farms))
    #
    # print("turrets:   " + str(turrets))
    # print("crystalMiners:   " + str(crystalMiners))
    # print("goldMiners:   " + str(goldMiners))
    # print("krakenCaptures:   " + str(krakenCaptures))
    #
    # print("actors:   " + str(actors))
    # # print("skins:   " + str(skins))
    # #
    # # print("items:   " + str(items))
    # # print("itemUses:   " + str(itemUses))

    # PROCESS THE DATA
    gameModesList = extraTools.giveListInOrder(gameModes)
    outcomesRate = round((extraTools.giveMeanOfList(outcomes) * 100), 2)
    afksRate = round((extraTools.giveMeanOfList(afks) * 100), 2)

    skillTiersMean = int(extraTools.giveMeanOfList(skillTiers))
    skillTiersMax = max(skillTiers)
    karmaLevelsMean = int(extraTools.giveMeanOfList(karmaLevels))
    karmaLevelsMax = max(karmaLevels)

    killsMean = round(extraTools.giveMeanOfList(kills), 2)
    killsTotal = round(sum(kills), 2)
    assistsMean = round(extraTools.giveMeanOfList(assists), 2)
    assistsTotal = round(sum(assists), 2)
    deathsMean = round(extraTools.giveMeanOfList(deaths), 2)
    deathsTotal = round(sum(deaths), 2)
    minionKillsMean = round(extraTools.giveMeanOfList(minionKills), 2)
    minionKillsTotal = round(sum(minionKills), 2)

    goldsMean = round(extraTools.giveMeanOfList(golds), 2)
    goldsTotal = round(sum(golds), 2)
    goldsMax = round(max(golds), 2)
    farmsMean = round(extraTools.giveMeanOfList(farms), 2)
    farmsTotal = round(sum(farms), 2)
    farmsMax = round(max(farms), 2)

    turretsMean = round(extraTools.giveMeanOfList(turrets), 2)
    turretsRate = round(((extraTools.giveMeanOfList(turrets) * 100) / (len(data) * 5)) * 100, 2)
    turretsTotal = round(sum(turrets), 2)
    turretsMax = round(max(turrets), 2)

    crystalMinersMean = round(extraTools.giveMeanOfList(crystalMiners), 2)
    crystalMinersRate = round(((extraTools.giveMeanOfList(crystalMiners) * 100) / (len(data) * 3)) * 100, 2)
    crystalMinersTotal = round(sum(crystalMiners), 2)
    crystalMinersMax = round(max(crystalMiners), 2)

    goldMinersMean = round(extraTools.giveMeanOfList(goldMiners), 2)
    goldMinersRate = round(((extraTools.giveMeanOfList(goldMiners) * 100) / (len(data) * 3)) * 100, 2)
    goldMinersTotal = round(sum(goldMiners), 2)
    goldMinersMax = round(max(goldMiners), 2)

    krakenCapturesMean = round(extraTools.giveMeanOfList(krakenCaptures), 2)
    krakenCapturesRate = round(((extraTools.giveMeanOfList(krakenCaptures) * 100) / (len(data) * 3)) * 100, 2)
    krakenCapturesTotal = round(sum(krakenCaptures), 2)
    krakenCapturesMax = round(max(krakenCaptures), 2)

    actorsList = extraTools.giveListInOrder(actors)
    # skinsList = extraTools.giveListInOrder(skins)
    #
    # itemsList = extraTools.giveListInOrder(items)
    # itemUsesList = extraTools.giveDictInOrder(itemUses, 1)

    if gameMode == "any":
        if len(gameModesList) >= 3:
            maxN = 3
            # print("maxN:   " + str(maxN) + " |List:   " + str(gameModesList))
        else:
            maxN = len(gameModesList) - 1
            # print("maxN:   " + str(maxN) + " |List:   " + str(gameModesList))
        num = 1
        gameModesString = ""
        while num <= maxN:
            gameModesString += "**" + str(num) + " ~ " + str(gameModesList[num - 1]) + "**\n"
            num += 1

        # FOR DEBUGGING
        # print("gameModes STRING:\n" + str(gameModesString))

    if len(actorsList) >= 3:
        maxN = 3
        # print("maxN:   " + str(maxN) + " |List:   " + str(actorsList))
    else:
        maxN = len(actorsList) - 1
        # print("maxN:   " + str(maxN) + " |List:   " + str(actorsList))
    num = 1
    actorsString = ""
    while num <= maxN:
        actorsString += "**" + str(num) + " ~ " + str(actorsList[num - 1]) + "**\n"
        num += 1

    # FOR DEBUGGING
    # print("actors STRING:\n" + str(actorsString))


    # if len(skinsList) >= 3:
    #     maxN = 3
    #     print("maxN:   " + str(maxN) + " |List:   " + str(skinsList))
    # else:
    #     maxN = len(skinsList) - 1
    #     print("maxN:   " + str(maxN) + " |List:   " + str(skinsList))
    # num = 1
    # skinsString = ""
    # while num <= maxN:
    #     skinsString += "**" + str(num) + " ~ " + str(skinsList[num - 1]) + "**\n"
    #     num += 1
    #
    # # FOR DEBUGGING
    # print("skins STRING:\n" + str(skinsString))
    #
    #
    # if len(itemsList) >= 3:
    #     maxN = 3
    #     print("maxN:   " + str(maxN) + " |List:   " + str(itemsList))
    # else:
    #     maxN = len(itemsList) - 1
    #     print("maxN:   " + str(maxN) + " |List:   " + str(itemsList))
    # num = 1
    # itemsString = ""
    # while num <= maxN:
    #     itemsString += "**" + str(num) + " ~ " + str(itemsList[num - 1]) + "**\n"
    #     num += 1
    #
    # # FOR DEBUGGING
    # print("items STRING:\n" + str(itemsString))
    #
    #
    # if len(itemUsesList) >= 3:
    #     maxN = 3
    #     print("maxN:   " + str(maxN) + " |List:   " + str(itemUsesList))
    # else:
    #     maxN = len(itemUsesList) - 1
    #     print("maxN:   " + str(maxN) + " |List:   " + str(itemUsesList))
    # num = 1
    # itemUsesString = ""
    # while num <= maxN:
    #     itemUsesString += "**" + str(num) + " ~ " + str(itemUsesList[num - 1]) + "**\n"
    #     num += 1
    #
    # # FOR DEBUGGING
    # print("itemUses STRING:\n" + str(itemUsesString))


    # Start of embed object
    embed = discord.Embed(
    title=languages.statsTitle(language, ign, region, gameMode),
    url="https://vgpro.gg/players//" + region + "/" + ign,
    description=languages.statsDescription(language, str(sampleSize), gameMode)
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    # Test img: "http://i63.tinypic.com/9k6xcj.jpg"
    embed.set_thumbnail(url="http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + actorsList[0] + ".png")

    embed.add_field(name=languages.statsFieldOneTitle(language), value=languages.statsFieldOne(language, latestMatchDate, tools.giveGameModeVG(latestMatchGameMode, 0)))

    if gameMode == "any":
        embed.add_field(name=languages.mostFrequentlyPlayedGameModes(language), value=gameModesString)

    embed.add_field(name=languages.mostFrequentlyUsedActors(language), value=actorsString)

    # embed.add_field(name=languages.statsFieldFourTitle(language), value=skinsString)

    # embed.add_field(name=languages.statsFieldFiveTitle(language), value=itemsString)

    # embed.add_field(name=languages.statsFieldSixTitle(language), value=itemUsesString)

    embed.add_field(name=languages.statsFieldSevenTitle(language), value=languages.statsFieldSeven(language, str(outcomesRate), str(afksRate), str(tools.giveFormat(skillTiersMean, "skillTier", emojis)), str(tools.giveFormat(skillTiersMax, "skillTier", emojis)), str(tools.giveFormat(karmaLevelsMean, "karma", emojis)), str(tools.giveFormat(karmaLevelsMax, "karma", emojis))))

    if compact == False:

        embed.add_field(name=languages.statsFieldEightTitle(language), value=languages.statsFieldEight(language, str(killsMean), str(killsTotal), str(assistsMean), str(assistsTotal), str(deathsMean), str(deathsTotal), str(minionKillsMean), str(minionKillsTotal)))

        embed.add_field(name=languages.statsFieldNineTitle(language), value=languages.statsFieldNine(language, str(goldsMean), str(goldsTotal), str(goldsMax), str(farmsMean), str(farmsTotal), str(farmsMax)))

        embed.add_field(name=languages.statsFieldTenTitle(language), value=languages.statsFieldTen(language, str(turretsMean), str(turretsRate), str(turretsTotal)))

        embed.add_field(name=languages.statsFieldElevenTitle(language), value=languages.statsFieldEleven(language, str(crystalMinersMean), str(crystalMinersRate), str(crystalMinersTotal)))

        embed.add_field(name=languages.statsFieldTwelveTitle(language), value=languages.statsFieldTwelve(language, str(goldMinersMean), str(goldMinersRate), str(goldMinersTotal), str(goldMinersMax)))

        embed.add_field(name=languages.statsFieldThirteenTitle(language), value=languages.statsFieldThirteen(language, str(krakenCapturesMean), str(krakenCapturesRate), str(krakenCapturesTotal), str(krakenCapturesMax)))

        embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

        # FOR DEBUGGING
        # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

        return embed

    else:

        embed.add_field(name=languages.statsFieldFourteenTitle(language), value=languages.statsFieldFourteen(language, str(killsMean), str(assistsMean), str(deathsMean), str(minionKillsMean), str(farmsMean), str(turretsTotal), str(crystalMinersTotal), str(goldMinersTotal), str(krakenCapturesTotal)))

        embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

        # FOR DEBUGGING
        # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

        return embed


def compareStatsEmbed(ignOne, ignTwo, regionOne="na", regionTwo="na", gameMode="any", days=28, compact=False, emojis=True, language="english", ad=""):
    """

    :param ignOne: In-game name of a VainGlory player; first player
    :param ignTwo: In-game name of a VaginGlory player; second player
    :param regionOne: Region of the first player
    :param regionTwo: Region of the second player
    :param gameMode: Game mode to sample stats from
    :param days: Days to sample stats from
    :param compact: If the content should be compact
    :param language: Language to display embed in
    :param ad: Ad to display at the end of footer
    :return: Discord embed object

    """

    # FOR DEBUGGING
    # print("STATS EMBED INPUT:\nIGN ONE:   " + str(ignOne) + " |REGION ONE:   " + str(regionOne) + " |IGN TWO:   " + str(ignTwo) + " |REGION TWO:   " + str(regionTwo) + " |GAMEMODE:   " + str(days))
    # print("COMPACT:   " + str(compact))

    dataOne = getMatches(ignOne, regionOne, gameMode)

    if "error" in dataOne:
        return ignOne

    dataTwo = getMatches(ignTwo, regionTwo, gameMode)

    if "error" in dataTwo:
        return ignTwo

    # To sample the same amount of matches
    if len(dataOne) > len(dataTwo):
        maxS = len(dataTwo) - 1

    else:
        maxS = len(dataOne) - 1

    # DATA
    # Get a time stamp for a date range to fetch data from
    dateRange = (datetime.datetime.today() - datetime.timedelta(days=days)).replace(tzinfo=None)

    # FOR DEBUGGING
    # print("DATE RANGE: " + str(dateRange))

    latestSkillTierOne = ""
    latestKarmaLevelOne = ""
    latestMatchDateOne = ""
    latestMatchGameModeOne = ""

    # gameModesOne = []
    outcomesOne = []
    afksOne = []

    # skillTiersOne = []
    # karmaLevelsOne = []

    killsOne = []
    assistsOne = []
    deathsOne = []
    # minionKillsOne = []

    # goldsOne = []
    # farmsOne = []

    turretsOne = []
    crystalMinersOne = []
    goldMinersOne = []
    krakenCapturesOne = []

    # actorsOne = []
    # skinsOne = []

    # itemsOne = []
    # itemUsesOne = {}

    num = 0
    sampleSize = 0
    for match in dataOne:
        # Break out of the loop once we get maximum number of samples allowed
        if num == maxS:
            break

        elif dateRange > (dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None):
            # FOR DEBUGGING
            # print("OLDER")

            break

        for roster in match["rosters"]:
            for participant in roster["participants"]:
                if participant["player"]["name"] == ignOne:

                    # gameModesOne.append(tools.giveGameModeVG(match["gameMode"]))
                    outcomesOne.append(participant["winner"])
                    afksOne.append(participant["wentAfk"])

                    # skillTiersOne.append(participant["skillTier"])
                    # karmaLevelsOne.append(participant["karmaLevel"])

                    killsOne.append(participant["kills"])
                    assistsOne.append(participant["assists"])
                    deathsOne.append(participant["deaths"])
                    # minionKillsOne.append(participant["minionKills"])

                    # goldsOne.append(participant["gold"])
                    # farmsOne.append(participant["farm"])

                    turretsOne.append(participant["turretCaptures"])
                    crystalMinersOne.append(participant["crystalMineCaptures"])
                    goldMinersOne.append(participant["goldMineCaptures"])
                    krakenCapturesOne.append(participant["krakenCaptures"])

                    # actorsOne.append(tools.cleanActorNameVG(participant["actor"]))
                    # skinsOne.append(participant["skinKey"])
                    #
                    # # Get each item and place it in the items list
                    # for item in participant["items"]:
                    #     itemsOne.append(tools.clearItemNameVG(item))
                    #
                    # # Get each item and value and place it in the itemUses list
                    # for item, value in dict(participant["itemUses"]).items():
                    #     if item in itemUsesOne:
                    #         itemUsesOne[tools.clearItemNameVG(item)] += value
                    #
                    #     else:
                    #         itemUsesOne[tools.clearItemNameVG(item)] = value

                    # Get data from the latest match
                    if num == 0:
                        latestMatchDateOne = str((dateutil.parser.parse(str(match["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"
                        latestMatchGameModeOne = tools.giveGameModeVG(str(match["gameMode"]))
                        latestSkillTierOne = tools.giveFormat(participant["skillTier"], "skillTier", emojis)
                        latestKarmaLevelOne = tools.giveFormat(participant["karmaLevel"], "karma", emojis)

                    # We got what we needed continue on to next match
                    continue

        num += 1
        sampleSize += 1

    maxS = sampleSize

    # FOR DEBUGGING
    # print("gameModesOne:   " + str(gameModesOne))
    # print("outcomesOne:   " + str(outcomesOne))
    # print("afksOne:    " + str(afksOne))
    #
    # print("skillTiersOne:   " + str(skillTiersOne))
    # print("karmaLevelOne:   " + str(karmaLevelsOne))
    #
    # print("killsOne:   " + str(killsOne))
    # print("assistsOne:   " + str(assistsOne))
    # print("deathsOne:   " + str(deathsOne))
    # print("minionKillsOne:   " + str(minionKillsOne))
    #
    # print("goldsOne:   " + str(goldsOne))
    # print("farmsOne:   " + str(farmsOne))
    #
    # print("turretsOne:   " + str(turretsOne))
    # print("crystalMinersOne:   " + str(crystalMinersOne))
    # print("goldMinersOne:   " + str(goldMinersOne))
    # print("krakenCapturesOne:   " + str(krakenCapturesOne))
    #
    # print("actorsOne:   " + str(actorsOne))
    # print("skinsOne:   " + str(skinsOne))
    #
    # print("itemsOne:   " + str(itemsOne))
    # print("itemUsesOne:   " + str(itemUsesOne))
    #
    # # PROCESS THE DATA
    # gameModesListOne = extraTools.giveListInOrder(gameModesOne)
    outcomesRateOne = round((extraTools.giveMeanOfList(outcomesOne) * 100), 2)
    afksRateOne = round((extraTools.giveMeanOfList(afksOne) * 100), 2)

    # skillTiersMeanOne = int(extraTools.giveMeanOfList(skillTiersOne))
    # skillTiersMaxOne = max(skillTiersOne)
    # karmaLevelsMeanOne = int(extraTools.giveMeanOfList(karmaLevelsOne))
    # karmaLevelsMaxOne = max(karmaLevelsOne)

    killsMeanOne = round(extraTools.giveMeanOfList(killsOne), 2)
    killsTotalOne = round(sum(killsOne), 2)
    assistsMeanOne = round(extraTools.giveMeanOfList(assistsOne), 2)
    assistsTotalOne = round(sum(assistsOne), 2)
    deathsMeanOne = round(extraTools.giveMeanOfList(deathsOne), 2)
    deathsTotalOne = round(sum(deathsOne), 2)
    # minionKillsMeanOne = round(extraTools.giveMeanOfList(minionKillsOne), 2)
    # minionKillsTotalOne = round(sum(minionKillsOne), 2)

    # goldsMeanOne = round(extraTools.giveMeanOfList(goldsOne), 2)
    # goldsTotalOne = round(sum(goldsOne), 2)
    # goldsMaxOne = round(max(goldsOne), 2)
    # farmsMeanOne = round(extraTools.giveMeanOfList(farmsOne), 2)
    # farmsTotalOne = round(sum(farmsOne), 2)
    # farmsMaxOne = round(max(farmsOne), 2)

    # turretsMeanOne = round(extraTools.giveMeanOfList(turretsOne), 2)
    turretsRateOne = round(((extraTools.giveMeanOfList(turretsOne) * 100) / (maxS * 5)) * 100, 2)
    # turretsTotalOne = round(sum(turretsOne), 2)
    # turretsMaxOne = round(max(turretsOne), 2)

    # crystalMinersMeanOne = round(extraTools.giveMeanOfList(crystalMinersOne), 2)
    crystalMinersRateOne = round(((extraTools.giveMeanOfList(crystalMinersOne) * 100) / (maxS * 3)) * 100, 2)
    # crystalMinersTotalOne = round(sum(crystalMinersOne), 2)
    # crystalMinersMaxOne = round(max(crystalMinersOne), 2)

    # goldMinersMeanOne = round(extraTools.giveMeanOfList(goldMinersOne), 2)
    goldMinersRateOne = round(((extraTools.giveMeanOfList(goldMinersOne) * 100) / (maxS * 3)) * 100, 2)
    # goldMinersTotalOne = round(sum(goldMinersOne), 2)
    # goldMinersMaxOne = round(max(goldMinersOne), 2)

    # krakenCapturesMeanOne = round(extraTools.giveMeanOfList(krakenCapturesOne), 2)
    krakenCapturesRateOne = round(((extraTools.giveMeanOfList(krakenCapturesOne) * 100) / (maxS * 3)) * 100, 2)
    # krakenCapturesTotalOne = round(sum(krakenCapturesOne), 2)
    # krakenCapturesMaxOne = round(max(krakenCapturesOne), 2)

    # actorsListOne = extraTools.giveListInOrder(actorsOne)
    # skinsListOne = extraTools.giveListInOrder(skinsOne)
    #
    # itemsListOne = extraTools.giveListInOrder(itemsOne)
    # itemUsesListOne = extraTools.giveDictInOrder(itemUsesOne, 1)

    # DATA
    latestSkillTierTwo = ""
    latestKarmaLevelTwo = ""
    latestMatchDateTwo = ""
    latestMatchGameModeTwo = ""

    # gameModesTwo = []
    outcomesTwo = []
    afksTwo = []

    # skillTiersTwo = []
    # karmaLevelsTwo = []

    killsTwo = []
    assistsTwo = []
    deathsTwo = []
    # minionKillsTwo = []

    # goldsTwo = []
    # farmsTwo = []

    turretsTwo = []
    crystalMinersTwo = []
    goldMinersTwo = []
    krakenCapturesTwo = []

    # actorsTwo = []
    # skinsTwo = []
    #
    # itemsTwo = []
    # itemUsesTwo = {}

    num = 0
    for match in dataTwo:
        # Break out of the loop once we get maximum number of samples allowed
        if num == maxS:
            break

        elif dateRange > (dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None):
            # FOR DEBUGGING
            # print("OLDER")

            break

        for roster in match["rosters"]:
            for participant in roster["participants"]:
                if participant["player"]["name"] == ignTwo:

                    # gameModesTwo.append(tools.giveGameModeVG(match["gameMode"]))
                    outcomesTwo.append(participant["winner"])
                    afksTwo.append(participant["wentAfk"])

                    # skillTiersTwo.append(participant["skillTier"])
                    # karmaLevelsTwo.append(participant["karmaLevel"])

                    killsTwo.append(participant["kills"])
                    assistsTwo.append(participant["assists"])
                    deathsTwo.append(participant["deaths"])
                    # minionKillsTwo.append(participant["minionKills"])

                    # goldsTwo.append(participant["gold"])
                    # farmsTwo.append(participant["farm"])

                    turretsTwo.append(participant["turretCaptures"])
                    crystalMinersTwo.append(participant["crystalMineCaptures"])
                    goldMinersTwo.append(participant["goldMineCaptures"])
                    krakenCapturesTwo.append(participant["krakenCaptures"])

                    # actorsTwo.append(tools.cleanActorNameVG(participant["actor"]))
                    # skinsTwo.append(participant["skinKey"])
                    #
                    # # Get each item and place it in the items list
                    # for item in participant["items"]:
                    #     itemsTwo.append(tools.clearItemNameVG(item))
                    #
                    # # Get each item and value and place it in the itemUses list
                    # for item, value in dict(participant["itemUses"]).items():
                    #     if item in itemUsesTwo:
                    #         itemUsesTwo[tools.clearItemNameVG(item)] += value
                    #
                    #     else:
                    #         itemUsesTwo[tools.clearItemNameVG(item)] = value

                    # Get data from the latest match
                    if num == 0:
                        latestMatchDateTwo = str((dateutil.parser.parse(str(match["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"
                        latestMatchGameModeTwo = tools.giveGameModeVG(str(match["gameMode"]))
                        latestSkillTierTwo = tools.giveFormat(participant["skillTier"], "skillTier", emojis)
                        latestKarmaLevelTwo = tools.giveFormat(participant["karmaLevel"], "karma", emojis)

                    # We got what we needed continue on to next match
                    continue

        num += 1
        sampleSize += 1

    # # FOR DEBUGGING
    # print("gameModesTwo:   " + str(gameModesTwo))
    # print("outcomesTwo:   " + str(outcomesTwo))
    # print("afksTwo:    " + str(afksTwo))
    #
    # print("skillTiersTwo:   " + str(skillTiersTwo))
    # print("karmaLevelTwo:   " + str(karmaLevelsTwo))
    #
    # print("killsTwo:   " + str(killsTwo))
    # print("assistsTwo:   " + str(assistsTwo))
    # print("deathsTwo:   " + str(deathsTwo))
    # print("minionKillsTwo:   " + str(minionKillsTwo))
    #
    # print("goldsTwo:   " + str(goldsTwo))
    # print("farmsTwo:   " + str(farmsTwo))
    #
    # print("turretsTwo:   " + str(turretsTwo))
    # print("crystalMinersTwo:   " + str(crystalMinersTwo))
    # print("goldMinersTwo:   " + str(goldMinersTwo))
    # print("krakenCapturesTwo:   " + str(krakenCapturesTwo))
    #
    # print("actorsTwo:   " + str(actorsTwo))
    # print("skinsTwo:   " + str(skinsTwo))
    #
    # print("itemsTwo:   " + str(itemsTwo))
    # print("itemUsesTwo:   " + str(itemUsesTwo))

    # PROCESS THE DATA
    # gameModesListTwo = extraTools.giveListInOrder(gameModesTwo)
    outcomesRateTwo = round((extraTools.giveMeanOfList(outcomesTwo) * 100), 2)
    afksRateTwo = round((extraTools.giveMeanOfList(afksTwo) * 100), 2)

    # skillTiersMeanTwo = int(extraTools.giveMeanOfList(skillTiersTwo))
    # skillTiersMaxTwo = max(skillTiersTwo)
    # karmaLevelsMeanTwo = int(extraTools.giveMeanOfList(karmaLevelsTwo))
    # karmaLevelsMaxTwo = max(karmaLevelsTwo)

    killsMeanTwo = round(extraTools.giveMeanOfList(killsTwo), 2)
    killsTotalTwo = round(sum(killsTwo), 2)
    assistsMeanTwo = round(extraTools.giveMeanOfList(assistsTwo), 2)
    assistsTotalTwo = round(sum(assistsTwo), 2)
    deathsMeanTwo = round(extraTools.giveMeanOfList(deathsTwo), 2)
    deathsTotalTwo = round(sum(deathsTwo), 2)
    # minionKillsMeanTwo = round(extraTools.giveMeanOfList(minionKillsTwo), 2)
    # minionKillsTotalTwo = round(sum(minionKillsTwo), 2)

    # goldsMeanTwo = round(extraTools.giveMeanOfList(goldsTwo), 2)
    # goldsTotalTwo = round(sum(goldsTwo), 2)
    # goldsMaxTwo = round(max(goldsTwo), 2)
    # farmsMeanTwo = round(extraTools.giveMeanOfList(farmsTwo), 2)
    # farmsTotalTwo = round(sum(farmsTwo), 2)
    # farmsMaxTwo = round(max(farmsTwo), 2)

    # turretsMeanTwo = round(extraTools.giveMeanOfList(turretsTwo), 2)
    turretsRateTwo = round(((extraTools.giveMeanOfList(turretsTwo) * 100) / (maxS * 5)) * 100, 2)
    # turretsTotalTwo = round(sum(turretsTwo), 2)
    # turretsMaxTwo = round(max(turretsTwo), 2)

    # crystalMinersMeanTwo = round(extraTools.giveMeanOfList(crystalMinersTwo), 2)
    crystalMinersRateTwo = round(((extraTools.giveMeanOfList(crystalMinersTwo) * 100) / (maxS * 3)) * 100, 2)
    # crystalMinersTotalTwo = round(sum(crystalMinersTwo), 2)
    # crystalMinersMaxTwo = round(max(crystalMinersTwo), 2)

    # goldMinersMeanTwo = round(extraTools.giveMeanOfList(goldMinersTwo), 2)
    goldMinersRateTwo = round(((extraTools.giveMeanOfList(goldMinersTwo) * 100) / (maxS * 3)) * 100, 2)
    # goldMinersTotalTwo = round(sum(goldMinersTwo), 2)
    # goldMinersMaxTwo = round(max(goldMinersTwo), 2)

    # krakenCapturesMeanTwo = round(extraTools.giveMeanOfList(krakenCapturesTwo), 2)
    krakenCapturesRateTwo = round(((extraTools.giveMeanOfList(krakenCapturesTwo) * 100) / (maxS * 3)) * 100, 2)
    # krakenCapturesTotalTwo = round(sum(krakenCapturesTwo), 2)
    # krakenCapturesMaxTwo = round(max(krakenCapturesTwo), 2)

    # actorsListTwo = extraTools.giveListInOrder(actorsTwo)
    # skinsListTwo = extraTools.giveListInOrder(skinsTwo)
    #
    # itemsListTwo = extraTools.giveListInOrder(itemsTwo)
    # # itemUsesListTwo = extraTools.giveDictInOrder(itemUsesTwo, 1)

    # SPECIAL PROCESS
    rate = round(abs(((killsTotalOne + assistsTotalOne) - (0.3 * deathsTotalOne)) / ((killsTotalOne + assistsTotalOne + (0.3 * deathsTotalOne)) + (killsTotalTwo + assistsTotalTwo + (0.3 * deathsTotalTwo))) * 100), 2)

    # FOR DEBUGGING
    # print("RATE:   " + str(rate))

    # Start of embed object
    embed = discord.Embed(
    title=ignOne + " & " + ignTwo,
    url="https://vgpro.gg/players//" + regionOne + "/" + ignOne,
    description=languages.compareStatsDescription(language, ignOne, ignTwo, regionOne, regionTwo, gameMode, str(days), str(sampleSize))
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    embed.add_field(name=languages.compareStatsFieldFiveTitle(language, ignOne, ignTwo), value=languages.compareStatsFieldFive(language, ignOne, ignTwo, str(rate)))

    embed.add_field(name=languages.compareStatsFieldFourTitle(language, ignOne), value=languages.compareStatsFieldFour(language, str(outcomesRateOne), str(afksRateOne)))

    embed.add_field(name=languages.compareStatsFieldFourTitle(language, ignTwo), value=languages.compareStatsFieldFour(language, str(outcomesRateTwo), str(afksRateTwo)))

    if compact == False:

        embed.add_field(name=languages.compareStatsFieldOneTitle(language, ignOne), value=languages.compareStatsFieldOne(language, latestSkillTierOne, latestKarmaLevelOne, latestMatchDateOne, latestMatchGameModeOne))

        embed.add_field(name=languages.compareStatsFieldOneTitle(language, ignTwo), value=languages.compareStatsFieldOne(language, latestSkillTierTwo, latestKarmaLevelTwo,  latestMatchDateTwo, latestMatchGameModeTwo))

        embed.add_field(name=languages.compareStatsFieldTwoTitle(language, ignOne), value=languages.compareStatsFieldTwo(language, str(killsMeanOne), str(killsTotalOne), str(assistsMeanOne), str(assistsTotalOne), str(deathsMeanOne), str(deathsTotalOne)))

        embed.add_field(name=languages.compareStatsFieldTwoTitle(language, ignTwo), value=languages.compareStatsFieldTwo(language, str(killsMeanTwo), str(killsTotalTwo), str(assistsMeanTwo), str(assistsTotalTwo), str(deathsMeanTwo), str(deathsTotalTwo)))

        embed.add_field(name=languages.compareStatsFieldThreeTitle(language, ignOne), value=languages.compareStatsFieldThree(language, str(turretsRateOne), str(crystalMinersRateOne), str(goldMinersRateOne), str(krakenCapturesRateOne)))

        embed.add_field(name=languages.compareStatsFieldThreeTitle(language, ignTwo), value=languages.compareStatsFieldThree(language, str(turretsRateTwo), str(crystalMinersRateTwo), str(goldMinersRateTwo), str(krakenCapturesRateTwo)))

    else:

        embed.add_field(name=languages.compareStatsFieldTwoTitle(language, ignOne), value=languages.compareStatsFieldTwo(language, str(killsMeanOne), str(killsTotalOne), str(assistsMeanOne), str(assistsTotalOne), str(deathsMeanOne), str(deathsTotalOne)))

        embed.add_field(name=languages.compareStatsFieldTwoTitle(language, ignTwo), value=languages.compareStatsFieldTwo(language, str(killsMeanTwo), str(killsTotalTwo), str(assistsMeanTwo), str(assistsTotalTwo), str(deathsMeanTwo), str(deathsTotalTwo)))

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    return embed


def latestMatchEmbed(ign, region, gameMode, compact=False, emojis=True, ad="", language="english"):
    """

    :param ign: In-game name of the VainGlory player
    :param region: Region of the VainGlory player
    :param gameMode: Game mode to look at
    :param compact: If info should be shown compacted
    :param ad: Ad to display at the end of footer
    :param language: Language to display information in
    :return: Discord embed object

    """

    data = getMatches(ign, region, gameMode)

    if "error" in data:
        return False

    matchData = data[0]

    # DATA
    thumbNail = "http://i63.tinypic.com/9k6xcj.jpg"
    # skillTier = "Unknown"
    # karma = "Unknown"
    winner = None

    matchId = matchData["id"]
    gameMode = str(tools.giveGameModeVG(matchData["gameMode"]))

    info = {}
    teamInfo = {}

    matchDate = str((dateutil.parser.parse(str(matchData["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"

    # Retrieve players data from match data
    num = 0
    maxNum = int(randrange(0, 6))
    for roster in matchData["rosters"]:
        info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {}
        teamInfo[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {

            "gold": roster["gold"],
            "heroKills": roster["heroKills"],
            "acesEarned": roster["acesEarned"],
            "turretKills": roster["turretKills"],
            # "turretRemaining": roster["turretsRemaining"],
            "krakenCaptures": roster["krakenCaptures"]

        }

        for participant in roster["participants"]:

            info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])] = {

                "skillTier": str(participant["skillTier"]),
                "karma": str(participant["karmaLevel"]),
                "level": str(participant["player"]["level"]),
                "actor": str(participant["actor"]),
                "kills": str(participant["kills"]),
                "assists": str(participant["assists"]),
                "deaths": str(participant["deaths"]),
                "farm": str(round(participant["farm"], 2)),
                "items": " - "

            }

            for item_name in participant["items"]:
                info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])]["items"] += str(tools.giveFormat(item_name, "item", emojis)) + " - "

            # Get data of player we're looking at
            if ign != "$random$" and participant["player"]["name"] == ign:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

            elif ign == "$random$" and num == maxNum:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

            elif ign == "$random$" and num >= 6:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

            num += 1

    if winner == True:
        colour = discord.Colour.green()

    elif winner == False:
        colour = discord.Colour.dark_red()

    else:
        colour = discord.Colour.dark_grey()

    # Start of embed object
    embed = discord.Embed(
    title=languages.matchesTitle(language, str(ign), str(region).upper(), str(gameMode)),
    url="https://vgpro.gg/players//" + region + "/" + ign,
    colour=colour,
    description=languages.matchDescriptionOne(language, str(matchDate), str(matchId))
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url=thumbNail)

    if compact == False:

        for team, data in info.items():

            embed.add_field(name="**" + team + "**", value=languages.matchGeneralView(language, str(round(teamInfo[team]["gold"], 2)), str(round(teamInfo[team]["heroKills"], 2)), str(round(teamInfo[team]["acesEarned"], 2)), str(round(teamInfo[team]["turretKills"], 2)), str(round(teamInfo[team]["krakenCaptures"], 2))))

            for name, stats in data.items():
                # msg += languages.playerMatchInfo(language, name, tools.giveFormat(stats["skillTier"], "skillTier", emojis), tools.giveFormat(stats["karma"], "karma", emojis), stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis), stats["items"]) + "\n"
                embed.add_field(name="__**" + str(name) + "**__", value=languages.playerMatchInfo(language, tools.giveFormat(stats["skillTier"], "skillTier", emojis), tools.giveFormat(stats["karma"], "karma", emojis), stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis), stats["items"]))

                # FOR DEBUGGING
                # break

    else:
        for team, data in info.items():

            embed.add_field(name="**" + team + "**", value=languages.matchGeneralView(language, str(round(teamInfo[team]["gold"], 2)), str(round(teamInfo[team]["heroKills"], 2)), str(round(teamInfo[team]["acesEarned"], 2)), str(round(teamInfo[team]["turretKills"], 2)), str(round(teamInfo[team]["krakenCaptures"], 2))))

            for name, stats in data.items():
                # msg += languages.playerMatchInfoCompact(language, name, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis)) + "\n"
                embed.add_field(name="__**" + str(name) + "**__", value=languages.playerMatchInfoCompact(language, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis)))

                # FOR DEBUGGING
                # break

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def matchEmbed(ign, matchId, region, compact=False, emojis=True, language="english", ad=""):
    """

    :param ign: Players vainglory in-game name.
    :param matchId: VainGlory match id.
    :param region: Region of match.
    :param compact: If information should be compact.
    :param language: Language to display info in.
    :param ad: Ad to add at the end of the footer.
    :return: Discord embed object.

    """

    matchData = getMatch(matchId, region)

    if "error" in matchData:
        return False

    matchData = matchData[0]

    # DATA
    thumbNail = "http://i63.tinypic.com/9k6xcj.jpg"
    # skillTier = "Unknown"
    # karma = "Unknown"
    winner = None

    matchId = matchData["id"]
    gameMode = str(tools.giveGameModeVG(matchData["gameMode"]))

    info = {}
    teamInfo = {}

    matchDate = str((dateutil.parser.parse(str(matchData["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"

    # Retrieve players data from match data
    num = 0
    maxNum = int(randrange(0, 6))
    for roster in matchData["rosters"]:
        info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {}
        teamInfo[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {

            "gold": roster["gold"],
            "heroKills": roster["heroKills"],
            "acesEarned": roster["acesEarned"],
            "turretKills": roster["turretKills"],
            # "turretRemaining": roster["turretsRemaining"],
            "krakenCaptures": roster["krakenCaptures"]

        }

        for participant in roster["participants"]:

            info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])] = {

                "skillTier": str(participant["skillTier"]),
                "karma": str(participant["karmaLevel"]),
                "level": str(participant["player"]["level"]),
                "actor": str(participant["actor"]),
                "kills": str(participant["kills"]),
                "assists": str(participant["assists"]),
                "deaths": str(participant["deaths"]),
                "farm": str(round(participant["farm"], 2)),
                "items": " - "

            }

            for item_name in participant["items"]:
                info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])]["items"] += str(tools.giveFormat(item_name, "item", emojis)) + " - "

            # Get data of player we're looking at
            if ign != "$random$" and participant["player"]["name"] == ign:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

            elif ign == "$random$" and num == maxNum:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

            elif ign == "$random$" and num >= 6:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

            num += 1

    if winner == True:
        colour = discord.Colour.green()

    elif winner == False:
        colour = discord.Colour.dark_red()

    else:
        colour = discord.Colour.dark_grey()

    # Start of embed object
    embed = discord.Embed(
    title=languages.matchesTitle(language, str(ign), str(region).upper(), str(gameMode)),
    url="https://vgpro.gg/players//" + region + "/" + ign,
    colour=colour,
    description=languages.matchDescriptionOne(language, str(matchDate), str(matchId))
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url=thumbNail)

    if compact == False:

        for team, data in info.items():

            embed.add_field(name="**" + team + "**", value=languages.matchGeneralView(language, str(round(teamInfo[team]["gold"], 2)), str(round(teamInfo[team]["heroKills"], 2)), str(round(teamInfo[team]["acesEarned"], 2)), str(round(teamInfo[team]["turretKills"], 2)), str(round(teamInfo[team]["krakenCaptures"], 2))))

            for name, stats in data.items():
                # msg += languages.playerMatchInfo(language, name, tools.giveFormat(stats["skillTier"], "skillTier", emojis), tools.giveFormat(stats["karma"], "karma", emojis), stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis), stats["items"]) + "\n"
                embed.add_field(name="__**" + str(name) + "**__", value=languages.playerMatchInfo(language, tools.giveFormat(stats["skillTier"], "skillTier", emojis), tools.giveFormat(stats["karma"], "karma", emojis), stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis), stats["items"]))

                # FOR DEBUGGING
                # break

    else:
        for team, data in info.items():

            embed.add_field(name="**" + team + "**", value=languages.matchGeneralView(language, str(round(teamInfo[team]["gold"], 2)), str(round(teamInfo[team]["heroKills"], 2)), str(round(teamInfo[team]["acesEarned"], 2)), str(round(teamInfo[team]["turretKills"], 2)), str(round(teamInfo[team]["krakenCaptures"], 2))))

            for name, stats in data.items():
                # msg += languages.playerMatchInfoCompact(language, name, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis)) + "\n"
                embed.add_field(name="__**" + str(name) + "**__", value=languages.playerMatchInfoCompact(language, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis)))

                # FOR DEBUGGING
                # break

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def matchesEmbed(matchData, ign, region, pageNum=1, pagesMax=50, compact=False, emojis=True, language="english", ad=""):
    """

    :param matchData: The matches data.
    :param ign: In-game name of the player whose data it belongs to.
    :param region: Region of the match.
    :param pageNum: Number of the match.
    :param pagesMax: Number of pages.
    :param compact: If information should be compacted.
    :param language: Language to display info in.
    :param ad: Ad to add at the end of the embed footer.
    :returns: Discord embed object.

    """

    # DATA
    thumbNail = "http://i63.tinypic.com/9k6xcj.jpg"
    # skillTier = "Unknown"
    # karma = "Unknown"
    winner = None

    matchId = matchData["id"]
    gameMode = str(tools.giveGameModeVG(matchData["gameMode"]))

    info = {}
    teamInfo = {}

    matchDate = str((dateutil.parser.parse(str(matchData["createdAt"]))).strftime("%d/%m/%Y %H:%M:%S")) + " GMT"

    # Retrieve players data from match data
    for roster in matchData["rosters"]:
        info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {}
        teamInfo[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {

            "gold": roster["gold"],
            "heroKills": roster["heroKills"],
            "acesEarned": roster["acesEarned"],
            "turretKills": roster["turretKills"],
            # "turretRemaining": roster["turretsRemaining"],
            "krakenCaptures": roster["krakenCaptures"]

        }

        for participant in roster["participants"]:

            info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])] = {

                "skillTier": str(participant["skillTier"]),
                "karma": str(participant["karmaLevel"]),
                "level": str(participant["player"]["level"]),
                "actor": str(participant["actor"]),
                "kills": str(participant["kills"]),
                "assists": str(participant["assists"]),
                "deaths": str(participant["deaths"]),
                "farm": str(round(participant["farm"], 2)),
                "items": " - "

            }

            for item_name in participant["items"]:
                info[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])]["items"] += str(tools.giveFormat(item_name, "item", emojis)) + " - "

            # Get data of player we're looking at
            if participant["player"]["name"] == ign:
                winner = participant["winner"]
                # karma = str(participant["karmaLevel"])
                # skillTier = str(participant["skillTier"])
                thumbNail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(tools.cleanHeroName(participant["actor"])) + ".png"

    # teamsString = "("
    # goldString = ""
    # heroKillsString = ""
    # acesEarnedString = ""
    # turretKillsString = ""
    # turretRemainingString = ""
    # krakenCapturesString = ""
    # for key, value in teamInfo.items():
    #     teamsString += key + " "
    #     goldString += "- " + str(value["gold"])
    #     heroKillsString += "- " + str(value["heroKills"])
    #     acesEarnedString += "- " + str(value["acesEarned"])
    #     turretKillsString += "- " + str(value["turretKills"])
    #     turretRemainingString += "- " + str(value["turretRemaining"])
    #     krakenCapturesString += "- " + str(value["krakenCaptures"])
    #
    # teamsString += ")"

    # FOR DEBUGGING
    # print("INFO:   " + str(info))

    if winner == True:
        colour = discord.Colour.green()

    elif winner == False:
        colour = discord.Colour.dark_red()

    else:
        colour = discord.Colour.dark_grey()

    # Start of embed object
    embed = discord.Embed(
    title=languages.matchesTitle(language, str(ign), str(region).upper(), str(gameMode)),
    url="https://vgpro.gg/players//" + region + "/" + ign,
    colour=colour,
    description=languages.matchesDescription(language, str(matchDate), str(matchId), str(pageNum), str(pagesMax))
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.set_thumbnail(url=thumbNail)

    if compact == False:

        for team, data in info.items():

            embed.add_field(name="**" + team + "**", value=languages.matchGeneralView(language, str(round(teamInfo[team]["gold"], 2)), str(round(teamInfo[team]["heroKills"], 2)), str(round(teamInfo[team]["acesEarned"], 2)), str(round(teamInfo[team]["turretKills"], 2)), str(round(teamInfo[team]["krakenCaptures"], 2))))

            for name, stats in data.items():
                # msg += languages.playerMatchInfo(language, name, tools.giveFormat(stats["skillTier"], "skillTier", emojis), tools.giveFormat(stats["karma"], "karma", emojis), stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis), stats["items"]) + "\n"
                embed.add_field(name="__**" + str(name) + "**__", value=languages.playerMatchInfo(language, tools.giveFormat(stats["skillTier"], "skillTier", emojis), tools.giveFormat(stats["karma"], "karma", emojis), stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis), stats["items"]))

                # FOR DEBUGGING
                # break

    else:
        for team, data in info.items():

            embed.add_field(name="**" + team + "**", value=languages.matchGeneralView(language, str(round(teamInfo[team]["gold"], 2)), str(round(teamInfo[team]["heroKills"], 2)), str(round(teamInfo[team]["acesEarned"], 2)), str(round(teamInfo[team]["turretKills"], 2)), str(round(teamInfo[team]["krakenCaptures"], 2))))

            for name, stats in data.items():
                # msg += languages.playerMatchInfoCompact(language, name, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis)) + "\n"
                embed.add_field(name="__**" + str(name) + "**__", value=languages.playerMatchInfoCompact(language, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], tools.giveFormat(stats["actor"], "hero", emojis)))

                # FOR DEBUGGING
                # break

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def matchesTelemetryEmbed(data, mode, ign, gameMode, matchId, actor, winner, side, sectionNum, sectionMax, compact=False, emojis=True, language="english", ad=""):
    """

    :param data: Data; can be a dict or list.
    :param mode: Type of data that should be displayed.
    :param ign: In-game name of the player we'er looking at.
    :param gameMode: Game mode of the match.
    :param matchId: Match's id.
    :param actor: Actor of the player we are looking at.
    :param winner: If the player won this match.
    :param side: Side the player we are looking on played on.
    :param sectionNum: Section we are looking at.
    :param sectionMax: Total amounts of sections.
    :param compact: If things displayed should be compacted.
    :param language: Language to display in.
    :param ad: Ad to add to the end of footer.
    :return: Discord embed object.

    """

    if sectionNum == -1:

        if winner == True:
            colour = discord.Colour.green()

        elif winner == False:
            colour = discord.Colour.dark_red()

        else:
            colour = discord.Colour.dark_grey()

        # Start of embed object
        embed = discord.Embed(
        title=languages.telemetryTitle(language, matchId),
        url=config.bot_server,
        colour=colour,
        description=languages.telemetryDescription(language, ign, "summary", str(sectionMax), str(len(data)), gameMode, matchId)
        )

        embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

        embed.set_thumbnail(url="http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + actor + ".png")

        if compact == False:

            for team, data in data.items():
                msg = ""
                for name, stats in data.items():
                    msg += languages.playerTelemetryMatchInfoCompact(language, name, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], stats["actor"]) + "\n"

                embed.add_field(name=languages.latestFieldOneTitle(language, team), value=msg)

        else:
            for team, data in data.items():
                msg = ""
                for name, stats in data.items():
                    msg += languages.playerTelemetryMatchInfoCompact(language, name, stats["kills"], stats["assists"], stats["deaths"], stats["farm"], stats["actor"]) + "\n"

                embed.add_field(name=languages.latestFieldOneTitle(language, team), value=msg)

        embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

        # FOR DEBUGGING
        # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

        return embed

    else:
        msg = ""
        if mode == 0:
            for event in data:
                try:
                    if event["type"] == "KillActor":
                        # If it's a hero kill mark hero kill
                        if event["payload"]["TargetIsHero"] == 1:
                            # Get the killer hero info
                            actorOne = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            teamOne = event["payload"]["Team"]

                            # Get the hero killed info
                            actorTwo = tools.giveFormat(event["payload"]["Killed"], "hero", emojis)
                            teamTwo = event["payload"]["KilledTeam"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            # FOR DEBUGGING
                            # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                            msg += languages.telemetryHeroKillHero(language, teamEmoji, actorOne, teamOne, actorTwo, teamTwo)

                            if len(msg) >= 500:
                                break

                        # If it's a turret mark a turret
                        elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                            # Get the killer hero info
                            actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryHeroKillTurret(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a crystal miner kill mark a flag
                        elif event["payload"]["Killed"] == "*JungleMinion_GoldMiner*":
                            # Get the killer hero info
                            actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryHeroKillGoldMiner(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a gold miner kill mark a flag
                        elif event["payload"]["Killed"] == "*JungleMinion_CrystalMiner*":
                            # Get the killer hero info
                            actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryHeroKillCrystalMiner(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a kraken mark a kraken
                        elif event["payload"]["Killed"] == "*Kraken_Captured*":
                            # Get the killer hero info
                            actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryHeroCaptureKraken(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a kraken mark a kraken
                        elif event["payload"]["Killed"] == "*Kraken_Jungle*":
                            # Get the killer hero info
                            actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryHeroKillKraken(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a vain crystal mark a crystal
                        elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                            # Get the killer hero info
                            actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryHeroKillVainCrystal(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's nothing above mark nothing
                        else:
                            continue

                    # Marks whenever a npc was kills
                    elif event["type"] == "NPCkillNPC":
                        # If it's a hero kill mark hero kill
                        if event["payload"]["TargetIsHero"] == 1:
                            # Get the npc info
                            actorOne = tools.cleanNonHeroName(event["payload"]["Actor"])
                            teamOne = event["payload"]["Team"]

                            # Get the hero killed info
                            actorTwo = tools.giveFormat(event["payload"]["Killed"], "hero", emojis)
                            teamTwo = event["payload"]["KilledTeam"]

                            # FOR DEBUGGING
                            # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcKillHero(language, teamEmoji, actorOne, teamOne, actorTwo, teamTwo)

                            if len(msg) >= 500:
                                break

                        # If it's a turret mark a turret
                        elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                            # Get the npc info
                            actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcKillTurret(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a crystal miner kill mark a flag
                        elif event["payload"]["Killed"] == "*JungleMinion_GoldMiner*":
                            # Get the npc info
                            actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcKillGoldMiner(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a gold miner kill mark a flag
                        elif event["payload"]["Killed"] == "*JungleMinion_CrystalMiner*":
                            # Get the npc info
                            actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcKillCrystalMiner(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a kraken mark a kraken
                        elif event["payload"]["Killed"] == "*Kraken_Captured*":
                            # Get the npc info
                            actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcCapturedKraken(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a kraken mark a kraken
                        elif event["payload"]["Killed"] == "*Kraken_Jungle*":
                            # Get the npc info
                            actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcKillKraken(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's a vain crystal mark a crystal
                        elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                            # Get the npc info
                            actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                            team = event["payload"]["Team"]

                            if event["payload"]["Team"] == side:
                                teamEmoji = ":large_blue_circle:"

                            else:
                                teamEmoji = ":red_circle:"

                            msg += languages.telemetryNpcKillVainCrystal(language, teamEmoji, actor, team)

                            if len(msg) >= 500:
                                break

                        # If it's nothing above mark nothing
                        else:
                            continue

                except:
                    continue

        elif mode == 1:
            for event in data:
                try:

                    if event["type"] == "HeroBan":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Hero"], "hero", emojis)
                        team = event["payload"]["Team"]
                        if team == "2":
                            team = "Right"

                        else:
                            team = "Left"

                        if team == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetryBanHero(language, teamEmoji, actor, team)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "HeroSelect":
                        # Get the players info
                        player = str(event["payload"]["Handle"])
                        actor = tools.giveFormat(event["payload"]["Hero"], "hero", emojis)
                        team = event["payload"]["Team"]
                        if team == "2":
                            team = "Right"

                        else:
                            team = "Left"

                        if team == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetrySelectHero(language, teamEmoji, player, actor)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "HeroSkinSelect":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Hero"], "hero", emojis)
                        skin = str(event["payload"]["Skin"]).replace("*", "")

                        teamEmoji = ":white_circle:"

                        msg += languages.telemetrySelectSkin(language, teamEmoji, actor, skin)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "HeroSwap":
                        # Get the players info
                        actorOne = tools.giveFormat(event["payload"][0]["Hero"], "hero", emojis)
                        actorTwo = tools.giveFormat(event["payload"][1]["Hero"], "hero", emojis)

                        team = event["payload"][0]["Team"]
                        if team == "2":
                            team = "Right"

                        else:
                            team = "Left"

                        if team == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetrySwapHero(language, teamEmoji, actorOne, actorTwo)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "LevelUp":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                        team = event["payload"]["Team"]

                        level = str(event["payload"]["Level"])

                        if event["payload"]["Team"] == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetryHeroLevelUp(language, teamEmoji, actor, team, level)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "UseAbility":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                        team = event["payload"]["Team"]

                        ability = tools.cleanHeroAbility(event["payload"]["Ability"])

                        if event["payload"]["Team"] == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetryHeroAbilityUse(language, teamEmoji, actor, team, ability)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "UseItemAbility":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                        team = event["payload"]["Team"]

                        ability = tools.cleanHeroAbility(event["payload"]["Ability"])

                        if event["payload"]["Team"] == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetryItemAbilityUse(language, teamEmoji, actor, team, ability)

                        if len(msg) >= 500:
                            break

                except:
                    continue

        elif mode == 2:
            for event in data:
                try:

                    if event["type"] == "BuyItem":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                        team = event["payload"]["Team"]

                        item = tools.giveFormat(event["payload"]["Item"], "item", emojis)

                        if event["payload"]["Team"] == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetryBuyItem(language, teamEmoji, actor, team, item)

                        if len(msg) >= 500:
                            break

                    elif event["type"] == "SellItem":
                        # Get the players info
                        actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                        team = event["payload"]["Team"]

                        item = tools.giveFormat(event["payload"]["Item"], "item", emojis)

                        if event["payload"]["Team"] == side:
                            teamEmoji = ":large_blue_circle:"

                        else:
                            teamEmoji = ":red_circle:"

                        msg += languages.telemetrySellItem(language, teamEmoji, actor, team, item)

                        if len(msg) >= 500:
                            break

                except:
                    continue

        # FOR DEBUGGING
        # print("TELEMETRY MSG BEFORE:\n" + str(msg))

        if msg == "":
            msg = "**Nothing to show** :shrug:"

        if len(msg) > 500:
            msg += "__**This Is As Much Information As Can Be Shown**__"

        # FOR DEBUGGING
        # print("TELEMETRY MSG AFTER:\n" + str(msg))
        # print("TELEMETRY MSG SIZE:   " + str(len(msg)))

        # Start of embed object
        embed = discord.Embed(
        title=languages.telemetryTitle(language, matchId),
        url=config.bot_server,
        colour=discord.Colour.purple(),
        description=languages.telemetryDescription(language, ign, str(sectionNum), str(sectionMax), str(len(data)), gameMode, matchId)
        )

        embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

        embed.set_thumbnail(url="http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + actor + ".png")

        if compact == False:

            embed.add_field(name="STUFF", value=msg)

            embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

            # FOR DEBUGGING
            # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

            return embed

        else:

            embed.add_field(name="STUFF", value=msg)

            embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

            # FOR DEBUGGING
            # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

            return embed

def telemetryMinute(data, side, compact=False, emojis=True, language="english"):
    msg = ""
    msgs = []
    for event in data:
        try:
            if event["type"] == "KillActor":
                # If it's a hero kill mark hero kill
                if event["payload"]["TargetIsHero"] == 1:
                    # Get the killer hero info
                    actorOne = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    teamOne = event["payload"]["Team"]

                    # Get the hero killed info
                    actorTwo = tools.giveFormat(event["payload"]["Killed"], "hero", emojis)
                    teamTwo = event["payload"]["KilledTeam"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    # FOR DEBUGGING
                    # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                    msg += languages.telemetryHeroKillHero(language, teamEmoji, actorOne, teamOne, actorTwo, teamTwo)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a turret mark a turret
                elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                    # Get the killer hero info
                    actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryHeroKillTurret(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a crystal miner kill mark a flag
                elif event["payload"]["Killed"] == "*JungleMinion_GoldMiner*":
                    # Get the killer hero info
                    actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryHeroKillGoldMiner(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a gold miner kill mark a flag
                elif event["payload"]["Killed"] == "*JungleMinion_CrystalMiner*":
                    # Get the killer hero info
                    actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryHeroKillCrystalMiner(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a kraken mark a kraken
                elif event["payload"]["Killed"] == "*Kraken_Captured*":
                    # Get the killer hero info
                    actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryHeroCaptureKraken(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a kraken mark a kraken
                elif event["payload"]["Killed"] == "*Kraken_Jungle*":
                    # Get the killer hero info
                    actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryHeroKillKraken(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a vain crystal mark a crystal
                elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                    # Get the killer hero info
                    actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryHeroKillVainCrystal(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

            elif event["type"] == "NPCkillNPC":
                # If it's a npc kill mark hero kill
                if event["payload"]["TargetIsHero"] == 1:
                    # Get the npc info
                    actorOne = tools.cleanNonHeroName(event["payload"]["Actor"])
                    teamOne = event["payload"]["Team"]

                    # Get the hero killed info
                    actorTwo = tools.giveFormat(event["payload"]["Killed"], "hero", emojis)
                    teamTwo = event["payload"]["KilledTeam"]

                    # FOR DEBUGGING
                    # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcKillHero(language, teamEmoji, actorOne, teamOne, actorTwo, teamTwo)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a turret mark a turret
                elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                    # Get the npc info
                    actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcKillTurret(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a crystal miner kill mark a flag
                elif event["payload"]["Killed"] == "*JungleMinion_GoldMiner*":
                    # Get the npc info
                    actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcKillGoldMiner(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a gold miner kill mark a flag
                elif event["payload"]["Killed"] == "*JungleMinion_CrystalMiner*":
                    # Get the npc info
                    actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcKillCrystalMiner(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a kraken mark a kraken
                elif event["payload"]["Killed"] == "*Kraken_Captured*":
                    # Get the npc info
                    actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcCapturedKraken(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a kraken mark a kraken
                elif event["payload"]["Killed"] == "*Kraken_Jungle*":
                    # Get the npc info
                    actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                    team = event["payload"]["Team"]

                    if event["payload"]["Team"] == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcKillKraken(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

                # If it's a vain crystal mark a crystal
                elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                    # Get the npc info
                    actor = tools.cleanNonHeroName(event["payload"]["Actor"])
                    team = event["payload"]["Team"]

                    if team == side:
                        teamEmoji = ":large_blue_circle:"

                    else:
                        teamEmoji = ":red_circle:"

                    msg += languages.telemetryNpcKillVainCrystal(language, teamEmoji, actor, team)

                    if len(msg) >= 1500:
                        msgs.append(msg)
                        msg = ""

            elif event["type"] == "HeroBan":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Hero"], "hero", emojis)
                team = event["payload"]["Team"]
                if team == "2":
                    team = "Right"

                else:
                    team = "Left"

                if team == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetryBanHero(language, teamEmoji, actor, team)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "HeroSelect":
                # Get the players info
                player = str(event["payload"]["Handle"])
                actor = tools.giveFormat(event["payload"]["Hero"]), "hero", emojis
                team = event["payload"]["Team"]
                if team == "2":
                    team = "Right"

                else:
                    team = "Left"

                if team == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetrySelectHero(language, teamEmoji, player, actor)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "HeroSkinSelect":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Hero"], "hero", emojis)
                skin = str(event["payload"]["Skin"]).replace("*", "")

                teamEmoji = ":white_circle:"

                msg += languages.telemetrySelectSkin(language, teamEmoji, actor, skin)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "HeroSwap":
                # Get the players info
                actorOne = tools.giveFormat(event["payload"][0]["Hero"], "hero", emojis)
                actorTwo = tools.giveFormat(event["payload"][1]["Hero"], "hero", emojis)

                team = event["payload"][0]["Team"]
                if team == "2":
                    team = "Right"

                else:
                    team = "Left"

                if team == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetrySwapHero(language, teamEmoji, actorOne, actorTwo)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "LevelUp":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                team = event["payload"]["Team"]

                level = str(event["payload"]["Level"])

                if event["payload"]["Team"] == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetryHeroLevelUp(language, teamEmoji, actor, team, level)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "UseAbility":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                team = event["payload"]["Team"]

                ability = tools.cleanHeroAbility(event["payload"]["Ability"])

                if event["payload"]["Team"] == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetryHeroAbilityUse(language, teamEmoji, actor, team, ability)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "UseItemAbility":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                team = event["payload"]["Team"]

                ability = tools.cleanHeroAbility(event["payload"]["Ability"])

                if event["payload"]["Team"] == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetryItemAbilityUse(language, teamEmoji, actor, team, ability)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "BuyItem":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                team = event["payload"]["Team"]

                item = tools.giveFormat(event["payload"]["Item"], "item", emojis)

                if event["payload"]["Team"] == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetryBuyItem(language, teamEmoji, actor, team, item)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

            elif event["type"] == "SellItem":
                # Get the players info
                actor = tools.giveFormat(event["payload"]["Actor"], "hero", emojis)
                team = event["payload"]["Team"]

                item = tools.giveFormat(event["payload"]["Item"], "item", emojis)

                if event["payload"]["Team"] == side:
                    teamEmoji = ":large_blue_circle:"

                else:
                    teamEmoji = ":red_circle:"

                msg += languages.telemetrySellItem(language, teamEmoji, actor, team, item)

                if len(msg) >= 1500:
                    msgs.append(msg)
                    msg = ""

        except:
            continue

    # FOR DEBUGGING
    # print("MSG SENT:   " + str(msg))
    # print("AMOUNT OF MSGs:   " + str(len(msgs)))

    if msg != "" and msg not in msgs:
        msgs.append(msg)

    if msgs == []:
        msgs = ["**Nothing to show** :shrug:"]

    return msgs


def topElementEmbed(topElements, ign, region="na", gameMode="any", days=28, compact=False, emojis=True, language="english", ad=""):
    """

    :param topElements: Element that should be listed.
    :param ign: In-game name of a VainGlory player
    :param region: Region of player
    :param gameMode: Game mode to sample stats from
    :param days: Days to sample stats from
    :param compact: If the content should be compact
    :param language: Language to display embed in
    :param ad: Ad to display at the end of footer
    :return: Discord embed object

    """

    # FOR DEBUGGING
    # print("STATS EMBED INPUT:\nIGN :   " + str(ign) + " |REGION :   " + str(region) + " |GAMEMODE:   " + str(days))

    data = getMatches(ign, region, gameMode)

    if "error" in data:
        return False

    # DATA
    # Get a time stamp for a date range to fetch data from
    dateRange = (datetime.datetime.today() - datetime.timedelta(days=days)).replace(tzinfo=None)

    # FOR DEBUGGING
    # print("DATE RANGE: " + str(dateRange))

    # latestSkillTier = ""
    # latestKarmaLevel = ""
    # latestMatchDate = ""
    # latestMatchGameMode = ""

    gameModes = []
    # outcomes = []
    # afks = []
    #
    # skillTiers = []
    # karmaLevels = []
    #
    # kills = []
    # assists = []
    # deaths = []
    # minionKills = []
    #
    # golds = []
    # farms = []
    #
    # turrets = []
    # crystalMiners = []
    # goldMiners = []
    # krakenCaptures = []

    actors = []
    skins = []

    items = []
    itemUses = {}

    for match in data:
        if dateRange > (dateutil.parser.parse(str(match["createdAt"]))).replace(tzinfo=None):
            # FOR DEBUGGING
            # print("OLDER")

            break

        for roster in match["rosters"]:
            for participant in roster["participants"]:
                if participant["player"]["name"] == ign:

                    gameModes.append(tools.giveGameModeVG(match["gameMode"]))
                    # outcomes.append(participant["winner"])
                    # afks.append(participant["wentAfk"])
                    #
                    # skillTiers.append(participant["skillTier"])
                    # karmaLevels.append(participant["karmaLevel"])
                    #
                    # kills.append(participant["kills"])
                    # assists.append(participant["assists"])
                    # deaths.append(participant["deaths"])
                    # minionKills.append(participant["minionKills"])
                    #
                    # golds.append(participant["gold"])
                    # farms.append(participant["farm"])
                    #
                    # turrets.append(participant["turretCaptures"])
                    # crystalMiners.append(participant["crystalMineCaptures"])
                    # goldMiners.append(participant["goldMineCaptures"])
                    # krakenCaptures.append(participant["krakenCaptures"])

                    actors.append(participant["actor"])
                    skins.append(participant["skinKey"])

                    # Get each item and place it in the items list
                    for item in participant["items"]:
                        items.append(item)

                    # Get each item and value and place it in the itemUses list
                    for item, value in dict(participant["itemUses"]).items():
                        if item in itemUses:
                            itemUses[item] += value

                        else:
                            itemUses[item] = value

                    # We got what we needed continue on to next match
                    continue

    # FOR DEBUGGING
    # print("gameModes:   " + str(gameModes))
    # print("outcomes:   " + str(outcomes))
    # print("afks:    " + str(afks))
    #
    # print("skillTiers:   " + str(skillTiers))
    # print("karmaLevel:   " + str(karmaLevels))
    #
    # print("kills:   " + str(kills))
    # print("assists:   " + str(assists))
    # print("deaths:   " + str(deaths))
    # print("minion kills:   " + str(minionKills))
    #
    # print("golds:   " + str(golds))
    # print("farms:   " + str(farms))
    #
    # print("turrets:   " + str(turrets))
    # print("crystalMiners:   " + str(crystalMiners))
    # print("goldMiners:   " + str(goldMiners))
    # print("krakenCaptures:   " + str(krakenCaptures))
    #
    # print("actors:   " + str(actors))
    # # print("skins:   " + str(skins))
    # #
    # # print("items:   " + str(items))
    # # print("itemUses:   " + str(itemUses))

    # PROCESS THE DATA
    gameModesList = extraTools.giveListInOrder(gameModes)
    # outcomesRate = round((extraTools.giveMeanOfList(outcomes) * 100), 2)
    # afksRate = round((extraTools.giveMeanOfList(afks) * 100), 2)
    #
    # skillTiersMean = int(extraTools.giveMeanOfList(skillTiers))
    # skillTiersMax = max(skillTiers)
    # karmaLevelsMean = int(extraTools.giveMeanOfList(karmaLevels))
    # karmaLevelsMax = max(karmaLevels)
    #
    # killsMean = round(extraTools.giveMeanOfList(kills), 2)
    # killsTotal = round(sum(kills), 2)
    # assistsMean = round(extraTools.giveMeanOfList(assists), 2)
    # assistsTotal = round(sum(assists), 2)
    # deathsMean = round(extraTools.giveMeanOfList(deaths), 2)
    # deathsTotal = round(sum(deaths), 2)
    # minionKillsMean = round(extraTools.giveMeanOfList(minionKills), 2)
    # minionKillsTotal = round(sum(minionKills), 2)
    #
    # goldsMean = round(extraTools.giveMeanOfList(golds), 2)
    # goldsTotal = round(sum(golds), 2)
    # goldsMax = round(max(golds), 2)
    # farmsMean = round(extraTools.giveMeanOfList(farms), 2)
    # farmsTotal = round(sum(farms), 2)
    # farmsMax = round(max(farms), 2)
    #
    # turretsMean = round(extraTools.giveMeanOfList(turrets), 2)
    # turretsRate = round(((extraTools.giveMeanOfList(turrets) * 100) / (len(data) * 5)) * 100, 2)
    # turretsTotal = round(sum(turrets), 2)
    # turretsMax = round(max(turrets), 2)
    #
    # crystalMinersMean = round(extraTools.giveMeanOfList(crystalMiners), 2)
    # crystalMinersRate = round(((extraTools.giveMeanOfList(crystalMiners) * 100) / (len(data) * 3)) * 100, 2)
    # crystalMinersTotal = round(sum(crystalMiners), 2)
    # crystalMinersMax = round(max(crystalMiners), 2)
    #
    # goldMinersMean = round(extraTools.giveMeanOfList(goldMiners), 2)
    # goldMinersRate = round(((extraTools.giveMeanOfList(goldMiners) * 100) / (len(data) * 3)) * 100, 2)
    # goldMinersTotal = round(sum(goldMiners), 2)
    # goldMinersMax = round(max(goldMiners), 2)
    #
    # krakenCapturesMean = round(extraTools.giveMeanOfList(krakenCaptures), 2)
    # krakenCapturesRate = round(((extraTools.giveMeanOfList(krakenCaptures) * 100) / (len(data) * 3)) * 100, 2)
    # krakenCapturesTotal = round(sum(krakenCaptures), 2)
    # krakenCapturesMax = round(max(krakenCaptures), 2)

    actorsList = extraTools.giveListInOrder(actors)
    skinsList = extraTools.giveListInOrder(skins)

    itemsList = extraTools.giveListInOrder(items)
    itemUsesList = extraTools.giveDictInOrder(itemUses, 1)

    if compact == False:
        limitNum = 10
    else:
        limitNum = 3

    if len(gameModesList) >= limitNum:
        maxN = limitNum
        # print("maxN:   " + str(maxN) + " |List:   " + str(gameModesList))
    else:
        maxN = len(gameModesList) - 1
        # print("maxN:   " + str(maxN) + " |List:   " + str(gameModesList))
    num = 1
    gameModesString = ""
    while num <= maxN:
        gameModesString += "**" + str(num) + " ~ " + str(gameModesList[num - 1]) + "**\n"
        num += 1

    # FOR DEBUGGING
    # print("gameModes STRING:\n" + str(gameModesString))

    if len(actorsList) >= limitNum:
        maxN = limitNum
        # print("maxN:   " + str(maxN) + " |List:   " + str(actorsList))
    else:
        maxN = len(actorsList) - 1
        # print("maxN:   " + str(maxN) + " |List:   " + str(actorsList))
    num = 1
    actorsString = ""
    while num <= maxN:
        actorsString += "**" + str(num) + " ~ " + str(tools.giveFormat(actorsList[num - 1], "hero", emojis)) + "**\n"
        num += 1

    # FOR DEBUGGING
    # print("actors STRING:\n" + str(actorsString))

    if len(skinsList) >= limitNum:
        maxN = limitNum
        # print("maxN:   " + str(maxN) + " |List:   " + str(skinsList))
    else:
        maxN = len(skinsList) - 1
        # print("maxN:   " + str(maxN) + " |List:   " + str(skinsList))
    num = 1
    skinsString = ""
    while num <= maxN:
        skinsString += "**" + str(num) + " ~ " + str(skinsList[num - 1]) + "**\n"
        num += 1

    # FOR DEBUGGING
    # print("skins STRING:\n" + str(skinsString))


    if len(itemsList) >= limitNum:
        maxN = limitNum
        # print("maxN:   " + str(maxN) + " |List:   " + str(itemsList))
    else:
        maxN = len(itemsList) - 1
        # print("maxN:   " + str(maxN) + " |List:   " + str(itemsList))
    num = 1
    itemsString = ""
    while num <= maxN:
        itemsString += "**" + str(num) + " ~ " + str(tools.giveFormat(itemsList[num - 1], "item", emojis)) + "**\n"
        num += 1

    # FOR DEBUGGING
    # print("items STRING:\n" + str(itemsString))


    if len(itemUsesList) >= limitNum:
        maxN = limitNum
        # print("maxN:   " + str(maxN) + " |List:   " + str(itemUsesList))
    else:
        maxN = len(itemUsesList) - 1
        # print("maxN:   " + str(maxN) + " |List:   " + str(itemUsesList))
    num = 1
    itemUsesString = ""
    while num <= maxN:
        itemUsesString += "**" + str(num) + " ~ " + str(tools.giveFormat(itemUsesList[num - 1], "item", emojis)) + "**\n"
        num += 1

    # FOR DEBUGGING
    # print("itemUses STRING:\n" + str(itemUsesString))

    # Start of embed object
    embed = discord.Embed(
    title=ign,
    url="https://vgpro.gg/players//" + region + "/" + ign,
    description=languages.topListDescription(language, ign, region, topElements)
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    # Test img: "http://i63.tinypic.com/9k6xcj.jpg"
    embed.set_thumbnail(url="http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + actorsList[0] + ".png")

    if gameMode != "any" and "gamemodes" in topElements:
        embed.add_field(name=languages.mostFrequentlyPlayedGameModes(language), value=gameModesString)

    if "heroes" in topElements:
        embed.add_field(name=languages.mostFrequentlyUsedActors(language), value=actorsString)

    if "skins" in topElements:
        embed.add_field(name=languages.mostFrequentlyUsedSkins(language), value=skinsString)

    if "items" in topElements:
        embed.add_field(name=languages.mostFrequentlyBoughtItems(language), value=itemsString)

    if "itemUse" in topElements:
        embed.add_field(name=languages.mostFrequentlyUsedItemsTitle(language), value=itemUsesString)

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed


def leaderboardEmbed(ign, prefixOne, prefixTwo, order="ascending", compact=False, language="english", ad=""):

    data = db.vgLeaderBoardDictionary(ign, prefixOne, prefixTwo, order)

    if data == False or data == None:
        return False

    num = 0

    if data[0].count() < 10:
        maxNum = data[0].count()

    else:
        maxNum = 9

    msg = ""

    for user in data[0]:

        # FOR DEBUGGING
        # print("USER:   " + str(user))

        msg += "**" + str(num + 1) + " - " + str(user["_id"]).replace("_", " ") + "** *|* **" + str(user["score"]) + "**\n"

        num += 1

        if num == maxNum:
            break

    msg += "\n__**Your Score:**__\n**" + str(data[1]["_id"]).replace("_", " ") + "** *|* **" + str(data[1]["score"]) + "**"

    # Start of embed object
    embed = discord.Embed(
    title=ign,
    url=config.bot_server,
    description=languages.leaderboardDescription(language, prefixOne, prefixTwo, ign)
    )

    embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

    embed.add_field(name="__**" + str(prefixOne).title() + " " + str(prefixTwo).title() + "**__", value=msg)

    embed.set_footer(text="Powered by MadGlory gamelocker!" + ad, icon_url=config.bot_icon)

    # FOR DEBUGGING
    # print("EMBED:   " + str(embed) + "\nEMBED DICT:   " + str(embed.to_dict()) + "\nEMBED JSON:   " + str(json.dumps(embed.to_dict())))

    return embed
