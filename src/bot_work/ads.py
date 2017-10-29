import datetime
import discord
import config
import pickle
from random import randint
from src.extra import tools


def storeAds():
    ads_e = config.ads_embed
    ads_t = config.ads_text

    try:

        with open(config.directory + "//pickle-db//embedAds.pickle", "wb") as handler:
            pickle.dump(ads_e, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("EMBED ADS SAVED:   " + str(ads_e))

    except Exception as e:
        print("!!!COULDN'T SAVE EMBED ADS!!!\n" + str(e))

    try:

        with open(config.directory + "//pickle-db//textAds.pickle", "wb") as handler:
            pickle.dump(ads_t, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("TEXT ADS SAVED:   " + str(ads_t))

    except Exception as e:
        print("!!!COULDN'T SAVE TEXT ADS!!!\n" + str(e))


def storeServers():
    server_q = config.ads_queue
    server_e = config.ads_excluded

    try:

        with open(config.directory + "//pickle-db//whiteListServersAds.pickle", "wb") as handler:
            pickle.dump(server_q, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("WHITE LIST SERVERS SAVED:   " + str(server_q))

    except Exception as e:
        print("!!!COULDN'T SAVE WHITE LIST SERVER ADS!!!\n" + str(e))

    try:

        with open(config.directory + "//pickle-db//excludedListServersAds.pickle", "wb") as handler:
            pickle.dump(server_e, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("EXCLUDED SERVERS SAVED:   " + str(server_e))

    except Exception as e:
        print("!!!COULDN'T SAVE EXCLUDED SERVER ADS!!!\n" + str(e))


def checkEmbedAds(server_id):
    """Checks if a server is due for an embed ad.

    :param server_id: Discord server id
    :returns: Returns a ads id or False if server is not due for ad

    """

    if checkServerExcludeAds(server_id) == True:
        if config.ads_excluded[server_id]["expires"] != False:
            # Get the time stamp for now
            now = datetime.datetime.now()

            if ((now - config.ads_excluded[server_id]["time"]).seconds / 86400) > config.ads_excluded[server_id]["expires"]:

                includeServerAds(server_id)

                ad = giveEmbedAds()

                addServerQueueAds(server_id, ad[1])

                # FOR DEBUGGING
                # print("AD BEING SENT:   " + str(ad[0]))

                return ad[0]

            else:

                # FOR DEBUGGING
                # print("SERVER DOESN'T GET ADS")

                return False

    elif checkServerQueueAds(server_id) == True:
        # Get the time stamp for now
        now = datetime.datetime.now()

        if ((now - config.ads_queue[server_id]["time"]).seconds / 60) > config.ads_queue[server_id]["expires"]:

            ad = giveEmbedAds()

            addServerQueueAds(server_id, ad[1])

            # FOR DEBUGGING
            # print("AD BEING SENT:   " + str(ad[0]))

            return ad[0]

        else:
            # print("!!!SERVER ON AD BREAK!!!\nTIME:   " + str(((now - config.ad_servers_queue[server_id]["time"]).seconds / 60)) + " |END OF BREAk:  " + str(config.ad_servers_queue[server_id]["expires"]))

            return False

    else:

        ad = giveEmbedAds()

        addServerQueueAds(server_id, ad[1])

        # FOR DEBUGGING
        # print("AD BEING SENT:   " + str(ad[0]))

        return ad[0]


def checkTextAds(server_id):
    """Checks if a server is due for an text ad.

    :param server_id: Discord server id
    :returns: Returns a text ads or "" if server doesn't receive ads

    """

    if checkServerExcludeAds(server_id) == True:
        if config.ads_excluded[server_id]["expires"] != False:
            # Get the time stamp for now
            now = datetime.datetime.now()

            if ((now - config.ads_excluded[server_id]["time"]).seconds / 86400) > config.ads_excluded[server_id]["expires"]:

                includeServerAds(server_id)

                ad = giveTextAds()

                # addServerQueueAds(server_id, ad[1])

                # FOR DEBUGGING
                # print("AD BEING SENT:   " + str(ad[0]))

                return ad

            else:

                # FOR DEBUGGING
                # print("SERVER DOESN'T GET ADS")

                return "Ads free!"

    else:

        ad = giveTextAds()

        # addServerQueueAds(server_id, ad[1])

        # FOR DEBUGGING
        # print("AD BEING SENT:   " + str(ad[0]))

        return ad


def giveTimeAds(expires):
    """Give valid number of time.

    :param expires: A integer
    :returns: A valid integer

    """

    if tools.isInt(expires) == False:
        return 30  # It's not a int to return 30 minutes

    if expires == False:
        return False  # This will never expire

    elif expires == True:
        return 30  # This is equal to 30 minutes

    expires = int(expires)  # Convert to int to prevent errors

    if expires < 30:
        return 30  # This is equal to 30 minutes

    elif expires > 10080:
        return 10080  # This is equal to a week

    else:
        return expires  # Return the given value as a int


def giveViewsAds(views):
    """Gives a valid number of views.

    :param views: A integer
    :returns: A valid number or False if never expires.

    """

    if tools.isInt(views) == False:
        return 500

    if views == True:
        return 500

    elif views == False:
        return False

    views = int(views)  # Convert to an int to prevent errors

    if views < 500:
        return 500

    elif views > 5000:
        return 5000

    else:
        return views


def giveEmbedAds():
    """Give the ID of a embed ad.

    :returns: List index[0]: ads ID, index[1]: break time given

    """

    keys = list(config.ads_embed.keys())

    # FOR DEBUGGING
    # print("KEYS:   " + str(keys))

    keys = str(keys[randint(0, (len(keys) - 1))])

    # FOR DEBUGGING
    # print("KEY:   " + str(keys))

    time = int(config.ads_embed[keys]["time"])

    # FOR DEBUGGING
    # print("TIME:   " + str(time))

    # FOR DEBUGGING
    # print("GIVE ADS:\nKEYS:   " + str(keys) + " |TIME:   " + str(time))

    return [keys, time]


def giveTextAds():
    """Give a text ad

    :returns: Text string

    """

    keys = list(config.ads_text.keys())

    # FOR DEBUGGING
    # print("KEYS:   " + str(keys))

    selected = keys[randint(0, (len(keys) - 1))]

    # FOR DEBUGGING
    # print("SELECTED TEXT AD:   " + str(selected))

    ad = dict(config.ads_text[selected])["text"]

    # FOR DEBUGGING
    # print("TEXT AD:   " + str(ad))

    removeViewsAds("text", selected)

    return ad


def checkServerQueueAds(discord_server):
    """Checks if a server is in ads break queue.

    :param discord_server: ID of the discord server
    :returns: True, if the server is in queue; False, if the server isn't in queue

    """

    if discord_server in config.ads_queue:
        return True

    else:
        return False


def addServerQueueAds(server_id, expires="60"):
    """Add a server to server ad break queue.

    :param server_id:  Discord ID of the server
    :param expires: Ad break given to server
    :returns: True, if server was successfully added to server queue; False, if server wasn't added to server ad break queue

    """

    try:

        # TODO STORE DATA

        # Create a time stamp
        time = datetime.datetime.now()

        config.ads_queue[server_id] = {"time": time, "expires": expires}
        storeServers()
        return True

    except:
        return False


def removeServerQueueAds(server_id):
    """Remove a server for server ad break queue.

    :param server_id: Discord server ID
    :returns: True, if server was removed successfully; False, if server wasn't removed

    """

    try:

        # TODO STORE ADS

        del config.ads_queue[server_id]
        storeServers()
        return True

    except:
        return False


def checkServerExcludeAds(server_id):
    """Checks if a server is loaded.

    :param server_id: ID of discord server
    :returns: True, if the given ID is excluded; False, if the given ID is not excluded

    """

    if server_id in config.ads_excluded:
        return True

    else:
        return False


def excludeServerAds(server_id, expires="False"):
    """If expires is set to False this server will never be removed from the excluded servers.

    :param server_id: ID of the discord server
    :param expires: Amount of days to exclude server for
    :returns: True, if server was excluded successfully; False, if server wasn't excluded

    """
    try:

        # TODO STORE DATA

        # Make a time stamp
        time = datetime.datetime.now()

        config.ads_excluded[server_id] = {"time": time, "expires": expires}
        storeServers()
        return True

    except:
        return False


def includeServerAds(server_id):
    """Remove a from the excluded ad servers by it's discord server id.

    :param server_id: Discord server id
    :returns: True, if server was included successfully; False, if the server wasn't excluded

    """

    try:

        # TODO STORE DATA

        del config.ads_excluded[server_id]
        storeServers()
        return True

    except:
        return False


def checkIfAds(type, ad_id):
    """Check if an add exist, text and embed ads.

    :param type: Type of ad to check for, embed or text
    :param ad_id: ID of ad
    :returns: True, if that ad does exist; False, if that ad doesn't exist

    """

    if type == "embed":

        if ad_id in config.ads_embed:
            return True

        else:
            return False

    elif type == "text":

        if ad_id in config.ads_text:
            return True

        else:
            return False


def addEmbedAds(ad_id, views, time, title, description, url, img):
    """Adds a embed ad to the ads.

    :param ad_id: Id to allocate this embed ad with
    :param views: Times this ad has to be seen before being removed
    :param time: Ad break given to servers when seeing this
    :param title: Title of the ads embed
    :param description: Text the ad displays on the embed
    :param url: Ads page(url)
    :param img: Url of an image to display on embed
    :returns: True, if ad was added successfully; False, if ad wasn't added

    """

    try:

        # TODO STORE DATA

        config.ads_embed[ad_id] = {"views": int(views), "time": int(time), "title": str(title), "url": str(url), "description": str(description), "img": str(img)}
        storeAds()
        return True

    except:
        return False


def addTextAds(ad_id, views, text):
    """Adds a embed ad to the ads.

    :param ad_id: Id to allocate this embed ad with
    :param views: Times this ad has to be seen before being removed
    :param text: Content that will be displayed at the end of most embeds(except other ads)
    :returns: True, if ad was added successfully; False, if ad wasn't added

    """

    try:

        # TODO STORE DATA

        config.ads_text[ad_id] = {"views": int(views), "text": str(text)}
        storeAds()
        return True

    except:
        return False


def removeAds(type, ad_id):
    """Remove an ad, embed or text, from the ads.

    :param type: Type of add to remove, embed or text
    :param ad_id: ID of ad
    :returns: True, if ad was removed successfully; False, if ad wasn't removed

    """

    if type == "embed":
        try:

            # TODO STORE DATA

            del config.ads_embed[ad_id]
            storeAds()
            return True

        except:
            return False

    if type == "text":
        try:

            # TODO STORE DATA

            del config.ads_text[ad_id]
            storeAds()
            return True

        except:
            return False


def removeViewsAds(type, ad_id):
    """Remove views from ads. If ads views are equal to or less then 0 removes the ad.

    :param type: Type of ad to remove views from.
    :param ad_id: ID of ad

    """

    if type == "embed":
        try:
            if config.ads_embed[ad_id]["views"] != False:
                config.ads_embed[ad_id]["views"] -= 1

                # If the views of an add is equal or less than 0 remove it
                if config.ads_embed[ad_id]["views"] <= 0:
                    removeAds("embed", ad_id)

                # TODO STORE DATA
                storeAds()

            return

        except:
            return

    elif type == "text":
        try:
            if config.ads_text[ad_id]["views"] != False:
                config.ads_text[ad_id]["views"] -= 1

                if config.ads_text[ad_id]["views"] <= 0:
                    removeAds("text", ad_id)

                # TODO STORE DATA
                storeAds()

            return

        except:
            return


def makeEmbedAds(ad_id):
    """Creates and returns an embed out of the ad id.

    :param ad_id: ID of ad
    :returns: Discord embed object

    """

    try:

        # FOR DEBUGGING
        # print("AD ID:   " + str(ad_id))

        # print("TITLE:   " + str(config.ads_embed[ad_id]["title"]) + "  |URL: " + str(config.ads_embed[ad_id]["url"]) + "  |DESCRIPTION: " + str(config.ads_embed[ad_id]["description"]))

        embed = discord.Embed(title=str(config.ads_embed[ad_id]["title"]), colour=discord.Colour.red(), url=str(config.ads_embed[ad_id]["url"]), description=str(config.ads_embed[ad_id]["description"]))

        # print("BOT NAME:   " + str(config.bot_name))

        embed.set_author(name=str(config.bot_name), url=str(config.bot_server), icon_url=str(config.bot_icon))

        embed.set_image(url=str(config.ads_embed[ad_id]["img"]))

        embed.set_footer(text="Sponsored Content - Thank you for supporting us :3 | Contact us if wish to be promote your own things.")

        removeViewsAds("embed", ad_id)

        return embed

    except Exception as e:
        print("AD EMBED ERROR:   " + str(e))
