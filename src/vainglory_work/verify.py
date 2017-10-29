"""
Verify users through unique item patterns.
"""

import random
from src.vainglory_work import core
from src.mongo_work import core as db

temp = {}


def itemPattern():
    """Gives an item pattern."""

    # Where the pattern is going to be stored
    pattern = []

    # Generate a random pattern of items.
    # Items using and there value:
    # 0 = Halcyon Potion
    # 1 = Weapon Infusion
    # 2 = Crystal Infusion
    for num in range(0, 5):
        pattern.append(random.randrange(0, 3))  # random from 0,1,2

    return pattern


def check(ign, pattern, matches):
    """Check if the latest match, of a list of matches, shows the pattern given."""

    # Get the latest match from the list of matches
    match = matches[0]

    # Get the players actor and side
    for roster in match['rosters']:
        for participant in roster['participants']:
            if participant['player']['name'] == ign:
                actor = participant['actor']

                if roster['side'] == 'left/blue':
                    side = 'Left'

                else:
                    side = 'Right'

                # We got what we wanted so break
                break

    # Get the matches telemetry data
    match = core.getTelemetry(match["telemetry"]["URL"])

    # List of items found
    items = []
    for event in match:
        if len(items) == 5:
            break

        # Find the first, 5 max, items bought by the player
        if event['type'] == 'BuyItem' and event['payload']['Team'] == side and event['payload']['Actor'] == actor:
            items.append(event['payload']['Item'])

    for event in items:

        if event == 'Halcyon Potion':
            items[items.index(event)] = 0  # Converts Halcyon Potion to 0

        elif event == 'Weapon Infusion':
            items[items.index(event)] = 1  # Converts Halcyon Potion to 1

        elif event == 'Crystal Infusion':
            items[items.index(event)] = 2  # Converts Halcyon Potion to 2

        else:
            pass  # Bought something else

    try:

        sorted(items, key=int)

    except:
        # FOR DEBUGGING
        print("ITEMS: " + str(items))

        return False

    # So that order doesn't matter
    if sorted(items, key=int) == sorted(pattern, key=int):
        return True

    else:
        # items = [x if x != 0 else 'Halcyon Potion' for x in items]
        # # Checks for all 1's and replaces it with Weapon Infusion
        # items = [x if x != 1 else 'Weapon Infusion' for x in items]
        # # Checks for all 2's and replaces it with Crystal Infusion
        # items = [x if x != 2 else 'Crystal Infusion' for x in items]
        # pattern_ = [
        #     x if x != 0 else 'Halcyon Potion' for x in pattern]
        # # Checks for all 1's and replaces it with Weapon Infusion
        # pattern_ = [x if x != 1 else 'Weapon Infusion' for x in pattern_]
        # # Checks for all 2's and replaces it with Crystal Infusion
        # pattern_ = [x if x != 2 else 'Crystal Infusion' for x in pattern_]

        return False

        # raise ValueError('Invalid Pattern:\nYours: ' + str(items) + "\nPattern: " + str(pattern_) + '\nRemember patterns do not have to be bought in order.')


def isVerifiedTo(user_id, ign, region):
    """Check if a discord user is verified to a specific VainGlory account.

    :parameter user_id:
    :parameter ign:
    :parameter region:
    :returns: True, if user is verified to given ign; False, if user isn't verified to given account

    """

    # Get the users data
    data = db.discordUserDictionary(user_id)

    # If no data was found on the user return false
    if data in [None, False]:
        return False

    else:
        if data["vaingloryRelated"]["verified"] == True and data["vaingloryRelated"]["verifiedName"] == ign and \
                        data["vaingloryRelated"]["verifiedRegion"] == region:
            return True

        else:
            return False


def giveVerified(user_id):
    """Returns a users verified status.

    :parameter user_id: Discord users id.
    :returns: True, if user is verified; False, if user isn't verified.

    """

    # Get the users data
    data = db.discordUserDictionary(user_id)

    # If no data was found on the user return false
    if data in [None, False]:
        return False

    else:
        return data["vaingloryRelated"]["verified"]


def giveIgn(user_id):
    """Returns a users verified ign.

    :param user_id: Discord users id.
    :return: ign; string or None.

    """

    # Get the users data
    data = db.discordUserDictionary(user_id)

    # If no data was found on the user return false
    if data in [None, False]:
        return None

    else:
        return data["vaingloryRelated"]["verified"]


def giveRegion(user_id):
    """Returns a users verified region.

    :param user_id: Discord users id.
    :return: region; string or None.

    """

    # Get the users data
    data = db.discordUserDictionary(user_id)

    # If no data was found on the user return false
    if data in [None, False]:
        return None

    else:
        return data["vaingloryRelated"]["verified"]


def giveIgnAndRegion(user_id):
    """Returns a users verified ign and region.

    :param user_id: Discord users id.
    :return: ign and region; string, string or None, None.

    """

    # Get the users data
    data = db.discordUserDictionary(user_id)

    # If no data was found on the user return false
    if data in [None, False]:
        return None, None

    else:
        return data["vaingloryRelated"]["verifiedName"], data["vaingloryRelated"]["verifiedRegion"]
