"""

Checks:
Check and validate input.

"""

from src.extra import tools


# Checks if PLAYER NAME is VALID
def checkPlayerName(name):
    if name == "":
        return False

    elif tools.isInt(name) == True:
        return False

    elif len(name) < 3:
        return False

    elif len(name) > 16:
        return False

    else:
        return True

# Check if COMMUNITY NAME, GUILD or TEAM, is VALID
def checkCommunityName(name):
    if name == "":
        return False

    elif tools.isInt(name) == True:
        return False

    elif len(name) < 3:
        return False

    elif len(name) > 16:
        return False

    else:
        return True

# Checks if a DATE is VALID
def checkDays(date):
    if date == "":
        return False

    elif tools.isInt(date) == False:
        return False

    elif date == False or date == True:
        return False

    else:
        return True


# Gives a VALID DATE
def giveDays(date):
    if checkDays(date) == False:
        return 28

    date = int(date)  # Convert DATE to INT to prevent ERRORS

    if date <= 0:
        return 1

    elif date > 28:
        return 28

    else:
        return date


def checkRegion(region):
    """Checks if given region is a valid Vainglory region.

    :argument region: String to check if valid region.
    :returns: True, if region is valid; False, if region isn't valid.

    """
    if region == "":
        return False

    if tools.isInt(region) == True:
        return False

    # All possible regions
    regions = [
        "na",
        "eu",
        "sg",
        "sea",
        "ea",
        "sa",
        "cn",
        "tournament-na",
        "tournament-eu",
        "tournament-sg",
        "tournament-ea",
        "tournament-sa"
    ]

    if region in regions:  # Checks that SERVER is found in possible SERVER
        return True

    else:
        return False


def giveRegion(region):
    """Gives a valid region if given region is in valid.

    :argument region: String to check
    :returns: String, na, eu, sg, ea, sa, cn, tournament-na, tournament-eu, tournament-sg, tournament-ea, tournament-sa

    """

    # Clean the input
    region = str(region.lower()).replace("t", "tournament")

    if region == "sea":
        region = "sg"

    if checkRegion(region) == False:
        return "na"

    return region


# Checks if GAMEMODE is VALID
def checkGameMode(game_mode):
    if tools.isInt(game_mode) == True:
        return False

    game_modes = ["any", "casual", "ranked", "royale", "blitz", "private_casual", "private_draft", "private_royale", "private_blitz"]  # POSSIBLE GAME MODES
    game_mode = str(game_mode.lower())

    if game_mode in game_modes:
        return True

    else:
        return False


# Gives a VALID GAMEMODE
def giveGameMode(game_mode):
    game_mode = str(game_mode).lower()  # Turn input into a string to prevent errors

    if game_mode == "br":
        game_mode = "royale"

    elif game_mode == "pc":
        game_mode = "private_casual"

    elif game_mode == "pd":
        game_mode = "private_draft"

    elif game_mode == "pr":
        game_mode = "private_royale"

    elif game_mode == "pb":
        game_mode = "private_blitz"

    if checkGameMode(game_mode) == False:
        return "any"

    # FOR DEBUGGING
    # print("GAME MODE: " + str(game_mode))

    return game_mode

# Checks if AUTO is VALID
def checkAuto(auto):
    if auto == "":
        return False

    auto = str(auto)
    auto = str(auto.lower())

    if auto == "false" or auto == "true":
        return True

    else:
        return False

# Gives a VALID AUTO
def giveAuto(auto):
    if checkAuto(auto) == False:
        return False

    auto = str(auto)
    auto = str(auto.lower())

    if auto == "false":
        return False

    elif auto == "true":
        return True

    else:
        return False


# Checks if PAGES is VALID
def checkPages(pages):
    if pages == "":
        return False

    elif tools.isInt(pages) == False:
        return False

    elif pages == False or pages == True:
        return False

    else:
        return True


# GIVES VALID PAGES
def givePages(pages, mode=0):
    if checkPages(pages) == False:
        if mode == 0:
            return 25

        elif mode == 1:
            return 1

        else:
            return 1

    pages = int(pages)

    if pages <= 0:
        return 1

    elif pages > 50:
        return 50

    else:
        return pages


def checkCommunityTag(tag):
    """Checks if given tag is valid.

    :param tag: String to check if valid tag.
    :return: True, if tag is valid; False, if tag isn't valid.

    """

    if len(tag) < 2:
        return False

    if len(tag) > 4:
        return False

    else:
        return True

