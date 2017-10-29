"""

Vg Tools:
Various function to make the vainglory life easier; and check/validate input.

"""

import random
from src.extra import tools
import datetime
import gamelocker
import config
import json

api = gamelocker.Vainglory(config.VG_KEY)

# Gives KARMA as a TITLE
def giveKarmaVG(karma, mode=0):
    if tools.isInt(karma) == False:  # CHECK that KARMA is VALID
        return "Wow that's some crazy karma!"

    karma = int(karma)  # Convert KARMA to INT to prevent ERRORS

    # CHANGE KARMA from a NUMBER to a STRING
    karma_dict = {

        0: ["Bad Karma", "http://i66.tinypic.com/2vsmdxi.jpg"],
        1: ["Good Karma", "http://i63.tinypic.com/2a9wrr7.jpg"],
        2: ["Great Karma", "http://i64.tinypic.com/sd1t3b.jpg"]

    }

    try:
        return karma_dict[karma][mode]

    except:
        if mode == 0:
            return "http://i63.tinypic.com/9k6xcj.jpg"

        elif mode == 1:
            return "Wow that's some crazy karma!"


# GIVES the IGN for MATCH MODE
def giveGameModeVG(mode, type=0):
    mode = str(mode)  # Convert MATCH to STRING to prevent ERRORS

    api_to_match = {
        "casual": "casual",
        "private": "private casual",
        "ranked": "rank",
        "private_party_draft_match": "private draft",
        "casual_aral": "battle royale",
        "private_party_aral_match": "private battle royale",
        "blitz_pvp_ranked": "blitz",
        "private_party_blitz_match": "private blitz"
    }

    match_to_api = {
        "casual": "casual",
        "blitz": "blitz_pvp_ranked",
        "royale": "casual_aral",
        "rank": "ranked"
    }

    # Return in-game name
    if type == 0:
        try:
            return api_to_match[mode]

        except:
            return mode

    # Return api name
    elif type == 1:
        try:
            return match_to_api[mode]

        except:
            return mode


# Gives SKILL TIER as a TITLE
def giveSkillTierVG(tier, mode=0):
    if tools.isInt(tier) == False:
        return "Unreal Rank"

    tier = int(tier)  # Convert TIER to INT to prevent ERRORS

    # Checks that TIER is in VALID RANGE
    if tier > 29 or tier < -1:
        return "Unreal Rank"

    skill_dict = {
        -1: ['Un-Ranked', 'http://i64.tinypic.com/30veur5.jpg'],
        0: ['Just Beginning - B', 'http://i66.tinypic.com/spj77t.jpg'],
        1: ['Just Beginning - S', 'http://i67.tinypic.com/24ct7qu.jpg'],
        2: ['Just Beginning - G', 'http://i63.tinypic.com/14kytzl.jpg'],
        3: ['Getting There - B', 'http://i66.tinypic.com/w8x5ci.jpg'],
        4: ['Getting There - S', 'http://i65.tinypic.com/2rc3f39.jpg'],
        5: ['Getting There - G', 'http://i66.tinypic.com/15guo43.jpg'],
        6: ['Rock Solid - B', 'http://i63.tinypic.com/99jgg4.jpg'],
        7: ['Rock Solid - S', 'http://i64.tinypic.com/nnksv9.jpg'],
        8: ['Rock Solid - G', 'http://i68.tinypic.com/120kpk9.jpg'],
        9: ['Worthy Foe - B', 'http://i63.tinypic.com/10zbkuw.jpg'],
        10: ['Worthy Foe - S', 'http://i64.tinypic.com/2igmao7.jpg'],
        11: ['Worthy Foe - G', 'http://i64.tinypic.com/m9ngpc.jpg'],
        12: ['Got Swagger - B', 'http://i64.tinypic.com/4rxoid.jpg'],
        13: ['Got Swagger - S', 'http://i68.tinypic.com/2lnib61.jpg'],
        14: ['Got Swagger - G', 'http://i63.tinypic.com/oqjgau.jpg'],
        15: ['Credible Threat - B', 'http://i65.tinypic.com/dphenn.jpg'],
        16: ['Credible Threat - S', 'http://i66.tinypic.com/2dr9law.jpg'],
        17: ['Credible Threat - G', 'http://i65.tinypic.com/20h6cti.jpg'],
        18: ['The Hotness - B', 'http://i65.tinypic.com/288vxuc.jpg'],
        19: ['The Hotness - S', 'http://i68.tinypic.com/2e3rby8.jpg'],
        20: ['The Hotness - G', 'http://i68.tinypic.com/dq3meg.jpg'],
        21: ['Simply Amazing - B', 'http://i65.tinypic.com/2hpm0d3.jpg'],
        22: ['Simply Amazing - S', 'http://i66.tinypic.com/2b19ap.jpg'],
        23: ['Simply Amazing - G', 'http://i65.tinypic.com/im5f13.jpg'],
        24: ['Pinnacle of Awesome - B', 'http://i65.tinypic.com/vp8f8l.jpg'],
        25: ['Pinnacle of Awesome - S', 'http://i68.tinypic.com/5wjhvs.jpg'],
        26: ['Pinnacle of Awesome- G', 'http://i65.tinypic.com/10r7rrs.jpg'],
        27: ['Vainglorious - B', 'http://i68.tinypic.com/27y8mdw.jpg'],
        28: ['Vainglorious - S', 'http://i64.tinypic.com/1znqsds.jpg'],
        29: ['Vainglorious - G', 'http://i65.tinypic.com/e6x74n.jpg']
    }

    return skill_dict[tier][mode]


# Will check that MODE is VALID
def isGameModeVG(game_mode, type=0):
    if tools.isInt(game_mode) == True:
        return False

    game_mode = str(game_mode)  # Convert MODE to STRING to prevent ERRORS

    modes = [
        "any",
        "casual",
        "ranked",
        "blitz",
        "royale"
    ]
    if game_mode in modes:
        return True

    else:
        return False


