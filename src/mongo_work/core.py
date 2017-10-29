import config
from pymongo import MongoClient, ASCENDING, DESCENDING
import datetime
import ast

client = MongoClient(config.mongo_host, config.mongo_port)  # Create a global instance of a mongo client


# Custom Functions
def dataBaseSize():
    """Get the database size."""

    try:

        msg = "```\n"
        for db in client.database_names():
            # Get db stats
            data = client[db].command("dbstats")

            # FOR DEBUGGING
            # print(str(db).upper() + " DATA: " + str(data))

            # Add info to msg
            msg += str(db) + " - Total Objects: " + str(data["objects"]) + " - Total Size: " + str(round((data["dataSize"] + data["storageSize"] + data["indexSize"]) / 1073741824, 3)) + " GB\n"

        msg += "```"

        # FOR DEBUGGING
        # print("MSG: " + msg)

        # Return msg
        return msg

    except Exception as e:
        print("!!!ERROR WHILE CALCULATING SIZE OF DATA BASE!!!\n" + str(e))


def getFromMongo(db_name, db_collection, db_filter):
    """Get data from Mongo DB.

    :argument db_name: Name of the data base.
    :argument db_collection: Name of the collection.
    :argument db_filter: Filter to fetch data with.
    :returns: A dict of the requested data.

    """

    try:

        # Convert the string to a dict
        if db_filter != "":
            db_filter = ast.literal_eval(db_filter)

        db = client[db_name]

        results = db[db_collection].find(db_filter)

        if results.count() == 0:
            return {"error": "nothing was found", "db_name": db_name, "db_collection": db_collection, "db_filter": db_filter}

        finalResult = []
        for result in results:
            finalResult.append(result)

        # Return msg
        return finalResult

    except Exception as e:
        print("!!!ERROR WHILE CALCULATING SIZE OF DATA BASE!!!\n" + str(e))


# General Functions
# Mongo Discord Server Functions <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def addDiscordServer(server_id, safe=True):
    """Add a server to the discord servers database.

    :parameter server_id: ID of discord server
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if serve was successfully added; False if server wasn't added

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        if safe == True:
            # Check if this server is already in the database
            if db["servers"].find({"_id": str(server_id)}).limit(1).count() > 0:
                return True

        # Server structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"_id": str(server_id), "general": {"prefix": str(config.default_prefix), "language": "english", "notify": True, "notifyOwner": False, "botChannel": False, "commandBans": [], "customCommands": {}, "memberJoin": {}, "memberLeave": {}}, "vaingloryRelated": {"compact": False, "emojis": True, "defaultRegion": "na", "guildName": None, "guildTag": None, "teamName": None, "teamTag": None}, "tournamentRelated": {"defaultGame": "vainglory", "data": []}}

        # Add server to database
        db["servers"].insert_one(structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING DISCORD SERVER " + str(server_id).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def removeDiscordServer(server_id, safe=True):
    """Remove a server from the discord servers database.

    :parameter server_id: ID of discord server
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if server was successfully removed; False, if server wasn't removed.

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        if safe == True:
            # Check if this server is not in the database
            if db["servers"].find({"_id": str(server_id)}).limit(1).count() == 0:
                return True

        db["servers"].remove({"_id": str(server_id)})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING DISCORD SERVER " + str(server_id).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateDiscordServer(server_id, update, safe=True, mode="$set"):
    """Update a discord servers data.

    :parameter server_id: ID of the discord server to update.
    :parameter update: What will be updated; as a dictionary.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :parameter mode: The type of update; Default: $set; Options: $set, $inc, $mul, $rename, $setOnInsert, $unset, $min, $max
    :returns: True, if data was updated successfully; False, if server data wasn't updated.

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        if safe == True:
            # Check if this server is not in the database
            if db["servers"].find({"_id": str(server_id)}).limit(1).count() == 0:
                if addDiscordServer(server_id, False) == False:
                    return False

        # # Checks if the update is to sub data
        # if section == "" or section == None or section == False:
        #     db["servers"].update_one({"_id": str(server_id)}, {"$set": {str(key): value}})
        #
        # else:
        #     db["servers"].update_one({"_id": str(server_id)}, {"$set": {str(section) + "." + str(key): value}})

        db["servers"].update_one({"_id": str(server_id)}, {mode: update})

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD SERVER " + str(server_id).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateDiscordServerArray(server_id, update, function="add", safe=True):
    """Update a servers array data.

    :parameter server_id: ID of the discord server to update.
    :parameter update: What will be updated; as a dictionary.
    :parameter function: Add, to add to an array; Remove, from an array
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if data was successfully added/removed; False, if data wasn't added/removed.

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        if safe == True:
            # Check if this server is not in the database
            if db["servers"].find({"_id": str(server_id)}).limit(1).count() == 0:
                if addDiscordServer(server_id, False) == True:
                    return False

        # Checks if the update is to sub data
        if function == "add":
            db["servers"].update_one({"_id": str(server_id)}, {"$addToSet": update})

        else:
            db["servers"].update_one({"_id": str(server_id)}, {"$pullAll": update})

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD SERVER " + str(server_id).upper() + " ARRAY!!!\nEXCEPTION:\n" + str(e))
        return False


