import config
from src.vainglory_work import tools
from src.mongo_work import core as db


def processMatch(matchData, ign, region):
    """

    :param matchData: Match data to check.
    :param ign: In-game name of player whose data is belongs to.
    :param region: Region of the match data.
    :return: Doesn't return anything; None

    """

    try:

        # print("!!!CHECKING MATCH DATA FOR LARBOARDS!!!")

        # DATA
        gameMode = tools.giveGameModeVG(matchData["gameMode"])

        # print("GAME MODE:   " + str(gameMode))

        # Check if the game mode is a game mode we record
        if gameMode not in ["casual", "ranked"]:
            # print("!!!MATCH ISN'T VALID!!!")
            return

        # print("!!!MATCH IS VALID!!!")

        afks = 0

        kills = 0
        assists = 0
        deaths = 0
        minionKills = 0

        gold = 0
        farm = 0

        # turrets = 0
        # crystalMiners = 0
        goldMiners = 0
        krakenCaptures = 0

        actor = "Unknown"
        # skins = []

        # items = []
        # itemUses = {}

        # Go trough match data and get variables used in the lapboards
        for roster in matchData["rosters"]:
            for participant in roster["participants"]:
                if participant["player"]["name"] == ign:
                    afks = participant["wentAfk"]

                    kills = participant["kills"]
                    assists = participant["assists"]
                    deaths = participant["deaths"]
                    minionKills = participant["minionKills"]

                    gold = participant["gold"]
                    farm = participant["farm"]

                    # turrets = participant["turretCaptures"]
                    # crystalMiners = participant["crystalMineCaptures"]
                    goldMiners = participant["goldMineCaptures"]
                    krakenCaptures = participant["krakenCaptures"]

                    actor = tools.cleanHeroName(participant["actor"])
                    # skins = participant["skinKey"]
                    #
                    # # Get each item and place it in the items list
                    # for item in participant["items"]:
                    #     items = tools.clearItemNameVG(item))
                    #
                    # # Get each item and value and place it in the itemUses list
                    # for item, value in dict(participant["itemUses"]).items():
                    #     if item in itemUses:
                    #         itemUses[tools.clearItemNameVG(item)] += value
                    #
                    #     else:
                    #         itemUses[tools.clearItemNameVG(item)] = value

                    # We got what we needed so stop
                    break

        # If the player's actor isn't found then return
        if actor == "":
            return

        roles = tools.giveActorsRoleList(actor)
        if "Unknown" in roles:
            return

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Afks", afks, "greater")
        db.updateVgLeaderBoard(ign, region, "Afks", afks, "greater")

        db.updateVgLeaderBoard(ign, actor, "Afks", afks, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Afks", afks, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Afks", afks, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Kills", kills, "greater")
        db.updateVgLeaderBoard(ign, region, "Kills", kills, "greater")

        db.updateVgLeaderBoard(ign, actor, "Kills", kills, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Kills", kills, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Kills", kills, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Assists", assists, "greater")
        db.updateVgLeaderBoard(ign, region, "Assists", assists, "greater")

        db.updateVgLeaderBoard(ign, actor, "Assists", assists, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Assists", assists, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Assists", assists, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Deaths", deaths, "greater")
        db.updateVgLeaderBoard(ign, region, "Deaths", deaths, "greater")

        db.updateVgLeaderBoard(ign, actor, "Deaths", deaths, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Deaths", deaths, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Deaths", deaths, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Minion Kills", minionKills, "greater")
        db.updateVgLeaderBoard(ign, region, "Minion Kills", minionKills, "greater")

        db.updateVgLeaderBoard(ign, actor, "Minion Kills", minionKills, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Minion Kills", minionKills, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Minion Kills", minionKills, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Gold", gold, "greater")
        db.updateVgLeaderBoard(ign, region, "Gold", gold, "greater")

        db.updateVgLeaderBoard(ign, actor, "Gold", gold, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Gold", gold, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Gold", gold, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Farm", farm, "greater")
        db.updateVgLeaderBoard(ign, region, "Farm", farm, "greater")

        db.updateVgLeaderBoard(ign, actor, "Farm", farm, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Farm", farm, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Farm", farm, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Gold Miners", goldMiners, "greater")
        db.updateVgLeaderBoard(ign, region, "Gold Miners", goldMiners, "greater")

        db.updateVgLeaderBoard(ign, actor, "Gold Miners", goldMiners, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Gold Miners", goldMiners, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Gold Miners", goldMiners, "greater")

        # Check if score is greater then the one already recorded if any.
        db.updateVgLeaderBoard(ign, "global", "Kraken Captures", krakenCaptures, "greater")
        db.updateVgLeaderBoard(ign, region, "Kraken Captures", krakenCaptures, "greater")

        db.updateVgLeaderBoard(ign, actor, "Kraken Captures", krakenCaptures, "greater")
        db.updateVgLeaderBoard(ign, roles[0], "Kraken Captures", krakenCaptures, "greater")
        db.updateVgLeaderBoard(ign, roles[1], "Kraken Captures", krakenCaptures, "greater")

    except Exception as e:
        print("ERROR WHILE PROCESSING MATCH IN LEADER BOARDS:\n" + str(e))


def processMatches(matchesData, ign, region):
    """

    :param matchesData: Match data to check.
    :param ign: In-game name of player whose data is belongs to.
    :param region: Region of the match data.
    :return: Doesn't return anything; None

    """

    try:

        # print("!!!CHECKING MATCH DATA FOR LARBOARDS!!!")

        for matchData in matchesData:

            # DATA
            gameMode = tools.giveGameModeVG(matchData["gameMode"])

            # print("GAME MODE:   " + str(gameMode))

            # Check if the game mode is a game mode we record
            if gameMode not in ["casual", "ranked"]:
                # print("!!!MATCH ISN'T VALID!!!")
                continue

            # print("!!!MATCH IS VALID!!!")

            afks = 0

            kills = 0
            assists = 0
            deaths = 0
            minionKills = 0

            gold = 0
            farm = 0

            # turrets = 0
            # crystalMiners = 0
            goldMiners = 0
            krakenCaptures = 0

            actor = "Unknown"
            # skins = []

            # items = []
            # itemUses = {}

            # Go trough match data and get variables used in the lapboards
            for roster in matchData["rosters"]:
                for participant in roster["participants"]:
                    if participant["player"]["name"] == ign:
                        afks = participant["wentAfk"]

                        kills = participant["kills"]
                        assists = participant["assists"]
                        deaths = participant["deaths"]
                        minionKills = participant["minionKills"]

                        gold = participant["gold"]
                        farm = participant["farm"]

                        # turrets = participant["turretCaptures"]
                        # crystalMiners = participant["crystalMineCaptures"]
                        goldMiners = participant["goldMineCaptures"]
                        krakenCaptures = participant["krakenCaptures"]

                        actor = tools.cleanHeroName(participant["actor"])
                        # skins = participant["skinKey"]
                        #
                        # # Get each item and place it in the items list
                        # for item in participant["items"]:
                        #     items = tools.clearItemNameVG(item))
                        #
                        # # Get each item and value and place it in the itemUses list
                        # for item, value in dict(participant["itemUses"]).items():
                        #     if item in itemUses:
                        #         itemUses[tools.clearItemNameVG(item)] += value
                        #
                        #     else:
                        #         itemUses[tools.clearItemNameVG(item)] = value

                        # We got what we needed so stop
                        break

            # If the player's actor isn't found then return
            if actor == "":
                continue

            roles = tools.giveActorsRoleList(actor)
            if "Unknown" in roles:
                continue

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Afks", afks, "greater")
            db.updateVgLeaderBoard(ign, region, "Afks", afks, "greater")

            db.updateVgLeaderBoard(ign, actor, "Afks", afks, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Afks", afks, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Afks", afks, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Kills", kills, "greater")
            db.updateVgLeaderBoard(ign, region, "Kills", kills, "greater")

            db.updateVgLeaderBoard(ign, actor, "Kills", kills, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Kills", kills, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Kills", kills, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Assists", assists, "greater")
            db.updateVgLeaderBoard(ign, region, "Assists", assists, "greater")

            db.updateVgLeaderBoard(ign, actor, "Assists", assists, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Assists", assists, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Assists", assists, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Deaths", deaths, "greater")
            db.updateVgLeaderBoard(ign, region, "Deaths", deaths, "greater")

            db.updateVgLeaderBoard(ign, actor, "Deaths", deaths, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Deaths", deaths, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Deaths", deaths, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Minion Kills", minionKills, "greater")
            db.updateVgLeaderBoard(ign, region, "Minion Kills", minionKills, "greater")

            db.updateVgLeaderBoard(ign, actor, "Minion Kills", minionKills, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Minion Kills", minionKills, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Minion Kills", minionKills, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Gold", gold, "greater")
            db.updateVgLeaderBoard(ign, region, "Gold", gold, "greater")

            db.updateVgLeaderBoard(ign, actor, "Gold", gold, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Gold", gold, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Gold", gold, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Farm", farm, "greater")
            db.updateVgLeaderBoard(ign, region, "Farm", farm, "greater")

            db.updateVgLeaderBoard(ign, actor, "Farm", farm, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Farm", farm, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Farm", farm, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Gold Miners", goldMiners, "greater")
            db.updateVgLeaderBoard(ign, region, "Gold Miners", goldMiners, "greater")

            db.updateVgLeaderBoard(ign, actor, "Gold Miners", goldMiners, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Gold Miners", goldMiners, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Gold Miners", goldMiners, "greater")

            # Check if score is greater then the one already recorded if any.
            db.updateVgLeaderBoard(ign, "global", "Kraken Captures", krakenCaptures, "greater")
            db.updateVgLeaderBoard(ign, region, "Kraken Captures", krakenCaptures, "greater")

            db.updateVgLeaderBoard(ign, actor, "Kraken Captures", krakenCaptures, "greater")
            db.updateVgLeaderBoard(ign, roles[0], "Kraken Captures", krakenCaptures, "greater")
            db.updateVgLeaderBoard(ign, roles[1], "Kraken Captures", krakenCaptures, "greater")

    except Exception as e:
        print("ERROR WHILE PROCESSING MATCHES IN LEADER BOARDS:\n" + str(e))