def giveTaunt(hero):
    if hero == "":
        pass

    else:
        if hero != "" and tools.isInt(hero) == True:
            return False

    hero = str(hero).lower()  # Convert to string and lower to prevent errors

    if hero == "":
        taunt = [
            "http://i.imgur.com/QWPzPSp.gif",
            "http://i.imgur.com/0VmwoyU.gif",
            "http://i.imgur.com/HZV04ew.gif",
            "http://i.imgur.com/YxjQN8l.gif",
            "http://i.imgur.com/zQ914kf.gif",
            "http://i.imgur.com/EvPLfXu.gif",
            "http://i.imgur.com/gA0BXzV.gif",
            "http://i.imgur.com/WIl0nBR.gif",
            "http://i.imgur.com/yIIujHK.gif",
            "http://i.imgur.com/lBZWyLy.gif",
            "http://i.imgur.com/95tpmvA.gif",
            "http://i.imgur.com/auCGVZ8.gif",
            "http://i.imgur.com/KhGmi7u.gif",
            "http://i.imgur.com/0WsmyBK.gif",
            "http://i.imgur.com/o0GAAPq.gif",
            "http://i.imgur.com/juYeHBB.gif",
            "http://i.imgur.com/2ozomsd.gif"
        ]

        return taunt[random.randint(1, len(taunt))]

    taunt = {
        "koshka": "http://i.imgur.com/QWPzPSp.gif",
        "taka": "http://i.imgur.com/0VmwoyU.gif",
        "rona": "http://i.imgur.com/HZV04ew.gif",
        "lance": "http://i.imgur.com/YxjQN8l.gif",
        "ozo": "http://i.imgur.com/zQ914kf.gif",
        "reim": "http://i.imgur.com/EvPLfXu.gif",
        "krul": "http://i.imgur.com/gA0BXzV.gif",
        "celeste": "http://i.imgur.com/WIl0nBR.gif",
        "grumpjaw": "http://i.imgur.com/yIIujHK.gif",
        "catherine": "http://i.imgur.com/lBZWyLy.gif",
        "baron": "http://i.imgur.com/95tpmvA.gif",
        "fortress": "http://i.imgur.com/auCGVZ8.gif",
        "gwen": "http://i.imgur.com/KhGmi7u.gif",
        "ardan": "http://i.imgur.com/0WsmyBK.gif",
        "glaive": "http://i.imgur.com/o0GAAPq.gif",
        "adagio": "http://i.imgur.com/juYeHBB.gif",
        "flicker": "http://i.imgur.com/2ozomsd.gif"
    }

    if hero in taunt:
        return taunt[hero]

    else:
        return False


# Clean hero name
def cleanHeroName(actor_name):
    """
    Clean a hero's name
    """

    try:

        actor_name = str(actor_name).replace("*", "")  # Convert hero name to string to prevent errors

        # List of old hero names
        old_heroes = {

            "Hero009": "Krul",
            "Hero010": "Skaarf",
            "Hero016": "Rona",
            "Sayoc": "Taka"

        }

        # List of hero names
        heroes = [

            "Adagio",
            "Alpha",
            "Ardan",
            "Baptiste",
            "Baron",
            "Blackfeather",
            "Catherine",
            "Celeste",
            "Flicker",
            "Fortress",
            "Glaive",
            "Gwen",
            "Krul",
            "Skaarf",
            "Rona",
            "Idris",
            "Joule",
            "Kestrel",
            "Koshka",
            "Lance",
            "Lyra",
            "Ozo",
            "Petal",
            "Phinn",
            "Reim",
            "Ringo",
            "Samuel",
            "SAW",
            "Taka",
            "Skye",
            "Vox",
            "Grumpjaw",
            "Reza"

        ]

        if actor_name in old_heroes:
            # FOR DEBUGGING
            # print("CLEAN OLD HERO NAME:\nOLD NAME:   " + str(actor_name) + " |NEW NAME:   " + str(old_heroes[actor_name]))

            actor_name = old_heroes[actor_name]

        if actor_name in heroes:

            # FOR DEBUGGING
            # print("CLEAN HERO NAME:\nORIGINAL:   " + str(actor_name) + "RETURNING:   " + str(actor_name))

            return actor_name

        else:

            # FOR DEBUGGING
            # print("CLEAN HERO NAME:\nORIGINAL:   " + str(actor_name) + "RETURNING:   " + str(actor_name))

            return actor_name

    except Exception as e:
        print("CLEAN HERO NAME ERROR:\n" + str(e))


