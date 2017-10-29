"""Global Variables

    Variables used throughout the bot.

"""

import os

# String directory from which bot is running.
directory = str(os.path.dirname(os.path.realpath(__file__))).replace('\\', "//")  # Path to working directory

# FOR DEBUGGING
# Prints where this bot is running from.
print("WORKING DIRECTORY: " + str(directory) + "\n---")

# Bot Variables XXXXXXXX---XXXXXXXX
# Discord API key, get yours here, https://discordapp.com/developers/docs/intro.
BOT_KEY = ""

# General Bot Data XXXX---XXXX
# A count of how many members the bot has; this has been done so that on large scale operations, with 1000+ of users the count won't take several minutes; and will only be done every so often(eg. every twelve hours).
# updated - time stamp ~ Last time this count has been done.
# count - integer ~ Number of members.
member_count = {
    "updated": None,
    "count": 0
}
discord_reports_channel = "[DISCORD CHANNEL ID]"  # A Channel's ID to which the bot will send user reports to; bot has to have access to it.
discord_logs_channel = "[DISCORD CHANNEL ID]"  # A Channel's ID to which the bot will send logs to; bot has to have access to it.
# A list of Discord IDs that belong to the bot owners.
owners = [
    "[DISCORD USER ID]"
]
# List of command modules loaded by the bot.
command_modules = [
    "src.bot_work.commands",
    "src.vainglory_work.commands",
    "src.mongo_work.commands"
]
# List of commands used in the bot.
commands = [
    "savevg",
    "player",
    "compareP",
    "compareUp",
    "latest",
    "match",
    "matches",
    "compareM",
    "telemetry",
    "stats",
    "compareS",
    "vlb",
    "top",
    "vainglorycharms",
    "userInfo",
    "serverInfo",
    "gifs"
]
server_data = {}  # Discord server's data. (?NOT USED ANYMORE?)
user_data = {}  # Discord user's data. (?NOT USED ANYMORE?)

# Config Bot Data XXXX---XXXX
default_prefix = "$"  # Prefix used by the bot to identify commands(eg. $help).
bot_name = "Computer"  # Bot's name.
bot_description = str(bot_name) + " made possible with love, Python, Discord API, and GameLocker API! :3"
bot_icon = "[URL]"  # URL to bots user icon(eg. png, jpg, etc.).
bot_server = "[URL]"  # URL to bots server.
bot_invite = "[URL]"  # URL from you can invite this bot.
bot_docs = "[URL]"  # URL to bots docs.
bot_docs_rep = "[URL]"  # URL to bots docs repository.
bot_donation = "[URL]"  # URL to donation page.
bot_embed_footer = "Made possible with love, Python, Discord API, and GameLocker API! :3"  # Footer used by default in embeds.

# Ad's Data XXXX---XXXX
# Embed ads which are promoted in chat, Discord, by the bot. They are promoted as independent embeds after a bots response.
# Embed Ad Structure:
# {
# "[ADD NAME]" : {
#   views : Boolean/Integer ~ Amount of views this ad has left before being removed; False, this ad is infinite; Integer, number of views left.
#   time : Integer ~ Ad break server gets after viewing this ad.
#   title : String ~ Title of the ad.
#   url : String ~ URL this ad is linked to.
#   description : String ~ Text content of this ad.
#   img : String ~ URL to a image shown with this ad.
#   }
# }
ads_embed = {
    "Computer": {
        "views": False,
        "time": 60,
        "title": "Computer",
        "url": "http://discord.me/ComputerBot",
        "description": "Thank you for choosing the ComputerBot! :smile:", "img": "http://i64.tinypic.com/2q24gsj.jpg"
    }
}
# Text ads which are promoted in chat, Discord, by the bot. They are promoted at the bottom of almost every embed, expect embed ads.
# Text Ad Structure:
# {
# "[ADD NAME]" : {
#   views : Boolean/Integer ~ Amount of views this ad has left before being removed; False, this ad is infinite; Integer, number of views left.
#   text : String ~ Content of this ad.
#   }
# }
ads_text = {
    "Computer": {
        "views": False,
        "text": "Thank you for choosing ComputerBot :3"
    }
}
ads_queue = {}  # Servers that are in a ad break.
ads_excluded = {}  # Servers that are excluded from ads, for reasons like donating, etc.

# Lottery's Data XXXX---XXXX
# Lottery settings; default.
# on : Boolean - True ~ Weather lottery is running or not.
# timeOut : Integer - 90 ~ Amount of time a user is in cool down before winning lottery again; in minutes.
# iceRate : Integer - 1000 ~ Rate by which a user has of winning ICE, a VainGlory in-game premium currency.
# iceAmount : Integer - 250 ~ Amount of ICE, a VainGlory in-game premium currency, a user wins.
lottery_settings = {
    "on": True,
    "timeOut": 90,
    "iceRate": 1000,
    "iceAmount": 250
}
lottery_queue = {}  # Users who have already won the lottery, and are in cool down.
lottery_excludes = []  # Users who should be excluded from the lottery, for reasons like abuse, cheating, etc.

# Mongo XXXXXXXX---XXXXXXXX
mongo_version = "Main"  # Database version(eg. Main, Test, etc.)
mongo_host = None  # Mongo data base ip     |   local-host/127.0.0.1: None       |    Bo's Host: Unknown
mongo_port = None  # Mongo data base port   |   local-port/54811(maybe?): None   |    Bo's Port: Unknown

# Vainglory XXXXXXXX---XXXXXXXX
# Vainglory GameLocker API key, get yours here, https://developer.vainglorygame.com/.
VG_KEY = ""
