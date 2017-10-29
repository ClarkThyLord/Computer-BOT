import config
import discord


def generateAnnouncement(msg_object):
    """Generate a announcement.

    :parameter msg_object: A dictionary with the following format: {"embed": [Boolean], "reason": [String], "from": [String], "msg": [String]}
    :returns: String or Embed Object; depends on msg.

    """

    if "embed" not in msg_object:
        msg_object["embed"] = True

    if "reason" not in msg_object:
        msg_object["reason"] = str(config.bot_name) + " Event"

    if "from" not in msg_object:
        msg_object["from"] = str(config.bot_name)

    if "to" not in msg_object:
        msg_object["to"] = "User"

    if "msg" not in msg_object:
        msg_object["msg"] = "/user/, hello from /server/!"

    # Add the mention at the start of msg if not found
    if "/user/" not in msg_object["msg"]:
        msg_object["msg"] = "/user/, " + msg_object["msg"]

    if msg_object["embed"] == True:
        result = discord.Embed(
            title=msg_object["reason"],
            colour=discord.Colour.orange(),
            url=config.bot_server,
            description=str(msg_object["msg"]).replace("/user/", msg_object["to"]).replace("/server/", msg_object["from"])
        )

    else:
        result = str(msg_object["msg"]).replace("/user/", msg_object["to"]).replace("/server/", msg_object["from"])

    return result