def cleanHeroAbility(abilityName):
    """Given the api name of an item turn it pretty.

    :param abilityName: String to make pretty
    :returns: String either the same string without * or a pretty version of the string

    """

    abilityName = str(abilityName)

    abilities = {
        "HERO_ABILITY_SAW_EXPLOSIVE_TIPPED_SHELLS_NAME": "Mad Cannon",
        "HERO_ABILITY_SEBA_B_NAME": "Ordained",
        "HERO_ABILITY_SKAARF_A_SPITFIRE": "Spitfire",
        "HERO_ABILITY_RINGO_HELLFIRE_SAKE_NAME": "Hellfire Brew",
        "HERO_ABILITY_CATHERINE_ARCANE_SHIELD_NAME": "Stormguard",
        "HERO_ABILITY_SEBA_C_NAME": "Fearsome Shade",
        "HERO_ABILITY_HERO021_B_NAME": "On Point",
        "HERO_ABILITY_CELESTE_A_NAME": "Heliogenesis",
        "HERO_ABILITY_PETAL_BRAMBLETHORN_SEED_NAME": "Brambleboom Seeds",
        "HERO_ABILITY_HERO036_B_NAME": "Fairy Dust",
        "HERO_ABILITY_REIM_A_NAME": "Winter Spire",
        "HERO_ABILITY_SKYE_C_NAME": "Death From Above",
        "HERO_ABILITY_HERO042_B_NAME": "Holy Nova",
        "HERO_ABILITY_SAYOC_B": "Kaku",
        "HERO_ABILITY_RONA_B_NAME": "Foesplitter",
        "HERO_ABILITY_KESTREL_C_NAME": "One Shot One Kill",
        "HERO_ABILITY_IDRIS_A_NAME": "Shroudstep",
        "HERO_ABILITY_REIM_B_NAME": "Chill Winds",
        "HERO_ABILITY_SKAARF_C_DRAGON_BREATH": "Dragon's Breath",
        "HERO_ABILITY_LANCE_C_NAME": "Combat Roll",
        "HERO_ABILITY_GLAIVE_TWISTED_STROKE_NAME": "Twisted Stroke",
        "HERO_ABILITY_CELESTE_C_NAME": "Solar Storm",
        "HERO_ABILITY_HERO036_C_NAME": "Mooncloak",
        "HERO_ABILITY_OZO_A_NAME": "Three-Ring Circus",
        "HERO_ABILITY_SAYOC_C": "X-Retsu",
        "HERO_ABILITY_JOULE_ORBITAL_NUKE": "Big Red Button",
        "HERO_ABILITY_HERO009_LIFE_FROM_PAIN_NAME": "Spectral Smite",
        "HERO_ABILITY_GWEN_B_NAME": "Skedaddle",
        "HERO_ABILITY_GRUMPJAW_B_NAME": "Hangry",
        "HERO_ABILITY_BARON_C_NAME": "Ion Cannon",
        "HERO_ABILITY_VOX_C_NAME": "Wait for It",
        "HERO_ABILITY_PETAL_THORNSTORM_NAME": "Spontaneous Combustion",
        "HERO_ABILITY_GRUMPJAW_C_NAME": "Stuffed",
        "HERO_ABILITY_LANCE_A_NAME": "Impale",
        "HERO_ABILITY_KOSHKA_TWIRL_NAME": "Twirly Death",
        "HERO_ABILITY_VOX_B_NAME": "Pulse",
        "HERO_ABILITY_KESTREL_B_NAME": "Active Camo",
        "HERO_ABILITY_REIM_C_NAME": "Valkyrie",
        "HERO_ABILITY_KOSHKA_POUNCE_NAME": "Pouncy Fun",
        "HERO_ABILITY_SKYE_B_NAME": "Suri Strike",
        "HERO_ABILITY_PETAL_SHOUT_OF_THE_ENTS_NAME": "Trampoline!",
        "HERO_ABILITY_SAMUEL_A_NAME": "Malice & Verdict",
        "HERO_ABILITY_RONA_C_NAME": "Red Mist",
        "HERO_ABILITY_RINGO_TWIRLING_SILVER_NAME": "Twirling Silver",
        "HERO_ABILITY_HERO042_A_NAME": "Benediction",
        "HERO_ABILITY_ALPHA_B_NAME": "Core Charge",
        "HERO_ABILITY_GRUMPJAW_A_NAME": "Grumpy",
        "HERO_ABILITY_GWEN_C_NAME": "Aces High",
        "HERO_ABILITY_CELESTE_B_NAME": "Core Collapse",
        "HERO_ABILITY_SAW_ROADIE_RUN_NAME": "Roadie Run",
        "HERO_ABILITY_HERO009_BURNING_WOUNDS_NAME": "Dead Man's Rush",
        "HERO_ABILITY_RONA_A_NAME": "Into the Fray",
        "HERO_ABILITY_HERO021_C_NAME": "Rose Offensive",
        "HERO_ABILITY_GLAIVE_AFTERBURN_NAME": "Afterburn",
        "HERO_ABILITY_ADAGIO_GASOLINE_SOAKED_NAME": "Agent of Wrath",
        "HERO_ABILITY_OZO_C_NAME": "Bangarang",
        "HERO_ABILITY_BARON_A_NAME": "Porcupine Mortar",
        "HERO_ABILITY_PHINN_B_NAME": "Polite Company",
        "HERO_ABILITY_KOSHKA_FRENZY_NAME": "Yummy Catnip Frenzy",
        "HERO_ABILITY_JOULE_RHAPSODY_POWERSLIDE": "Thunder Strike",
        "HERO_ABILITY_LANCE_B_NAME": "Gythian Wall",
        "HERO_ABILITY_IDRIS_B_NAME": "Chakram",
        "HERO_ABILITY_ARDAN_A": "Vanguard",
        "HERO_ABILITY_SKYE_A_NAME": "Forward Barrage",
        "HERO_ABILITY_SAW_SUPPRESSING_FIRE_NAME": "Suppressing Fire",
        "HERO_ABILITY_FORTRESS_B_NAME": "Law of the Claw",
        "HERO_ABILITY_SKAARF_B_GOOP": "Goop",
        "HERO_ABILITY_CATHERINE_ASSASSINS_CHARGE_NAME": "Merciless Pursuit",
        "HERO_ABILITY_ADAGIO_FORTUNES_SMILE_NAME": "Gift of Fire",
        "HERO_ABILITY_OZO_B_NAME": "Acrobounce",
        "HERO_ABILITY_VOX_A_NAME": "Sonic Zoom",
        "HERO_ABILITY_GLAIVE_BLOODSONG_NAME": "Bloodsong",
        "HERO_ABILITY_SAYOC_A": "Kaiten",
        "HERO_ABILITY_PHINN_A_NAME": "Quibble",
        "HERO_ABILITY_HERO021_A_NAME": "Feint of Hearth",
        "HERO_ABILITY_RINGO_WING_CUT_NAME": "Achilles Shot",
        "HERO_ABILITY_HERO042_C_NAME": "Divine Intervention",
        "HERO_ABILITY_LYRA_A_NAME": "Imperial Sigil",
        "HERO_ABILITY_JOULE_RHAPSODY_CANNONS": "Rocket Leap",
        "HERO_ABILITY_CATHERINE_DEADLY_GRACE_NAME": "Blast Tremor",
        "HERO_ABILITY_BARON_B_NAME": "Jump Jets",
        "HERO_ABILITY_ARDAN_B": "Blood for Blood",
        "HERO_ABILITY_ARDAN_C": "Gauntlet",
        "HERO_ABILITY_SEBA_A_NAME": "Bad Mojo",
        "HERO_ABILITY_LYRA_C_NAME": "Arcane Passage",
        "HERO_ABILITY_SAMUEL_C_NAME": "Oblivion",
        "HERO_ABILITY_KESTREL_A_NAME": "Glimmershot",
        "HERO_ABILITY_ALPHA_C_NAME": "Termniation Protocol",
        "HERO_ABILITY_LYRA_B_NAME": "Bright Bulwark",
        "HERO_ABILITY_ALPHA_A_NAME": "Prime Directive",
        "HERO_ABILITY_IDRIS_C_NAME": "Shimmer Strike",
        "HERO_ABILITY_ADAGIO_FRIENDSHIP_NAME": "Verse of Judgement",
        "HERO_ABILITY_FORTRESS_C_NAME": "Attack of the Pack",
        "HERO_ABILITY_PHINN_C_NAME": "Forced Accord",
        "HERO_ABILITY_HERO036_A_NAME": "Binding Light",
        "HERO_ABILITY_GWEN_A_NAME": "Buckshot Bonanza",
        "HERO_ABILITY_FORTRESS_A_NAME": "Truth of the Tooth",
        "HERO_ABILITY_HERO009_SHIMMERHEART_NAME": "From Hell's Heart",
        "HERO_ABILITY_SAMUEL_B_NAME": "Drifting Dark",
        "HERO_ABILITY_REZA_A_NAME": "Scorcher",
        "HERO_ABILITY_REZA_B_NAME": "Troublemaker",
        "HERO_ABILITY_REZA_C_NAME": "Netherform Detonator"

    }

    if abilityName in abilities:
        return abilities[abilityName]

    else:
        return abilityName.replace("*", "")


