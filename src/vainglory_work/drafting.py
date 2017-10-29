import config
import traceback
from src.vainglory_work import tools
from src.mongo_work import core as db


def processMatch(matchData):
    """

    :param matchData: Match data to check.
    :return: None, doesn't return anything.

    """

    try:

        # FOR DEBUGGING
        # print("!!!CHECKING MATCH DATA FOR DRAFTING!!!")
        # print("MATCH DATA: " + str(matchData))

        # DATA
        gameMode = tools.giveGameModeVG(matchData["gameMode"])

        # FOR DEBUGGING
        # print("GAME MODE:   " + str(gameMode))

        # Check if the game mode is a game mode we record
        if gameMode not in ["casual", "rank"]:
            # FOR DEBUGGING
            # print("!!!MATCH ISN'T VALID!!!")

            return

        # print("!!!MATCH IS VALID!!!")

        # Go trough match data and get variables used in the lapboards
        rosterNum = 0
        for roster in matchData["rosters"]:
            for participant in roster["participants"]:

                # FOR DEBUGGING
                # print("ROSTER PARTICIPANT: " + str(participant))

                mainHero = tools.cleanHeroName(participant["actor"])

                if participant["winner"] == True:
                    key = "wins"

                else:
                    key = "losses"

                db.updateVgHero(mainHero, "total" + key.title(), 1)
                db.updateVgHero(mainHero, "totalKills", participant["kills"])
                db.updateVgHero(mainHero, "totalDeaths", participant["deaths"])
                db.updateVgHero(mainHero, "totalAssists", participant["assists"])
                db.updateVgHero(mainHero, "totalMinionKills", participant["minionKills"])
                db.updateVgHero(mainHero, "totalFarm", participant["farm"])
                db.updateVgHero(mainHero, "totalGold", participant["gold"])
                db.updateVgHero(mainHero, "totalTurrets", participant["turretCaptures"])
                db.updateVgHero(mainHero, "totalGoldMiners", participant["goldMineCaptures"])
                db.updateVgHero(mainHero, "totalCrystalMiners", participant["crystalMineCaptures"])
                db.updateVgHero(mainHero, "totalKrakens", participant["krakenCaptures"])

                for item in participant["items"]:
                    db.updateVgHeroItem(mainHero, tools.cleanItemName(item), key, 1)

                if rosterNum == 0:
                    for subParticipant in matchData["rosters"][1]["participants"]:
                        subHero = tools.cleanHeroName(subParticipant["actor"])

                        db.updateVgHeroSubHero(mainHero, subHero, key, 1)

                else:
                    for subParticipant in matchData["rosters"][0]["participants"]:
                        subHero = tools.cleanHeroName(subParticipant["actor"])

                        db.updateVgHeroSubHero(mainHero, subHero, key, 1)

            rosterNum += 1

    except Exception as e:
        print("ERROR WHILE PROCESSING MATCH IN DRAFTING:\n" + str(e) + "\n\nTRACEBACK:\n" + str(traceback.format_exc()) + "\n")


def processMatches(matchesData):
    """

    :param matchesData: List of matches data to check.
    :return: None, doesn't return anything.

    """

    try:

        # FOR DEBUGGING
        # print("!!!CHECKING MATCH DATA FOR DRAFTING!!!")

        for matchData in matchesData:

            # DATA
            gameMode = tools.giveGameModeVG(matchData["gameMode"])

            # FOR DEBUGGING
            # print("GAME MODE:   " + str(gameMode))

            # Check if the game mode is a game mode we record
            if gameMode not in ["casual", "rank"]:
                # FOR DEBUGGING
                # print("!!!MATCH ISN'T VALID!!!")
                return

            # print("!!!MATCH IS VALID!!!")

            # Go trough match data and get variables used in the lapboards
            rosterNum = 0
            for roster in matchData["rosters"]:
                for participant in roster["participants"]:

                    # FOR DEBUGGING
                    # print("ROSTER PARTICIPANT: " + str(participant))

                    mainHero = tools.cleanHeroName(participant["actor"])

                    if participant["winner"] == True:
                        key = "wins"

                    else:
                        key = "losses"

                    db.updateVgHero(mainHero, "total" + key.title(), 1)
                    db.updateVgHero(mainHero, "totalKills", participant["kills"])
                    db.updateVgHero(mainHero, "totalDeaths", participant["deaths"])
                    db.updateVgHero(mainHero, "totalAssists", participant["assists"])
                    db.updateVgHero(mainHero, "totalMinionKills", participant["minionKills"])
                    db.updateVgHero(mainHero, "totalFarm", participant["farm"])
                    db.updateVgHero(mainHero, "totalGold", participant["gold"])
                    db.updateVgHero(mainHero, "totalTurrets", participant["turretCaptures"])
                    db.updateVgHero(mainHero, "totalGoldMiners", participant["goldMineCaptures"])
                    db.updateVgHero(mainHero, "totalCrystalMiners", participant["crystalMineCaptures"])
                    db.updateVgHero(mainHero, "totalKrakens", participant["krakenCaptures"])

                    for item in participant["items"]:
                        db.updateVgHeroItem(mainHero, tools.cleanItemName(item), key, 1)

                    if rosterNum == 0:
                        for subParticipant in matchData["rosters"][1]["participants"]:
                            subHero = tools.cleanHeroName(subParticipant["actor"])

                            db.updateVgHeroSubHero(mainHero, subHero, key, 1)

                    else:
                        for subParticipant in matchData["rosters"][0]["participants"]:
                            subHero = tools.cleanHeroName(subParticipant["actor"])

                            db.updateVgHeroSubHero(mainHero, subHero, key, 1)

                rosterNum += 1

    except Exception as e:
        print("ERROR WHILE PROCESSING MATCHES IN DRAFTING:\n" + str(e))