def giveCommunityTag(tag):
    """Gives a valid tag format if given tag is valid.

    :argument tag: String to check if valid tag.
    :returns: Valid tag format; False, if tag isn't valid.

    """

    if checkCommunityTag(tag) == False:
        return False

    tag = str(tag).upper()

    return tag

def checkLevel(level):
    if tools.isInt(level) == False:
        return False

    elif level == True or level == False:
        return False

    else:
        return True

def giveLevel(level):
    if checkLevel(level) == False:
        return 1

    level = int(level)

    if level < 1:
        return 1

    elif level > 100:
        return 100

    else:
        return level


# CHECKS that MEMBERSHIP is VALID
def checkMembership(membership):
    if tools.isInt(membership) == True:
        return False

    memberships = ["open", "private"]  # Possible memberships
    membership = str(membership).lower()

    if membership in memberships:
        return True

    else:
        return False

# Gives VALID MEMBERSHIP
def giveMembership(membership):
    if checkMembership(membership) == False:
        return "open"

    memberships = ["open", "private"]  # Possible memberships
    membership = str(membership).lower()

    if membership in memberships:
        return membership
    else:
        return "open"


# Gives a VALID NUMBER TIER
def giveTierNum(tier):
    if tools.isInt(tier) == False:
        return -1

    if tier == False or tier == True:
        return -1

    tier = int(tier)

    if tier < -1:
        return -1

    elif tier >29:
        return 29

    else:
        return tier


# Gives VALID TIER IGN GIVEN NUMBER or NAME
def giveTier(tier):
    if tools.isInt(tier) == False:
        tier = str(tier).lower()

    tiers = {
       -1: "unranked",
        0: "just_beginning-B",
        1: "just_beginning-S",
        2: "just_beginning-G",
        3: "getting_there-B",
        4: "getting_there-S",
        5: "getting_there-G",
        6: "rock_solid-B",
        7: "rock_solid-S",
        8: "rock_solid-G",
        9: "worthy_foe-B",
        10: "worthy_foe-S",
        11: "worthy_foe-G",
        12: "got_swagger-B",
        13: "got_swagger-S",
        14: "got_swagger-G",
        15: "credible_threat-B",
        16: "credible_threat-S",
        17: "credible_threat-G",
        18: "the_hotness-B",
        19: "the_hotness-S",
        20: "the_hotness-G",
        21: "simply_amazing-B",
        22: "simply_amazing-S",
        23: "simply_amazing-G",
        24: "pinnacle_of_awesome-B",
        25: "pinnacle_of_awesome-S",
        26: "pinnacle_of_awesome-G",
        27: "vainglorious-B",
        28: "vainglorious-S",
        29: "vainglorious-G"
              }
    # print(tier)
    tiers_inv = {v: k for k, v in tiers.items()}
    # print(tiers_inv)

    if tier in tiers:
        return tiers[tier]

    elif tier in tiers_inv:
        return tier

    else:
        return "unranked"


# Checks that LANGUAGE IS VALID
def checkLanguage(language):
    language = str(language)

    if len(language) < 0:
        return False

    if len(language) > 16:
        return False


def giveLanguage(language):
    if checkLanguage(language) == False:
        return "english"

    else:
        return language


# Checks that CONTACT IS VALID
def checkContact(contact):
    contact = str(contact)

    if len(contact) < 0:
        return False

    if len(contact) > 115:
        return False

    return True

# Checks if XP is VALID
def checkFame(Fame):
    if tools.isInt(Fame) == False:
        return False

    if Fame == False or Fame == True:
        return False

    if Fame == "":
        return False

    return True


# Gives a VALID XP
def giveFame(Fame):
    if checkFame(Fame) == False:
        return 0

    Fame = int(Fame)

    if Fame < 0:
        return 0

    if Fame > 999999999999:
        return 999999999999


def giveOrder(order):
    if tools.isInt(order) == True:
        return "ascending"

    if order not in ["ascending", "descending"]:
        return "ascending"

    return order


def checkFilterOne(filterOne):
    if tools.isInt(filterOne) == True:
        return False

    if filterOne not in ["global"] and checkRole(filterOne) == False and checkPosition(filterOne) == False:
        if checkHeroActorName(filterOne) == False and checkRegion(filterOne) == False:
            return False

    return True

def checkPosition(position):
    if tools.isInt(position) == True:
        return False

    position = str(position).title()

    if position not in ['Protector', 'Warrior', 'Mage', 'Sniper', 'Assassin']:
        return False

    return True