def cleanNonHeroName(nonActorName):
    """Given the api name of an item turn it pretty.

    :param nonActorName: String to make pretty
    :returns: String either the same string without * or a pretty version of the string

    """

    nonActorName = str(nonActorName)

    nonActors = {
        "*JungleMinion_GoldMiner*": "Gold Miner",
        "*JungleMinion_CrystalMiner*": "Crystal Miner",
        "*Neutral_JungleMinion_DefaultBig*": "Back Minion",
        "*Neutral_JungleMinion_DefaultSmall*": "Shop Minion",
        "*JungleMinion_TreeEnt*": " Treant",
        "*LeadMinion*": "Lane Lead Minion",
        "*TankMinion*": "Lane Tank Minion",
        "*RangedMinion*": "Lane Ranged Minion",
        "*Kraken_Captured*": "Captured Kraken",
        "*Kraken_Jungle*": "Kraken",
        "*Turret*": "Turret",
        "*VainTurret*": "Vain Turret",
        "*VainCrystalAway*": "Vain Crystal",
        "*FortressMinion*": "Fortress Wolf"
    }

    if nonActorName in nonActors:
        return nonActors[nonActorName]

    else:
        return nonActorName.replace("*", "")


def cleanItemName(item_name):
    """Given the api name of an item turn it pretty.

    :param item_name: String to make pretty
    :returns: String either the same string without * or a pretty version of the string

    """

    item_name = str(item_name)

    items = {
        "Aftershock": "Aftershock",
        "Armor2": "Coat of Plates",
        "Armor3": "Metal Jacket",
        "Armor Shredder": "Bonesaw",
        "Atlas Pauldron": "Atlas Pauldron",
        "AttackSpeed1": "Swift Shooter",
        "AttackSpeed2": "Blazing Salvo",
        "BarbedNeedle": "Barbed Needle",
        "Boots1": "Sprint Boots",
        "Boots2": "Travel Boots",
        "Boots3": "Journey Boots",
        "BreakingPoint": "Breaking Point",
        "Broken Myth": "Broken Myth",
        "Clockwork": "Clockwork",
        "Cogwheel": "Chronograph",
        "Contraption": "Contraption",
        "Cooldown1": "Hourglass",
        "Critical": "Tyrant's Monocle",
        "Crucible": "Crucible",
        "Crystal1": "Crystal Bit",
        "Crystal2": "Eclipse Prism",
        "Crystal3": "Shatterglass",
        "Crystal Matrix": "Aegis",
        "Echo": "Echo",
        "EveOfHarvest": "Eve of Harvest",
        "Flare": "Flare",
        "Flaregun": "Flare Gun",
        "Fountain of Renewal": "Fountain of Renewal",
        "Frostburn": "Frostburn",
        "Halcyon Chargers": "Halcyon Chargers",
        "Health2": "Dragonheart",
        "Heavy Prism": "Heavy Prism",
        "Heavy Steel": "Heavy Steel",
        "IronguardContract": "Ironguard Contract",
        "Lifewell": "Lifespring",
        "Light Armor": "Light Armor",
        "Light Shield": "Light Shield",
        "LuckyStrike": "Lucky Strike",
        "Minion Candy": "Minion Candy",
        "MinionsFoot": "Minion's Foot",
        "Mulled Wine": "Halcyon Potion",
        "NullwaveGauntlet": "Nullwave Gauntlet",
        "Oakheart": "Oakheart",
        "PiercingShard": "Piercing Shard",
        "PiercingSpear": "Piercing Spear",
        "PoisonedShiv": "Poisoned Shiv",
        "Protector Contract": "Protector Contract",
        "Reflex Block": "Reflex Block",
        "Scout Trap": "Scout Trap",
        "Serpent Mask": "Serpent Mask",
        "Shield 2": "Kinetic Shield",
        "Shiversteel": "Shiversteel",
        "Six Sins": "Six Sins",
        "SlumberingHusk": "Slumbering Husk",
        "Steam Battery": "Energy Battery",
        "Stormcrown": "Stormcrown",
        "StormguardBanner": "Stormguard Banner",
        "Tension Bow": "Tension Bow",
        "Tornado Trigger": "Tornado Trigger",
        "Void Battery": "Void Battery",
        "War Treads": "War Treads",
        "Weapon3": "Sorrowblade",
        "Weapon Blade": "Weapon Blade",
        "*1000_Item_HalcyonPotion*": "Halcyon Potion",
        "*1002_Item_WeaponBlade*": "Weapon Blade",
        "*1003_Item_CrystalBit*": "Crystal Bit",
        "*1004_Item_SwiftShooter*": "Swift Shooter",
        "*1005_Item_SixSins*": "Six Sins",
        "*1009_Item_EclipsePrism*": "Eclipse Prism",
        "*1010_Item_BlazingSalvo*": " Blazing Salvo",
        "*1012_Item_Sorrowblade*": "Sorrowblade",
        "*1013_Item_Shatterglass*": "Shatterglass",
        "*1014_Item_TornadoTrigger*": "Tornado Trigger",
        "*1015_Item_Oakheart*": "Oakheart",
        "*1016_Item_Dragonheart*": "Dragonheart",
        "*1017_Item_LightArmor*": "Light Armor",
        "*1022_Item_CoatOfPlates*": "Coat of Plates",
        "*1024_Item_MetalJacket*": "Metal Jacket",
        "*1025_Item_EnergyBattery*": "Energy Battery",
        "*1026_Item_Hourglass*": "Hourglass",
        "*1027_Item_VoidBattery*": "Void Battery",
        "*1028_Item_Chronograph*": "Chronograph",
        "*1029_Item_Clockwork*": "Clockwork",
        "*1030_Item_SprintBoots*": "Sprint Boots",
        "*1032_Item_TravelBoots*": "Travel Boots",
        "*1034_Item_SerpentMask*": "Serpent Mask",
        "*1035_Item_TensionBow*": "Tension Bow",
        "*1038_Item_Flare*": "Flare",
        "*1039_Item_Bonesaw*": "Bonesaw",
        "*1041_Item_MinionCandy*": "Minion Candy",
        "*1042_Item_Shiversteel*": "Shiversteel",
        "*1043_Item_ReflexBlock*": "Reflex Block",
        "*1044_Item_Frostburn*": "Frostburn",
        "*1045_Item_FountainOfRenewal*": "Fountain of Renewal",
        "*1046_Item_Crucible*": "Crucible",
        "*1047_Item_JourneyBoots*": "Journey Boots",
        "*1049_Item_TyrantsMonocle*": "Tyrant's Monocle",
        "*1050_Item_Aftershock*": "Aftershock",
        "*1052_Item_WeaponInfusion*": "Weapon Infusion",
        "*1053_Item_CrystalInfusion*": "Crystal Infusion",
        "*1054_Item_ScoutTrap*": "Scout Trap",
        "*1055_Item_BrokenMyth*": "Broken Myth",
        "*1056_Item_WarTreads*": "War Treads",
        "*1057_Item_AtlasPauldron*": "Atlas Pauldron",
        "*1059_Item_BookOfEulogies*": "Book of Eulogies",
        "*1060_Item_BarbedNeedle*": "Barbed Needle",
        "*1061_Item_LightShield*": "Light Shield",
        "*1062_Item_KineticShield*": "Kinetic Shield",
        "*1063_Item_Aegis*": "Aegis",
        "*1064_Item_Lifespring*": "Lifespring",
        "*1065_Item_HeavySteel*": "Heavy Steel",
        "*1066_Item_PiercingSpear*": "Piercing Spear",
        "*1067_Item_BreakingPoint*": "Breaking Point",
        "*1068_Item_LuckyStrike*": "Lucky Strike",
        "*1069_Item_AlternatingCurrent*": "Alternating Current",
        "*1070_Item_PiercingShard*": "Piercing Shard",
        "*1071_Item_EveOfHarvest*": "Eve of Harvest",
        "*1072_Item_HeavyPrism*": "Heavy Prism",
        "*1073_Item_IronguardContract*": "Ironguard Contract",
        "*1074_Item_StormguardBanner*": "Stormguard Banner",
        "*1079_Item_Contraption*": "Contraption",
        "*1080_Item_MinionsFoot*": "Minion's Foot",
        "*1084_Item_ProtectorContract*": "Protector Contract",
        "*1087_Item_HalcyonChargers*": "Halcyon Chargers",
        "*1088_Item_Flaregun*": "Flare Gun",
        "*1090_Item_Stormcrown*": "Stormcrown",
        "*1092_Item_PoisonedShiv*": "Poisoned Shiv",
        "*1095_Item_NullwaveGauntlet*": "Nullwave Gauntlet",
        "*1097_Item_Echo*": "Echo",
        "*1105_Item_SlumberingHusk*": "Slumbering Husk",
        "*1085_Item_DragonbloodContract*": "Dragonblood Contract",
        "*Item_AtlasPauldron*": "Atlas Pauldron",
        "*Item_CoatOfPlates*": "Coat Of Plates",
        "*Item_Crucible*": "Crucible",
        "*Item_Dragonheart*": "Dragonheart",
        "*Item_FountainOfRenewal*": "Fountain Of Renewal",
        "*Item_IronguardContract*": "Ironguard Contract",
        "*Item_KineticShield*": "Kinetic Shield",
        "*Item_Lifespring*": "Lifespring",
        "*Item_LightArmor*": "Light Armor",
        "*Item_ScoutTrap*": "Scout Trap",
        "*Item_SprintBoots*": "Sprint Boots",
        "*Item_TensionBow*": "Tension Bow",
        "*Item_WeaponBlade*": "Weapon Blade",
        "*Item_WeaponInfusion*": "Weapon Infusion",
        "*Item_Aegis*": "Aegis",
        "*Item_BlazingSalvo*": "Blazing Salvo",
        "*Item_BookOfEulogies*": "Book Of Eulogies",
        "*Item_BreakingPoint*": "Breaking Point",
        "*Item_HalcyonPotion*": "Halcyon Potion",
        "*Item_HeavySteel*": "Heavy Steel",
        "*Item_LightShield*": "Light Shield",
        "*Item_LuckyStrike*": "Lucky Strike",
        "*Item_MinionsFoot*": "Minions Foot",
        "*Item_ReflexBlock*": "Reflex Block",
        "*Item_SixSins*": "Six Sins",
        "*Item_SwiftShooter*": "Swift Shooter",
        "*Item_TravelBoots*": "Travel Boots",
        "*Item_TyrantsMonocle*": "Tyrants Monocle",
        "*Item_BrokenMyth*": "Broken Myth",
        "*Item_CrystalBit*": "Crystal Bit",
        "*Item_CrystalInfusion*": "Crystal Infusion",
        "*Item_EclipsePrism*": "Eclipse Prism",
        "*Item_EnergyBattery*": "Energy Battery",
        "*Item_Frostburn*": "Frostburn",
        "*Item_HeavyPrism*": "Heavy Prism",
        "*Item_PiercingShard*": "Piercing Shard",
        "*Item_VoidBattery*": "Void Battery",
        "*Item_Oakheart*": "Oakheart",
        "*Item_Shiversteel*": "Shiversteel",
        "*Item_Sorrowblade*": "Sorrowblade",
        "*Item_TornadoTrigger*": "Tornado Trigger",
        "*Item_CandyShop_Taunt*": "Taunt",
        "*Item_CandyShop_VOTaunt*": "Voiceover Taunt",
        "*Item_Flare*": "Flare",
        "*Item_Flaregun*": "Flaregun",
        "*Item_WarTreads*": "War Treads",
        "*Item_EveOfHarvest*": "Eve Of Harvest",
        "*Item_HalcyonChargers*": "Halcyon Chargers",
        "*1002_Item_CandyShop_Kissy*": "Kiss Taunt",
        "*1005_Item_CandyShop_Taunt*": "Taunt",
        "*1007_Item_CandyShop_VOTaunt*": "Voiceover Taunt",
        "*Item_Chronograph*": "Chronograph",
        "*Item_Contraption*": "Contraption",
        "*Item_MinionCandy*": "Minion Candy",
        "*Item_PiercingSpear*": "Piercing Spear",
        "*Item_BarbedNeedle*": "Barbed Needle",
        "*Item_JourneyBoots*": "Journey Boots",
        "*Item_SerpentMask*": "Serpent Mask",
        "*Item_Aftershock*": "Aftershock",
        "*Item_Hourglass*": "Hourglass",
        "*Item_MetalJacket*": "Metal Jacket",
        "*Item_Stormcrown*": "Stormcrown",
        "*Item_StormguardBanner*": "Stormguard Banner",
        "*Item_CandyShop_Kissy*": "Kiss Taunt",
        "*Item_Shatterglass*": "Shatterglass",
        "*Item_Bonesaw*": "Bonesaw",
        "*Item_SlumberingHusk*": "Slumbering Husk",
        "*Item_NullwaveGauntlet*": "Nullwave Gauntlet",
        "*Item_PoisonedShiv*": "Poisoned Shiv",
        "*Item_Clockwork*": "Clockwork",
        "*Item_AlternatingCurrent*": "Alternating Current",
        "*Item_DragonbloodContract*": "Dragonblood Contract"
    }

    if item_name in items:
        return items[item_name]

    else:
        return item_name.replace("*", "")