def checkDiscordServers(db_filter={}):
    """Check if something exist in the discord servers db.

    :parameter db_filter: Filter to find data with.
    :returns: True, if data was found; False, if data wasn't found.

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        # Check if data looking for is in the discord users db
        if db["servers"].find(db_filter).limit(1).count() > 0:
            return True

        else:
            return False

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD SERVERS " + str(db_filter).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def discordServerDictionary(server_id):
    """Fetches a servers data.

    :parameter server_id: ID of the discord server to fetch for.
    :returns: Dictionary of server data.

    """

    try:

        # Connect to the correct discord database
        db = client["discord" + str(config.mongo_version)]

        # Check if this server is not in the database
        if db["servers"].find({"_id": str(server_id)}).limit(1).count() == 0:
            return False

        server = db["servers"].find_one({"_id": str(server_id)})

        # FOR DEBUGGING
        # print("SERVER:   " + str(server))

        return server

    except Exception as e:
        print("!!!ERROR WHILE FETCHING DISCORD SERVER " + str(server_id).upper() + " DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


def getDiscordServers(db_filter={}):
    """Fetches server data, with a filter, and put's it in a cursor object.

    :parameter db_filter: Filter to search data by.
    :returns: Cursor, object full of server data; False, on error/if nothing was found

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        users = db["servers"].find(db_filter)

        # Check if anything was found
        if users.count() == 0:
            return False

        # FOR DEBUGGING
        # print("SERVERS CURSOR OBJECT:   " + str(users))
        # for user in users:
        #     print("SERVER IN USERS: " + str(user))

        return users

    except Exception as e:
        print("!!!ERROR WHILE FETCHING DISCORD SERVERS BY " + str(db_filter) + " DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


# Mongo Discord User Functions <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def addDiscordUser(user_id, safe=True):
    """Add a user to the discord users database.

    :parameter user_id: ID of the Discord user.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if user was successfully added; False if user wasn't added.

    """

    try:

        # Connect to the main discord database
        db = client["discord" + str(config.mongo_version)]

        if safe == True:
            # Check if this user is already in the database
            if db["users"].find({"_id": str(user_id)}).limit(1).count() > 0:
                return True

        # User structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"_id": str(user_id), "general": {"language": "english"}, "vaingloryRelated": {"compact": False, "emojis": True, "quickName": None, "quickRegion": None, "quickGuildName": None, "quickTeamName": None, "verified": False, "verifiedName": None, "verifiedRegion": None, "canCreate": True, "playerProfile": {}, "guildProfile": {}, "teamProfile": {}}, "tournamentRelated": {"tournamentsIn": []}}

        # Add user to database
        db["users"].insert_one(structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING DISCORD USER " + str(user_id).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def removeDiscordUser(user_id, safe=True):
    """Remove a user from the discord users database.

    :parameter user_id: ID of discord user
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if user was successfully removed; False, if user wasn't removed.

    """

    try:

        # Connect to the main discord database
        db = client["discord" + str(config.mongo_version)]

        if safe == True:
            # Check if this user is not in the database
            if db["users"].find({"_id": str(user_id)}).limit(1).count() == 0:
                return True

        db["users"].remove({"_id": str(user_id)})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING DISCORD USER " + str(user_id).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateDiscordUser(user_id, update, safe=True, mode="$set"):
    """Update discord user data.

    :parameter user_id: ID of the Discord user.
    :parameter update: What's going to be updated.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :parameter mode: The type of update; Default: $set; Options: $set, $inc, $mul, $rename, $setOnInsert, $unset, $min, $max
    :returns: True, if data was updated successfully; False, if user data wasn't updated.

    """

    try:

        # Connect to the main discord database
        db = client["discord" + str(config.mongo_version)]

        if safe == True:
            # Check if this user is not in the database
            if db["users"].find({"_id": str(user_id)}).limit(1).count() == 0:
                if addDiscordUser(user_id, False) == False:
                    return False

        db["users"].update_one({"_id": str(user_id)}, {mode: update})

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD USER " + str(user_id).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateDiscordUserWith(db_filter, update, safe=True, mode="$set"):
    """Update discord user data.

    :parameter db_filter: Filter to find data with.
    :parameter update: What's going to be updated.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :parameter mode: The type of update; Default: $set; Options: $set, $inc, $mul, $rename, $setOnInsert, $unset, $min, $max
    :returns: True, if data was updated successfully; False, if user data wasn't updated.

    """

    try:

        # Connect to the main discord database
        db = client["discord" + str(config.mongo_version)]

        if safe == True:
            # Check if this user is not in the database
            if db["users"].find(db_filter).limit(1).count() == 0:
                return False

        db["users"].update_one(db_filter, {mode: update})

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD USER WITH THE FOLLOWING " + str(db_filter) + "!!!\nEXCEPTION:\n" + str(e))
        return False


def checkDiscordUsers(db_filter={}):
    """Check if something exist in the discord users db.

    :parameter db_filter: Filter to find data with.
    :returns: True, if data was found; False, if data wasn't found.

    """

    try:

        # Connect to the main discord database
        db = client["discord" + str(config.mongo_version)]

        # Check if data looking for is in the discord users db
        if db["users"].find(db_filter).limit(1).count() > 0:
            return True

        else:
            return False

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD USER " + str(db_filter).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateDiscordUsersArray(user_id, update, function="add", safe=True):
    """Update a servers array data.

    :parameter user_id: ID of the discord user to update.
    :parameter update: What will be updated; as a dictionary.
    :parameter function: Add, to add to an array; Remove, from an array
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if data was successfully added/removed; False, if data wasn't added/removed.

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        if safe == True:
            # Check if this server is not in the database
            if db["users"].find({"_id": str(user_id)}).limit(1).count() == 0:
                if addDiscordServer(user_id, False) == True:
                    return False

        # Checks if the update is to sub data
        if function == "add":
            db["servers"].update_one({"_id": str(user_id)}, {"$addToSet": update})

        else:
            db["servers"].update_one({"_id": str(user_id)}, {"$pullAll": update})

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING DISCORD SERVER " + str(user_id).upper() + " ARRAY!!!\nEXCEPTION:\n" + str(e))
        return False


def discordUserDictionary(user_id):
    """Fetches the user data and put's it in a dict.

    :parameter user_id: ID of the discord user
    :returns: Dictionary full of user data

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        # Check if this user is not in the database
        if db["users"].find({"_id": str(user_id)}).limit(1).count() == 0:
            return False

        user = db["users"].find_one({"_id": str(user_id)})

        # FOR DEBUGGING
        # print("USER DICTIONARY:   " + str(user))

        return user

    except Exception as e:
        print("!!!ERROR WHILE FETCHING DISCORD USER " + str(user_id).upper() + " DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


def getDiscordUsers(db_filter={}):
    """Fetches users data, with a filter, and put's it in a cursor object.

    :parameter db_filter: Filter to search data by.
    :returns: Cursor, object full of user data; False, on error/if nothing was found

    """

    try:

        db = client["discord" + str(config.mongo_version)]  # Connect to the main discord database

        users = db["users"].find(db_filter)

        # Check if anything was found
        if users.count() == 0:
            return False

        # FOR DEBUGGING
        # print("USERS CURSOR OBJECT:   " + str(users))
        # for user in users:
        #     print("USER IN USERS: " + str(user))

        return users

    except Exception as e:
        print("!!!ERROR WHILE FETCHING DISCORD USERS BY " + str(db_filter) + " DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


# Mongo Vainglory Match Data Functions <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def addVgMatchData(player_name, player_region, game_mode, data, safe=True):
    """Add match data to the vainglory_work database.

    :parameter player_name: Name of player; data's owner.
    :parameter player_region: Region to store to.
    :parameter game_mode: Game mode to store to.
    :parameter data: Data to store.
    :parameter safe: True, checks to see if adding is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully added; False if vgData wasn't added.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(game_mode).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG MATCH DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is already in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() > 0:
                # Instead of adding update the data with current data
                return updateVgMatchData(player_name, player_region, game_mode, data, False)

        # FOR DEBUGGING
        # print("LAST API UPDATE: " + data[0]["createdAt"])

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"_id": str(player_name), "lastUpdate": str(datetime.datetime.now()), "lastUpdateApi": data[0]["createdAt"], "data": data}

        # Add vgData
        db[collection].insert_one(structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING VG MATCH DATA OF " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def removeVgMatchData(player_name, player_region, game_mode, safe=True):
    """Remove a players match data from the vainglory_work database.

    :parameter player_name: Name of player; data's owner.
    :parameter player_region: Region to remove to.
    :parameter game_mode: Game mode to remove to.
    :parameter safe: True, checks to see if removing is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully removed; False, if vgData wasn't removed.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(game_mode).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG MATCH DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return False

        # Remove data
        db[collection].remove({"_id": str(player_name)})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING VG MATCH DATA FOR " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateVgMatchData(player_name, player_region, game_mode, data, safe=True):
    """Update a players match data.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region to update to
    :parameter game_mode: Game mode to update to
    :parameter data: Data to update with
    :parameter safe: True, checks to see if updating is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(game_mode).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG MATCH DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return addVgMatchData(player_name, player_region, game_mode, data, False)

        # FOR DEBUGGING
        # print("LAST API UPDATE: " + data[0]["createdAt"])

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"lastUpdate": str(datetime.datetime.now()), "lastUpdateApi": data[0]["createdAt"], "data": data}

        # Replace with new data
        db[collection].replace_one({"_id": str(player_name)}, structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING VG MATCH DATA FROM " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def vgMatchDataDictionary(player_name, player_region, game_mode, safe=True):
    """Fetches the players match data and put's it into a dict.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region to fetch from
    :parameter game_mode: Game mode to fetch from
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: Dictionary full of match data

    """

    try:

        # Connect to the main vainglory_work database
        db = client["vainglory" + str(config.mongo_version)]

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(game_mode).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG MATCH DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return False

        match = db[collection].find_one({"_id": str(player_name)})

        # FOR DEBUGGING
        # print("MATCH DICTIONARY:   " + str(match))

        return match

    except Exception as e:
        print("!!!ERROR WHILE FETCHING VG MATCH DATA FROM " + str(player_name).upper() + " DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


def checkVgMatchData(player_name, player_region, game_mode, valid=4, safe=True):
    """Checks vg match database to see if we have any valid match data.

    :parameter player_name: Name of player; data's owner.
    :parameter player_region: Region to fetch from.
    :parameter game_mode: Game mode to fetch from.
    :parameter valid: Time frame, in minutes, where data is relevant.
    :parameter safe: True, checks to see if check is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: A dictionary with the following responds: found: if data was found in db, valid: if data found is valid, data: the data found.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(game_mode).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG MATCH DATA:   " + str(collection))

        data = db[collection].find_one({"_id": str(player_name)})

        # Check if this vgData is not in the database
        if data == None:
            # FOR DEBUGGING
            # print("VG MATCH DATA FOUND:   False")

            # Data in db is no good
            return {"found": False, "valid": False, "data": None}

        then = datetime.datetime.strptime(str(data["lastUpdate"]), "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.datetime.now()

        difference = (now - then).seconds / 60

        # FOR DEBUGGING
        # print("DIFFERENCE: " + str(difference) + " |VALID: " + str(valid))

        # Checks if the last update has past the relevance window
        if difference > valid:
            # FOR DEBUGGING
            # print("VG MATCH DATA FOUND:   False")

            # Data in db is no good
            return {"found": True, "valid": False, "data": data["data"]}

        # FOR DEBUGGING
        # print("VG MATCH DATA FOUND:   True\nLAST UPDATE:   " + str(then) + "\nNOW:   " + str(now) + "\nTIME DIFFERENCE:   " + str(difference) + "\nVALID TIME WINDOW:   " + str(valid) + "\nIS RELEVANT:   True")

        # Data in db is good
        return {"found": True, "valid": True, "data": data["data"]}

    except Exception as e:
        print("!!!ERROR WHILE CHECKING FOR VG MATCH DATA FOR " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


# Mongo Vainglory Match Data Functions <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def addVgPlayerData(player_name, player_region, data, safe=True):
    """Add a player's data to the vaingloryMain database.

    :parameter player_name: Name of player; data's owner.
    :parameter player_region: Region to store to.
    :parameter data: Data to store.
    :parameter safe: True, checks to see if adding is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully added; False if vgData wasn't added.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + "Players")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG PLAYER DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is already in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() > 0:
                # Instead of adding update the data with current data
                return updateVgPlayerData(player_name, player_region, data, False)

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"_id": str(player_name), "lastUpdate": str(datetime.datetime.now()), "lastUpdateApi": data["createdAt"], "data": data}

        # Add vgData
        db[collection].insert_one(structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING VG PLAYER DATA OF " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def removeVgPlayerData(player_name, player_region, safe=True):
    """Remove a players data from the vaingloryMain database.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region to remove to
    :parameter safe: True, checks to see if removing is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was successfully removed; False, if vgData wasn't removed.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + "Players")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG PLAYER DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return False

        # Remove data
        db[collection].remove({"_id": str(player_name)})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING VG PLAYER DATA FOR " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def updateVgPlayerData(player_name, player_region, data, safe=True):
    """Update a players data.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region to update to
    :parameter data: Data to update with
    :parameter safe: True, checks to see if updating is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + "Players")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG PLAYER DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return addVgPlayerData(player_name, player_region, data, False)

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"lastUpdate": str(datetime.datetime.now()), "lastUpdateApi": data["createdAt"], "data": data}

        # Replace with new data
        db[collection].replace_one({"_id": str(player_name)}, structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING VG MATCH DATA FROM " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def vgPlayerDataDictionary(player_name, player_region, safe=True):
    """Fetches the players data and put's it into a dict.

    :parameter player_name: Name of player; data's owner.
    :parameter player_region: Region to fetch from.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: Dictionary full of data.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + "Players")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG PLAYER DATA:   " + str(collection))

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return False

        player = db[collection].find_one({"_id": str(player_name)})

        # FOR DEBUGGING
        # print("PLAYER DICTIONARY:   " + str(player))

        return player

    except Exception as e:
        print("!!!ERROR WHILE FETCHING VG PLAYER DATA FROM " + str(player_name).upper() + " DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


def checkVgPlayerData(player_name, player_region, valid=4, safe=True):
    """Checks vg player database to see if we have any valid player data.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region to fetch from
    :parameter valid: Time frame, in minutes, where data is relevant
    :parameter safe: True, checks to see if check is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: A dictionary with the following responds: found: if data was found in db, valid: if data found is valid, data: the data found.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + "Players")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG PLAYER DATA:   " + str(collection))

        data = db[collection].find_one({"_id": str(player_name)})

        # Check if this vgData is not in the database
        if data == None:
            # FOR DEBUGGING
            # print("VG PLAYER DATA FOUND:   False")
            return {"found": False, "valid": False, "data": None}

        then = datetime.datetime.strptime(str(data["lastUpdate"]), "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.datetime.now()

        difference = (now - then).seconds / 60

        # Checks if the last update has past the relevance window
        if difference > valid:
            return {"found": True, "valid": False, "data": data["data"]}

        # FOR DEBUGGING
        # print("VG PLAYER DATA FOUND:   True\nLAST UPDATE:   " + str(then) + "\nNOW:   " + str(now) + "\nTIME DIFFERENCE:   " + str(difference) + "\nVALID TIME WINDOW:   " + str(valid) + "\nIS RELEVANT:   True")

        return {"found": True, "valid": True, "data": data["data"]}

    except Exception as e:
        print("!!!ERROR WHILE CHECKING FOR VG PLAYER DATA FOR " + str(player_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


# Mongo Vainglory Leader Boards Functions <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def addToVgLeaderBoards(player_name, player_region, leader_board, score, safe=True):
    """Add players data to the vainglory_work leader board.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region of the player; global, na, eu, sg, ea, sa
    :parameter leader_board: Leader board to add to; Camel case sensitive, no blank spaces
    :parameter score: Score to store
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was successfully added; False if vgData wasn't added

    """

    try:

        db = client["vaingloryLeaderBoards" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(leader_board).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        player_name = str(player_name).replace(" ", "_")

        # FOR DEBUGGING
        # print("PLAYER NAME:   " + str(player_name))

        if safe == True:
            # Check if this vgData is already in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() > 0:
                # Instead of adding update the data with current data
                return setVgLeaderBoard(player_name, player_region, leader_board, score, False)

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"_id": player_name, "score": float(score)}

        # Add vgData
        db[collection].insert_one(structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING " + str(player_name).upper() + " TO VG " + str(leader_board) + " LEADER BOARD!!!\nEXCEPTION:\n" + str(e))
        return False


def removeFromVgLeaderBoards(player_name, player_region, leader_board, safe=True):
    """Remove a players score board data from the vainglory_work database.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region of the player; global, na, eu, sg, ea, sa
    :parameter leader_board: Leader board to add to; Camel case sensitive, no blank spaces
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was successfully removed; False, if vgData wasn't removed.

    """

    try:

        db = client["vaingloryLeaderBoards" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(leader_board).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        player_name = str(player_name).replace(" ", "_")

        # FOR DEBUGGING
        # print("PLAYER NAME:   " + player_name)

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return False

        # Remove data
        db[collection].remove({"_id": str(player_name)})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING " + str(player_name).upper() + " FROM VG " + str(leader_board).upper() + " LEADER BOARD!!!\nEXCEPTION:\n" + str(e))
        return False


def setVgLeaderBoard(player_name, player_region, leader_board, score, safe=True):
    """Set a players score board data.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region of the player; global, na, eu, sg, ea, sa
    :parameter leader_board: Leader board to update to
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vaingloryLeaderBoards" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(leader_board).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        player_name = str(player_name).replace(" ", "_")

        # FOR DEBUGGING
        # print("PLAYER NAME:   " + player_name)

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return addToVgLeaderBoards(player_name, player_region, leader_board, score, False)

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"score": score}

        # Replace with new data
        db[collection].replace_one({"_id": str(player_name)}, structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING " + str(player_name).upper() + " IN VG " + str(leader_board).upper() + " LEADER BOARD!!!\nEXCEPTION:\n" + str(e))
        return False


def updateVgLeaderBoard(player_name, player_region, leader_board, score, ifIs="greater", safe=True):
    """Update a players score board data, if the value that's going to update is greater or less then the current value.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region of the player; global, na, eu, sg, ea, sa
    :parameter leader_board: Leader board to update to
    :parameter score: Score to update with.
    :parameter ifIs: Greater, when you want to update only if greater; Smaller, when you want to update only if less.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vaingloryLeaderBoards" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(leader_board).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        player_name = str(player_name).replace(" ", "_")

        # FOR DEBUGGING
        # print("PLAYER NAME:   " + player_name)

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
                return addToVgLeaderBoards(player_name, player_region, leader_board, score, False)

        # Update with new data
        if ifIs == "greater":
            db[collection].update_one({"_id": str(player_name)}, {"$max": {"score": score}})

        elif ifIs == "smaller":
            db[collection].update_one({"_id": str(player_name)}, {"$min": {"score": score}})

        else:
            return False

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING " + str(player_name).upper() + " IN VG " + str(leader_board).upper() + " LEADER BOARD!!!\nEXCEPTION:\n" + str(e))
        return False


def vgLeaderBoardDictionary(player_name, player_region, leader_board, sort="ascending"):
    """Fetches a leader board in a dict and returns it.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region of the player; global, na, eu, sg, ea, sa
    :parameter leader_board: Leader board to update to
    :parameter sort: How to sort the leader board; ascending, descending or null
    :returns: List; index 0, dict of all the players; index 1, data of player

    """

    try:

        db = client["vaingloryLeaderBoards" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(leader_board).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        ign = player_name
        player_name = str(player_name).replace(" ", "_")

        # FOR DEBUGGING
        # print("PLAYER NAME:   " + player_name)

        if sort == "ascending":
            leaderboard = (db[collection].find().sort("score", ASCENDING))
        elif sort == "descending":
            leaderboard = (db[collection].find().sort("score", DESCENDING))

        else:
            leaderboard = (db[collection].find().sort("score", ASCENDING))

        if sort == "ascending":
            player = db[collection].find({"_id": str(player_name)}).sort("score", ASCENDING)

        elif sort == "descending":
            player = db[collection].find({"_id": str(player_name)}).sort("score", DESCENDING)

        else:
            player = db[collection].find({"_id": str(player_name)}).sort("score", ASCENDING)

        # FOR DEBUGGING
        # print("!!!GOT PLAYER!!!")

        if player.count() == 0:

            # FOR DEBUGGING
            # print("!!!PLAYER NOT FOUND IN LEADER BOARDS!!!")

            player = {"_id": ign, "score": "Unknown"}

        else:

            # FOR DEBUGGING
            # print("!!!PLAYER FOUND!!!")

            player = player[0]

        result = [leaderboard, player]

        # FOR DEBUGGING
        # print("LARBOARD DICTIONARY:   " + str(leaderboard))

        return result

    except Exception as e:
        print("!!!ERROR WHILE FETCHING " + str(player_name).upper() + " VG LEADER BOARD DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


def vgUserLeaderBoardDictionary(player_name, player_region, leader_board):
    """Fetches the players leader board data and put's it into a dict.

    :parameter player_name: Name of player; data's owner
    :parameter player_region: Region of the player; global, na, eu, sg, ea, sa
    :parameter leader_board: Leader board to update to
    :returns: Dictionary full of players leader board data

    """

    try:

        db = client["vaingloryLeaderBoards" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = (str(player_region).lower() + str(leader_board).title()).replace(" ", "")

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        player_name = str(player_name).replace(" ", "_")

        # FOR DEBUGGING
        # print("PLAYER NAME:   " + player_name)

        # Check if this vgData is not in the database
        if db[collection].find({"_id": str(player_name)}).limit(1).count() == 0:
            return False

        leaderboard = db[collection].find_one({"_id": str(player_name)})

        # FOR DEBUGGING
        # print("LEADER BOARD DICTIONARY:   " + str(leaderboard))

        return leaderboard

    except Exception as e:
        print("!!!ERROR WHILE FETCHING " + str(player_name).upper() + " VG LEADER BOARD DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


# Mongo Vainglory Heroes Functions <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def addVgHero(hero_name, safe=True):
    """Add a hero to the VainGlory db.

    :parameter hero_name: Name of the hero
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was successfully added; False if vgData wasn't added

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        if safe == True:
            # Check if this vgData is already in the database
            if db[collection].find({"_id": str(hero_name)}).limit(1).count() > 0:
                # Instead of adding set the data with current data
                return setVgHero(hero_name, safe=False)

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"_id": hero_name, "totalWins": 0, "totalLosses": 0, "totalKills": 0, "totalDeaths": 0, "totalAssists": 0, "totalMinionKills": 0, "totalFarm": 0, "totalGold": 0, "totalTurrets": 0, "totalGoldMiners": 0, "totalCrystalMiners": 0, "totalKrakens": 0, "items": {}, "heroes": {}}

        # Add vgData
        db[collection].insert_one(structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING " + str(hero_name).upper() + " TO VG HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def removeVgHero(hero_name, safe=True):
    """Remove a hero from the VainGlory db.

    :parameter hero_name: Name of hero
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was successfully removed; False, if vgData wasn't removed.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": hero_name}).limit(1).count() == 0:
                return False

        # Remove data
        db[collection].remove({"_id": hero_name})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING " + str(hero_name).upper() + " FROM VG HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def setVgHero(hero_name, totalWins=0, totalLosses=0, totalDeaths=0, totalKills=0, totalAssists=0, totalMinionKills=0, totalFarm=0, totalGold=0, totalTurrets=0, totalGoldMiners=0, totalCrystalMiners=0, totalKrakens=0, items={}, heroes={}, safe=True):
    """Set a players score board data.

    :parameter hero_name: Name of player; data's owner
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": hero_name}).limit(1).count() == 0:
                return addVgHero(hero_name, safe=False)

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"totalWins": totalWins, "totalLosses": totalLosses, "totalKills": totalKills, "totalDeaths": totalDeaths, "totalAssists": totalAssists, "totalMinionKills": totalMinionKills, "totalFarm": totalFarm, "totalGold": totalGold, "totalTurrets": totalTurrets, "totalGoldMiners": totalGoldMiners, "totalCrystalMiners": totalCrystalMiners, "totalKrakens": totalKrakens, "items": items, "heroes": heroes}

        # Replace with new data
        db[collection].replace_one({"_id": hero_name}, structure)

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING " + str(hero_name).upper() + " IN VG HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def updateVgHero(hero_name, key, value=1, updateAs="add", safe=True):
    """Update a heroes keys accordingly.

    :parameter hero_name: Name of hero.
    :parameter key: Key to update.
    :parameter value: Value to update Key with.
    :parameter updateAs: How date should be updated; add, add to the current data; sub, subtract to the current data; set, set the data to value.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        if safe == True:
            # Check if this vgData is not in the database
            if db[collection].find({"_id": hero_name}).limit(1).count() == 0:
                result = addVgHero(hero_name, safe=False)
                if result == False:
                    return False

        # FOR DEBUGGING
        # print("UPDATING AS: " + str(updateAs))

        # Update with new data
        if updateAs == "set":
            # FOR DEBUGGING
            # print("UPDATED AS: " + updateAs)
            db[collection].update({"_id": hero_name}, {"$set": {key: value}})

        elif updateAs in ["add", "sub"]:
            # FOR DEBUGGING
            # print("UPDATED AS: " + updateAs)
            db[collection].update({"_id": hero_name}, {"$inc": {key: value}})

        else:
            return False

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING " + str(hero_name).upper() + " IN VG HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def vgHeroDictionary(hero_name):
    """Fetches a heroes data.

    :parameter hero_name: Name of player; data's owner
    :returns: Dictionary full of players leader board data

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        # Check if this vgData is not in the database
        if db[collection].find({"_id": hero_name}).limit(1).count() == 0:
            return False

        hero = db[collection].find_one({"_id": hero_name})

        # FOR DEBUGGING
        # print("HERO DICTIONARY:   " + str(hero))

        return hero

    except Exception as e:
        print("!!!ERROR WHILE FETCHING " + str(hero_name).upper() + " VG HERO DICTIONARY!!!\nEXCEPTION:\n" + str(e))
        return False


def getFromVgHero(hero_name, key, safe=True):
    """Get a value from vg leader boards.

    :parameter hero_name: Name of player.
    :parameter key: Value you wanna fetch for.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: Returns the asked for value; False, if retrieve wasn't possible

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG LEADER BOARD:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        if safe == True:
            # Check if this player is not in the database
            if db[collection].find({"_id": hero_name}).limit(1).count() == 0:
                return False

        data = db[collection].find_one({"_id": hero_name}, {key: 1})

        # FOR DEBUGGING
        # print("FETCHED DATA IS:   " + str(data))

        return data

    except Exception as e:
        print("!!!ERROR WHILE FETCHING VG HERO FROM " + str(hero_name).upper() + "!!!\nEXCEPTION:\n" + str(e))
        return False


def addVgHeroSubHero(hero_name, sub_hero_name, safe=True):
    """Add a sub hero to a hero in the VainGlory db.

    :parameter hero_name: Name of the hero.
    :parameter sub_hero_name: Name of the sub hero.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully added; False if vgData wasn't added.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        sub_hero_name = str(sub_hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("SUB HERO NAME: " + sub_hero_name)

        if safe == True:
            # Check if this vgData is already in the database
            data = db[collection].find({"_id": str(hero_name)}).limit(1)
            if data.count() < 1:
                result = addVgHero(hero_name, safe=False)
                if result == False:
                    return False

            else:
                if str(sub_hero_name).lower() in data[0]["heroes"]:
                    return True

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"wins": 0, "losses": 0}

        # Add vgData
        db[collection].update({"_id":  str(hero_name)}, {"$set": {"heroes." + str(sub_hero_name).replace(" ", "_").lower(): structure}})

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING " + str(hero_name).upper() + " TO VG SUB HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def removeVgHeroSubHero(hero_name, sub_hero_name, safe=True):
    """Remove a hero from the VainGlory db.

    :parameter hero_name: Name of hero.
    :parameter sub_hero_name: Name of the sub hero.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully removed; False, if vgData wasn't removed.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        sub_hero_name = str(sub_hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("SUB HERO NAME: " + sub_hero_name)

        if safe == True:
            # Check if this vgData is already in the database
            data = db[collection].find({"_id": str(hero_name)}).limit(1)
            if data.count() < 1:
                return addVgHero(hero_name, safe=False)

            else:
                if sub_hero_name in data[0]["heroes"]:
                    return True

        # Remove data
        db[collection].update({"_id":  str(hero_name)}, {"$unset": {"heroes." + sub_hero_name: 1}})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING " + str(hero_name).upper() + " FROM VG SUB HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def updateVgHeroSubHero(hero_name, sub_hero_name, key, value, updateAs="add", safe=True):
    """Update a heroes keys accordingly.

    :parameter hero_name: Name of hero.
    :parameter sub_hero_name: Name of the sub hero.
    :parameter key: Key to update.
    :parameter value: Value to update Key with.
    :parameter updateAs: How date should be updated; add, add to the current data; sub, subtract to the current data; set, set the data to value.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROES:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        sub_hero_name = str(sub_hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("SUB HERO NAME: " + sub_hero_name)

        if safe == True:
            # Check if this vgData is not in the database
            data = db[collection].find({"_id": str(hero_name)}).limit(1)
            if data.count() < 1:
                result = addVgHero(hero_name, safe=False)
                if result == False:
                    return False

                result = addVgHeroSubHero(hero_name, sub_hero_name, safe=False)
                if result == False:
                    return False
            else:
                if sub_hero_name not in data[0]["heroes"]:
                    result = addVgHeroSubHero(hero_name, sub_hero_name, safe=False)
                    if result == False:
                        return False

        # Update with new data
        if updateAs == "set":
            db[collection].update({"_id": str(hero_name)}, {"$set": {"heroes." + sub_hero_name + "." + str(key): value}})

        elif updateAs in ["add", "sub"]:
            db[collection].update({"_id": str(hero_name)}, {"$inc": {"heroes." + sub_hero_name + "." + str(key): value}})

        else:
            return False

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING " + str(hero_name).upper() + " IN VG SUB HEROES!!!\nEXCEPTION:\n" + str(e))
        return False


def addVgHeroItem(hero_name, item_name, safe=True):
    """Add a item to a hero in the VainGlory db.

    :parameter hero_name: Name of the hero.
    :parameter item_name: Name of the item.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully added; False if vgData wasn't added.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HERO ITEMS:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        item_name = str(item_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("ITEM NAME: " + item_name)

        if safe == True:
            # Check if this vgData is already in the database
            data = db[collection].find({"_id": hero_name}).limit(1)
            if data.count() < 1:
                result = addVgHero(hero_name, safe=False)
                if result == False:
                    return False

            else:
                if item_name in data[0]["items"]:
                    return True

        # vgData structure !!!UPDATE THIS WHEN EDITING STRUCTURE!!!
        structure = {"wins": 0, "losses": 0}

        # Add vgData
        db[collection].update({"_id":  hero_name}, {"$set": {"items." + item_name: structure}})

        return True

    except Exception as e:
        print("!!!ERROR WHILE ADDING " + str(hero_name).upper() + " TO VG HERO ITEMS!!!\nEXCEPTION:\n" + str(e))
        return False


def removeVgHeroItem(hero_name, item_name, safe=True):
    """Remove a hero from the VainGlory db.

    :parameter hero_name: Name of hero.
    :parameter item_name: Name of the item.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was successfully removed; False, if vgData wasn't removed.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HERO ITEMS:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        # Clean up item name
        item_name = str(item_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("ITEM NAME: " + item_name)

        if safe == True:
            # Check if this vgData is already in the database
            data = db[collection].find({"_id": hero_name}).limit(1)
            if data.count() < 1:
                result = addVgHero(hero_name, safe=False)
                if result == False:
                    return False

            else:
                if item_name not in data[0]["items"]:
                    return True

        # Remove data
        db[collection].update({"_id":  hero_name}, {"$unset": {"items." + item_name: 1}})

        return True

    except Exception as e:
        print("!!!ERROR WHILE REMOVING " + str(hero_name).upper() + " FROM VG HERO ITEMS!!!\nEXCEPTION:\n" + str(e))
        return False


def updateVgHeroItem(hero_name, item_name, key, value=1, updateAs="add", safe=True):
    """Update a heroes item keys accordingly.

    :parameter hero_name: Name of hero.
    :parameter item_name: Name of the item.
    :parameter key: Key to update.
    :parameter value: Value to update Key with.
    :parameter updateAs: How date should be updated; add, add to the current data; sub, subtract to the current data; set, set the data to value.
    :parameter safe: True, checks to see if fetching is possible takes a little bit more time; False, doesn't check anything just updates.
    :returns: True, if vgData was updated successfully; False, if vgData data wasn't updated.

    """

    try:

        db = client["vainglory" + str(config.mongo_version)]  # Connect to the main vainglory_work database

        # Choose the correct collection accordingly
        collection = "heroes"

        # FOR DEBUGGING
        # print("COLLECTION NAME FOR VG HEROE ITEMS:   " + str(collection))

        hero_name = str(hero_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("HERO NAME: " + hero_name)

        # Clean up item name
        item_name = str(item_name).replace(" ", "_").lower()

        # FOR DEBUGGING
        # print("ITEM NAME: " + item_name)

        if safe == True:
            # Check if this vgData is not in the database
            data = db[collection].find({"_id": hero_name}).limit(1)
            if data.count() < 1:
                result = addVgHero(hero_name, safe=False)
                if result == False:
                    return False

                result = addVgHeroItem(hero_name, item_name, safe=False)
                if result == False:
                    return False
            else:
                if item_name not in data[0]["items"]:
                    result = addVgHeroItem(hero_name, item_name, safe=False)
                    if result == False:
                        return False

        # FOR DEBUGGING
        # print("UPDATE TYPE:" + str(updateAs))

        # Update with new data
        if updateAs == "set":
            # FOR DEBUGGING
            # print("UPDATE AS: " + updateAs)

            db[collection].update({"_id": hero_name}, {"$set": {"items." + item_name + "." + str(key): value}})

        elif updateAs in ["add", "sub"]:
            # FOR DEBUGGING
            # print("UPDATE AS: " + updateAs)

            db[collection].update({"_id": hero_name}, {"$inc": {"items." + item_name + "." + str(key): value}})

        else:
            return False

        return True

    except Exception as e:
        print("!!!ERROR WHILE UPDATING " + str(hero_name).upper() + " IN VG HERO ITEMS!!!\nEXCEPTION:\n" + str(e))
        return False
