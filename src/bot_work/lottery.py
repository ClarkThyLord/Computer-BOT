import discord
import pickle
import config
import datetime
import random
from src.bot_work import languages


def storeSettings():
    lottery_settings = config.lottery_settings

    try:

        with open(config.directory + "//pickle-db//lotterySettings.pickle", "wb") as handler:
            pickle.dump(lottery_settings, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("LOTTERY SETTINGS SAVED:   " + str(ads_e))

    except Exception as e:
        print("!!!COULDN'T SAVE LOTTERY SETTINGS!!!\n" + str(e))


def storeLottery():
    lottery_queue = config.lottery_queue
    lottery_excludes = config.lottery_excludes

    try:

        with open(config.directory + "//pickle-db//lotteryQueue.pickle", "wb") as handler:
            pickle.dump(lottery_queue, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("LOTTERY QUEUE SAVED:   " + str(ads_e))

    except Exception as e:
        print("!!!COULDN'T SAVE LOTTERY QUEUE!!!\n" + str(e))

    try:

        with open(config.directory + "//pickle-db//lotteryExcluded.pickle", "wb") as handler:
            pickle.dump(lottery_excludes, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("LOTTERY EXCLUDED SAVED:   " + str(ads_e))

    except Exception as e:
        print("!!!COULDN'T SAVE LOTTERY EXCLUDED!!!\n" + str(e))


def checkUser(user_id):
    """See if a user win's the lottery.

    :parameter user_id: User's discord id.
    :returns: True, user has won the lottery; False, user has not won the lottery.

    """

    try:

        if config.lottery_settings["on"] == False:
            return False

        if user_id in config.lottery_excludes:
            return False

        else:
            if user_id in config.lottery_queue:
                # Get the time stamp for now
                now = datetime.datetime.now()

                if ((now - config.lottery_queue[user_id]).seconds / 60) > config.lottery_settings["timeOut"]:

                    config.lottery_queue[user_id] = now

                    storeLottery()

                    if round(random.randrange(1, config.lottery_settings["iceRate"])) == 1:
                        return True

                    else:
                        return False

                else:
                    return False

            else:
                # Get the time stamp for now
                now = datetime.datetime.now()

                config.lottery_queue[user_id] = now

                storeLottery()

                if round(random.randrange(1, config.lottery_settings["iceRate"])) == 1:
                    return True

                else:
                    return False

    except Exception as e:
        print("ERROR IN CHECK USER LOTTERY:   " + str(e))

        return False


def lotteryEmbed(language, name):
    """Creates and returns a lottery embed.

    :parameter language: Language embed should be shown in.
    :parameter name: Name of the winner.
    :returns: Discord embed object.

    """

    try:

        # FOR DEBUGGING
        # print("AD ID:   " + str(ad_id))

        embed = discord.Embed(title=languages.lotteryTitle(language, name), colour=discord.Colour.gold(), url=str(config.bot_server), description=languages.lotteryDescription(language))

        embed.set_author(name=str(config.bot_name), url=str(config.bot_server), icon_url=str(config.bot_icon))

        embed.set_image(url="https://vaingloryhack.com/wp-content/uploads/2017/03/download.png")

        embed.set_footer(text="Thank you for supporting us :3 | Contact us!")

        return embed

    except Exception as e:
        print("LOTTERY EMBED ERROR:   " + str(e))