def matchTelemetryDict(matchData, ign="$random$"):
    """Sort a matches telemetry data by minute.

    :param matchData: Match data.
    :param ign: In-game name of player we are looking at; "$random$", to pick a random player.
    :return: A dictionary with telemetry data sorted by minutes; Index -1: summary of match, Index -2: info on player we are looking at.

    """

    try:

        # DATA
        matchId = matchData["id"]
        gameMode = str(giveGameModeVG(matchData["gameMode"]))
        telemetryData = api.telemetry(matchData["telemetry"]["URL"])

        # FOR DEBUGGING
        # print("TELEMETRY DATA:   " + str(telemetryData))

        extraInfo = {
            "ign": ign,
            "actor": "Unknown",
            "skillTier": "Unknown",
            "karma": "Unknown",
            "winner": None,
            "matchId": matchId,
            "gameMode": gameMode,
            "side": "Left"
        }

        playersInfo = {}

        num = 0
        randomNum = random.randint(0, 6)

        # FOR DEBUGGING
        # print("RANDOM NUM:   " + str(randomNum))

        # Retrieve players data from match data
        for roster in matchData["rosters"]:
            playersInfo[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])] = {}

            for participant in roster["participants"]:

                # Get data of player we're looking at
                if ign == "$random$" and num == randomNum:
                    extraInfo["ign"] = str(participant["player"]["name"])
                    extraInfo["actor"] = cleanHeroName(participant["actor"])
                    extraInfo["skillTier"] = str(giveSkillTierVG(participant["skillTier"]))
                    extraInfo["karma"] = str(giveKarmaVG(participant["karmaLevel"]))
                    extraInfo["winner"] = participant["winner"]
                    if roster["side"] == "left/blue":
                        extraInfo["side"] = "Left"
                    else:
                        extraInfo["side"] = "Right"

                elif participant["player"]["name"] == ign:
                    extraInfo["actor"] = cleanHeroName(participant["actor"])
                    extraInfo["skillTier"] = str(giveSkillTierVG(participant["skillTier"]))
                    extraInfo["karma"] = str(giveKarmaVG(participant["karmaLevel"]))
                    extraInfo["winner"] = participant["winner"]
                    if roster["side"] == "left/blue":
                        extraInfo["side"] = "Left"
                    else:
                        extraInfo["side"] = "Right"


                playersInfo[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])] = {

                    "skillTier": str(giveSkillTierVG(participant["skillTier"])),
                    "karma": str(giveKarmaVG(participant["karmaLevel"])),
                    "level": str(participant["player"]["level"]),
                    "actor": str(cleanHeroName(participant["actor"])),
                    "kills": str(participant["kills"]),
                    "assists": str(participant["assists"]),
                    "deaths": str(participant["deaths"]),
                    "farm": str(round(participant["farm"], 2)),
                    "items": " - "

                }

                for item_name in participant["items"]:
                    playersInfo[str(roster["side"]) + " - Winner: " + str(roster["participants"][0]["winner"])][str(participant["player"]["name"])]["items"] += str(cleanItemName(item_name)) + " - "

                num += 1

        if extraInfo["actor"] == "Unknown":
            return False

        key1 = telemetryData[0]
        key2 = telemetryData[-1]

        # API time
        keyTimeOne = str(key1["time"])
        keyTimeTwo = str(key2["time"])

        # FOR DEBUGGING
        # print("Key One:   " + str(key1))
        # print("First Event Time:   " + str(key_time1))
        # print("Key Two:   " + str(key2))
        # print("Last Event Time:   " + str(key_time2))

        # Python time
        keyTimeOne = datetime.datetime.strptime(keyTimeOne, "%Y-%m-%dT%H:%M:%S%z")
        keyTimeTwo = datetime.datetime.strptime(keyTimeTwo, "%Y-%m-%dT%H:%M:%S%z")

        # FOR DEBUGGING
        # print("\n")
        # print("Python Time 1:   " + str(key_time1))
        # print("Python Time 2:   " + str(key_time2))

        time = (keyTimeTwo - keyTimeOne).seconds

        # FOR DEBUGGING
        # print("\n")
        # print("Match Time:   " + str(time / 60).replace(".", ":"))

        currentTime = 1
        data = {-2: extraInfo, -1: playersInfo, 0: []}
        for event in telemetryData:

            # Check if event is relevant | event["type"] == "SellItem" event["type"] == "LevelUp"
            if event["type"] == "PlayerFirstSpawn" or event["type"] == "LearnAbility" or event["type"] == "GoldFromTowerKill" or event["type"] == "GoldFromGoldMine" or event["type"] == "GoldFromKrakenKill" or event["type"] == "DealDamage" or event["type"] == "EarnXP":
                continue

            else:
                # Get the current even time relevant to first event time
                event_time = (datetime.datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%S%z") - keyTimeOne).seconds / 60

                # FOR DEBUGGING
                # print("\nEVENT:   " + str(event) + "\nEVENT TIME:   " + str(event_time).replace(".", ":"))
                # print("CURRENT EVENT TIME LINE:   " + str(event_timeline))
                if event_time >= currentTime:
                    # print("XXX>   EVENT TIME:   " + str(event_time) + " IS GREATER THAN CURRENT TIME:   " + str(current_time) + "   <XXX")

                    data[currentTime] = []
                    currentTime += 1

                data[(currentTime - 1)].append(event)

        # print("\n")
        # print("EVENT TIME LINE:   " + str(event_timeline))
        # print("SIZE OF EVENT TIME LINE:   " + str(len(event_timeline)))
        # total_events = 0
        # for event_group in data:
        #     # print("EVENT " + str(event_group) + ":   " + str(len(event_timeline[event_group])))
        #
        #     total_events += len(data[event_group])

        # print("CAPTURED:   " + str(total_events) + " / " + str(len(telemetry_json)))

        # FOR DEBUGGING
        # with open("test.json", "w") as handler:
        #     json.dump(data, handler)
        # print("!!!SAVED TELEMETRY JSON!!!")

        return data

    except Exception as e:
        print("ERROR:   " + str(e))
        pass


def matchTimeLine(matchData, ign="$random$"):
    """Gives you a time line of the matches telemetry.

    :param matchData: Match data.
    :param ign: In-game name of player we are looking at; "$random$", to pick a random player.
    :return: A dictionary with telemetry data sorted by minutes.

    """

    # DATA
    matchId = matchData["id"]
    gameMode = str(giveGameModeVG(matchData["gameMode"]))
    telemetryData = api.telemetry(matchData["telemetry"]["URL"])

    # FOR DEBUGGING
    # print("TELEMETRY DATA:   " + str(telemetryData))

    key1 = telemetryData[0]  # First event of match
    key2 = telemetryData[-1]  # Second event of match

    # API time
    key_time1 = str(key1["time"])
    key_time2 = str(key2["time"])

    # FOR DEBUGGING
    # print("Key One:   " + str(key1))
    # print("First Event Time:   " + str(key_time1))
    # print("Key Two:   " + str(key2))
    # print("Last Event Time:   " + str(key_time2))

    # Python time
    key_time1 = datetime.datetime.strptime(key_time1, "%Y-%m-%dT%H:%M:%S%z")
    key_time2 = datetime.datetime.strptime(key_time2, "%Y-%m-%dT%H:%M:%S%z")

    # FOR DEBUGGING
    # print("Python Time 1:   " + str(key_time1))
    # print("Python Time 2:   " + str(key_time2))

    time = (key_time2 - key_time1).seconds

    # FOR DEBUGGING
    # print("Match Time:   " + str(time / 60).replace(".", ":"))

    current_time = 1
    event_timeline = {0: []}
    for event in telemetryData:

        # Check if event is relevant
        if event["type"] in ["HeroBan", "HeroSelect", "HeroSkinSelect", "HeroSwap", "PlayerFirstSpawn", "LevelUp", "LearnAbility", "DealDamage", "EarnXP", "GoldFromTowerKill", "GoldFromGoldMine", "GoldFromKrakenKill", "SellItem"]:
            pass

        else:
            # Get the current even time relevant to first event time
            event_time = (datetime.datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%S%z") - key_time1).seconds / 60

            # FOR DEBUGGING
            # print("\nEVENT:   " + str(event) + "\nEVENT TIME:   " + str(event_time).replace(".", ":"))
            # print("CURRENT EVENT TIME LINE:   " + str(event_timeline))
            if event_time >= current_time:
                # print("XXX>   EVENT TIME:   " + str(event_time) + " IS GREATER THAN CURRENT TIME:   " + str(current_time) + "   <XXX")

                event_timeline[current_time] = []
                current_time += 1

            event_timeline[(current_time - 1)].append(event)

    # FOR DEBUGGING
    # print("EVENT TIME LINE:   " + str(event_timeline))
    # print("SIZE OF EVENT TIME LINE:   " + str(len(event_timeline)))
    total_events = 0
    for event_group in event_timeline:
        # print("EVENT " + str(event_group) + ":   " + str(len(event_timeline[event_group])))

        total_events += len(event_timeline[event_group])

    # FOR DEBUGGING
    # print("CAPTURED:   " + str(total_events) + " / " + str(len(telemetry_json)))

    return event_timeline


def giveActorsRoleList(actorName):
    """Gives you default position and role of a actor.

    :param actorName: Actors name to retrive their position and role.
    :return: A list with actor position at index 0, and actor role at index 1; ["Unknown", "Unknown"] if actor isn't found.

    """

    actorName = str(actorName).replace("*", "")

    actorRoles = {
        "Adagio": ["Lane", "Protector"],
        "Alpha": ["Jungle", "Warrior"],
        "Ardan": ["Captain", "Protector"],
        "Baptiste": ["Jungle", "Mage"],
        "Baron": ["Lane", "Sniper"],
        "Blackfeather": ["Lane", "Assassin"],
        "Catherine": ["Captain", "Protector"],
        "Celeste": ["Lane", "Mage"],
        "Flicker": ["Jungle", "Protector"],
        "Fortress": ["Jungle", "Protector"],
        "Glaive": ["Jungle", "Warrior"],
        "Grumpjaw": ["Jungle", "Warrior"],
        "Gwen": ["Lane", "Sniper"],
        "Krul": ["Jungle", "Warrior"],
        "Skaarf": ["Lane", "Mage"],
        "Rona": ["Jungle", "Warrior"],
        "Idris": ["Jungle", "Assassin"],
        "Joule": ["Jungle", "Warrior"],
        "Kestrel": ["Lane", "Sniper"],
        "Koshka": ["Jungle", "Assassin"],
        "Lance": ["Captain", "Protector"],
        "Lyra": ["Captain", "Protector"],
        "Ozo": ["Jungle", "Assassin"],
        "Petal": ["Jungle", "Sniper"],
        "Phinn": ["Captain", "Protector"],
        "Reim": ["Jungle", "Mage"],
        "Ringo": ["Lane", "Sniper"],
        "Samuel": ["Lane", "Mage"],
        "SAW": ["Lane", "Sniper"],
        "Taka": ["Jungle", "Assassin"],
        "Skye": ["Lane", "Sniper"],
        "Vox": ["Lane", "Sniper"],
        "Grace": ["Captain", "Protector"]
    }

    if actorName in actorRoles:
        return actorRoles[actorName]

    else:
        return ["Unknown", "Unknown"]


# NOTE!
# BOT MUST BE IN SERVERS WITH CUSTOM EMOJIS TO MAKE USE OF THEM!

def itemToEmojiVG(item_name):
    """Given the item name turn it into a emoji string.

    :param item_name: String to make pretty
    :returns: String either the same string without * or a emoji version of the string

    """

    item_name = str(cleanItemName(item_name)).lower()

    items = {

        "poisoned shiv": "<:048:333992835558932491>",
        "nullwave gauntlet": "<:044:333992835571515422>",
        "crystal bit": "<:016:333992823571480577>",
        "piercing spear": "<:047:333992834094989312>",
        "clockwork": "<:012:333992833591541761>",
        "minions foot": "<:043:333992830122852352>",
        "minion candy": "<:042:333992821415608321>",
        "book of eulogies": "<:008:333992830655791105>",
        "kinetic shield": "<:035:333992829376397313>",
        "lucky strike": "<:040:333992829909204993>",
        "lifespring": "<:037:333992834627534860>",
        "aftershock": "<:002:333992807050248194>",
        "fountain of renewal": "<:026:333992832249495555>",
        "echo": "<:020:333992835080650762>",
        "heavy steel": "<:031:333992824792023061>",
        "journey boots": "<:034:333992829456089088>",
        "flare": "<:024:333992819406667779>",
        "protector contract": "<:050:333992835407937537>",
        "breaking point": "<:009:333992831016370178>",
        "piercing shard": "<:046:333992834090795009>",
        "halcyon chargers": "<:028:333992834724003843>",
        "crystal infusion": "<:017:333992831448383489>",
        "barbed needle": "<:005:333992830835884032>",
        "coat of plates": "<:013:333992831360303106>",
        "dragonblood contract": "<:018:333992834938175488>",
        "energy battery": "<:022:333992823999168515>",
        "atlas pauldron": "<:004:333992822573105172>",
        "hourglass": "<:032:333992825282887681>",
        "aegis": "<:001:333992796648374277>",
        "frostburn": "<:027:333992833646198787>",
        "alternating current": "<:003:333992822430760970>",
        "heavy prism": "<:030:333992832199294978>",
        "flaregun": "<:025:333992835185377280>",
        "crucible": "<:015:333992831448252417>",
        "broken myth": "<:010:333992831091867650>",
        "chronograph": "<:011:333992831549046785>",
        "metal jacket": "<:041:333992832501022725>",
        "eve of harvest": "<:023:333992832278986753>",
        "ironguard contract": "<:033:333992835252748308>",
        "eclipse prism": "<:021:333992832203489280>",
        "blazing salvo": "<:006:333992817808506881>",
        "halcyon potion": "<:029:333992819939213314>",
        "light armor": "<:039:333992825580552193>",
        "bonesaw": "<:007:333992830475304962>",
        "light shield": "<:039:333992825580552193>",
        "contraption": "<:014:333992834245984257>",
        "pot of gold": "<:049:333992835592355840>",
        "oakheart": "<:045:333992826360823808>",
        "level juice": "<:036:333992834900164609>",
        "dragonheart": "<:019:333992831817613312>",
        "tyrants monocle": "<:066:333994046269685761>",
        "stormcrown": "<:060:333994046622007297>",
        "sorrowblade": "<:058:333994045405659137>",
        "six sins": "<:056:333994045540007937>",
        "reflex block": "<:051:333994032684597249>",
        "war treads": "<:069:333994046571937794>",
        "weapon blade": "<:070:333994043451113474>",
        "slumbering husk": "<:057:333994046492114949>",
        "weapon infusion": "<:071:333994047444090882>",
        "tension bow": "<:063:333994045707780108>",
        "scout trap": "<:052:333994025453617154>",
        "travel boots": "<:065:333994044655009802>",
        "tornado trigger": "<:064:333994044545957888>",
        "shatterglass": "<:054:333994043342061568>",
        "sprint boots": "<:059:333994042079576070>",
        "void battery": "<:068:333994046131273729>",
        "shiversteel": "<:055:333994044894085122>",
        "swift shooter": "<:062:333994039667851266>",
        "stormguard banner": "<:061:333994046043455489>",
        "serpent mask": "<:053:333994044868919296>"

    }

    if item_name in items:
        return items[item_name]

    else:

        # FOR DEBUGGING
        print("HERO EMOJI NOT FOUND: " + item_name)

        return item_name.title()


def skillTierToEmoji(skillTier):
    """Give emojis representation of skill tier."""

    skillTier = str(skillTier)

    skillTiers = {

        "-1": "<:0_1:336227076829085696>",
        "0": "<:000:336226975272402944>",
        "1": "<:001:336227011280502785>",
        "2": "<:002:336227043328917505>",
        "3": "<:003:336226960160194561>",
        "4": "<:004:336226957731692545>",
        "5": "<:005:336226984524775424>",
        "6": "<:006:336227024077062154>",
        "7": "<:007:336227024136044545>",
        "8": "<:008:336227074534539265>",
        "9": "<:009:336227159607738370>",
        "10": "<:010:336227183351824385>",
        "11": "<:011:336227244152193024>",
        "12": "<:012:336227304269414400>",
        "13": "<:013:336227315086524417>",
        "14": "<:014:336227388843229184>",
        "15": "<:015:336227345025466369>",
        "16": "<:016:336227320484593664>",
        "17": "<:017:336227408585818112>",
        "18": "<:018:336227421076324352>",
        "19": "<:019:336227420728328192>",
        "20": "<:020:336227428525408259>",
        "21": "<:021:336227370841407488>",
        "22": "<:022:336227348452081674>",
        "23": "<:023:336227431885176846>",
        "24": "<:027:336227435064328202>",
        "25": "<:028:336227413413462017>",
        "26": "<:029:336227446691069952>",
        "27": "<:024:336227371659296780>",
        "28": "<:025:336227396426399754>",
        "29": "<:026:336227453251092480>"

    }

    if skillTier in skillTiers:
        return skillTiers[skillTier]

    else:
        # FOR DEBUGGING
        print("SKILL TIER EMOJI NOT FOUND: " + skillTier)

        return giveSkillTierVG(skillTier)


def karmaToEmoji(karma):
    """Gives emoji representation of karma."""

    karma = str(karma)

    karmas = {

        "0": "<:bad:324670994797166592>",
        "1": "<:good:324670994553765890>",
        "2": "<:great:324670995027853312>",

    }

    if karma in karmas:
        return karmas[karma]

    else:
        # FOR DEBUGGING
        print("KARMA EMOJI NOT FOUND: " + karma)

        return giveKarmaVG(karma)


def heroToEmoji(hero):
    """Gives emoji representation of hero."""

    hero = str(hero).lower().replace("*", "")

    heros = {

        "adagio": "<:001:334004905742303232>",
        "alpha": "<:002:334004937920872449>",
        "ardan": "<:003:334004940840108032>",
        "baptiste": "<:004:334004937442852864>",
        "baron": "<:005:334004940424871947>",
        "blackfeather": "<:006:334004948301774858>",
        "catherine": "<:007:334004945005051925>",
        "celeste": "<:008:334004952844468237>",
        "flicker": "<:009:334004991239127040>",
        "fortress": "<:010:334004995726770187>",
        "glaive": "<:011:334004989187981312>",
        "grace": "<:012:334004996330749952>",
        "grumpjaw": "<:013:334004993449263104>",
        "gwen": "<:014:334004996536401925>",
        "idris": "<:015:334004993981939713>",
        "joule": "<:016:334004994162294795>",
        "kestrel": "<:017:334004994694971392>",
        "koshka": "<:018:334080530813419522>",
        "krul": "<:019:334004995563323395>",
        "lance": "<:020:334004994346844161>",
        "lyra": "<:021:334004996267966465>",
        "ozo": "<:022:334004996205182980>",
        "petal": "<:023:334004994292449280>",
        "phinn": "<:024:334004995324379136>",
        "reim": "<:025:334004995949330432>",
        "ringo": "<:026:334004992958529536>",
        "rona": "<:027:334004996473356310>",
        "samuel": "<:028:334004991025086464>",
        "saw": "<:029:334004995848405004>",
        "skaarf": "<:030:334004993642332160>",
        "skye": "<:031:334004990991663104>",
        "taka": "<:032:334004995961782272>",
        "vox": "<:034:334004996985323520>",
        "reza": "<:35:344582697945137152>"

    }

    if hero in heros:
        return heros[hero]

    else:
        # FOR DEBUGGING
        print("HERO EMOJI NOT FOUND: " + hero)

        return hero.title()


def giveFormat(value, type="", format=False):
    """Format the value according to it's type.

    :param value: Value to format; String or integer.
    :param type: What the value represents.
    :param format: False, clean up the given value; True, value to emoji.
    :returns: String; value in the correct format.

    """

    # TODO HERO ABILITIES AND TALENTS

    if type == "hero":
        if format == True:
            return heroToEmoji(value)

        else:
            return cleanHeroName(value)

    elif type == "item":
        if format == True:
            return itemToEmojiVG(value)

        else:
            return cleanItemName(value)

    elif type == "skillTier":
        if format == True:
            return skillTierToEmoji(value)

        else:
            return giveSkillTierVG(value)

    elif type == "karma":
        if format == True:
            return karmaToEmoji(value)

        else:
            return giveKarmaVG(value)

    else:
        return str(value).replace("*", "")
