import config
import discord
import pickle
from discord.ext import commands
from src.mongo_work import core as db
from traceback import format_exc
from src.bot_work import core

# Load pickles XXXXXXXX---XXXXXXXX
try:

    with open(config.directory + "//pickle-db//embedAds.pickle", "rb") as handler:
        config.ads_embed = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN EMBED ADS HAVE BEEN LOADED
    print("!!!EMBED ADS HAVE BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN EMBED ADS ISN'T ABLE TO BE LOADED
    print("!!!COULDN'T LOAD EMBED ADS!!!")

try:

    with open(config.directory + "//pickle-db//textAds.pickle", "rb") as handler:
        config.ads_text = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN TEXT ADS HAVE BEEN LOADED
    print("!!!TEXT ADS HAVE BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN TEXT ADS ISN'T ABLE TO BE LOADED
    print("!!!COULDN'T LOAD TEXT ADS!!!")

try:

    with open(config.directory + "//pickle-db//whiteListServersAds.pickle", "rb") as handler:
        config.ads_queue = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN WHITE LIST SERVERS ADS HAS BEEN LOADED
    print("!!!WHITE LIST SERVERS HAVE BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN WHITE LIST SERVERS ADS ISN'T ABLE TO BE LOADED
    print("!!!COULDN'T LOAD WHITE LIST SERVER ADS!!!")

try:

    with open(config.directory + "//pickle-db//excludedListServersAds.pickle", "rb") as handler:
        config.ads_excluded = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN EXCLUDED SERVERS HAS BEEN LOADED
    print("!!!EXCLUDED SERVERS HAVE BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN EXCLUDED SERVERS ADS ISN'T ABLE TO LOADED
    print("!!!COULDN'T LOAD EXCLUDED SERVER ADS!!!")

try:

    with open(config.directory + "//pickle-db//lotterySettings.pickle", "rb") as handler:
        config.lottery_settings = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN LOTTERY SETTINGS HAS BEEN LOADED
    print("!!!LOTTERY SETTINGS HAS BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN LOTTERY SETTINGS ISN'T ABLE TO LOADED
    print("!!!COULDN'T LOAD LOTTERY SETTINGS!!!")

try:

    with open(config.directory + "//pickle-db//lotteryQueue.pickle", "rb") as handler:
        config.lottery_queue = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN LOTTERY QUEUE HAS BEEN LOADED
    print("!!!LOTTERY QUEUE HAS BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN LOTTERY QUEUE ISN'T ABLE TO BE LOADED
    print("!!!COULDN'T LOAD LOTTERY QUEUE!!!")

try:

    with open(config.directory + "//pickle-db//lotteryExcluded.pickle", "rb") as handler:
        config.lottery_excludes = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN LOTTERY EXCLUDED HAS BEEN LOADED
    print("!!!LOTTERY EXCLUDED HAS BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN LOTTERY EXCLUDED ISN'T ABLE TO BE LOADED
    print("!!!COULDN'T LOAD LOTTERY EXCLUDED!!!")

try:

    with open(config.directory + "//pickle-db//memberCount.pickle", "rb") as handler:
        config.member_count = pickle.load(handler)

    # FOR DEBUGGING
    # PRINT WHEN MEMBER COUNT HAS BEEN LOADED
    print("!!!MEMBER COUNT HAS BEEN LOADED!!!")

except:
    # FOR DEBUGGING
    # PRINT WHEN MEMBER COUNT ISN'T ABLE TO BE LOADED
    print("!!!COULDN'T LOAD MEMBER COUNT!!!")


# START BOT CODE   <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
bot = commands.Bot(command_prefix=str(config.default_prefix), description=str(config.bot_description))


@bot.event
async def on_ready():
    """When the bot is ready to function and serve users."""
    # FOR DEBUGGING
    # PRINT BOT'S NAME AND BOT'S USER ID
    print('\nLogged In As:   ' + bot.user.name + " |ID:   " + bot.user.id + "\n\n")  # PRINT the IDENTIFIERS of the BOT

    # Setup the bot's playing status.
    await bot.change_presence(game=discord.Game(name=str(config.default_prefix) + "help"))


@bot.event
async def on_message(message):
    """Whenever a message is inputted via Discord chat."""

    # If this is a bot don't process the commands, to prevent spam.
    if message.author.bot == True:
        return

    try:
        # Fetch the prefix via the server's ID.
        prefix = db.discordServerDictionary(message.server.id)
        # If no server data is found assume prefix to be default.
        if prefix == False:
            prefix = str(config.default_prefix)
        else:
            try:
                prefix = prefix["general"]["prefix"]
            except:
                prefix = str(config.default_prefix)

        bot.command_prefix = [prefix]  # Use the fetched prefix as server prefix
    except:
        bot.command_prefix = [str(config.default_prefix)]  # Use default prefix as server prefix

    # Send the message to be processed by the bot
    await bot.process_commands(message)


@bot.event
async def on_command_error(event, *args, **kwargs):
    """Whenever the bot experiences an error(eg. command not found)."""

    raw = args[0]

    # Check if this error came from a private channel(eg. direct message).
    if raw.message.channel.is_private == True:
        return

    # Fetches the servers data with the server's ID.
    data = db.discordServerDictionary(raw.message.server.id)

    # If no server data is found then return.
    if data in [False, None]:
        return

    # If server data is found, but no custom commands were found then return.
    elif data["general"]["customCommands"] == {}:
        return

    # Get the first word after the prefix; this would in theory be a "custom command".
    command_name = str(list(str(raw.message.content).split(" "))[0]).replace(data["general"]["prefix"], "")

    # If command_name is one of the servers custom command do the following.
    if command_name in data["general"]["customCommands"]:
        # If custom command responds should be sent to the server
        if data["general"]["customCommands"][command_name]["destination"] == "here":
            if data["general"]["botChannel"] != False:
                # Get a channel object from what's in bot channel
                destination = bot.get_channel(data["general"]["botChannel"])

                # Send to wherever called from if a bot cannot find channel
                if destination in [False, None]:
                    destination = raw.message.channel

            else:
                # Send to wherever called from if a bot channel is not setup
                destination = raw.message.channel

        # If custom command responds should be sent to the authors pm
        else:
            destination = raw.message.author

        msg_object = data["general"]["customCommands"][command_name]

        # Add necessary stuff
        msg_object["from"] = str(raw.message.server)
        try:
            msg_object["to"] = raw.message.author.mention
        except:
            msg_object["to"] = str(raw.message.author)

        # Send response as embed
        if msg_object["embed"] == True:
            await bot.send_message(destination, embed=core.generateAnnouncement(msg_object))

        # Send response as markdown
        else:
            await bot.send_message(destination, core.generateAnnouncement(msg_object))

@bot.event
async def on_server_remove(server):
    """Whenever a server removes the bot."""

    try:

        if db.removeDiscordServer(server.id) == False:
            # FOR DEBUGGING
            # PRINT WHEN A SERVER HAS REMOVED THE BOT FROM ITSELF, AND SUCCESSFULLY FROM DB DB
            print("!!!" + str(server) + " SERVER DATA WASN'T REMOVED!!!")

        else:
            # FOR DEBUGGING
            # PRINT WHEN A SERVER HAS REMOVED THE BOT FROM ITSELF, AND UNSUCCESSFULLY FROM OUR DB
            print("!!!REMOVED " + str(server) + " SERVER DATA!!!")

        # Either way send this message to the owner of the server.
        await bot.send_message(server.owner, "I've been **successfully removed** from your server, **" + str(server) + "**, have a great day! :wave:")

    except:
        # FOR DEBUGGING
        # PRINT WHEN REMOVING A SERVER CAUSED AN ERROR
        print("!!!SOMETHING WENT WRONG WHILE REMOVING " + str(server) + " SERVER DATA!!!\nERROR:\n" + str(format_exc()))


@bot.event
async def on_server_join(server):
    """Whenever a server adds the bot."""

    try:

        if db.addDiscordServer(server.id) == False:
            await bot.send_message(server.owner, "**Something went wrong** while **joining your server, " + str(server) + ",** you might want to **re-invite me!** :grimacing:")
            return

        await bot.send_message(server.owner, "I've successfully **joined your server, " + str(server) + ",** thank you for choosing *ComputerBot*! :smile:\nFor a list of commands enter **" + config.default_prefix + "help** or visit the bots **docs**, " + config.bot_docs + ".\nYou can also **configure me on your server** with the **server commands** take a look at them with **" + config.default_prefix + "help server**")

    except:
        # FOR DEBUGGING
        # PRINT WHEN ADDING A SERVER CAUSED AN ERROR
        print("!!!SOMETHING WENT WRONG WHILE TRYING TO ADD " + str(server) + " SERVER DATA!!!\nERROR:\n" + str(format_exc()))


@bot.event
async def on_member_join(member):
    """Whenever a user joins a server."""

    data = db.discordServerDictionary(member.server.id)

    # If no data, in our DB, is found on the server.
    if data in [False, None]:
        return

    elif data["general"]["memberJoin"] == {}:
        return

    else:
        # FOR DEBUGGING
        # print("MEMBER JOIN EVENTS: " + str(data["general"]["memberJoin"]))

        if "announce" in data["general"]["memberJoin"]:
            # FOR DEBUGGING
            # print("!!!ANNOUNCING THE NEW MEMBER!!!")

            # Destination to send to
            if data["general"]["memberJoin"]["announce"]["destination"] != "pm":
                # Get a channel object from what's in destination
                destination = bot.get_channel(data["general"]["memberJoin"]["announce"]["destination"])

                # Send to servers general chat if a bot cannot find channel
                if destination in [False, None]:
                    destination = member.server

            # If should be sent to members pms
            else:
                destination = member

            # FOR DEBUGGING
            # print("DESTINATION: " + str(destination))

            msg_object = data["general"]["memberJoin"]["announce"]

            # FOR DEBUGGING
            # print("MEMBER DIR: " + str(dir(member)))

            msg_object["from"] = str(member.server)
            msg_object["to"] = member.mention

            # FOR DEBUGGING
            # print("MSG OBJECT: " + str(msg_object))

            if msg_object["embed"] == True:
                await bot.send_message(destination, embed=core.generateAnnouncement(msg_object))

            else:
                await bot.send_message(destination, core.generateAnnouncement(msg_object))

        if "giveRole" in data["general"]["memberJoin"]:
            # FOR DEBUGGING
            # print("!!!GIVING ROLE TO NEW MEMBER!!!")

            giveRole = None
            for role in member.server.roles:
                if role.id == data["general"]["memberJoin"]["giveRole"]["role"]:
                    giveRole = role

                    # We got what we wanted so break
                    break

            if giveRole == None:
                # FOR DEBUGGING
                # print("!!!COULD NOT GIVE ROLE BECAUSE ROLE DOESN'T EXIST!!!")

                return

            # FOR DEBUGGING
            # print("GIVE ROLE: " + str(giveRole))

            try:

                await bot.add_roles(member, giveRole)

            except Exception as e:
                print("!!!CAN'T GIVE ROLE!!!\nERROR:\n" + str(e) + "\nFORMAT: " + str(format_exc()))


@bot.event
async def on_member_remove(member):
    """Whenever a user leaves a server."""

    # FOR DEBUGGING
    # print("Member Leave:\nMember: " + str(member))

    # FOR DEBUGGING
    # print("SERVER ID: " + str(member.server.id))

    data = db.discordServerDictionary(member.server.id)

    # FOR DEBUGGING
    # print("DATA: " + str(data))

    if data in [False, None]:
        # FOR DEBUGGING
        # print("!!!NO SERVER DATA!!!")

        return

    elif data["general"]["memberLeave"] == {}:
        # FOR DEBUGGING
        # print("!!!NO MEMBER LEAVE EVENTS!!!")

        return

    else:
        # FOR DEBUGGING
        # print("MEMBER LEAVE EVENTS: " + str(data["general"]["memberLeave"]))

        if "announce" in data["general"]["memberLeave"]:
            # FOR DEBUGGING
            # print("!!!ANNOUNCING THE LEAVING MEMBER!!!")

            # Destination to send to
            if data["general"]["memberLeave"]["announce"]["destination"] != "pm":

                # Get a channel object from what's in destination
                destination = bot.get_channel(data["general"]["memberLeave"]["announce"]["destination"])

                # Send to servers general chat if a bot cannot find channel
                if destination in [False, None]:
                    destination = member.server

            # If should be sent to members pms
            else:
                destination = member

            # FOR DEBUGGING
            # print("DESTINATION: " + str(destination))

            msg_object = data["general"]["memberLeave"]["announce"]

            msg_object["from"] = str(member.server)
            try:

                msg_object["to"] = member.mention

            except:
                msg_object["to"] = str(member)

            # FOR DEBUGGING
            # print("MSG OBJECT: " + str(msg_object))

            if msg_object["embed"] == True:

                await bot.send_message(destination, embed=core.generateAnnouncement(msg_object))

            else:
                await bot.send_message(destination, core.generateAnnouncement(msg_object))


@bot.event
async def on_channel_delete(channel):
    """Whenever a server deleted a channel."""

    try:

        server = channel.server

        # Get the servers data
        data = db.discordServerDictionary(server.id)

        # FOR DEBUGGING
        # print("SERVER DATA:   " + str(data))

        if data == False or data == None:
            # FOR DEBUGGING
            # print("!!!NO DATA ON " + str(server) + " A DISCORD SERVER!!!")

            return

        # FOR DEBUGGING
        # print("CHANNEL DELETED:   " + str(channel.id))
        # print("BOT CHANNEL:   " + str(data["general"]["botChannel"]))

        if channel.id == data["general"]["botChannel"]:
            # print("!!!SETTING BOT CHANNEL TO FALSE!!!")
            if db.updateDiscordServer(server.id, {"general.botChannel": False}) == False:
                # FOR DEBUGGING
                # print("!!!CAN'T UPDATE BOT SERVER CHANNEL!!!")

                return

            # Msg server owner about the update to the bot's channel
            await bot.send_message(server.owner, "Bot's **channel, " + str(channel) + ", in " + str(server) + " has been deleted** which means the **bot, " + config.bot_name + ", will now respond from wherever it's called on...** :eyes:")

        else:
            # FOR DEBUGGING
            # print("!!!NOTHING TO CHANGE!!!")

            pass

        # Member join events
        if data["general"]["memberJoin"] == {}:
            # FOR DEBUGGING
            # print("!!!NO MEMBER JOIN EVENTS!!!")

            pass

        else:
            if "announce" in data["general"]["memberJoin"]:
                # FOR DEBUGGING
                # print("!!!THERE IS A ANNOUNCE JOINING MEMBER EVENT!!!")

                # Check if the announce event is on
                if data["general"]["memberLeave"]["announce"]["to"] == channel.id:
                    # FOR DEBUGGING
                    # print("MEMBER JOIN ANNOUNCEMENT CHANNEL IS REMOVED: " + str(channel))

                    pass

        # Member leave events
        if data["general"]["memberLeave"] == {}:
            # FOR DEBUGGING
            # print("!!!NO MEMBER LEAVE EVENTS!!!")

            pass

        else:
            if "announce" in data["general"]["memberLeave"]:
                # FOR DEBUGGING
                # print("!!!THERE IS A ANNOUNCE LEAVING MEMBER EVENT!!!")

                # Check if the announce event is on
                if data["general"]["memberLeave"]["announce"]["to"] == channel.id:
                    # FOR DEBUGGING
                    # print("MEMBER LEAVE ANNOUNCEMENT CHANNEL IS REMOVED: " + str(channel))

                    pass

        # FOR DEBUGGING
        # print("!!!SERVER " + str(server) + " DATA HAS BEEN UPDATED!!!")

    except Exception as e:
        # FOR DEBUGGING
        # print("!!!SOMETHING WENT WRONG WHILE TRYING TO UPDATE SERVERS DATA WITH THE " + str(channel) + " CHANNEL!!!\nERROR:\n" + str(e))

        return


@bot.event
async def on_server_role_delete(role):
    """Whenever a server role is removed."""

    try:

        # FOR DEBUGGING
        # print("Server Role Remove:\nRole: " + str(role))

        # FOR DEBUGGING
        # print("SERVER ID: " + str(role.server.id))

        data = db.discordServerDictionary(role.server.id)

        # FOR DEBUGGING
        # print("DATA: " + str(data))

        if data in [False, None]:
            # FOR DEBUGGING
            # print("!!!NO SERVER DATA!!!")

            return

        # Member joins events
        if data["general"]["memberJoin"] == {}:
            # FOR DEBUGGING
            # print("!!!NO MEMBER JOINS EVENTS!!!")

            pass

        else:
            if "giveRole" in data["general"]["memberJoin"]:
                # FOR DEBUGGING
                # print("!!!THERE IS GIVE ROLE TO MEMBER JOINING EVENT!!!")

                # Check if it's the same id of the role that we give out
                if data["general"]["memberJoin"]["giveRole"]["role"] == role.id:
                    # FOR DEBUGGING
                    # print("SPECIFIED ROLE HAS BEEN REMOVED: " + str(role))

                    if db.updateDiscordServer(role.server.id, {"general.memberJoin.giveRole": 1}, mode="$unset") == True:
                        await bot.send_message(role.server.owner, "Role, **" + str(role) + "**, given to new members has been removed from server, **" + str(role.server) + "**, so we won't be giving it to new members anymore... :eyes:")

                    else:
                        await bot.send_message(role.server.owner, "Role, **" + str(role) + "**, given to new member has been removed from server, **" + str(role.server) + "**, and while trying to fix this up an error occurred which means on role giving to new members might be broken... :confused:\nContact the developers here:\n__**" + str(config.bot_server) + "**__")


    except Exception as e:
        # FOR DEBUGGING
        # print("!!!SOMETHING WENT WRONG WHILE TRYING TO UPDATE SERVER DATA WITH " + str(role).upper() + " ROLE!!!\nERROR:\n" + str(e))

        return


if __name__ == "__main__":
    """Load and run the bot if this is the executed file"""

    print("!!!LOADING EXTENSION COMMANDS!!!")
    for extension in config.command_modules:
        try:  # Load extension commands in other command modules
            bot.load_extension(extension)

            print("!!!" + str(extension) + " HAS BEEN LOADED!!!")

        except Exception as e:  # If there is an error print it
            print("!!!" + str(extension) + " WAS NOT LOADED!!!\nREASON:\n" + str(e) + "\n---\n" + str(format_exc()))

    print("!!!ALL EXTENSION COMMANDS HAVE BEEN LOADED!!!")

    bot.run(config.BOT_KEY)  # Run the bot
