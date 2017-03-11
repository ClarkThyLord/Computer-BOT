# VG_toolbox
# Functions that make the Vainglory life easier
"""
List of Functions:
    giveKarmaVG
    giveMatchVG
    giveSkillTierVG
    isServerVG
    isGameModeVG

"""

import TOOL_module as tools

# Gives KARMA as a TITLE
def giveKarmaVG(karma, mode=0):
    # CHECK that KARMA is VALID
    if tools.isIntTOOL(karma) == False:
        return "Wow that's some crazy karma!"
    karma = int(karma)  # Convert KARMA to INT to prevent ERRORS

    # CHANGE KARMA from a NUMBER to a STRING
    karma_dict = {
    0 : ["Bad Karma", "http://i66.tinypic.com/2vsmdxi.jpg"],
    1 : ["Good Karma", "http://i63.tinypic.com/2a9wrr7.jpg"],
    2 : ["Great Karma", "http://i64.tinypic.com/sd1t3b.jpg"]}

    try:
        return karma_dict[karma][mode]
    except:
        if mode == 0:
            return "http://i63.tinypic.com/9k6xcj.jpg"
        elif mode == 1:
            return "Wow that's some crazy karma!"

# GIVES the IGN for MATCH MODE
def giveMatchVG(match, mode=0):
    # Check that MATCH is VALID
    if tools.isIntTOOL(match) == True:
        return "That one match..."

    match = str(match)  # Convert MATCH to STRING to prevent ERRORS
    
    match_dict = {
     "blitz_pvp_ranked": "Blitz",
     "casual_aral": "Battle Royal",
     "private": "Private Casual",
     "private_party_draft_match": "Private Draft",
     "private_party_blitz_match": "Private Blitz",
     "private_party_aral_match":"Private Battle Royal",
     "casual": "Casual Match",
     "ranked": "Rank Match"}

    try:
        return match_dict[match]

    except:
        return match

# Gives SKILL TIER as a TITLE
def giveSkillTierVG(tier, mode=0):
    if tools.isIntTOOL(tier) == False:
        return "Unreal Rank"

    tier = int(tier)  # Convert TIER to INT to prevent ERRORS

    # Checks that TIER is in VALID RANGE
    if tier > 29 or tier < -1:
        return "Unreal Rank"

    skill_dict = {
     -1: ['Un-Ranked', 'http://i64.tinypic.com/30veur5.jpg'],
     0:  ['Just Beginning - B', 'http://i66.tinypic.com/spj77t.jpg'],
     1:  ['Just Beginning - S', 'http://i67.tinypic.com/24ct7qu.jpg'],
     2:  ['Just Beginning - G', 'http://i63.tinypic.com/14kytzl.jpg'],
     3:  ['Getting There - B', 'http://i66.tinypic.com/w8x5ci.jpg'],
     4:  ['Getting There - S', 'http://i65.tinypic.com/2rc3f39.jpg'],
     5:  ['Getting There - G', 'http://i66.tinypic.com/15guo43.jpg'],
     6:  ['Rock Solid - B', 'http://i63.tinypic.com/10zbkuw.jpg'],
     7:  ['Rock Solid - S', 'http://i64.tinypic.com/2igmao7.jpg'],
     8:  ['Rock Solid - G', 'http://i64.tinypic.com/m9ngpc.jpg'],
     9:  ['Worthy Foe - B', 'http://i63.tinypic.com/99jgg4.jpg'],
     10:  ['Worthy Foe - S', 'http://i64.tinypic.com/nnksv9.jpg'],
     11:  ['Worthy Foe - G', 'http://i68.tinypic.com/120kpk9.jpg'],
     12:  ['Got Swagger - B', 'http://i64.tinypic.com/4rxoid.jpg'],
     13:  ['Got Swagger - S', 'http://i68.tinypic.com/2lnib61.jpg'],
     14:  ['Got Swagger - G', 'http://i63.tinypic.com/oqjgau.jpg'],
     15:  ['Credible Threat - B', 'http://i65.tinypic.com/dphenn.jpg'],
     16:  ['Credible Threat - S', 'http://i66.tinypic.com/2dr9law.jpg'],
     17:  ['Credible Threat - G', 'http://i65.tinypic.com/20h6cti.jpg'],
     18:  ['The Hotness - B', 'http://i65.tinypic.com/288vxuc.jpg'],
     19:  ['The Hotness - S', 'http://i68.tinypic.com/2e3rby8.jpg'],
     20:  ['The Hotness - G', 'http://i68.tinypic.com/dq3meg.jpg'],
     21:  ['Simply Amazing - B', 'http://i65.tinypic.com/2hpm0d3.jpg'],
     22:  ['Simply Amazing - S', 'http://i66.tinypic.com/2b19ap.jpg'],
     23:  ['Simply Amazing - G', 'http://i65.tinypic.com/im5f13.jpg'],
     24:  ['Pinnacle of Awesome - B', 'http://i65.tinypic.com/vp8f8l.jpg'],
     25:  ['Pinnacle of Awesome - S', 'http://i68.tinypic.com/5wjhvs.jpg'],
     26:  ['Pinnacle of Awesome- G', 'http://i65.tinypic.com/10r7rrs.jpg'],
     27:  ['Vainglorious - B', 'http://i68.tinypic.com/27y8mdw.jpg'],
     28:  ['Vainglorious - S', 'http://i64.tinypic.com/1znqsds.jpg'],
     29:  ['Vainglorious - G', 'http://i65.tinypic.com/e6x74n.jpg']
    }

    return skill_dict[tier][mode]

# Will check that MODE is VALID
def isGameModeVG(mode, type=0):
    if tools.isIntTOOL(mode) == True:
        return False

    mode = str(mode)  # Convert MODE to STRING to prevent ERRORS

    modes = [
        "any",
        "casual",
        "ranked",
        "blitz",
        "royale"
        ]
    if mode in modes:
        return True
    else:
        return False

# Will check that SERVER is VALID
def isServerVG(server, type=0):
    if tools.isIntTOOL(server) == True:
        return False

    server = str(server)  # Convert SERVER to STRING to prevent ERRORS

    # All possible SERVERS
    servers = [
            "na",
            "eu",
            "sg",
            "sea",
            "ea",
            "sa"
            ]

    if server in servers:  # Checks that SERVER is found in possible SERVER
        return True

    else:
        return False
