# VG Module:
# Functions using the VG API. Functions using Discord libraries will be marked by, "!!!DISCORD!!!", in their description.

# IMPORTS
import gamelocker
import datetime
import TOOL_module as tools
from gamelocker.strings import pretty

# VG Variables-- Use #1 = , Use #2 = Object Oriented
keyVG = ""  # VG_API_TOKEN_HERE
apiVG = gamelocker.Gamelocker(keyVG).Vainglory()  # Use #1


# Will get the COMMAND given and EXECUTE the according FUNCTION
async def commandVG(client, message, something):
    COMMAND =  message.content.split()  # SPLIT up the MESSAGE to form the COMMAND

    # Check the SIZE of the COMMAND to narrow down the POSSIBILITIES
    if len(COMMAND) == 1:  # 1 PIECE to the COMMAND in other words just >VG
        await client.send_message(message.channel, "**>VG** ~ *Command used in a model for Computer Bot.*"
        "\n**>VG help** ~ *for a list of VG commands*")

    elif len(COMMAND) == 2:  # 2 PIECES to the COMMAND
        if str(COMMAND[1]) == "help":  # >VG help
            await client.send_message(message.channel, "**(R) = required input - (O) = optional input**\n**>VG** ~ Command used in a model for Computer Bot. "
        "\n**>VG help** ~ *for a list of commands*\n**>VG player NAME** ~ *Check if IGN is in VG database! ~ NAME - (R)In game name ~*\n**>VG performance NAME DAYS** ~ *Check match performance in a range of days ~ NAME - (R)In game name, DAYS - (O)Day range ~*")  # SEND MSG

        else:  # COMMAND is ILLEGAL for not being VALID
            await client.send_message(message.channel, "That isn't a command for **>VG**!\n**>VG** ~ *for a list of VG commands*")  # SEND MSG

    elif len(COMMAND) == 3:  # 3 PIECES to the COMMAND
        if str(COMMAND[1]) == "player":  # >VG player
            await client.send_message(message.channel, getIDVG(COMMAND[2]))  # PROCESS DATA RETURN and MSG

        elif str(COMMAND[1]) == "performance":  # >VG performance NAME
            msg = await client.send_message(message.channel, "Looking at " + COMMAND[2] + " match history from the past 7 days... :eyes:")  # Send MSG saying DATA is being PROCESSED
            await client.edit_message(msg, getPlayerPerformanceVG(COMMAND[2]))  # PROCESS DATA RETURN and REPLACE MSG

        else:  # COMMAND is ILLEGAL for not being VALID
            await client.send_message(message.channel, "That isn't a command for **>VG**!\n**>VG** ~ *for a list of VG commands*")

    elif len(COMMAND) == 4:  # 4 PIECES to the COMMAND

        if str(COMMAND[1]) == "performance":  # >VG performance NAME DAYS

            if isinstance(COMMAND[3], int) == True:
                days = int(COMMAND[3])
                if days > 93:  # If DAYS is ILLEGAL for being to BIG set 93
                    days = 93

                if days <= 0:  # If DAYS is ILLEGAL for being to SMALL set 1
                    days = 1

                msg = await client.send_message(message.channel, "Looking at " + COMMAND[2] + " match history from the past " + str(days) + " days... :eyes:")  # Send MSG saying DATA is being PROCESSED
                await client.edit_message(msg, getPlayerPerformanceVG(COMMAND[2], days))  # PROCESS DATA RETURN and REPLACE MSG

            else:  # COMMAND is ILLEGAL for not being VALID
                await client.send_message(message.channel, "**" + str(COMMAND[3]) + "** *isn't a valid date span!*")  # SEND MSG

    else:  # COMMAND is ILLEGAL for not being VALID
        await client.send_message(message.channel, "That isn't a command for **>VG**!\n**>VG** ~ *for a list of VG commands*")  # SEND MSG

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
def getPlayerPerformanceVG(name, days=7, type=0):
    name = str(name)  # Convert NAME to STRING to prevent errors
    days = int(days)  # Convert DAYS to INT to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=days)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    try:
        matches = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]": 50, "filter[playerNames]": name})  # GET MATCHES

    except:
        return "Couldn't get any matches for **" + name + "** from the past " + str(days) + " days!"  # RETURN if player MATCHES AREN'T FOUND

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
        items = stats["items"]

        actor.append(attributes["actor"])
        assists.append(stats["assists"])
        crystalMineCaptures.append(stats["crystalMineCaptures"])
        deaths.append(stats["deaths"])
        farm.append(stats["farm"])
        goldMineCaptures.append(stats["goldMineCaptures"])
        # itemslist.append(stats["items"])

        for item in stats["items"]:
            itemslist.append(item)

        karmaLevel.append(stats["karmaLevel"])
        kills.append(stats["kills"])
        krakenCaptures.append(stats["krakenCaptures"])
        minionKills.append(stats["minionKills"])
        skillTier.append(stats["skillTier"])
        skinKey.append(stats["skinKey"])
        turretCaptures.append(stats["turretCaptures"])
        wentAfk.append(stats["wentAfk"])
        winner.append(stats["winner"])

        if num == size:
            level = stats["level"]
        num += 1

    print(itemslist)

    msg = "```"

    # Adding the TOP ACTORS used in the past X days to MSG
    actors = tools.giveListInOrderTOOL(actor)
    
    
    num = 0
    while num < 5:
        num += 1
        msg += "**" + str(num) + "** ~ *" + str(pretty(actors[num])) + "*\n"

    # Adding KILLS MEAN from the past X days to MSG
    msg += "\n**Kills per Game:** *" + str(tools.giveMeanOfList(kills)) + "*"

    # Adding ASSISTS MEAN from the past X days to MSG
    msg += "\n**Assists per Game:** *" + str(tools.giveMeanOfList(assists)) + "*"

    # Adding DEATHS MEAN from the past X days to MSG
    msg += "\n**Deaths per Game:** *" + str(tools.giveMeanOfList(deaths)) + "*"

    # Adding FARM MEAN from the past X days to MSG
    msg += "\n**Farm per Game:** *" + str(tools.giveMeanOfList(farm)) + "*"

    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"
    #
    # # Adding  MEAN from the past X days to MSG
    # msg += "\n**:** *" + str(tools.giveMeanOfList()) + "*"

    msg += "\n```"
    return msg