def checkHeroActorName(actor):
    if tools.isInt(actor) == True:
        return False

    actor = str(actor).title()

    if actor not in ["Adagio", "Alpha", "Ardan", "Baptiste", "Baron", "Blackfeather", "Catherine", "Celeste", "Flicker", "Fortress", "Glaive", "Grumpjaw", "Gwen", "Krul", "Skaarf", "Rona", "Idris", "Joule", "Kestrel", "Koshka", "Lance", "Lyra", "Ozo", "Petal", "Phinn", "Reim", "Ringo", "Samuel", "Saw", "Taka", "Skye", "Vox", "Grace", "Reza"]:
        return False

    return True


def checkFilterTwo(filterTwo):
    if tools.isInt(filterTwo) == True:
        return False

    if filterTwo not in ['afks', 'assists', 'deaths', 'farm', 'gold', 'goldMiners', 'kills', 'krakenCaptures', 'minionKills']:
        return False

    return True


def checkCommunityLevel(level):
    if tools.isInt(level) == False:
        return False

    level = int(level)

    if level < 0:
        return False

    elif level > 99:
        return False

    else:
        return True


def giveCommunityLevel(level):
    if checkCommunityLevel(level) == False:
        return 0

    if level < 0:
        return 0

    elif level > 99:
        return 99

    else:
        return level


def checkSkillTier(skillTier):
    if tools.isInt(skillTier) == False:
        return False

    skillTier = int(skillTier)

    if skillTier < -1:
        return False

    elif skillTier > 29:
        return False

    else:
        return True


def giveSkillTier(skillTier):
    if checkSkillTier(skillTier) == False:
        return -1

    skillTier = int(skillTier)

    if skillTier < -1:
        return -1

    elif skillTier > 29:
        return 29

    else:
        return skillTier


def checkCommunityDescription(description):
    if tools.isInt(description) == True:
        return False

    description = str(description)

    if len(description) < 15:
        return False

    elif len(description) > 1000:
        return False

    else:
        return True


def checkCommunityTime(time):
    if tools.isInt(time) == True:
        return False

    time = str(time).lower()

    times = {

        "morning",
        "midday",
        "night",
        "allday"

    }

    if time in times:
        return True

    else:
        return False


def giveCommunityTime(time):
    if tools.isInt(time) == True:
        return "anytime"

    time = str(time).lower()

    times = {

        "morning",
        "midday",
        "night",
        "anytime"

    }

    if time in times:
        return time

    else:
        return "anytime"


def checkBoolean(ans):
    if tools.isInt(ans) == True:
        return False

    ans = str(ans).lower()

    answers = [

        "true",
        "t",
        "false",
        "f"

    ]

    if ans in answers:
        return True

    else:
        return False


def giveBoolean(ans):
    if tools.isInt(ans) == True:
        return True

    ans = str(ans).lower()

    answers = {

        "true": True,
        "t": True,
        "false": False,
        "f": False

    }

    if ans in answers:
        return answers[ans]

    else:
        return True


def checkCommunityType(communityType):
    if tools.isInt(communityType) == True:
        return False

    communityType = str(communityType).lower()

    communityTypes = {
        "casual",
        "semi",
        "competitive",
        "school"
    }

    if communityType in communityTypes:
        return True

    else:
        return False


def giveCommunityType(communityType):
    if tools.isInt(communityType) == True:
        return "casual"

    communityType = str(communityType).lower()

    communityTypes = {
        "casual",
        "semi",
        "competitive",
        "school"
    }

    if communityType in communityTypes:
        return communityType

    else:
        return "casual"


def checkRole(role):
    if tools.isInt(role) == True:
        return False

    role = str(role).lower()

    roles = [
        "any",
        "lane",
        "laner",
        "jungle",
        "jungler",
        "captain"
    ]

    if role in roles:
        return True

    else:
        return False


def giveRole(role):
    if checkRole(role) == False:
        return "any"

    roles = [
        "any",
        "lane",
        "laner",
        "jungle",
        "jungler",
        "captain"
    ]

    if role in roles:
        return roles[role]

    else:
        return "any"


def checkPower(power):
    if tools.isInt(power) == True:
        return False

    powers = [
        "weapon",
        "wp",
        "crystal",
        "cp",
        "utility",
        "up"
    ]

    if power in powers:
        return True

    else:
        return False


def givePower(power):
    if tools.isInt(power) == True:
        return "any"

    powers = {
        "any": "any",
        "weapon": "weapon",
        "wp": "weapon",
        "crystal": "crystal",
        "cp": "crystal",
        "utility": "utility",
        "up": "utility"
    }

    if power in powers:
        return powers[power]

    else:
        return "any"
