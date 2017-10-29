import asyncio
import config
import os
import discord
from discord.ext import commands
from src.bot_work import ads, lottery
from src.mongo_work import core as db
from src.vainglory_work import languages, checks, core, gifs, tools, verify
from traceback import format_exc

# Module Variables
msgs = {}  # List of msgs to keep track of; Format {"(msg_id)": {"type": "("type of msg", data...}, ...}
temp = {}  # List of temp data to keep track of; Format {"(user_id)": {"ign": "(String)", "region": "(String Region)", "pattern": "(List)"}, ...}


class Vainglory():

    def __init__(self, bot):
        """At creation of this objects setup what's needed."""

        self.bot = bot  # Create a bots instance in this object

    async def on_reaction_add(self, reaction, user):
        """Runs whenever a reaction to a msg is added."""

        try:

            global msgs

            # FOR DEBUGGING
            # print("MESSAGE AUTHOR:   " + str(reaction.message.author) + " |USER:   " + str(user) + " |BOT:   " + str(self.bot))

            # Returns if the reaction was added by the bot
            if reaction.message.author == user:
                return

            msg = reaction.message

            # FOR DEBUGGING
            # print("MSGS DICT:   " + str(msgs))
            # print("MSG:  " + str(msg) + " |MSG ID:   " + str(msg.id) + " |REACTION EMOJI:   " + str(reaction.emoji) + " |DATA NUM:   " + str(msgs[str(msg.id)]["dataNum"]) + " |PAGES:   " + str(msgs[str(msg.id)]["pagesMax"] - 1))

            if str(msg.id) in msgs:
                if msgs[str(msg.id)]["type"] == "matches":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["dataNum"] < (msgs[str(msg.id)]["pagesMax"] - 1):
                        # Update msg's data
                        msgs[str(msg.id)]["dataNum"] += 1
                        msgs[str(msg.id)]["pageNum"] += 1

                        data = msgs[str(msg.id)]

                        embed = core.matchesEmbed(data["data"][data["dataNum"]], data["ign"], data["region"], data["pageNum"], data["pagesMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                        await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["dataNum"] > 0:
                        # Update msg's data
                        msgs[str(msg.id)]["dataNum"] -= 1
                        msgs[str(msg.id)]["pageNum"] -= 1

                        data = msgs[str(msg.id)]

                        embed = core.matchesEmbed(data["data"][data["dataNum"]], data["ign"], data["region"], data["pageNum"], data["pagesMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                        await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == "⏺":
                        if msg.channel.is_private == True:
                            try:

                                info = {}

                                # Get the users name in text
                                info["mention"] = str(user)

                                data = db.discordUserDictionary(user.id)

                                # FOR DEBUGGING
                                # print("USER DATA:   " + str(data))

                                if data == False or data == None:
                                    info["language"] = "english"
                                    info["destination"] = user

                                else:
                                    info["language"] = data["general"]["language"]
                                    info["destination"] = user

                            except:
                                info = {"language": "english", "destination": user}

                        else:

                            info = await self.getInfo(msg, ["destination", "language"], "gifs")

                            # Get the users mention
                            info["mention"] = str((await self.bot.get_user_info(user.id)).mention)

                        data = msgs[str(msg.id)]

                        embed = discord.Embed(
                        title="Vainglory Match GIF Generator",
                        url=config.bot_server,
                        colour=discord.Colour.orange(),
                        description="What sorta information should be diplayed in the gif?\n:one: **- hero kills**\n:two: **- non-hero kills**\n:three: **- hero abilities**\n:four: **- item abilities**\n:1234: **- everything above**"
                        )

                        msg = await self.bot.send_message(info["destination"], info["mention"], embed=embed)

                        try:

                            await self.bot.add_reaction(msg, '\U00000031\U000020e3')  # Add :one: reaction
                            await self.bot.add_reaction(msg, '\U00000032\U000020e3')  # Add :two: reaction
                            await self.bot.add_reaction(msg, '\U00000033\U000020e3')  # Add :three: reaction
                            await self.bot.add_reaction(msg, '\U00000034\U000020e3')  # Add :four: reaction
                            await self.bot.add_reaction(msg, '\U0001f522')  # Add :1234: reaction

                        except Exception as e:
                            # FOR DEBUGGING
                            # print("ERROR: " + str(e))

                            pass

                        # FOR DEBUGGING
                        # print("USER: " + str(user))

                        ans = await self.bot.wait_for_reaction(message=msg, emoji=['\U00000031\U000020e3', '\U00000032\U000020e3', '\U00000033\U000020e3', '\U00000034\U000020e3', '\U0001f522'], user=user, timeout=30)

                        if ans == None:
                            await self.bot.send_message(info["destination"], languages.gifLineThree(info["language"], info["mention"]))
                            return

                        # FOR DEBUGGING
                        # print("ANS: " + str(ans) + " |ONE: " + str(ans[0]) + " |TWO: " + str(ans[1]))
                        # print("REACTION: " + str(ans[0].emoji))

                        if ans[0].emoji == "1⃣":
                            ans = 1

                        elif ans[0].emoji == "2⃣":
                            ans = 2

                        elif ans[0].emoji == "3⃣":
                            ans = 3

                        elif ans[0].emoji == "4⃣":
                            ans = 4

                        elif ans[0].emoji == "🔢":
                            ans = 5

                        else:
                            ans = 5

                        # FOR DEBUGGING
                        # print("ANS: " + str(ans))

                        await self.bot.edit_message(msg, languages.gifLineOne(info["language"], info["mention"]))

                        # path = gifs.generateGIF(data["data"][data["dataNum"]], data["ign"])
                        path = await self.bot.loop.run_in_executor(None, gifs.generateGIF, data["data"][data["dataNum"]], data["ign"], ans)

                        # FOR DEBUGGING
                        # print("PATH: " + str(path))

                        await self.bot.edit_message(msg, languages.gifLineTwo(info["language"], info["mention"]))

                        try:

                            await self.bot.send_file(info["destination"], path)

                        except:
                            # FOR DEBUGGING
                            # print("ERROR SENDING GIF: " + str(format_exc()))

                            await self.bot.send_message(info["destination"], languages.unSentFile(info["language"], info["mention"]))
                            return

                        await self.bot.edit_message(msg, languages.sentFile(info["language"], info["mention"]))

                        try:
                            if path != None:
                                os.remove(path)

                                # FOR DEBUGGING
                                # print("REMOVED IMG AT:\n" + str(path))

                        except:
                            await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(user) + "```Couldn't removed file at:\n" + str(path) + "```")

                    elif reaction.emoji == '🎦':
                        if msg.channel.is_private == True or msgs[str(msg.id)]["telemetry"] > 5:
                            try:

                                info = {"mention": str(user)}

                                data = db.discordUserDictionary(user.id)

                                if data == False or data == None:
                                    info["language"] = "english"
                                    info["compact"] = False
                                    info["emojis"] = True
                                    info["destination"] = user
                                    info["textAd"] = ads.giveTextAds()
                                    if info["textAd"] in [None, False]:
                                        info["textAd"] = "Thank you for choosing ComputerBot :3"

                                else:

                                    try:

                                        info["language"] = data["general"]["language"]

                                    except:
                                        info["language"] = "english"

                                    try:

                                        info["compact"] = data["vaingloryRelated"]["compact"]

                                    except:
                                        info["compact"] = False

                                    try:

                                        info["emojis"] = data["vaingloryRelated"]["emojis"]

                                    except:
                                        info["emojis"] = True

                                    info["destination"] = user

                                    info["textAd"] = ads.giveTextAds()
                                    if info["textAd"] in [None, False]:
                                        info["textAd"] = "Thank you for choosing ComputerBot :3"

                            except:
                                info = {"language": "english", "compact": False, "emojis": True, "destination": user}

                        else:

                            info = await self.getInfo(msg, ["destination", "language", "compact", "emojis", "textAd"], "telemetry")

                            # Get the users mention
                            info["mention"] = str((await self.bot.get_user_info(user.id)).mention)

                        msgs[str(msg.id)]["telemetry"] += 1

                        data = msgs[str(msg.id)]

                        msg = await self.bot.send_message(info["destination"], languages.telemetryLineOne(info["language"], info["mention"]))

                        data = tools.matchTelemetryDict(data["data"][data["dataNum"]], data["ign"])

                        # FOR DEBUGGING
                        # print("MATCH TELEMETRY DATA:   " + str(data))
                        # print("MSG:   " + str(msg))
                        # print("info["destination"]:   " + str(info["destination"]))

                        await self.bot.edit_message(msg, info["mention"], embed=core.matchesTelemetryEmbed(data[-1], 0, data[-2]["ign"], data[-2]["gameMode"], data[-2]["matchId"], data[-2]["actor"], data[-2]["winner"], data[-2]["side"], -1, len(data), info["compact"], info["emojis"], info["language"], info["textAd"]))

                        #Add reactions to the embed msg
                        try:

                            await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                            await self.bot.add_reaction(msg, '\U0001f504')  # Add arrows counter clock wise reaction
                            await self.bot.add_reaction(msg, '\U000025b6')  # Add the arrow forward reaction
                            await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

                        except:
                            pass

                        if "error-emojis" in info:
                            await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

                        msgs[msg.id] = {"type": "telemetry", "data": data, "mode": 0, "sectionNum": -1, "sectionMax": (len(data) - 3), "compact": info["compact"], "emojis": info["emojis"], "language": info["language"], "ad": info["textAd"]}

                        # FOR DEBUGGING
                        # print("MSG SAVED:   " + str(msgs[msg.id]))
                        # print("MSGS AFTER:   " + str(msgs))

                        try:

                            if msg.channel != None:
                                ad = ads.checkEmbedAds(msg.server.id)

                                if ad != False:
                                    ad = ads.makeEmbedAds(ad)

                                    # FOR DEBUGGING
                                    # print("AD IS:  " + str(ad))

                                    ad = await self.bot.send_message(info["destination"], embed=ad)

                                    await asyncio.sleep(30)

                                    await self.bot.delete_message(ad)

                        except Exception as e:
                            print("ERROR:   " + str(e))
                            pass

                        await asyncio.sleep(330)

                        try:

                            # Delete the msg data from msgs
                            del msgs[msg.id]

                        except:
                            pass

                elif msgs[msg.id]["type"] == "telemetry":
                    if reaction.emoji == '➡' and msgs[msg.id]["sectionNum"] < msgs[msg.id]["sectionMax"]:
                            # Update msg's data
                            msgs[msg.id]["sectionNum"] += 1

                            data = msgs[msg.id]

                            # FOR DEBUGGING
                            # print("MSG DATA:   " + str(data))

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP ADDING NEXT:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '⬅' and msgs[msg.id]["sectionNum"] > -1:
                            # Update msg's data
                            msgs[msg.id]["sectionNum"] -= 1

                            data = msgs[msg.id]

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP ADDING BACK:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '🔄':
                        if msgs[msg.id]["mode"] < 2:
                            msgs[msg.id]["mode"] += 1

                            data = msgs[msg.id]

                            # FOR DEBUGGING
                            # print("MSG DATA:   " + str(data))

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP ADDING SWITCH 1:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                        elif msgs[msg.id]["mode"] == 2:
                            msgs[msg.id]["mode"] = 0

                            data = msgs[msg.id]

                            # FOR DEBUGGING
                            # print("MSG DATA:   " + str(data))

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP ADDING SWITCH 2:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '▶':
                        try:

                            # Get the users name in text
                            mention = str(user)

                            data = db.discordUserDictionary(user.id)

                            # FOR DEBUGGING
                            # print("USER DATA:   " + str(data))

                            if data in [False, None]:
                                language = "english"
                                compact = False
                                emojis = True
                                destination = user

                            else:
                                try:

                                    language = data["general"]["language"]

                                except:
                                    language = "english"

                                try:

                                    compact = data["vaingloryRelated"]["compact"]

                                except:
                                    compact = False

                                try:

                                    emojis = data["vaingloryRelated"]["emojis"]

                                except:
                                    emojis = True

                                destination = user

                        except:
                            mention = str(user)
                            language = "english"
                            compact = False
                            emojis = True
                            destination = user

                        data = msgs[msg.id]

                        minute = data["sectionNum"]
                        matchId = data["data"][-2]["matchId"]

                        # FOR DEBUGGING
                        # print("MSG DATA:   " + str(data))

                        if msgs[msg.id]["sectionNum"] in [-1]:
                            await self.bot.send_message(destination, languages.telemetryLineTwo(language, mention))
                            return

                        await self.bot.send_message(destination, languages.telemetryLineOne(language, mention))

                        try:

                            data = core.telemetryMinute(data["data"][data["sectionNum"]], data["data"][-2]["side"], compact, emojis, language)

                        except Exception as e:
                            # print("FUCK UP ADDING PLAY:   " + str(e))
                            return

                        for msg in data:
                            await self.bot.send_message(destination, msg)

                        await self.bot.send_message(destination, languages.telemetryLineThree(language, mention, str(minute), str(matchId)))

        except:
            await self.bot.send_message(reaction.message.channel, "Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(reaction.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.send_message(reaction.message.channel, "A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.send_message(reaction.message.channel, "A **report** has been successfully sent to the developers! :hugging:")

    async def on_reaction_remove(self, reaction, user):
        """Runs whenever a reaction to a msg is removed."""

        try:

            global msgs

            # FOR DEBUGGING
            # print("MESSAGE AUTHOR:   " + str(reaction.message.author) + " |USER:   " + str(user) + " |BOT:   " + str(self.bot))

            # Returns if the reaction was added by the bot
            if reaction.message.author == user:
                return

            msg = reaction.message

            # FOR DEBUGGING
            # print("MSGS DICT:   " + str(msgs))
            # print("MSG:  " + str(msg) + " |MSG ID:   " + str(msg.id) + " |REACTION EMOJI:   " + str(reaction.emoji) + " |DATA NUM:   " + str(msgs[str(msg.id)]["dataNum"]) + " |PAGES:   " + str(msgs[str(msg.id)]["pagesMax"] - 1))

            if str(msg.id) in msgs:
                if msgs[str(msg.id)]["type"] == "matches":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["dataNum"] < (msgs[str(msg.id)]["pagesMax"] - 1):
                        # Update msg's data
                        msgs[str(msg.id)]["dataNum"] += 1
                        msgs[str(msg.id)]["pageNum"] += 1

                        data = msgs[str(msg.id)]

                        embed = core.matchesEmbed(data["data"][data["dataNum"]], data["ign"], data["region"], data["pageNum"], data["pagesMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                        await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["dataNum"] > 0:
                        # Update msg's data
                        msgs[str(msg.id)]["dataNum"] -= 1
                        msgs[str(msg.id)]["pageNum"] -= 1

                        data = msgs[str(msg.id)]

                        embed = core.matchesEmbed(data["data"][data["dataNum"]], data["ign"], data["region"], data["pageNum"], data["pagesMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                        await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == "⏺":
                        if msg.channel.is_private == True:
                            try:

                                info = {}

                                # Get the users name in text
                                info["mention"] = str(user)

                                data = db.discordUserDictionary(user.id)

                                # FOR DEBUGGING
                                # print("USER DATA:   " + str(data))

                                if data == False or data == None:
                                    info["language"] = "english"
                                    info["destination"] = user

                                else:
                                    info["language"] = data["general"]["language"]
                                    info["destination"] = user

                            except:
                                info = {"language": "english", "destination": user}

                        else:

                            info = await self.getInfo(msg, ["destination", "language"], "gifs")

                            # Get the users mention
                            info["mention"] = str((await self.bot.get_user_info(user.id)).mention)

                        data = msgs[str(msg.id)]

                        embed = discord.Embed(
                        title="Vainglory Match GIF Generator",
                        url=config.bot_server,
                        colour=discord.Colour.orange(),
                        description="What sorta information should be diplayed in the gif?\n:one: **- hero kills**\n:two: **- non-hero kills**\n:three: **- hero abilities**\n:four: **- item abilities**\n:1234: **- everything above**"
                        )

                        msg = await self.bot.send_message(info["destination"], info["mention"], embed=embed)

                        try:

                            await self.bot.add_reaction(msg, '\U00000031\U000020e3')  # Add :one: reaction
                            await self.bot.add_reaction(msg, '\U00000032\U000020e3')  # Add :two: reaction
                            await self.bot.add_reaction(msg, '\U00000033\U000020e3')  # Add :three: reaction
                            await self.bot.add_reaction(msg, '\U00000034\U000020e3')  # Add :four: reaction
                            await self.bot.add_reaction(msg, '\U0001f522')  # Add :1234: reaction

                        except Exception as e:
                            # FOR DEBUGGING
                            # print("ERROR: " + str(e))

                            pass

                        # FOR DEBUGGING
                        # print("USER: " + str(user))

                        ans = await self.bot.wait_for_reaction(message=msg, emoji=['\U00000031\U000020e3', '\U00000032\U000020e3', '\U00000033\U000020e3', '\U00000034\U000020e3', '\U0001f522'], user=user, timeout=30)

                        if ans == None:
                            await self.bot.send_message(info["destination"], languages.gifLineThree(info["language"], info["mention"]))
                            return

                        # FOR DEBUGGING
                        # print("ANS: " + str(ans) + " |ONE: " + str(ans[0]) + " |TWO: " + str(ans[1]))
                        # print("REACTION: " + str(ans[0].emoji))

                        if ans[0].emoji == "1⃣":
                            ans = 1

                        elif ans[0].emoji == "2⃣":
                            ans = 2

                        elif ans[0].emoji == "3⃣":
                            ans = 3

                        elif ans[0].emoji == "4⃣":
                            ans = 4

                        elif ans[0].emoji == "🔢":
                            ans = 5

                        else:
                            ans = 5

                        # FOR DEBUGGING
                        # print("ANS: " + str(ans))

                        await self.bot.edit_message(msg, languages.gifLineOne(info["language"], info["mention"]))

                        # path = gifs.generateGIF(data["data"][data["dataNum"]], data["ign"])
                        path = await self.bot.loop.run_in_executor(None, gifs.generateGIF, data["data"][data["dataNum"]], data["ign"], ans)

                        # FOR DEBUGGING
                        # print("PATH: " + str(path))

                        await self.bot.edit_message(msg, languages.gifLineTwo(info["language"], info["mention"]))

                        try:

                            await self.bot.send_file(info["destination"], path)

                        except:
                            # FOR DEBUGGING
                            # print("ERROR SENDING GIF: " + str(e) + "\n\n" + str(format_exc()))

                            await self.bot.send_message(info["destination"], languages.unSentFile(info["language"], info["mention"]))
                            return

                        await self.bot.edit_message(msg, languages.sentFile(info["language"], info["mention"]))

                        try:
                            if path != None:
                                os.remove(path)

                                # FOR DEBUGGING
                                # print("REMOVED IMG AT:\n" + str(path))

                        except:
                            await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(user) + "```Couldn't removed file at:\n" + str(path) + "```")

                    elif reaction.emoji == '🎦':
                        if msg.channel.is_private == True or msgs[str(msg.id)]["telemetry"] > 5:
                            try:

                                info = {"mention": str(user)}

                                data = db.discordUserDictionary(user.id)

                                if data == False or data == None:
                                    info["language"] = "english"
                                    info["compact"] = False
                                    info["emojis"] = True
                                    info["destination"] = user
                                    info["textAd"] = ads.giveTextAds()
                                    if info["textAd"] in [None, False]:
                                        info["textAd"] = "Thank you for choosing ComputerBot :3"

                                else:

                                    try:

                                        info["language"] = data["general"]["language"]

                                    except:
                                        info["language"] = "english"

                                    try:

                                        info["compact"] = data["vaingloryRelated"]["compact"]

                                    except:
                                        info["compact"] = False

                                    try:

                                        info["emojis"] = data["vaingloryRelated"]["emojis"]

                                    except:
                                        info["emojis"] = True

                                    info["destination"] = user

                                    info["textAd"] = ads.giveTextAds()
                                    if info["textAd"] in [None, False]:
                                        info["textAd"] = "Thank you for choosing ComputerBot :3"

                            except:
                                info = {"language": "english", "compact": False, "emojis": True, "destination": user}

                        else:

                            info = await self.getInfo(msg, ["destination", "language", "compact", "emojis", "textAd"], "telemetry")

                            # Get the users mention
                            info["mention"] = str((await self.bot.get_user_info(user.id)).mention)

                        msgs[str(msg.id)]["telemetry"] += 1

                        data = msgs[str(msg.id)]

                        # FOR DEBUGGING
                        # print("MSG DATA:   " + str(data))
                        # print("REQUEST:   " + str(data["data"][data["dataNum"]]))
                        # print("IGN:   " + str(data["ign"]))
                        # print("MSGS MSG BEFORE:   " + str(msgs[str(msg.id)]))

                        msg = await self.bot.send_message(info["destination"], languages.telemetryLineOne(info["language"], info["mention"]))

                        data = tools.matchTelemetryDict(data["data"][data["dataNum"]], data["ign"])

                        # FOR DEBUGGING
                        # print("MATCH TELEMETRY DATA:   " + str(data))

                        await self.bot.edit_message(msg, info["mention"], embed=core.matchesTelemetryEmbed(data[-1], 0, data[-2]["ign"], data[-2]["gameMode"], data[-2]["matchId"], data[-2]["actor"], data[-2]["winner"], data[-2]["side"], -1, len(data), info["compact"], info["emojis"], info["language"], info["textAd"]))

                        #Add reactions to the embed msg
                        try:

                            await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                            await self.bot.add_reaction(msg, '\U0001f504')  # Add arrows counter clock wise reaction
                            await self.bot.add_reaction(msg, '\U000025b6')  # Add the arrow forward reaction
                            await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

                        except:
                            pass

                        if "error-emojis" in info:
                            await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

                        msgs[msg.id] = {"type": "telemetry", "data": data, "mode": 0, "sectionNum": -1, "sectionMax": (len(data) - 3), "compact": info["compact"], "language": info["language"], "emojis": info["emojis"], "ad": info["textAd"]}

                        # FOR DEBUGGING
                        # print("MSG SAVED:   " + str(msgs[msg.id]))
                        # print("MSGS AFTER:   " + str(msgs))

                        try:

                            if msg.channel != None:
                                ad = ads.checkEmbedAds(msg.server.id)

                                if ad != False:
                                    ade = ads.makeEmbedAds(ad)

                                    # FOR DEBUGGING
                                    # print("AD IS:  " + str(ade))

                                    ad = await self.bot.send_message(info["destination"], embed=ade)

                                    await asyncio.sleep(30)

                                    await self.bot.delete_message(ad)

                        except Exception as e:
                            print("ERROR:   " + str(e))
                            pass

                        await asyncio.sleep(330)

                        try:

                            # Delete the msg data from msgs
                            del msgs[msg.id]

                        except:
                            pass

                elif msgs[msg.id]["type"] == "telemetry":
                    if reaction.emoji == '➡' and msgs[msg.id]["sectionNum"] < msgs[msg.id]["sectionMax"]:
                            # Update msg's data
                            msgs[msg.id]["sectionNum"] += 1

                            data = msgs[msg.id]

                            # FOR DEBUGGING
                            # print("MSG DATA:   " + str(data))

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP REMOVING NEXT:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '⬅' and msgs[msg.id]["sectionNum"] > -1:
                            # Update msg's data
                            msgs[msg.id]["sectionNum"] -= 1

                            data = msgs[msg.id]

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP REMOVING BACK:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '🔄':
                        if msgs[msg.id]["mode"] < 2:
                            msgs[msg.id]["mode"] += 1

                            data = msgs[msg.id]

                            # FOR DEBUGGING
                            # print("MSG DATA:   " + str(data))

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP REMOVING SWITCH 1:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                        elif msgs[msg.id]["mode"] == 2:
                            msgs[msg.id]["mode"] = 0

                            data = msgs[msg.id]

                            # FOR DEBUGGING
                            # print("MSG DATA:   " + str(data))

                            try:

                                embed = core.matchesTelemetryEmbed(data["data"][data["sectionNum"]], data["mode"], data["data"][-2]["ign"], data["data"][-2]["gameMode"], data["data"][-2]["matchId"], data["data"][-2]["actor"], data["data"][-2]["winner"], data["data"][-2]["side"], data["sectionNum"], data["sectionMax"], data["compact"], data["emojis"], data["language"], data["ad"])

                            except Exception as e:
                                print("FUCK UP REMOVING SWITCH 2:   " + str(e))
                                return

                            await self.bot.edit_message(msg, embed=embed)

                    elif reaction.emoji == '▶':
                        try:

                            # Get the users name in text
                            mention = str(user)

                            data = db.discordUserDictionary(user.id)

                            # FOR DEBUGGING
                            # print("USER DATA:   " + str(data))

                            if data in [False, None]:
                                language = "english"
                                compact = False
                                emojis = True
                                destination = user

                            else:
                                try:

                                    language = data["general"]["language"]

                                except:
                                    language = "english"

                                try:

                                    compact = data["vaingloryRelated"]["compact"]

                                except:
                                    compact = False

                                try:

                                    emojis = data["vaingloryRelated"]["emojis"]

                                except:
                                    emojis = True

                                destination = user

                        except:
                            mention = str(user)
                            language = "english"
                            compact = False
                            emojis = True
                            destination = user

                        data = msgs[msg.id]

                        minute = data["sectionNum"]
                        matchId = data["data"][-2]["matchId"]

                        # FOR DEBUGGING
                        # print("MSG DATA:   " + str(data))

                        if msgs[msg.id]["sectionNum"] in [-1]:
                            await self.bot.send_message(destination, languages.telemetryLineTwo(language, mention))
                            return

                        await self.bot.send_message(destination, languages.telemetryLineOne(language, mention))

                        try:

                            data = core.telemetryMinute(data["data"][data["sectionNum"]], data["data"][-2]["side"], compact, emojis, language)

                        except Exception as e:
                            print("FUCK UP REMOVING PLAY:   " + str(e))
                            return

                        for msg in data:
                            await self.bot.send_message(destination, msg)

                        # FOR DEBUGGING
                        # print("!!!DONE DICTATING!!!")

                        await self.bot.send_message(destination, languages.telemetryLineThree(language, mention, str(minute), str(matchId)))

        except Exception:
            await self.bot.send_message(reaction.message.channel, "Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(reaction.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.send_message(reaction.message.channel, "A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.send_message(reaction.message.channel, "A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def savevg(self, raw, player_name="", region="na", guild_name="Unknown", team_name="Unknown"):
        """Safe VainGlory data like player name, region, etc. for quick searches, use of certain commands without arguments, with VainGlory related commands.

                >savevg (player_name) (region) (guild_name) (team_name)
            player_name   -   Player's VainGlory in-game name
            region        -   VainGlory region
            guild_name    -   VainGlory in-game guild name
            team_name     -   VainGlory in-game team name

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
            $savevg ClarkthyLord na Kings_Home Thy_True_Kings

            Example 2:
            $savevg ClarkthyLord na "Kings Home" "Thy True Kings"

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention"], "savevg")

            if player_name == "":
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            player_name = str(player_name)

            if checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            region = checks.giveRegion(region)

            if checks.checkCommunityName(guild_name) == False:
                await self.bot.send_message(info["destination"], languages.notVgGuildName(info["language"], info["mention"], guild_name))
                return

            guild_name = str(guild_name).replace("_", " ")

            if checks.checkCommunityName(team_name) == False:
                await self.bot.send_message(info["destination"], languages.notVgTeamName(info["language"], info["mention"], team_name))
                return

            team_name = str(team_name).replace("_", " ")

            msg = await self.bot.send_message(info["destination"], languages.saveVGLineOne(info["language"], info["mention"], player_name, region, guild_name, team_name))

            if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.quickName": str(player_name)}) == True and db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.quickRegion": str(region)}) == True and db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.quickGuildName": str(guild_name)}) == True and db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.quickTeamName": str(team_name)}) == True:
                await self.bot.edit_message(msg, languages.saveVGLineTwo(info["language"], info["mention"], player_name, region, guild_name, team_name))
                return

            else:
                await self.bot.edit_message(msg, languages.saveVGLineThree(info["language"], info["mention"], player_name, region, guild_name, team_name))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")


    @commands.command(pass_context=True)
    async def verify(self, raw, player_name="", region="na"):
        """Link your in-game account to your discord account to use advance ComputerBot features. You can only verify one account per discord account!

                >verify (player_name) (region)
            player_name   -   Your VainGlory in-game name.   -   Choose the wrong region? Enter $ followed by a region to change it
            region        -   Your VainGlory region.

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $verify ClarkthyLord na

            Example 2:
                $verify "L3oN " eu

            Example 3 to change region:
                $verify $cn

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention"])
            info["destination"] = raw.message.author

            # FOR DEBUGGING
            # print("INFO: " + str(info))


            # If this user has already started the verification process
            if raw.message.author.id in temp:
                if player_name == "$cancel":
                    try:

                        del temp[raw.message.author.id]

                        await self.bot.send_message(info["destination"], languages.verifyLineEight(info["language"], info["mention"]))

                        return

                    except:
                        await self.bot.send_message(info["destination"], languages.verifyLineEight(info["language"], info["mention"]))
                        return

                if player_name.startswith("$") == True:
                    if checks.checkRegion(player_name.replace("$", "")) == True:
                        temp[raw.message.author.id]["region"] == player_name.replace("$", "")

                # Create an instance of the temp data
                data = temp[raw.message.author.id]

                msg = await self.bot.send_message(info["destination"], languages.verifyLineOne(info["language"], info["mention"], data["ign"], data["region"]))

                # Get the matches of the ign and region provided before hand
                matches = core.getMatches(data["ign"], data["region"], "blitz")

                # FOR DEBUGGING
                # print("MATCHES: " + str(matches) + "\nMATCHES LLENGTH: " + str(len(matches)))

                try:

                    if matches in [False, None]:
                        await self.bot.edit_message(msg, languages.verifyLineTwo(info["language"], info["mention"], data["ign"], data["region"]))
                        return

                    elif "error" in matches:
                        await self.bot.edit_message(msg, languages.verifyLineTwo(info["language"], info["mention"], data["ign"], data["region"]))
                        return

                except:
                    await self.bot.edit_message(msg, languages.verifyLineTwo(info["language"], info["mention"], data["ign"], data["region"]))
                    return

                result = verify.check(data["ign"], data["pattern"], matches)

                if result == True:

                    # Setup verified, verifiedName, verifiedRegion
                    if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.verified": True}) == True and db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.verifiedName": data["ign"]}) == True and db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.verifiedRegion": data["region"]}) == True:
                        await self.bot.edit_message(msg, languages.verifyLineThree(info["language"], info["mention"], data["ign"], data["region"]))

                    # Remove the users data from temp data
                    try:

                        del temp[raw.message.author.id]

                    except:
                        pass

                    return

                else:
                    await self.bot.edit_message(msg, languages.verifyReqNot(info["language"], info["mention"], data["ign"], data["region"]))
                    return

            else:
                if player_name == "":
                    await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                    return

                elif checks.checkPlayerName(player_name) == False:
                    await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], str(player_name)))
                    return

                elif db.checkDiscordUsers({"vaingloryRelated.verifiedName": str(player_name)}) == True:
                    await self.bot.send_message(info["destination"], languages.verifyLineFour(info["language"], info["mention"], str(player_name)))
                    return

                else:
                    msg = await self.bot.send_message(info["destination"], languages.verifyLineFive(info["language"], info["mention"]))

                    region = checks.giveRegion(region)

                    pattern = verify.itemPattern()

                    # FOR DEBUGGING
                    # print("PATTERN: " + str(pattern))

                    # Message being sent
                    items = ""
                    for item in pattern:
                        # Items using and there value:
                        # 0 = Halcyon Potion
                        # 1 = Weapon Infusion
                        # 2 = Crystal Infusion
                        if item == 0:
                            items += "Halcyon Potion\n"

                        elif item == 1:
                            items += "Weapon Infusion\n"

                        elif item == 2:
                            items += "Crystal Infusion\n"

                    await self.bot.edit_message(msg, languages.verifyLineSix(info["language"], str(player_name), str(region), items, str(self.bot.command_prefix[0])))

                    temp[raw.message.author.id] = {"ign": player_name, "region": region, "pattern": pattern}

                    # FOR DEBUGGING
                    # print("TEMP DATA: " + str(temp[raw.message.author.id]))

                    await asyncio.sleep(900)

                    try:

                        del temp[raw.raw.message.author.id]

                        await self.bot.send_message(info["destination"], languages.verifyLineSeven(info["language"], info["mention"]))

                    except:
                        pass

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")


    @commands.command(pass_context=True)
    async def player(self, raw, player_name="", region="na"):
        """Get a players VainGlory info.

                >player (player_name) (region)
            player_name   -   Players VainGlory in-game name.
            region        -   Players VainGlory region.

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $player ClarkthyLord na

            Example 2:
                $player "L3oN " eu

            Example 3 using mentions:
                $player @Clark thy Lord

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "emojis", "textAd", "userData"], "player")

            if len(raw.message.mentions) == 1:
                # Fetches the mention's user data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                # Check that data is not faulty
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                # Check if user is verified; and if so give verified data
                if data["vaingloryRelated"]["verified"] == True:
                    player_name = data["vaingloryRelated"]["verifiedName"]
                    region = data["vaingloryRelated"]["verifiedRegion"]

                else:  # Give quick data
                    player_name = data["vaingloryRelated"]["quickName"]
                    region = data["vaingloryRelated"]["quickRegion"]

            elif player_name in ["", "$"]:
                # Check that data is not faulty
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                # Check if user is verified; and if so give verified data
                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:  # Give quick data
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            # Check that a player name was given
            if player_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            elif checks.checkPlayerName(player_name) == False:  # Check that the player name given is valid
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            # Give the default region, na, if non is given or format the given region
            region = checks.giveRegion(region)

            msg = await self.bot.send_message(info["destination"], languages.playerLineOne(info["language"], info["mention"], player_name, region))

            # Get the player embed
            embed = core.playerEmbed(player_name, region, info["emojis"], info["language"], info["textAd"])

            # FOR DEBUGGING
            # print("PLAYER EMBED:   " + str(embed.to_dict()))

            # If embed is faulty
            if embed == False:
                await self.bot.edit_message(msg, languages.playerLineTwo(info["language"], info["mention"], player_name, region))
                return

            await self.bot.edit_message(msg, new_content=info["mention"], embed=embed)

            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def compareP(self, raw, player_names="", player_regions="na"):
        """Compare multiple players from VainGlory; players who are in the same region.

                >compareP (player_names) (player_regions)
            player_names     -   Players VainGlory in-game name.   -   Separate names with ,
            player_regions   -   Players VainGlory region.

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $player ClarkthyLord,AmethystCrow,jeovanne na

            Example 2:
                $player "ClarkthyLord,AmethystCrow,jeovanne,BryceHi " na

            Example 3 using savevg, where $ is your info:
                $player $,AmethystCrow,jeovanne na

            Example 4 using mentions:
                $player @Clark thy Lord @AmethystCrow @Jeovanne

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "textAd", "userData"], "compareP")

            if len(raw.message.mentions) == 1:
                player_names = ""

                # Check if data in invalid
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                # Get verified data if verified
                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = str(dict(info["userData"])["vaingloryRelated"]["verifiedName"])

                else:  # Get quick data if nothing found
                    player_name = str(dict(info["userData"])["vaingloryRelated"]["quickName"])

                # Check if player name is given
                if player_name in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                    return

                # Checks that ign is valid
                elif checks.checkPlayerName(player_name) == False:
                    await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                    return

                # Add to string of igns using
                player_names += player_name + ","

                # Fetch users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                # Check if data in invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                # Get verified data if verified
                if data["vaingloryRelated"]["verified"] == True:
                    if data["vaingloryRelated"]["verifiedName"] != player_name:
                        player_name = data["vaingloryRelated"]["quickName"]

                    else:
                        await self.bot.send_message(info["destination"], languages.duplicateIgn(info["language"], info["mention"]))
                        return

                else:  # Get quick data if nothing found
                    if data["vaingloryRelated"]["quickName"] != player_name:
                        player_name = data["vaingloryRelated"]["quickName"]

                    else:
                        await self.bot.send_message(info["destination"], languages.duplicateIgn(info["language"], info["mention"]))
                        return

                # Check if player name is given
                if player_name in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                    return

                # Checks that ign is valid
                elif checks.checkPlayerName(player_name) == False:
                    await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                    return

                # Add to string of igns using
                player_names += player_name + ","

            elif len(raw.message.mentions) >= 2:
                num = 0
                player_names = ""
                for user in raw.message.mentions:
                    # Fetch users data
                    data = db.discordUserDictionary(user.id)

                    # Check if data in invalid
                    if data in [False, None]:
                        await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(user)))
                        return

                    # Get verified data if verified
                    if data["vaingloryRelated"]["verified"] == True:
                        player_name = data["vaingloryRelated"]["verifiedName"]

                    else:  # Get quick data if nothing found
                        player_name = data["vaingloryRelated"]["quickName"]

                    # Check if player name is given
                    if player_name in [False, None]:
                        await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                        return

                    # Checks that ign is valid
                    elif checks.checkPlayerName(player_name) == False:
                        await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                        return

                    # Add to string of igns using
                    player_names += player_name + ","

                    num += 1
                    if num == 6:
                        break

            else:
                if player_names == "":
                    await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                    return

                # Split the string of palyers into a list
                playerList = str(player_names).split(",", 6)

                # FOR DEBUGGING
                # print("PLAYER NAMES BEFORE:   " + str(player_names))
                # print("PLAYER LIST:   " + str(playerList) + "  |LENGTH:   " + str(len(playerList)))

                if len(playerList) <= 1:
                    await self.bot.send_message(info["destination"], languages.comparePlayersLineOne(info["language"]))
                    return

                num = 0
                player_names = ""
                for player_name in playerList:

                    # Convert player names into a string to be safe
                    player_name = str(player_name)

                    # Check if he called on his quick data
                    if player_name == "$":
                        # Check if data in invalid
                        if info["userData"] in [False, None]:
                            await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                            return

                        # Get verified data if verified
                        if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                            player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]

                        else:  # Get quick data if nothing found
                            player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]

                    if player_name in [False, None]:
                        await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                        return

                    # Checks that ign is valid
                    elif checks.checkPlayerName(player_name) == False:
                        await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                        return

                    # Add to string of igns using
                    player_names += player_name + ","

                    num += 1
                    if num == 6:
                        break

            # FOR DEBUGGING
            print("PLAYER NAMES AFTER:   " + str(player_name))

            # Give a valid region is non given or format region given
            player_regions = checks.giveRegion(player_regions)

            msg = await self.bot.send_message(info["destination"], languages.playerLineOne(info["language"], info["mention"], player_names, player_regions))

            # Get the players embed
            embed = core.comparePlayersEmbed(player_names, player_regions, info["language"], info["textAd"])

            # Check if embed is valid
            if embed == False:
                await self.bot.edit_message(msg, languages.playerLineTwo(info["language"], info["mention"], player_names, player_regions))
                return

            # FOR DEBUGGING
            # print("PLAYER EMBED:   " + str(embed))

            await self.bot.edit_message(msg, str(info["mention"]), embed=embed)

            # Check if this channel has problems with external emojis
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except Exception:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def compareUp(self, raw, player_one_name="", player_two_name="", player_one_region="na", player_two_region="na"):
        """Compare two players from Vainglory; players who are in different regions.

                >compareUp (player_one_name) (player_two_name) (player_one_region) (player_two_region)
            player_one_name     -   Player's VainGlory in-game name; first player   -   Enter as $ to use custom filters
            player_two_name     -   Player's VainGlory in-game name; second player
            player_one_region   -   Player's VainGlory region of the first player
            player_two_region   -   Player's VainGlory region of the second player

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $compareUp ClarkthyLord AmethystCrow na eu

            Example 2:
                $compareUp ClarkthyLord "L3oN " na eu

            Example 3 with savevg, ign given will be compared with your data:
                $compareUp AmethystCrow na

            Example 4 with mention, mention given will be compared with you data:
                $compareUp @Clark thy Lord

            Example 5 with mentions:
                $compareUp @Clark thy Lord @Amethyst Crow

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "emojis", "textAd", "userData"], "compareUp")

            # Check if a mention was made
            if len(raw.message.mentions) == 1:
                # Check if data is invalid
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                # Check if data is invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_two_name = data["vaingloryRelated"]["verifiedName"]
                    player_two_region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_two_name = data["vaingloryRelated"]["quickName"]
                    player_two_region = data["vaingloryRelated"]["quickRegion"]

            # Check if at least two mentions where made
            elif len(raw.message.mentions) >= 2:
                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                # Check if data is invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_one_name = data["vaingloryRelated"]["verifiedName"]
                    player_one_region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_one_name = data["vaingloryRelated"]["quickName"]
                    player_one_region = data["vaingloryRelated"]["quickRegion"]

                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[1]).id)

                # Check if data is invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[1])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_two_name = data["vaingloryRelated"]["verifiedName"]
                    player_two_region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_two_name = data["vaingloryRelated"]["quickName"]
                    player_two_region = data["vaingloryRelated"]["quickRegion"]

            elif player_two_name == "":
                # Move values over two arguments
                player_two_name = player_one_name
                player_two_region = player_two_region

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            # Check that player one name is given
            if player_one_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            # Check that player one name is valid
            elif checks.checkPlayerName(player_one_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_one_name))
                return

            # Format variables accordingly
            player_one_name = str(player_one_name)
            player_one_region = checks.giveRegion(player_one_region)

            # Check that player one name is given
            if player_two_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            # Check that player one name is valid
            elif checks.checkPlayerName(player_two_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_two_name))
                return

            # Format variables accordingly
            player_two_name = str(player_two_name)
            player_two_region = checks.giveRegion(player_two_region)

            # Check if player names given are the same
            if player_one_name == player_two_name:
                await self.bot.say(languages.duplicateIgn(info["language"], info["mention"]))
                return

            msg = await self.bot.send_message(info["destination"], languages.compareUniquePlayersLineOne(info["language"], info["mention"], player_one_name, player_one_region, player_two_name, player_two_region))

            # Get embed object
            embed = core.compareUniquePlayersEmbed(player_one_name, player_two_name, player_one_region, player_two_region, info["emojis"], info["language"], info["textAd"])

            # Check if data wasn't found on a player
            if embed == player_one_name:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"],  player_one_name, player_one_region))
                return

            elif embed == player_two_name:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"],  player_two_name, player_two_region))
                return

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            # Check if this channel has problems with external emojis
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def stats(self, raw, player_name="", region="na", game_mode="any", days="28"):
        """Get a player's stats from VainGlory.

                >stats (player_name) (region) (game_mode) (days)
            player_name   -   Player's VainGlory in-game name   -   Enter $ to use quick data
            region        -   Player's VainGlory region
            game_mode     -   Game mode stats should sampled from
            days          -   Days stats should sampled from

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg
            Game Modes: any, casual, rank, royale, blitz

            Example 1:
                $stats ClarkthyLord na casual 7

            Example 2:
                $stats "L3oN " eu blitz 3

            Example 3 with savevg and custom filters:
                $stats $ ranked 20

            Example 4 using mention:
                $stats @Clark thy Lord

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd", "userData"], "stats")

            if len(raw.message.mentions) >= 1:

                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_name = data["vaingloryRelated"]["verifiedName"]
                    region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = data["vaingloryRelated"]["quickName"]
                    region = data["vaingloryRelated"]["quickRegion"]

            elif player_name == "":

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            elif player_name == "$":
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                # Move variables over two
                days = game_mode
                game_mode = region

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            # Check if player name is given
            if player_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            # Check if player name given is valid
            if checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            # Give valid values if non given or format given values
            region = checks.giveRegion(region)
            days = checks.giveDays(days)
            game_mode = checks.giveGameMode(game_mode)

            msg = await self.bot.send_message(info["destination"], languages.statsLineOne(info["language"], info["mention"], player_name, region, game_mode, str(days)))

            embed = core.statsEmbed(player_name, region, game_mode, days, info["compact"], info["emojis"], info["language"], info["textAd"])

            # Check if embed is invalid
            if embed == False:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"], player_name, region))
                return

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            # Check if this channel has problems with external emojis
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def compareS(self, raw, player_one_name="", player_two_name="", player_one_region="na", player_two_region="na", game_mode="any", days="28"):
        """Compare two players stats from Vainglory; players who are in different regions.

                >compareS (player_one_name) (player_two_name) (player_one_region) (player_two_region) (game_mode) (days)
            player_one_name     -   Player's VainGlory in-game name; first player
            player_two_name     -   Player's VainGlory in-game name; second player
            player_one_region   -   Player's VainGlory region of the first player
            player_two_region   -   Player's VainGlory region of the second player
            game_mode           -   Game mode stats should be sampled from
            days                -   Date range stats should be sampled from

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg
            Game Modes: any, casual, rank, royale, blitz

            Example 1:
                $compareS ClarkthyLord L3oN na eu casual 7

            Example 2:
                $compareS ClarkthyLord "L3oN " na eu ranked 31

            Example 3 with savevg first ign given will be compared with your quick name:
                $compareS AmethystCrow

            Example 4 with savevg and custom filters:
                $compareS $ "L3oN " eu rank 7

            Example 5 with mentions and savevg, compare you and mentioned user:
                $compareS @AmethystCrow

            Example 6 with mentions:
                $compareS @ClarkthyLord @AmethystCrow

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd", "userData"], "compareS")

            if len(raw.message.mentions) == 1:

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

                # Fetch mentions data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                # Check if mentions data is invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                # Check if user is verified
                if data["vaingloryRelated"]["verified"] == True:
                    player_two_name = data["vaingloryRelated"]["verifiedName"]
                    player_two_region = data["vaingloryRelated"]["verifiedRegion"]

                else:  # Give quick data
                    player_two_name = data["vaingloryRelated"]["quickName"]
                    player_two_region = data["vaingloryRelated"]["quickRegion"]

            elif len(raw.message.mentions) >= 2:

                # Fetch mentions data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                # Check if mentions data is invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str((raw.message.mentions[0]).id)))
                    return

                # Check if user is verified
                if data["vaingloryRelated"]["verified"] == True:
                    player_one_name = data["vaingloryRelated"]["verifiedName"]
                    player_one_region = data["vaingloryRelated"]["verifiedRegion"]

                else:  # Give quick data
                    player_one_name = data["vaingloryRelated"]["quickName"]
                    player_one_region = data["vaingloryRelated"]["quickRegion"]

                # Fetch mentions data
                data = db.discordUserDictionary((raw.message.mentions[1]).id)

                # Check if mentions data is invalid
                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[1])))
                    return

                # Check if user is verified
                if data["vaingloryRelated"]["verified"] == True:
                    player_two_name = data["vaingloryRelated"]["verifiedName"]
                    player_two_region = data["vaingloryRelated"]["verifiedRegion"]

                else:  # Give quick data
                    player_two_name = data["vaingloryRelated"]["quickName"]
                    player_two_region = data["vaingloryRelated"]["quickRegion"]

            elif player_one_name == "$":

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                # Move values to correct place
                days = game_mode
                game_mode = player_two_region
                player_two_region = player_one_region

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_one_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    player_one_region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            elif player_two_name == "":
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_two_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    player_two_region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_two_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    player_two_region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            if player_one_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            if checks.checkPlayerName(player_one_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_one_name))
                return

            if player_two_name == "" or player_two_name == None:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            if checks.checkPlayerName(player_two_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_two_name))
                return

            # Give valid vales if non given or format values accordingly
            player_one_region = checks.giveRegion(player_one_region)
            player_two_region = checks.giveRegion(player_two_region)
            days = checks.giveDays(days)
            game_mode = checks.giveGameMode(game_mode)

            msg = await self.bot.send_message(info["destination"], languages.compareStatsLineOne(info["language"], info["mention"], player_one_name, player_two_name, player_one_region, player_two_region, game_mode, str(days)))

            embed = core.compareStatsEmbed(player_one_name, player_two_name, player_one_region, player_two_region, game_mode, days, info["compact"], info["emojis"], info["language"], info["textAd"])

            # Check if data on a player isn't found
            if embed == player_one_name:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"], player_one_name, player_one_region))
                return

            if embed == player_two_name:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"], player_two_name, player_two_region))
                return

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            # Check if emoji sending is ducked up on this channel
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def latest(self, raw, player_name="", region="na", game_mode="any"):
        """Get a players latest match in VainGlory.

                >latest (player_name) (region) (game_mode)
            player_name   -   Player's VainGlory in-game name.
            region        -   Player's VainGlory region.
            game_mode     -   Type of matches to look for

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $latest ClarkthyLord na casual

            Example 2 with savevg and custom filters:
                $latest $ rank

            Example 3 with mentions:
                $latest @Clark thy Lord

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd", "userData"], "latest")

            if len(raw.message.mentions) > 0:
                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_name = data["vaingloryRelated"]["verifiedName"]
                    region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = data["vaingloryRelated"]["quickName"]
                    region = data["vaingloryRelated"]["quickRegion"]

            elif player_name == "":
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            elif player_name == "$":
                # Move variable accordingly
                game_mode = region

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            # Check if no player name was given
            if player_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            # Check if player name given is invalid
            elif checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            # Give valid values if non given or format given values
            region = checks.giveRegion(region)
            game_mode = checks.giveGameMode(game_mode)

            msg = await self.bot.send_message(info["destination"], languages.latestLineOne(info["language"], info["mention"], game_mode, player_name, region))

            embed = core.latestMatchEmbed(player_name, region, game_mode, info["compact"], info["emojis"], info["textAd"], info["language"])

            # Check if embed is whack
            if embed == False:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"], player_name, region))
                return

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            # Check if emoji sending is ducked up on this channel
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def match(self, raw, match_id="", region="na", player_name="$random$"):
        """Get a matches info from VainGlory.

                >match (match_id) (region) (player_name)
            match_id      -   ID of the match.
            region        -   Player's VainGlory region.
            player_name   -   Player who we're looking at.   -   Default: $random

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $match D2U31DK3421-F3F23-U43D eu

            Example 2:
                $match D2U31DK3421-F3F23-U43D eu ClarkthyLord

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd"], "match")

            # Check if match id is not given
            if match_id == "":
                await self.bot.send_message(info["destination"], languages.noMatchId(info["language"], info["mention"]))
                return

            # Give valid value if non given or format values given
            region = checks.giveRegion(region)

            msg = await self.bot.send_message(info["destination"], languages.matchLineOne(info["language"], info["mention"], match_id, region))

            embed = core.matchEmbed(player_name, match_id, region, info["compact"], info["emojis"], info["language"], info["textAd"])

            # Check if embed is invalid
            if embed == False:
                await self.bot.edit_message(msg, languages.matchNotFound(info["language"], info["mention"], match_id, region))
                return

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            # If sending emojis on this channel is ducked
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def matches(self, raw, player_name="", region="na", game_mode="any"):
        """Get a players matches from VainGlory.

                >matches (player_name) (region) (game_mode)
            player_name   -   Player's VainGlory in-game name
            region        -   Player's VainGlory region
            game_mode     -   Type of matches to show

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg
            Game Modes: any, casual, rank, royale, blitz

            Example 1:
                $matches ClarkthyLord na casual

            Example 2:
                $matches "L3oN " eu ranked

            Example 3 with savevg and custom filters:
                $matches $ rank

            Example 4 with mentions:
                $matches @Clark thy Lord

        """

        global msgs

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd", "userData"], "matches")

            if len(raw.message.mentions) >= 1:

                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                print(data)

                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_name = data["vaingloryRelated"]["verifiedName"]
                    region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = data["vaingloryRelated"]["quickName"]
                    region = data["vaingloryRelated"]["quickRegion"]

            elif player_name == "":

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"]:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            elif player_name == "$":

                # Move values to correct variables
                game_mode = region

                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"]:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            # Check if player name is not given
            if player_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            # Check if player name given is invalid
            elif checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            # Give valid values if non given or format given values
            region = checks.giveRegion(region)
            game_mode = checks.giveGameMode(game_mode)

            msg = await self.bot.send_message(info["destination"], languages.matchesLineOne(info["language"], info["mention"], player_name, region, game_mode))

            # Get matches of player
            data = core.getMatches(player_name, region, game_mode)

            # FOR DEBUGGING
            # print("MATCHES FETCHED:   " + str(data))

            # Check if data is invalid
            if "error" in data:
                await self.bot.edit_message(msg, languages.playerNotFound(info["language"], info["mention"], player_name, region))
                return

            embed = core.matchesEmbed(data[0], player_name, region, 1, len(data), info["compact"], info["emojis"], info["language"], info["textAd"])  # Will contain two embeds

            await self.bot.edit_message(msg, info["mention"], embed=embed)  # This is msg

            #Add reactions to the embed msg
            try:

                await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                await self.bot.add_reaction(msg, '\U0001f3a6')  # Add film button reaction
                await self.bot.add_reaction(msg, '\U000023fa')  # Add record button reaction
                await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

            except:
                pass

            # If this channel is ducked for sending emojis
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            msgs[msg.id] = {"type": "matches", "ign": player_name, "region": region, "data": data, "dataNum": 0, "pageNum": 1, "pagesMax": len(data), "telemetry": 0, "compact": info["compact"], "emojis": info["emojis"], "language": info["language"], "ad": info["textAd"]}

            # FOR DEBUGGING
            # print("MSGS AFTER:   " + str(msgs))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])


            # Sleep for some time then delete what's being saved
            await asyncio.sleep(330)

            try:

                # Delete the msg data from msgs
                del msgs[msg.id]

            except:
                pass

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    # @commands.command(pass_context=True)
    # async def compareM(self, raw, first_match_id="", second_match_id="", first_match_region="na", second_match_region="na"):
    #     """Compare two matches from VainGlory.
    #
    #             >compareM (first_match_id) (second_match_id) (first_match_region) (second_match_region)
    #         first_match_id        -   ID of the VainGlory match; first match
    #         second_match_id       -   ID of the VainGlory match; second match
    #         first_match_region    -   Region of the first match
    #         second_match_region   -   Region of the second match
    #
    #     """
    #
    #     await self.bot.say(str(raw.message.content))

    @commands.command(pass_context=True)
    async def telemetry(self, raw, match_id="", match_region="na", player_name="$random$"):
        """Show a matches telemetry from VainGlory.

                >telemetry (match_id) (match_region) (player_name)
            match_id       -   ID of the VainGlory match
            match_region   -   Region of the VainGLory match
            player_name    -   In-game name of a player in that match.   -   Default: $random

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example:
                $match 6d6c3d78-2270-11e7-ba8d-0242ac110008 na

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd"], "telemetry")

            if match_id == "":
                await self.bot.send_message(info["destination"], languages.noMatchId(info["language"], info["mention"]))
                return

            match_region = checks.giveRegion(match_region)

            if checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            msg = await self.bot.send_message(info["destination"], languages.telemetryLineOne(info["language"], info["mention"]))

            data = core.getMatch(match_id, match_region)

            if "error" in data or data in [False, None]:
                await self.bot.edit_message(msg, languages.matchNotFound(info["language"], info["mention"], str(match_id), str(match_region)))
                return

            data = tools.matchTelemetryDict(data[0], player_name)

            # FOR DEBUGGING
            # print("MATCH TELEMETRY DATA:   " + str(data))

            await self.bot.edit_message(msg, info["mention"], embed=core.matchesTelemetryEmbed(data[-1], 0, data[-2]["ign"], data[-2]["gameMode"], data[-2]["matchId"], data[-2]["actor"], data[-2]["winner"], data[-2]["side"], -1, len(data), info["compact"], info["emojis"], info["language"], info["textAd"]))

            #Add reactions to the embed msg
            try:

                await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                await self.bot.add_reaction(msg, '\U0001f504')  # Add arrows counter clock wise reaction
                await self.bot.add_reaction(msg, '\U000025b6')  # Add the arrow forward reaction
                await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

            except:
                pass

            # If sending emojis is ducked on this channel
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            msgs[msg.id] = {"type": "telemetry", "data": data, "mode": 0, "sectionNum": -1, "sectionMax": (len(data) - 3), "compact": info["compact"], "emojis": info["emojis"], "language": info["language"], "ad": info["textAd"]}

            # FOR DEBUGGING
            # print("MSG SAVED:   " + str(msgs[msg.id]))
            # print("MSGS AFTER:   " + str(msgs))

            await self.embedAd(raw, info["destination"])

            # Wait then delete what's been saved
            await asyncio.sleep(330)

            try:

                # Delete the msg data from msgs
                del msgs[msg.id]

            except:
                pass

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    # @commands.command(pass_context=True)
    # async def compareT(self, raw, match_one_id="", match_two_id="", match_one_region="na", match_two_region="na"):
    #     """Compares two match telemetry from VainGlory.
    #
    #             >telemetry (match_id) (match_region)
    #         match_one_id       -   ID of the VainGlory match; first match
    #         match_one_id       -   ID of the VainGlory match; second match
    #         match_one_region   -   Region of the first match VainGLory match
    #         match_one_region   -   Region of the second match VainGLory match
    #
    #         Example:
    #             $match 6d6c3d78-2270-11e7-ba8d-0242ac110008 6d6c3d78-2270-11e7-ba8d-0242ac110008 na eu
    #
    #     """

    @commands.command(pass_context=True)
    async def vlb(self, raw, player_name="", filter_one="global", filter_two="gold", order="descending"):
        """Fetch one of our larboard relating to VainGlory!

                >vlb (player_name) (filter_one) (filter_two) (order)
            player_name   -   Player's in-game name.
            filter_one    -   Filter leader board by this key word.   -   Options: region, hero_name, position, role
            filter_two    -   Filter leader board by this key word.   -   Options: afks, assists, deaths, farm, gold, goldMiners, kills, krakenCaptures, minionKills
            order         -   Order of leader board.                  -   Options: ascending and descending

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example 1:
                $vlb ClarkthyLord Adagio kills Ascending

            Example 2:
                $vlb ClartkhyLord lane gold descending

            Example 3 with savevg and custom filters:
                $vlb $ lane gold descending

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "textAd", "userData"], "vlb")

            if player_name in ["", "$"]:
                if info["userData"] in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]

            if str(player_name) in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            elif checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            if checks.checkFilterOne(filter_one) == False:
                await self.bot.send_message(info["destination"], languages.leaderboardFilterOneNotReal(info["language"], info["mention"], str(filter_one)))
                return

            if checks.checkFilterTwo(filter_two) == False:
                await self.bot.send_message(info["destination"], languages.leaderboardFilterTwoNotReal(info["language"], info["mention"], str(filter_two)))
                return

            order = checks.giveOrder(order)

            msg = await self.bot.send_message(info["destination"], languages.leaderboardLineOne(info["language"], info["mention"], filter_one, filter_two, player_name))

            embed = core.leaderboardEmbed(player_name, filter_one, filter_two, order, info["compact"], info["language"], info["textAd"])

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def top(self, raw, top_elements="heroes", player_name="", region="na", game_mode="any", days="29"):
        """Fetch the top list of elements.

                >top (top) (player_name) (region) (game_mode) (days)
            top_elements   -   Name of data to list.   -   gamemodes, heroes, skins, items, itemUse
            player_name    -   Player's VainGlory in-game name.
            region         -   Region of leader board.
            game_mode      -   Game mode matches to sample from.
            days           -   Days to sample list from.

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg
            Game Modes: any, casual, rank, royale, blitz

            Example 1:
                $top items ClarkthyLord na any 93

            Example 2:
                $top items,heroes,itemUse ClarkthyLord na casual 3

            Example 3 with savevg and custom filters:
                $matches itemUse $ rank 2

            Example 4 with mentions:
                $matches heroes @Clark thy Lord

        """

        try:

            info = await self.getInfo(raw.message, ["destination", "language", "mention", "compact", "emojis", "textAd", "userData"], "top")

            if len(raw.message.mentions) >= 1:

                # Fetch mentioned users data
                data = db.discordUserDictionary((raw.message.mentions[0]).id)

                if data in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickDataOnMention(info["language"], info["mention"], str(raw.message.mentions[0])))
                    return

                if data["vaingloryRelated"]["verified"] == True:
                    player_name = data["vaingloryRelated"]["verifiedName"]
                    region = data["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = data["vaingloryRelated"]["quickName"]
                    region = data["vaingloryRelated"]["quickRegion"]

            elif player_name == "":

                if dict(info["userData"]) in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            elif player_name == "$":

                # Move variables accordingly
                days = game_mode
                game_mode = region

                if dict(info["userData"]) in [False, None]:
                    await self.bot.send_message(info["destination"], languages.noQuickData(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                    return

                if dict(info["userData"])["vaingloryRelated"]["verified"] == True:
                    player_name = dict(info["userData"])["vaingloryRelated"]["verifiedName"]
                    region = dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]

                else:
                    player_name = dict(info["userData"])["vaingloryRelated"]["quickName"]
                    region = dict(info["userData"])["vaingloryRelated"]["quickRegion"]

            # Check if player name is given
            if player_name in ["", None]:
                await self.bot.send_message(info["destination"], languages.noPlayerName(info["language"], info["mention"]))
                return

            # Check if player name given is valid
            elif checks.checkPlayerName(player_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], player_name))
                return

            # Give valid values if non given or format given values
            region = checks.giveRegion(region)
            days = checks.giveDays(days)

            if top_elements == "":
                languages.noTopElement(info["language"], info["mention"])
                return

            if "," in top_elements:
                elementList = str(top_elements).split(",")
                for element in elementList:
                    if element not in ["gamemodes", "heroes", "skins", "items", "itemUse"]:
                        languages.invalidTopElement(info["language"], info["mention"], str(element))
                        return

            else:
                if top_elements not in ["gamemodes", "heroes", "skins", "items", "itemUse"]:
                    languages.invalidTopElement(info["language"], info["mention"], str(top_elements))
                    return

            msg = await self.bot.send_message(info["destination"], languages.topListLineOne(info["language"], info["mention"], top_elements, player_name, region, game_mode, str(days)))

            embed = core.topElementEmbed(top_elements, player_name, region, game_mode, days, info["compact"], info["emojis"], info["language"], info["textAd"])

            await self.bot.edit_message(msg, info["mention"], embed=embed)

            # Check if sending emojis on this channel is ducked up
            if "error-emojis" in info:
                await self.bot.send_message(info["destination"], languages.noEmojisAllowed(info["language"]))

            await self.lotteryCheck(raw, info["destination"], info["language"])

            await self.embedAd(raw, info["destination"])

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    async def getInfo(self, message, req=[], check=""):
        """Gives info needed to function related to Vainglory.

            :param message: A discord message object.
            :param req: A list, containg Strings, of everything needed. Options: userData, serverData, mention, textAd, destination, language, compact, emojis
            :param check: Check if this value effects the outcome of the data.
            :returns: Information required to function.

        """

        # FOR DEBUGGING
        # print("---INPUT:\nMESSAGE: " + str(message) + "\nREQ: " + str(req) + "\nCHECK: " + str(check) + "\n---")

        if req == []:
            return {"error": "REQ IS EMPTY"}

        # Values to give when all goes wrong
        defaults = {
            "userData": False,
            "serverData": False,
            "mention": str(message.author),
            "textAd": "Thank you for choosing ComputerBot :3",
            "destination": message.author,
            "language": "english",
            "compact": False,
            "emojis": True
        }

        result = {}  # What's going to be sent
        try:

            # If communication pipe is private, Example: private messages
            if message.channel.is_private == True:
                try:

                    if "mention" in req:
                        result["mention"] = defaults["mention"]

                    if "textAd" in req:
                        try:

                            result["textAd"] = ads.giveTextAds()

                            if result["textAd"] in [None, False]:
                                result["textAd"] = defaults["textAd"]

                        except:
                            result["textAd"] = defaults["textAd"]

                    # Fetch data on user
                    data = db.discordUserDictionary(message.author.id)

                    # FOR DEBUGGING
                    # print("USER DATA:   " + str(data))

                    # If no data is found relative to the user return the default settings
                    if data in [False, None]:

                        if "userData" in req:
                            result["userData"] = defaults["userData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

                    # Data relative to the user was found
                    else:

                        if "userData" in req:
                            result["userData"] = data

                        if "language" in req:
                            try:

                                result["language"] = data["general"]["language"]

                            except:  # Set to default if not found
                                result["language"] = defaults["language"]

                        if "compact" in req:
                            try:

                                result["compact"] = data["vaingloryRelated"]["compact"]

                            except:  # Set to default if not found
                                result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            try:

                                result["emojis"] = data["vaingloryRelated"]["emojis"]

                            except:  # Set to default if not found
                                result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = message.author

                # In-case of a huge error return default settings
                except:
                        if "userData" in req:
                            result["userData"] = defaults["userData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

            # If communication pipe isn't private, Example: server/guild
            else:
                try:

                    if "mention" in req:
                        try:
                            result["mention"] = str((await self.bot.get_user_info(message.author.id)).mention)

                        except:
                            result["mention"] = defaults["mention"]

                    if "textAd" in req:
                        try:

                            result["textAd"] = ads.checkTextAds(message.server.id)

                            if result["textAd"] in [None, False]:
                                result["textAd"] = defaults["textAd"]

                        except:
                            result["textAd"] = defaults["textAd"]

                    # Fetch data on discord server
                    data = db.discordServerDictionary(message.server.id)

                    # FOR DEBUGGING
                    # print("SERVER DATA:   " + str(data))

                    # If no data is found relative to the server return the default settings
                    if data in [False, None]:

                        if "serverData" in req:
                            result["serverData"] = defaults["serverData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            if (message.server.get_member(self.bot.user.id)).server_permissions.external_emojis == False:
                                result["emojis"] = False
                                result["error-emojis"] = True  # State that emojis can't be sent because of set up

                            else:
                                result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = message.channel

                    # If the value, check, given is not permitted on this communication pipe then give from user data instead
                    elif check != "" and check in data["general"]["commandBans"]:
                        try:

                            userData = db.discordUserDictionary(message.author.id)

                            # FOR DEBUGGING
                            # print("USER DATA:   " + str(userData))

                            # If no data is found relative to the user return the default settings
                            if userData in [False, None]:

                                if "userData" in req:
                                    result["userData"] = defaults["userData"]

                                if "serverData" in req:
                                    result["serverData"] = data

                                if "language" in req:
                                    result["language"] = defaults["language"]

                                if "compact" in req:
                                    result["compact"] = defaults["compact"]

                                if "emojis" in req:
                                    result["emojis"] = defaults["emojis"]

                                if "destination" in req:
                                    result["destination"] = message.author

                            # Data relative to the user was found
                            else:

                                if "userData" in req:
                                    result["userData"] = userData

                                if "serverData" in req:
                                    result["serverData"] = data

                                if "language" in req:
                                    try:

                                        result["language"] = userData["general"]["language"]

                                    except:  # Set to default if not found
                                        result["language"] = defaults["language"]

                                if "compact" in req:
                                    try:

                                        result["compact"] = userData["vaingloryRelated"]["compact"]

                                    except:  # Set to default if not found
                                        result["compact"] = defaults["compact"]

                                if "emojis" in req:
                                    try:

                                        result["emojis"] = userData["vaingloryRelated"]["emojis"]

                                    except:  # Set to default if not found
                                        result["emojis"] = defaults["emojis"]

                                if "destination" in req:
                                    result["destination"] = message.author

                        # In-case of a huge error return default settings
                        except:
                                if "userData" in req:
                                    result["userData"] = defaults["userData"]

                                if "serverData" in req:
                                    result["serverData"] = data

                                if "language" in req:
                                    result["language"] = defaults["language"]

                                if "compact" in req:
                                    result["compact"] = defaults["compact"]

                                if "emojis" in req:
                                    result["emojis"] = defaults["emojis"]

                                if "destination" in req:
                                    result["destination"] = defaults["destination"]

                    # Data relative to the server was found
                    else:
                        if "serverData" in req:
                            result["serverData"] = data

                        if "language" in req:
                            try:

                                result["language"] = data["general"]["language"]

                            except:  # Set to default if not found
                                result["language"] = defaults["language"]

                        if "compact" in req:
                            try:

                                result["compact"] = data["vaingloryRelated"]["compact"]

                            except:  # Set to default if not found
                                result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            try:

                                result["emojis"] = data["vaingloryRelated"]["emojis"]

                            except:  # Set to default if not found
                                result["emojis"] = defaults["emojis"]

                            if result["emojis"] == True and (message.server.get_member(self.bot.user.id)).server_permissions.external_emojis == False:
                                result["emojis"] = False
                                result["error-emojis"] = True  # State that emojis can't be sent because of set up

                        if "destination" in req:
                            try:

                                # Get the channels ID or state(False/None if nothing is set)
                                result["destination"] = data["general"]["botChannel"]

                                # If bot channel is not set for the server then send to the same channel
                                if result["destination"] in [False, None]:
                                    result["destination"] = message.channel

                                # If bot channel is set do the following
                                else:
                                    # Get a channel object from what's in bot channel
                                    result["destination"] = self.bot.get_channel(result["destination"])

                                    # If discord couldn't find this channel then set to default
                                    if result["destination"] in [False, None]:
                                        result["destination"] = message.channel

                            except:  # Set to default  if not found
                                result["destination"] = message.channel

                except:  # In-case of a huge error return default settings
                        if "serverData" in req:
                            result["serverData"] = defaults["serverData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            result["emojis"] = defaults["emojis"]

                            if result["emojis"] == True and (message.server.get_member(self.bot.user.id)).server_permissions.external_emojis == False:
                                result["emojis"] = False
                                result["error-emojis"] = True  # State that emojis can't be sent because of set up

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

                if "userData" in req and "userData" not in result:
                    try:

                        result["userData"] = db.discordUserDictionary(message.author.id)

                        if result["userData"] in [False, None]:
                            result["userData"] = defaults["userData"]

                    except:
                        result["userData"] = defaults["userData"]

                if "serverData" in req and "serverData" not in result:
                    try:

                        result["serverData"] = db.discordServerDictionary(message.server.id)

                        if result["serverData"] in [False, None]:
                            result["serverData"] = defaults["serverData"]

                    except:
                        result["serverData"] = defaults["serverData"]

            # FOR DEBUGGING
            # print("---OUTPUT:\nINFO: " + str(result) + "\n---")

            return result

        except:
            # FOR DEBUGGING
            print("ERROR INFORMATION GATHERING:   " + str(format_exc()))

            return {"error": str(format_exc())}

    async def embedAd(self, raw, destination):
        # Gives an add if server is due a add

            try:

                if raw.message.channel.is_private != True:
                    ad = ads.checkEmbedAds(raw.message.server.id)

                    if ad in [None, False]:
                        return False

                    else:
                        ad = ads.makeEmbedAds(ad)

                        # FOR DEBUGGING
                        # print("AD IS:  " + str(ade))

                        ad = await self.bot.send_message(destination, embed=ad)

                        await asyncio.sleep(30)

                        await self.bot.delete_message(ad)

            except Exception as e:
                print("ERROR EMBED AD:   " + str(e))

    async def lotteryCheck(self, raw, destination, language):
        # Gives an add if server is due a add

            try:

                result = lottery.checkUser(str(raw.message.author.id))

                if result == True:
                    embed = lottery.lotteryEmbed(language, str(raw.message.author))

                    await self.bot.send_message(destination, embed=embed)
                    await self.bot.send_message(raw.message.author, embed=embed)
                    await self.bot.send_message(self.bot.get_channel("323559624672411649"), embed=embed)

            except Exception as e:
                print("ERROR LOTTERY CHECK:   " + str(e))


class Matching():

    def __init__(self, bot):
        """At creation of this objects setup what's needed."""

        self.bot = bot  # Create a bots instance in this object

    async def on_reaction_add(self, reaction, user):
        """Runs whenever a reaction to a msg is added."""

        try:

            global msgs

            # FOR DEBUGGING
            # print("MESSAGE AUTHOR:   " + str(reaction.message.author) + " |USER:   " + str(user) + " |BOT:   " + str(self.bot))

            # Returns if the reaction was added by the bot
            if reaction.message.author == user:
                return

            msg = reaction.message

            # FOR DEBUGGING
            # print("MSGS DICT:   " + str(msgs))
            # print("MSG:  " + str(msg) + " |MSG ID:   " + str(msg.id) + " |REACTION EMOJI:   " + str(reaction.emoji) + " |DATA NUM:   " + str(msgs[str(msg.id)]["dataNum"]) + " |PAGES:   " + str(msgs[str(msg.id)]["pagesMax"] - 1))

            if str(msg.id) in msgs:
                if msgs[str(msg.id)]["type"] == "playerProfiles":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["profileNum"] != (msgs[str(msg.id)]["profiles"].count() - 1):
                        msgs[str(msg.id)]["profileNum"] += 1

                        await self.bot.edit_message(msg, await self.playerProfile(msgs[str(msg.id)]["profiles"][msgs[str(msg.id)]["profileNum"]]))

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["profileNum"] != 0:
                        msgs[str(msg.id)]["profileNum"] -= 1

                        await self.bot.edit_message(msg, await self.playerProfile(msgs[str(msg.id)]["profiles"][msgs[str(msg.id)]["profileNum"]]))

                    elif reaction.emoji == "⏺":

                        try:

                            rec = await self.bot.get_user_info(dict(msgs[str(msg.id)]["profiles"][msgs[str(msg.id)]["profileNum"]])["_id"])

                            if rec.id in msgs[str(msg.id)]["sent"]:
                                return

                            else:
                                msgs[str(msg.id)]["sent"].append(rec.id)

                            await self.bot.send_message(rec, str(user) + ", want to get in contact with you over VG!")

                        except:
                            await self.bot.send_message(user, "Contact request couldn't be sent! :confused:")

                        await self.bot.send_message(user, "Contact request has be sent! :hugging:")

                elif msgs[str(msg.id)]["type"] == "guildProfiles":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["profileNum"] != (msgs[str(msg.id)]["profiles"].count() - 1):
                        msgs[str(msg.id)]["profileNum"] += 1

                        await self.bot.edit_message(msg, await self.guildProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["profileNum"] != 0:
                        msgs[str(msg.id)]["profileNum"] -= 1

                        await self.bot.edit_message(msg, await self.guildProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                elif msgs[str(msg.id)]["type"] == "teamProfiles":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["profileNum"] != (msgs[str(msg.id)]["profiles"].count() - 1):
                        msgs[str(msg.id)]["profileNum"] += 1


                        await self.bot.edit_message(msg, await self.teamProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["profileNum"] != 0:
                        msgs[str(msg.id)]["profileNum"] -= 1

                        await self.bot.edit_message(msg, await self.teamProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

        except:
            await self.bot.send_message(reaction.message.channel, "Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(reaction.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.send_message(reaction.message.channel, "A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.send_message(reaction.message.channel, "A **report** has been successfully sent to the developers! :hugging:")

    async def on_reaction_remove(self, reaction, user):
        """Runs whenever a reaction to a msg is removed."""

        try:

            global msgs

            # FOR DEBUGGING
            # print("MESSAGE AUTHOR:   " + str(reaction.message.author) + " |USER:   " + str(user) + " |BOT:   " + str(self.bot))

            # Returns if the reaction was added by the bot
            if reaction.message.author == user:
                return

            msg = reaction.message

            # FOR DEBUGGING
            # print("MSGS DICT:   " + str(msgs))
            # print("MSG:  " + str(msg) + " |MSG ID:   " + str(msg.id) + " |REACTION EMOJI:   " + str(reaction.emoji) + " |DATA NUM:   " + str(msgs[str(msg.id)]["dataNum"]) + " |PAGES:   " + str(msgs[str(msg.id)]["pagesMax"] - 1))

            if str(msg.id) in msgs:
                if msgs[str(msg.id)]["type"] == "playerProfiles":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["profileNum"] != (msgs[str(msg.id)]["profiles"].count() - 1):
                        msgs[str(msg.id)]["profileNum"] += 1

                        await self.bot.edit_message(msg, await self.playerProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["profileNum"] != 0:
                        msgs[str(msg.id)]["profileNum"] -= 1

                        await self.bot.edit_message(msg, await self.playerProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                    elif reaction.emoji == "⏺":

                        try:

                            rec = await self.bot.get_user_info(dict(msgs[str(msg.id)]["profiles"][msgs[str(msg.id)]["profileNum"]])["_id"])

                            if rec.id in msgs[str(msg.id)]["sent"]:
                                return

                            else:
                                msgs[str(msg.id)]["sent"].append(rec.id)

                            await self.bot.send_message(rec, str(user) + ", want to get in contact with you over VG!")

                        except:
                            await self.bot.send_message(user, "Contact request couldn't be sent! :confused:")

                        await self.bot.send_message(user, "Contact request has be sent! :hugging:")

                elif msgs[str(msg.id)]["type"] == "guildProfiles":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["profileNum"] != (msgs[str(msg.id)]["profiles"].count() - 1):
                        msgs[str(msg.id)]["profileNum"] += 1

                        await self.bot.edit_message(msg, await self.guildProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["profileNum"] != 0:
                        msgs[str(msg.id)]["profileNum"] -= 1

                        await self.bot.edit_message(msg, await self.guildProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                elif msgs[str(msg.id)]["type"] == "teamProfiles":
                    if reaction.emoji == '➡' and msgs[str(msg.id)]["profileNum"] != (msgs[str(msg.id)]["profiles"].count() - 1):
                        msgs[str(msg.id)]["profileNum"] += 1


                        await self.bot.edit_message(msg, await self.teamProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

                    elif reaction.emoji == '⬅' and msgs[str(msg.id)]["profileNum"] != 0:
                        msgs[str(msg.id)]["profileNum"] -= 1

                        await self.bot.edit_message(msg, await self.teamProfile(msgs[str(msg.id)]["profiles"]["profileNum"]))

        except:
            await self.bot.send_message(reaction.message.channel, "Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(reaction.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.send_message(reaction.message.channel, "A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.send_message(reaction.message.channel, "A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def profileP(self, raw, description="", voice="", roles="", favRole="", favPower="", favGameMode="", reqSkillTier="", primeTime=""):
        """Create or edit your VainGlory player profile on ComputerBot. You'll need to be verified, by ComputerBot, to make use of this feature!

                >profileP (description) (voice) (roles) (favRole) (favPower) (reqSkillTier) (primeTime)
            description    -   Description for your profile.   -   No more then 1000 characters, surround by ""; enter as $remove to remove this profile; $show to show your profile.
            voice          -   If you're willing to do voice chat while playing.   -   Default: true; Options: true, false.
            roles          -   What roles you're able to play.   -    Default: None, Options: None, Any, Lane, Captain, Jungle; Separate multiple roles with ,
            favRole        -   What role you play most.   -   Default: unknown; Options: unknown, captain, lane, jungle.
            favPower       -   What power you play most.   -   Default: unknown; Options: unknown, weapon, crystal, captain.
            favGameMode    -   What game mode you play most.   -   Default: unknown; Options: unknown, rank, casual, royale, blitz.
            reqSkillTier   -   What skill tier someone has to be to see your profile.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            primeTime      -   Your best time to play.   -   Default: allday; Options: allday, morning, midday, night.

            Edit Options: $remove, $show, $description, $voice, $roles, $favRole, $favPower, $favGameMode, $reqSkillTier, $primeTime

            Example 1:
                >profileP "Looking to find someone to play rank with!" true lane,jungle lane weapon casual 14 night

            Example edit profile properties:
                >profileP $roles lane,jungle

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "userData"])
            info["destination"] = raw.message.author

            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return

            # Setup variables
            description = str(description)
            voice = str(voice)
            roles = str(roles)
            favRole = str(favRole)
            favPower = str(favPower)
            reqSkillTier = str(reqSkillTier)
            primeTime = str(primeTime)
            
            defaults = {
                
                "description": "Just another VainGlory player!",
                "voice": "true",
                "roles": "any",
                "favRole": "unknown",
                "favPower": "unknown",
                "favGameMode": "unknown",
                "reqSkillTier": "-1",
                "primeTime": "allday"
                
            }

            if description.lower() == "$description":
                # Check if this user has a profile to modify
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                # Check if the value to change with wasn't given
                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "description"))
                    return

                elif checks.checkCommunityDescription(voice) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "description"))
                    return

                # Modify the profile
                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.description": voice}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "description", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "description", "player"))

                return

            elif description.lower() == "$voice":
                # Check if the user hass a profile to modify
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                # Check if value to update with is given
                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "voice"))
                    return

                elif checks.checkBoolean(voice) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "voice"))
                    return

                # Format the given value
                voice = checks.giveBoolean(voice)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.voice": voice}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "voice", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "voice", "player"))

                return

            elif description.lower() == "$roles":
                # Check if the user has a profile to edit
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                # Check if value to update with is given
                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "voice"))
                    return

                # Clear each role and append to roles
                roles = []
                for role in list((str(voice).lower()).split(",")):
                    if checks.checkRole(role) == False:
                        await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(role), "role"))
                        return

                    elif str(role).lower() == "any":
                        roles = ["any", "lane", "captain", "jungle"]
                        break

                    elif role not in roles:
                        roles.append(str(role).lower())

                if "lane" and "captain" and "jungle" in roles and "any" not in roles:
                    roles = ["any", "lane", "captain", "jungle"]

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.roles": roles}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "roles", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "roles", "player"))

                return

            elif description.lower() == "$favrole":
                # Check if user has a profile to modify
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                # Check if the value to update with was given
                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "favorite role"))
                    return

                elif checks.checkRole(voice) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "favorite role"))
                    return

                voice = checks.giveRole(voice)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.favRole": voice}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "favorite role", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "favorite role", "player"))

                return

            elif description.lower() == "$favpower":
                # Check if user has a profile to modify
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "favorite power"))
                    return

                elif checks.checkPower(voice) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "favorite power"))
                    return

                voice = checks.givePower(voice)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.favPower": voice}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "favorite power", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "favorite power", "player"))

                return

            elif description.lower() == "$favgamemode":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "favorite game mode"))
                    return

                elif checks.checkGameMode(voice) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "favorite game mode"))
                    return

                voice = checks.giveGameMode(voice)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.favGameMode": voice}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "favorite game mode", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "favorite game mode", "player"))

                return

            elif description.lower() == "$reqskilltier":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "required skill tier"))
                    return

                elif checks.checkSkillTier(voice) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "required skill tier"))
                    return

                voice = checks.giveSkillTier(voice)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.reqSkillTier": voice}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "required skill tier", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "required skill tier", "player"))

                return

            elif description.lower() == "$primetime":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                if voice == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "prime time"))
                    return

                realPrimeTimes = []
                for time in list((str(voice).lower()).split(",")):
                    time = str(time).lower()
                    if checks.checkCommunityTime(time) == False:
                        await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                        return

                    elif time == "allday":
                        realPrimeTimes = ["allday", "morning", "midday", "night"]
                        break

                    elif time not in realPrimeTimes:
                        realPrimeTimes.append(time)

                if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                    realPrimeTimes = ["allday", "morning", "midday", "night"]

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile.primeTime": realPrimeTimes}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "prime time", "player"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "prime time", "player"))

                return

            elif description.lower() == "$show":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                await self.bot.send_message(info["destination"], languages.profileTest(info["language"], info["mention"], "player"))

                await self.bot.send_message(info["destination"], embed=await self.playerProfile(dict(info["userData"])["vaingloryRelated"]["playerProfile"]))

                return

            # Check if player wants to remove profile
            elif description.lower() == "$remove":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                    return

                msg = await self.bot.send_message(info["destination"], languages.profileRemoving(info["language"], info["mention"], "player"))

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile": 1}, mode="$unset") == True:
                    await self.bot.edit_message(msg, languages.profileRemoved(info["language"], info["mention"], "player"))

                else:
                    await self.bot.edit_message(msg, languages.profileNotRemoved(info["language"], info["mention"], "player"))

                return
            
            if description == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **description**, *no more then 1000 characters*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    description = defaults["description"]
                    
                else:
                    description = msg.content
                
            if checks.checkCommunityDescription(description) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(description), "description"))
                return

            if voice == "":
                await self.bot.send_message(info["destination"], info["mention"], ", do you **voice**, *true or false*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    voice = defaults["voice"]
                    
                else:
                    voice = msg.content

            if checks.checkBoolean(voice) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "voice"))
                return

            voice = checks.giveBoolean(voice)

            if roles == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what **roles** do you play, *any - lane - captain - jungle and sepeate with ,*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    roles = defaults["roles"]
                    
                else:
                    roles = msg.content

            relRoles = []
            for role in list((str(roles).lower()).split(",")):
                if checks.checkRole(role) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(role), "role"))
                    return

                elif str(role).lower() == "any":
                    relRoles = ["any", "lane", "captain", "jungle"]
                    break

                elif role not in relRoles:
                    relRoles.append(str(role).lower())

            if "lane" and "captain" and "jungle" in relRoles and "any" not in relRoles:
                relRoles = ["any", "lane", "captain", "jungle"]
                    
            if favRole == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **favorite role**, *lane - captain - jungle*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    favRole = defaults["favRole"]
                    
                else:
                    favRole = msg.content
                    
            if checks.checkRole(favRole) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(favRole), "favorite role"))
                return

            favRole = str(favRole).lower()
            
            if favPower == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **favorite power**, *weapon - crystal - utility*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    favPower = defaults["favPower"]
                    
                else:
                    favPower = msg.content
                    
            if checks.checkPower(favPower) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(favPower), "favorite power"))
                return

            favPower = checks.givePower(favPower)
            
            if favGameMode == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **favorite game mode**, *casual, ranked, royale, blitz*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    favGameMode = defaults["favGameMode"]
                    
                else:
                    favGameMode = msg.content

            if checks.checkGameMode(favGameMode) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(favGameMode), "favorite game mode"))
                return

            favGameMode = str(favGameMode).lower()
            
            if reqSkillTier == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **required skill tier**, *-1 to 29 scale*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    reqSkillTier = defaults["reqSkillTier"]
                    
                else:
                    reqSkillTier = msg.content

            if checks.checkSkillTier(reqSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqSkillTier), "required skill tier"))
                return

            reqSkillTier = checks.giveSkillTier(reqSkillTier)
            
            if primeTime == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **prime time**, *allday - morning - midday - night*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    primeTime = defaults["primeTime"]
                    
                else:
                    primeTime = msg.content

            realPrimeTimes = []
            for time in list((str(primeTime).lower()).split(",")):
                time = str(time).lower()
                if checks.checkCommunityTime(time) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                    return

                elif time == "allday":
                    realPrimeTimes = ["allday", "morning", "midday", "night"]
                    break

                elif time not in realPrimeTimes:
                    realPrimeTimes.append(time)

            if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                realPrimeTimes = ["allday", "morning", "midday", "night"]

            await self.bot.send_message(info["destination"], languages.settingUpProfile(info["language"], info["mention"], "player"))

            # Setup profile object
            try:

                # Get ign and region
                ign, region = verify.giveIgnAndRegion(raw.message.author.id)

                # FOR DEBUGGING
                # print("IGN: " + str(ign) + " |REGION: " + str(region))

                data = list(core.getPlayers(ign, region))[0]

                # FOR DEBUGGING
                # print("DATA: " + str(data))

                # Check if something was found on player if not don't continue
                try:

                    if data in [False, None]:
                        await self.bot.send_message(info["destination"], languages.playerNotFound(info["language"], info["mention"], dict(info["userData"])["vaingloryRelated"]["verifiedName"], dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]))
                        return

                    elif "error" in data:
                        await self.bot.send_message(info["destination"], languages.playerNotFound(info["language"], info["mention"], dict(info["userData"])["vaingloryRelated"]["verifiedName"], dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]))
                        return

                except:
                    await self.bot.send_message(info["destination"], languages.playerNotFound(info["language"], info["mention"], dict(info["userData"])["vaingloryRelated"]["verifiedName"], dict(info["userData"])["vaingloryRelated"]["verifiedRegion"]))
                    return

                # Update this when changing the profile object
                profile_object = {

                    "voice": voice,
                    "roles": relRoles,
                    "favRole": favRole,
                    "favPower": favPower,
                    "favGameMode": favGameMode,
                    "reqSkillTier": reqSkillTier,
                    "primeTime": realPrimeTimes,
                    "description": description,
                    "ComputerKarma": 0,
                    "player": data

                }

                # FOR DEBUGGING
                print("PROFILE OBJECT: " + str(profile_object))

            except:
                await self.bot.send_message(info["destination"], languages.settingUpProfileErrorLineOne(info["language"], info["mention"], "player"))

                try:

                    await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

                except Exception as e:
                    await self.bot.send_message(info["destination"], languages.settingUpProfileErrorLineTwo(info["language"], info["mention"], str(e)))
                    return

                await self.bot.send_message(info["destination"], languages.settingUpProfileErrorLineThree(info["language"], info["mention"]))

                return


            if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.playerProfile": profile_object}):
                msg = await self.bot.send_message(info["destination"], languages.profileAdded(info["language"], info["mention"], "player"))

                await self.bot.edit_message(msg, languages.profileTest(info["language"], info["mention"], "player"))

                await self.bot.send_message(info["destination"], embed=await self.playerProfile(profile_object))

            else:
                await self.bot.send_message(info["destination"], languages.profileNotAdded(info["language"], info["mention"], "player"))

            return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def profileG(self, raw, guild_name="", guild_tag="", guild_level="", guild_region="", description="", guild_language="", guild_type="", reqSkillTier="", primeTime="", recruiting="", contact=""):
        """Create or edit your VainGlory guild profile on ComputerBot. You'll need to be verified, by ComputerBot, to make use of this feature!

                >profileG (guild_name) (guild_tag) (guild_level) (guild_region) (description) (guild_language) (guild_type) (reqSkillTier) (primeTime) (recruiting) (contact)
            guild_name       -   Guild's in-game name; enter as $remove to remove this profile; $show to show your profile.
            guild_tag        -   Guild's in-game tag.
            guild_level      -   Guild's in-game level.
            guild_region     -   Guild's in-game region.
            description      -   Description for your guilds profile.   -   No more then 1000 characters, surround by "".
            guild_language   -   Language this guild speaks primarily.   -   No more then 15 characters.
            guild_type       -   Type of guild   -   Default: casual; Options: casual, semi, competitive, school
            reqSkillTier     -   What skill tier someone has to be to see this guild profile.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            primeTime        -   Guild's most active time.   -   Default: allday; Options: allday, morning, midday, night.
            recruiting       -   If this guild is looking to recruit new members.   -   Default: true; Options: true, false
            contact          -   Where interested users should contact.   -   Default: $me(your user discord tag)

            Edit Options: $remove, $show, $name, $tag, $level, $region, $description, $language, $type, $reqSkillTier, $primeTime, $recruiting, $contact

            Example:
                >profileG "Kings Home" TTKG 77 na "Looking for new active members!" english casual -1 midday true www.myurl.com/guild_application

            Example edit profile properties:
                >profileG $level 77

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "userData"])
            info["destination"] = raw.message.author

            # Check if the users is verified by us
            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return
            
            # Convert to strings
            guild_name = str(guild_name)
            guild_tag = str(guild_tag)
            guild_level = str(guild_level)
            guild_region = str(guild_region)
            description = str(description)
            guild_language = str(guild_language)
            guild_type = str(guild_type)
            reqSkillTier = str(reqSkillTier)
            primeTime = str(primeTime)
            recruiting = str(recruiting)
            contact = str(contact)
            
            defaults = {
                
                "guild_level": 0,
                "guild_region": "na",
                "description": "Just another VainGlory guild!",
                "guild_language": "english",
                "guild_type": "casual",
                "reqSkillTier": -1,
                "primeTime": "allday",
                "recruiting": "false",
                "contact": "$me"
                
            }

            # To edit specific sections of profile
            if guild_name.lower() == "$name":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild name"))
                    return

                elif checks.checkCommunityName(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild name"))
                    return

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.name": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "name", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "name", "guild"))

                return

            elif guild_name.lower() == "$tag":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild tag"))
                    return

                elif checks.checkCommunityTag(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild tag"))
                    return

                guild_tag = checks.giveCommunityTag(guild_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.tag": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "tag", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "tag", "guild"))

                return

            elif guild_name.lower() == "$level":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild level"))
                    return
                
                elif checks.checkCommunityLevel(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild level"))
                    return
                
                guild_tag = int(guild_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.level": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "level", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "level", "guild"))

                return

            elif guild_name.lower() == "$region":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild region"))
                    return

                elif checks.checkRegion(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild region"))
                    return

                guild_tag = checks.giveRegion(guild_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.region": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "region", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "region", "guild"))

                return

            elif guild_name.lower() == "$description":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "description"))
                    return

                elif checks.checkCommunityDescription(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), 'description, surround with "" and no more then 1000 characters'))
                    return

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.description": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "description", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "description", "guild"))

                return

            elif guild_name.lower() == "$language":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "language"))
                    return

                elif checks.checkLanguage(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild language, no more then 15 characters"))
                    return

                guild_tag = str(guild_tag).lower()

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.language": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "language", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "language", "guild"))

                return

            elif guild_name.lower() == "$type":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild type"))
                    return

                elif checks.checkCommunityType(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild type, please use the following casual, semi, competitive, school"))
                    return

                guild_tag = checks.giveCommunityType(guild_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.type": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "type", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "type", "guild"))

                return

            elif guild_name.lower() == "$reqskilltier":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "required skill tier"))
                    return

                elif checks.checkSkillTier(guild_tag):
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "required skill tier, please use the -1 to 29 scale"))
                    return

                guild_tag = checks.giveSkillTier(guild_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.reqSkillTier": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "required skill tier", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "required skill tier", "guild"))

                return

            elif guild_name.lower() == "$recruiting":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "recruiting"))
                    return
                
                elif checks.checkBoolean(guild_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "recruiting"))
                    return

                guild_tag = checks.giveBoolean(guild_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.recruiting": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "recruiting", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "recruiting", "guild"))

                return

            elif guild_name.lower() == "$contact":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "contact"))
                    return
                
                elif guild_tag == "$me":
                    guild_tag = str(raw.message.author)

                elif len(guild_tag) < 15 or len(guild_tag) > 125:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), 'contact, surround by "", and no less then 15 and no more then 125 characters'))
                    return

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.contact": guild_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "contact", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "contact", "guild"))

                return

            elif guild_name.lower() == "$primetime":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                if guild_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "prime time"))
                    return

                realPrimeTimes = []
                for time in list((str(guild_tag).lower()).split(",")):
                    time = str(time).lower()
                    if checks.checkCommunityTime(time) == False:
                        await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                        return

                    elif time == "allday":
                        realPrimeTimes = ["allday", "morning", "midday", "night"]
                        break

                    elif time not in realPrimeTimes:
                        realPrimeTimes.append(time)

                if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                    realPrimeTimes = ["allday", "morning", "midday", "night"]

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile.primeTime": realPrimeTimes}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "prime time", "guild"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "prime time", "guild"))

                return

            elif guild_name.lower() == "$show":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                await self.bot.send_message(info["destination"], languages.profileTest(info["language"], info["mention"], "guild"))

                await self.bot.send_message(info["destination"], embed=await self.guildProfile(dict(info["userData"])["vaingloryRelated"]["guildProfile"]))

                return

            # Check if user wants to remove profile
            elif guild_name.lower() == "$remove":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["guildProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                    return

                msg = await self.bot.send_message(info["destination"], languages.profileRemoving(info["language"], info["mention"], "guild"))

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile": 1}, mode="$unset") == True:
                    await self.bot.edit_message(msg, languages.profileRemoved(info["language"], info["mention"], "guild"))

                else:
                    await self.bot.edit_message(msg, languages.profileNotRemoved(info["language"], info["mention"], "guild"))

                return

            if guild_name == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild name**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:    
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild name"))
                    return
                
                else:
                    guild_name = msg.content
                
            if checks.checkCommunityName(guild_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_name),"guild name"))
                return

            if guild_tag == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild's tag**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild tag"))
                    return
                
                else:
                    guild_tag = msg.content

            if checks.checkCommunityTag(guild_tag) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_tag), "guild tag"))
                return

            guild_tag = checks.giveCommunityTag(guild_tag)
            
            if guild_level == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild's level**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    guild_level = defaults["guild_level"]
                
                else:
                    guild_level = msg.content

            if checks.checkCommunityLevel(guild_level) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_level), "guild level"))
                return

            guild_level = int(guild_level)
            
            if guild_region == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild's region**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    guild_region = defaults["guild_region"]
                
                else:
                    guild_region = msg.content

            if checks.checkRegion(guild_region) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_region), "guild region"))
                return

            guild_region = checks.giveRegion(guild_region)
            
            if description == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild's description**, *no more then 1000 characters*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    description = defaults["description"]
                
                else:
                    description = msg.content

            if checks.checkCommunityDescription(description) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(description), 'description, surround with "" and no more then 1000 characters'))
                return
            
            if guild_language == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild language**, *no more then 15 characters*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    guild_language = defaults["guild_language"]
                
                else:
                    guild_language = msg.content

            if checks.checkLanguage(guild_language) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_language), "guild language, no more then 15 characters"))
                return

            guild_language = str(guild_language).lower()
            
            if reqSkillTier == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild required skill tier**, *please use the -1 to 29 scale*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    reqSkillTier = defaults["reqSkillTier"]
                
                else:
                    reqSkillTier = msg.content

            if checks.checkSkillTier(reqSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqSkillTier), "required skill tier, please use the -1 to 29 scale"))
                return

            reqSkillTier = checks.giveSkillTier(reqSkillTier)
            
            if primeTime == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild prime time**, *allday - morning - midday - night*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    primeTime = defaults["primeTime"]
                
                else:
                    primeTime = msg.content


            realPrimeTimes = []
            for time in list((str(primeTime).lower()).split(",")):
                time = str(time).lower()
                if checks.checkCommunityTime(time) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                    return

                elif time == "allday":
                    realPrimeTimes = ["allday", "morning", "midday", "night"]
                    break

                elif time not in realPrimeTimes:
                    realPrimeTimes.append(time)

            if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                realPrimeTimes = ["allday", "morning", "midday", "night"]
            
            if guild_type == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild type**, *casual - semi - competitive - school*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    guild_type = defaults["guild_type"]
                
                else:
                    guild_type = msg.content

            if checks.checkCommunityType(guild_type) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_type), "guild type, please use the following casual, semi, competitive, school"))
                return

            guild_type = str(guild_type).lower()
            
            if recruiting == "":
                await self.bot.send_message(info["destination"], info["mention"], ", is your **guild recruiting**, *true or false*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    recruiting = defaults["recruiting"]
                
                else:
                    recruiting = msg.content

            if checks.checkBoolean(recruiting) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(recruiting), "recruiting, please use false or true"))
                return

            recruiting = checks.giveBoolean(recruiting)
            
            if contact == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **guild's contact**, * $me for your discord tagl anything else no less then 15 and no less then 125 characters*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    contact = defaults["contact"]
                
                else:
                    contact = msg.content

            if contact == "$me":
                contact = str(raw.message.author)

            elif len(contact) < 15 or len(contact) > 125:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(contact), 'contact, surround by "", and no less then 15 and no more then 125 characters'))
                return

            msg = await self.bot.send_message(info["destination"], languages.settingUpProfile(info["language"], info["mention"], "guild"))

            # Setup profile object
            try:

                # Update this when changing the profile object
                profile_object = {

                    "name": guild_name,
                    "tag": guild_tag,
                    "level": guild_level,
                    "region": guild_region,
                    "reqSkillTier": reqSkillTier,
                    "language": guild_language,
                    "primeTime": realPrimeTimes,
                    "type": guild_type,
                    "description": description,
                    "contact": contact,
                    "recruiting": recruiting

                }

                # FOR DEBUGGING
                print("PROFILE OBJECT: " + str(profile_object))

            except:
                await self.bot.edit_message(msg, languages.settingUpProfileErrorLineOne(info["language"], info["mention"], "guild"))

                try:

                    await self.bot.edit_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

                except Exception as e:
                    await self.bot.edit_message(msg, languages.settingUpProfileErrorLineTwo(info["language"], info["mention"], str(e)))
                    return

                await self.bot.edit_message(msg, languages.settingUpProfileErrorLineThree(info["language"], info["mention"]))

                return


            if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.guildProfile": profile_object}):
                await self.bot.edit_message(msg, languages.settingUpProfileDone(info["language"], info["mention"], "guild"))

                await self.bot.send_message(info["destination"], languages.profileTest(info["language"], info["mention"], "guild"), embed = await self.guildProfile(profile_object))

            else:
                await self.bot.edit_message(msg, languages.settingUpProfileNotDone(info["language"], info["mention"], "guild"))

            return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def profileT(self, raw, team_name="", team_tag="", team_skillTier="", team_region="", description="", team_language="", team_type="", reqSkillTier="", roles="", primeTime="", recruiting="", contact=""):
        """Create or edit your VainGlory team profile on ComputerBot. You'll need to be verified, by ComputerBot, to make use of this feature!

                >profileG (team_name) (team_tag) (team_skillTier) (team_region) (description) (team_language) (team_type) (reqSkillTier) (roles) (primeTime) (recruiting) (contact)
            team_name        -   Team's in-game name; enter as $remove to remove this profile; $show to show your profile.
            team_tag         -   Team's in-game tag.
            team_skillTier   -   Team's in-game skill tier.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            team_region      -   Team's in-game region.
            description      -   Description for your teams profile.   -   No more then 1000 characters, surround by "".
            team_language    -   Language this team speaks primarily.   -   No more then 15 characters.
            team_type        -   Type of team   -   Default: casual; Options: casual, semi, competitive, school.
            roles            -   Roles the team is looking for.   -   Default: None, Options: None, Any, Lane, Captain, Jungle; Seperate multiple roles with ,
            reqSkillTier     -   What skill tier someone has to be to see this team profile.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            primeTime        -   team's most active time.   -   Default: allday; Options: allday, morning, midday, night.
            recruiting       -   If this team is looking to recruit new members.   -   Default: true; Options: true, false
            contact          -   Where interested users should contact.   -   Default: $me(your user discord tag)

            Edit Options: $remove, $show, $name, $tag, skillTier, $region, $description, $language, $reqSkillTier, $primeTime, $recruiting, $contact

            Example:
                >profileG "Kings Home" TTKG 77 na "Looking for new active members!" english casual -1 midday true www.myurl.com/team_application

            Example edit profile properties:
                >profileT $roles captain

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "userData"])
            info["destination"] = raw.message.author

            # Check if the users is verified by us
            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return

            # Convert to strings
            team_name = str(team_name)
            team_tag = str(team_tag)
            team_skillTier = str(team_skillTier)
            team_region = str(team_region)
            description = str(description)
            team_language = str(team_language)
            team_type = str(team_type)
            roles = str(roles)
            reqSkillTier = str(reqSkillTier)
            primeTime = str(primeTime)
            recruiting = str(recruiting)
            contact = str(contact)

            defaults = {

                "team_skillTier": 0,
                "team_region": "na",
                "description": "Just another VainGlory team!",
                "team_language": "english",
                "team_type": "casual",
                "roles": "any",
                "reqSkillTier": -1,
                "primeTime": "allday",
                "recruiting": "false",
                "contact": "$me"

            }

            # To edit specific sections of profile
            if team_name.lower() == "$name":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team name"))
                    return

                elif checks.checkCommunityName(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team name"))
                    return

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.name": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "name", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "name", "team"))

                return

            elif team_name.lower() == "$tag":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team tag"))
                    return

                elif checks.checkCommunityTag(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team tag"))
                    return

                team_tag = checks.giveCommunityTag(team_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.tag": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "tag", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "tag", "team"))

                return

            elif team_name.lower() == "$skilltier":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team skill tier"))
                    return

                elif checks.checkSkillTier(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team skillTier, please use the -1 to 29 scale"))
                    return

                team_tag = int(team_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.skillTier": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "team skillTier", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "team skillTier", "team"))

                return

            elif team_name.lower() == "$region":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team region"))
                    return

                elif checks.checkRegion(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team region"))
                    return

                team_tag = checks.giveRegion(team_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.region": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "region", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "region", "team"))

                return

            elif team_name.lower() == "$description":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "description"))
                    return

                elif checks.checkCommunityDescription(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), 'description, surround with "" and no more then 1000 characters'))
                    return

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.description": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "description", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "description", "team"))

                return

            elif team_name.lower() == "$language":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "language"))
                    return

                elif checks.checkLanguage(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team language, no more then 15 characters"))
                    return

                team_tag = str(team_tag).lower()

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.language": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "language", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "language", "team"))

                return

            elif team_name.lower() == "$type":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team type"))
                    return

                elif checks.checkCommunityType(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team type, please use the following casual, semi, competitive, school"))
                    return

                team_tag = checks.giveCommunityType(team_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.type": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "type", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "type", "team"))

                return

            elif team_name.lower() == "$reqskilltier":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "required skill tier"))
                    return

                elif checks.checkSkillTier(team_tag):
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "required skill tier, please use the -1 to 29 scale"))
                    return

                team_tag = checks.giveSkillTier(team_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.reqSkillTier": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "reqSkillTier", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "reqSkillTier", "team"))

                return

            elif team_name.lower() == "$recruiting":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "recruiting"))
                    return

                elif checks.checkBoolean(team_tag) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "recruiting"))
                    return

                team_tag = checks.giveBoolean(team_tag)

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.recruiting": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "recruiting", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "recruiting", "team"))

                return

            elif team_name.lower() == "$contact":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "contact"))
                    return

                elif team_tag == "$me":
                    team_tag = str(raw.message.author)

                elif len(team_tag) < 15 or len(team_tag) > 125:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), 'contact, surround by "", and no less then 15 and no more then 125 characters'))
                    return

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.contact": team_tag}) == True:
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "contact", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "contact", "team"))

                return

            elif team_name.lower() == "$primetime":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                if team_tag == "":
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "prime time"))
                    return

                realPrimeTimes = []
                for time in list((str(team_tag).lower()).split(",")):
                    time = str(time).lower()
                    if checks.checkCommunityTime(time) == False:
                        await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                        return

                    elif time == "allday":
                        realPrimeTimes = ["allday", "morning", "midday", "night"]
                        break

                    elif time not in realPrimeTimes:
                        realPrimeTimes.append(time)

                if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                    realPrimeTimes = ["allday", "morning", "midday", "night"]

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile.primeTime": realPrimeTimes}):
                    await self.bot.send_message(info["destination"], languages.profileSectionUpdated(info["language"], info["mention"], "prime time", "team"))

                else:
                    await self.bot.send_message(info["destination"], languages.profileSectionNotUpdated(info["language"], info["mention"], "prime time", "team"))

                return

            elif team_name.lower() == "$show":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                await self.bot.send_message(info["destination"], languages.profileTest(info["language"], info["mention"], "team"))

                await self.bot.send_message(info["destination"], embed=await self.teamProfile(dict(info["userData"])["vaingloryRelated"]["teamProfile"]))

                return

            # Check if user wants to remove profile
            elif team_name.lower() == "$remove":
                if info["userData"] == False:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return

                elif dict(info["userData"])["vaingloryRelated"]["teamProfile"] == {}:
                    await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                    return
                
                msg = await self.bot.send_message(info["destination"], languages.profileRemoving(info["language"], info["mention"], "team"))

                if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile": 1}, mode="$unset") == True:
                    await self.bot.edit_message(msg, languages.profileRemoved(info["language"], info["mention"], "team"))

                else:
                    await self.bot.edit_message(msg, languages.profileNotRemoved(info["language"], info["mention"], "team"))

                return

            if team_name == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team name**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)
                
                if msg == None:
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team name"))
                    return
                
                else:
                    team_name = msg.content

            if checks.checkCommunityName(team_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_name), "team name"))
                return

            if team_tag == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team tag**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team tag"))
                    return

                else:
                    team_tag = msg.content

            if checks.checkCommunityTag(team_tag) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_tag), "team tag"))
                return

            team_tag = checks.giveCommunityTag(team_tag)

            if team_skillTier == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team required skill tier**, *-1 to 29 scale*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    team_skillTier = defaults["team_skillTier"]

                else:
                    team_skillTier = msg.content

            if checks.checkSkillTier(team_skillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_skillTier), "team skillTier, please use the -1 to 29 scale"))
                return

            team_skillTier = int(team_skillTier)

            if team_region == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's region**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    team_region = defaults["team_region"]

                else:
                    team_region = msg.content

            if checks.checkRegion(team_region) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_region), "team region"))
                return

            team_region = checks.giveRegion(team_region)

            if description == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's description**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    description = defaults["description"]

                else:
                    description = msg.content

            if checks.checkCommunityDescription(description) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(description), 'description, surround with "" and no more then 1000 characters'))
                return

            if team_language == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's language**?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    team_language = defaults["team_language"]

                else:
                    team_language = msg.content

            if checks.checkLanguage(team_language) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_language), "team language, no more then 15 characters"))
                return

            team_language = str(team_language).lower()

            if roles == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's roles**, *any - lane - captain - jungle*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    roles = defaults["roles"]

                else:
                    roles = msg.content

            relRoles = []
            for role in list((str(roles).lower()).split(",")):
                if checks.checkRole(role) == False and str(role).lower() != "none":
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(role), "role"))
                    return

                role = str(role).lower()

                if role not in relRoles:
                    relRoles.append(role)

                elif role == "any":
                    relRoles = ["any", "lane", "captain", "jungle"]
                    break

                elif role == "none":
                    relRoles = ["none"]
                    break

            if "lane" and "captain" and "jungle" in relRoles and "any" not in roles:
                relRoles = ["any", "lane", "captain", "jungle"]

            if reqSkillTier == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's required skill tier**, *-1 to 29 scale*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    reqSkillTier = defaults["reqSkillTier"]

                else:
                    reqSkillTier = msg.content

            if checks.checkSkillTier(reqSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqSkillTier), "required skill tier, please use the -1 to 29 scale"))
                return

            reqSkillTier = checks.giveSkillTier(reqSkillTier)

            if primeTime == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's prime time**, *allday - morning - midday - night*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    primeTime = defaults["primeTime"]

                else:
                    primeTime = msg.content

            realPrimeTimes = []
            for time in list((str(primeTime).lower()).split(",")):
                time = str(time).lower()
                if checks.checkCommunityTime(time) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                    return

                elif time == "allday":
                    realPrimeTimes = ["allday", "morning", "midday", "night"]
                    break

                elif time not in realPrimeTimes:
                    realPrimeTimes.append(time)

            if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                realPrimeTimes = ["allday", "morning", "midday", "night"]

            if team_type == "":
                await self.bot.send_message(info["destination"], info["mention"], ", what's your **team's type**, *casual - semi - competitive - school*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    team_type = defaults["team_type"]

                else:
                    team_type = msg.content

            if checks.checkCommunityType(team_type) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_type), "team type, please use the following casual, semi, competitive, school"))
                return

            team_type = str(team_type).lower()

            if recruiting == "":
                await self.bot.send_message(info["destination"], info["mention"], ", is your **team recruiting**, *true or false*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    recruiting = defaults["recruiting"]

                else:
                    recruiting = msg.content

            if checks.checkBoolean(recruiting) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(recruiting), "recruiting, please use false or true"))
                return

            recruiting = checks.giveBoolean(recruiting)

            if recruiting == "":
                await self.bot.send_message(info["destination"], info["mention"], ", is your **team's contact**, *$me for your discord tag or anything else above 15 and under 125 characters*?")
                msg = await self.bot.wait_for_message(timeout=30, author=raw.message.author, channel=raw.message.author)

                if msg == None:
                    contact = defaults["contact"]

                else:
                    contact = msg.content

            if contact == "$me":
                contact = str(raw.message.author)

            elif len(contact) < 15 or len(contact) > 125:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(contact), 'contact, surround by "", and no less then 15 and no more then 125 characters'))
                return

            msg = await self.bot.send_message(info["destination"], languages.settingUpProfile(info["language"], info["mention"], "team"))

            # Setup profile object
            try:

                # Update this when changing the profile object
                profile_object = {

                    "name": team_name,
                    "tag": team_tag,
                    "skillTier": team_skillTier,
                    "region": team_region,
                    "roles": relRoles,
                    "reqSkillTier": reqSkillTier,
                    "language": team_language,
                    "primeTime": realPrimeTimes,
                    "type": team_type,
                    "description": description,
                    "contact": contact,
                    "recruiting": recruiting

                }

                # FOR DEBUGGING
                print("PROFILE OBJECT: " + str(profile_object))

            except:
                await self.bot.edit_message(msg, languages.settingUpProfileErrorLineOne(info["language"], info["mention"], "team"))

                try:

                    await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

                except Exception as e:
                    await self.bot.edit_message(msg, languages.settingUpProfileErrorLineTwo(info["language"], info["mention"], str(e)))
                    return

                await self.bot.edit_message(msg, languages.settingUpProfileErrorLineThree(info["language"], info["mention"]))

                return


            if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.teamProfile": profile_object}):
                await self.bot.edit_message(msg, languages.settingUpProfileDone(info["language"], info["mention"], "team"))

                await self.bot.send_message(info["destination"], languages.profileTest(info["language"], info["mention"], "team"), embed = await self.teamProfile(profile_object))

            else:
                await self.bot.edit_message(msg, languages.settingUpProfileNotDone(info["language"], info["mention"], "team"))

            return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    # @commands.group(pass_context=True)
    # async def find(self, raw):
    #     """Commands used to find ComputerBot profiles for players, guild and teams."""
    #     pass

    @commands.command(pass_context=True)
    async def vgQp(self, raw, game_mode=""):
        """Find players relative to your ComputerBot profile.

                >vgQp (game_mode)
            game_mode   -   Game mode you're intrested in played.

            Example:
                >vgQp ranked

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "userData"])

            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return

            elif dict(info["userData"])["vaingloryRelated"]["playerProfile"] == {}:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                return

            # Set up what we're looking for
            db_filter = {

                "vaingloryRelated.playerProfile.player.skillTier": {"$gte": dict(info["userData"])["vaingloryRelated"]["playerProfile"]["player"]["skillTier"] - 4, "$lte": dict(info["userData"])["vaingloryRelated"]["playerProfile"]["player"]["skillTier"] + 4},
                "vaingloryRelated.playerProfile.voice": dict(info["userData"])["vaingloryRelated"]["playerProfile"]["voice"]

            }

            if game_mode != "":
                db_filter["vaingloryRelated.playerProfile.player.favGameMode"] = checks.giveGameMode(game_mode)

            msg = await self.bot.send_message(info["destination"], info["mention"] + ", looking for **players relative to your profile**... :eyes:")

            profiles = db.getDiscordUsers(db_filter)

            if profiles == False:
                await self.bot.edit_message(msg, info["mention"] + ", no **players** matching the likes of you where found... :confused:")
                return

            # To collect profiles
            # FOR DEBUGGING
            # print("USER PROFILES: " + str(profiles))
            newProfiles = []
            for profile in profiles:
                # FOR DEBUGGING
                # print("PROFILE: " + str(profile))

                stuff = profile["vaingloryRelated"]["playerProfile"]

                stuff["_id"] = profile["_id"]

                newProfiles.append(stuff)

            # FOR DEBUGGING
            # print("NEW USER PROFILES: " + str(newProfiles))

            await self.bot.edit_message(msg, info["mention"], embed=await self.playerProfile(newProfiles[0]))

            msgs[msg.id] = {"type": "playerProfiles", "profiles": newProfiles, "profileNum": 0, "sent": []}

            if len(newProfiles) > 1:
                #Add reactions to the embed msg
                try:

                    await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                    await self.bot.add_reaction(msg, '\U000023fa')  # Add record button reaction
                    await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

                except:
                    pass

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def vgP(self, raw, region="na", reqSkillTier="-1", voice="true", roles="any", favRole="any", favPower="", favGameMode="", primeTime="allday"):
        """Find a player profile on ComputerBot.

                >vgP (region) (reqSkillTier) (voice) (roles) (favRole) (favPower) (favGameMode) (primeTime)
            region         -   Player's region
            reqSkillTier   -   What skill tier someone has to be to see your profile.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            voice          -   If you're willing to do voice chat while playing.   -   Default: true; Options: true, false.
            roles          -   What roles you're able to play.   -    Default: None, Options: None, Any, Lane, Captain, Jungle; Separate multiple roles with ,
            favRole        -   What role you play most.   -   Default: unknown; Options: unknown, captain, lane, jungle.
            favPower       -   What power you play most.   -   Default: unknown; Options: unknown, weapon, crystal, captain.
            favGameMode    -   What game mode you play most.   -   Default: unknown; Options: unknown, rank, casual, royale, blitz.
            primeTime      -   Your best time to play.   -   Default: allday; Options: allday, morning, midday, night.

            Example:
                >vgP na 19 true lane,captain captain utility rank night

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "usersData"])

            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return

            db_filter = {

                "vaingloryRelated.verifiedRegion": checks.giveRegion(region)

            }

            if checks.checkBoolean(voice) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(voice), "voice"))
                return

            db_filter["vaingloryRelated.playerProfile.voice"] = checks.giveBoolean(voice)

            relRoles = []
            for role in list((str(roles).lower()).split(",")):
                if checks.checkRole(role) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(role), "role"))
                    return

                role = checks.giveRole(role)

                if role == "any":
                    relRoles = ["any", "lane", "captain", "jungle"]
                    break

                elif role not in relRoles:
                    relRoles.append(role)

            if "lane" and "captain" and "jungle" in relRoles and "any" not in relRoles:
                    relRoles = ["any", "lane", "captain", "jungle"]

            if relRoles != []:
                db_filter["vaingloryRelated.playerProfile.roles"] = {"$in": relRoles}

            if checks.checkRole(favRole) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(favRole), "favorite role"))
                return

            db_filter["vaingloryRelated.playerProfile.favRole"] = str(favRole).lower()

            if checks.checkPower(favPower) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(favPower), "favorite game mode"))
                return

            db_filter["vaingloryRelated.playerProfile.favPower"] = checks.givePower(favPower)

            if checks.checkGameMode(favGameMode) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(favGameMode), "favorite game mode"))
                return

            db_filter["vaingloryRelated.playerProfile.faveGameMode"] = str(favGameMode).lower()

            if checks.checkSkillTier(reqSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqSkillTier), "required skill tier"))
                return

            db_filter["vaingloryRelated.playerProfile.reqSkillTier"] = checks.giveSkillTier(reqSkillTier)

            realPrimeTimes = []
            for time in list((str(primeTime).lower()).split(",")):
                time = str(time).lower()
                if checks.checkCommunityTime(time) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                    return

                elif time == "allday":
                    realPrimeTimes = ["allday", "morning", "midday", "night"]
                    break

                elif time not in realPrimeTimes:
                    realPrimeTimes.append(time)

            if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                realPrimeTimes = ["allday", "morning", "midday", "night"]

            if realPrimeTimes != []:
                db_filter["vaingloryRelated.playerProfile.primeTime"] = {"$in": realPrimeTimes}

            msg = await self.bot.send_message(info["destination"], info["mention"] + ", **looking for relative profiles**... :eyes:")

            # FOR DEBUGGING
            print("DB FILTER: " + str(db_filter))

            profiles = db.getDiscordUsers(db_filter)

            if profiles == False:
                await self.bot.edit_message(msg, info["mention"] + ", no **players** matching the likes of you where found... :confused:")
                return

            # To collect profiles
            # FOR DEBUGGING
            # print("USER PROFILES: " + str(profiles))
            newProfiles = []
            for profile in profiles:
                # FOR DEBUGGING
                # print("PROFILE: " + str(profile))

                stuff = profile["vaingloryRelated"]["playerProfile"]

                stuff["_id"] = profile["_id"]

                newProfiles.append(stuff)

            # FOR DEBUGGING
            # print("NEW USER PROFILES: " + str(newProfiles))

            await self.bot.edit_message(msg, info["mention"], embed=await self.playerProfile(newProfiles[0]))

            msgs[msg.id] = {"type": "playerProfiles", "profiles": newProfiles, "profileNum": 0, "sent": []}

            if len(newProfiles) > 1:
                #Add reactions to the embed msg
                try:

                    await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                    await self.bot.add_reaction(msg, '\U000023fa')  # Add record button reaction
                    await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

                except:
                    pass

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def vgUp(self, raw, player_ign="", player_region="na"):
        """Find a player profile on ComputerBot.

                >vgUp (player_ign) (player_region)
            player_ign      -   Player's in-game name.
            player_region   -   Player's in-game region.

            Regions: na, eu, sa, ea, sg, cn, t-na, t-eu, t-sa, t-ea, t-sg

            Example:
                >vgUp ClarkthyLord na

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination"])

            if checks.checkPlayerName(player_ign) == False:
                await self.bot.send_message(info["destination"], languages.invalidPlayerName(info["language"], info["mention"], str(player_ign)))
                return

            player_region = checks.giveRegion(player_region)

            profiles = db.getDiscordUsers({"vaingloryRelated.verifiedName": str(player_ign), "vaingloryRelated.verifiedRegion": str(player_region)})

            # FOR DEBUGGING
            # print("PROFILE: " + str(profiles))
            # print(profiles)

            if profiles == False:
                await self.bot.send_message(info["destination"], info["mention"] + ", **player profile** on **" + str(player_ign) + "**, **" + player_region + "**... :confused:")
                return

            # Out of scope thing
            playerProfile = {}
            for profile in profiles:
                playerProfile = profile["vaingloryRelated"]["playerProfile"]
                break

            # FOR DEBUGGING
            # print("PLAYER PROFILE:")
            # print(playerProfile)

            try:

                await self.bot.send_message(info["destination"], info["mention"], embed=await self.playerProfile(playerProfile))

            except:
                # FOR DEBUGGING
                # print("ERROR SENDING UNIQUE PLAYER PROFILE: " + str(format_exc()))

                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "player"))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def vgG(self, raw, guild_region="na", reqLevel="0", reqSkillTier="-1", primeTime="allday", guild_type="casual", recruiting="true", guild_language=""):
        """Find a guild profile on ComputerBot.

                >vgG (guild_region) (reqLevel) (reqSkillTier) (primeTime) (guild_type) (recruiting) (guild_language)
            guild_region     -   Guild's in-game region.
            reqLevel         -   Guild's in-game skill tier.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            reqSkillTier     -   What skill tier someone has to be to see this guild profile.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            primeTime        -   Guild's most active time.   -   Default: allday; Options: allday, morning, midday, night.
            guild_type       -   Type of guild   -   Default: casual; Options: casual, semi, competitive, school.
            recruiting       -   If this guild is looking to recruit new members.   -   Default: true; Options: true, false
            guild_language   -   Language this guild speaks primarily.   -   No more then 15 characters.

            Example:
                >vgG na 19 lane 21 allday casual true english

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "userData"])

            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return

            db_filter = {}

            if checks.checkRegion(guild_region) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_region), "guild region"))
                return

            db_filter["vaingloryRelated.guildProfile.region"] = checks.giveRegion(guild_region)

            if checks.checkCommunityLevel(reqLevel) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqLevel), "guild level"))
                return

            db_filter["vaingloryRelated.guildProfile.level"] = int(reqLevel)

            if checks.checkSkillTier(reqSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqSkillTier), "required skill tier, please use the -1 to 29 scale"))
                return

            db_filter["vaingloryRelated.guildProfile.reqSkillTier"] = checks.giveSkillTier(reqSkillTier)

            realPrimeTimes = []
            for time in list((str(primeTime).lower()).split(",")):
                time = str(time).lower()
                if checks.checkCommunityTime(time) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                    return

                elif time == "allday":
                    realPrimeTimes = ["allday", "morning", "midday", "night"]
                    break

                elif time not in realPrimeTimes:
                    realPrimeTimes.append(time)

            if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                realPrimeTimes = ["allday", "morning", "midday", "night"]

            if realPrimeTimes != []:
                db_filter["vaingloryRelated.guildProfile.primeTime"] = {"$in": realPrimeTimes}

            if guild_type == "":
                pass

            elif checks.checkCommunityType(guild_type) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_type), "guild type, please use the following casual, semi, competitive, school"))
                return

            else:
                db_filter["vaingloryRelated.guildProfile.type"] = str(guild_type).lower()

            if checks.checkBoolean(recruiting) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(recruiting), "recruiting, please use false or true"))
                return

            db_filter["vaingloryRelated.guildProfile.recruiting"] = checks.giveBoolean(recruiting)

            if guild_language == "":
                pass

            elif checks.checkLanguage(guild_language) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_language), "guild language, no more then 15 characters"))
                return

            else:
                db_filter["vaingloryRelated.guildProfile.language"] = str(guild_language).lower()

            # FOR DEBUGGING
            print("DB FILTER: " + str(db_filter))

            profiles = db.getDiscordUsers(db_filter)

            # FOR DEBUGGING
            print("PROFILES: " + str(profiles))

            if profiles == False:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], info["guild"]))
                return

            realProfiles = []
            for profile in profiles:
                realProfiles.append(profile["vaingloryRelated"]["guildProfile"])

            msg = await self.bot.send_message(info["destination"], info["mention"], embed=await self.guildProfile(realProfiles[0]))

            msgs[msg.id] = {"type": "guildProfiles", "profiles": realProfiles, "profileNum": 0}

            if len(realProfiles) > 1:
                #Add reactions to the embed msg
                try:

                    await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                    await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

                except:
                    pass

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def vgUg(self, raw, guild_name="", guild_region="na"):
        """Look up a guild profile, on ComputerBot, by it's name and region.

                >vgUg (guild_name) (guild_region)
            guild_name     -   Guild's name.     -   Surround with "".
            guild_region   -   Guild's region.   -   Default: na; Options: na, eu, sa, ea, sg, cn

            Example:
                >vgUg "Kings Home" na

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination"])

            # Convert to string just to be sure
            guild_name = str(guild_name)

            if guild_name == "":
                await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "guild name"))
                return

            elif checks.checkCommunityName(guild_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(guild_name), "gulid name"))
                return

            guild_region = checks.giveRegion(guild_region)

            profiles = db.getDiscordUsers({"vaingloryRelated.guildProfile.name": guild_name, "vaingloryRelated.guildProfile.region": guild_region})

            # FOR DEBUGGING
            # print("GUILD PROFILE: " + str(profiles))

            if profiles == False:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                return

            guildProfile = {}
            for profile in profiles:
                guildProfile = profile["vaingloryRelated"]["guildProfile"]
                break

            try:

                await self.bot.send_message(info["destination"], info["mention"], embed=await self.guildProfile(guildProfile))

            except:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "guild"))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def vgT(self, raw, team_region="na", reqTeamSkillTier="-1", roles="any", reqSkillTier="-1", team_type="casual", primeTime="allday", team_language="", recruiting="true"):
        """Find a team profile on ComputerBot.

                >vgT (team_region) (reqTeamSkillTier) (roles) (reqSkillTier) (primeTime) (team_type) (recruiting) (team_language)
            team_region        -   Team's in-game region.
            reqTeamSkillTier   -   Team's in-game skill tier.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            roles              -   Roles the team is looking for.   -   Default: None, Options: None, Any, Lane, Captain, Jungle; Seperate multiple roles with ,
            reqSkillTier       -   What skill tier someone has to be to see this team profile.   -   Default: -1; Scale: -1(Unranked) - 29(Vainglorious).
            primeTime          -   team's most active time.   -   Default: allday; Options: allday, morning, midday, night.
            team_type          -   Type of team   -   Default: casual; Options: casual, semi, competitive, school.
            recruiting         -   If this team is looking to recruit new members.   -   Default: true; Options: true, false
            team_language      -   Language this team speaks primarily.   -   No more then 15 characters.

            Example:
                >vgT na 19 lane 21 allday casual true english

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "userData"])

            if verify.giveVerified(raw.message.author.id) == False:
                await self.bot.send_message(info["destination"], languages.notVerified(info["language"], info["mention"], str(self.bot.command_prefix[0])))
                return

            db_filter = {}

            if checks.checkRegion(team_region) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_region), "team region"))
                return

            db_filter["vaingloryRelated.teamProfile.region"] = checks.giveRegion(team_region)

            if checks.checkSkillTier(reqTeamSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqTeamSkillTier), "team skillTier, please use the -1 to 29 scale"))
                return

            db_filter["vaingloryRelated.teamProfile.skillTier"] = int(reqTeamSkillTier)

            relRoles = []
            for role in list((str(roles).lower()).split(",")):
                if checks.checkRole(role) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(role), "role"))
                    return

                role = checks.giveRole(role)

                if role == "any":
                    relRoles = ["any", "lane", "captain", "jungle"]
                    break

                elif role not in relRoles:
                    relRoles.append(role)

            if "lane" and "captain" and "jungle" in relRoles and "any" not in relRoles:
                    relRoles = ["any", "lane", "captain", "jungle"]

            if relRoles != []:
                db_filter["vaingloryRelated.playerProfile.roles"] = {"$in": relRoles}

            if checks.checkSkillTier(reqSkillTier) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(reqSkillTier), "required skill tier, please use the -1 to 29 scale"))
                return

            db_filter["vaingloryRelated.teamProfile.reqSkillTier"] = checks.giveSkillTier(reqSkillTier)

            realPrimeTimes = []
            for time in list((str(primeTime).lower()).split(",")):
                time = str(time).lower()
                if checks.checkCommunityTime(time) == False:
                    await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(time), "prime time"))
                    return

                elif time == "allday":
                    realPrimeTimes = ["allday", "morning", "midday", "night"]
                    break

                elif time not in realPrimeTimes:
                    realPrimeTimes.append(time)

            if "morning" and "midday" and "night" in realPrimeTimes and "allday" not in realPrimeTimes:
                realPrimeTimes = ["allday", "morning", "midday", "night"]

            if realPrimeTimes != []:
                db_filter["vaingloryRelated.teamProfile.primeTime"] = {"$in": realPrimeTimes}

            if checks.checkCommunityType(team_type) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_type), "team type, please use the following casual, semi, competitive, school"))
                return

            db_filter["vaingloryRelated.teamProfile.teamType"] = str(team_type).lower()

            if checks.checkBoolean(recruiting) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(recruiting), "recruiting, please use false or true"))
                return

            db_filter["vaingloryRelated.teamProfile.recruiting"] = checks.giveBoolean(recruiting)

            if team_language == "":
                pass

            elif checks.checkLanguage(team_language) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_language), "team language, no more then 15 characters"))
                return

            else:
                db_filter["vaingloryRelated.teamProfile.language"] = str(team_language).lower()

            # FOR DEBUGGING
            print("DB FILTER: " + str(db_filter))

            profiles = db.getDiscordUsers(db_filter)

            # FOR DEBUGGING
            print("PROFILES: " + str(profiles))

            if profiles == False:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                return

            realProfiles = []
            for profile in profiles:
                realProfiles.append(profile["vaingloryRelated"]["teamProfile"])

            msg = await self.bot.send_message(info["destination"], info["mention"], embed=await self.teamProfile(realProfiles[0]))

            msgs[msg.id] = {"type": "teamProfiles", "profiles": realProfiles, "profileNum": 0}

            if len(realProfiles) > 1:
                #Add reactions to the embed msg
                try:

                    await self.bot.add_reaction(msg, '\U00002b05')  # Add left arrow reaction
                    await self.bot.add_reaction(msg, '\U000027a1')  # Add right arrow reaction

                except:
                    pass

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def vgUt(self, raw, team_name="", team_region=""):
        """Look up a team profile, on ComputerBot, by it's name and region.

                >vgUt (team_name) (team_region)
            team_name     -   Teams's name.     -   Surround with "".
            team_region   -   Teams's region.   -   Default: na; Options: na, eu, sa, ea, sg, cn

            Example:
                >vgUt "Thy True Kings" na

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination"])

            # Convert to string just to be sure
            team_name = str(team_name)

            if team_name == "":
                await self.bot.send_message(info["destination"], languages.noInput(info["language"], info["mention"], "team name"))
                return

            elif checks.checkCommunityName(team_name) == False:
                await self.bot.send_message(info["destination"], languages.invalidInput(info["language"], info["mention"], str(team_name), "gulid name"))
                return

            team_region = checks.giveRegion(team_region)

            profiles = db.getDiscordUsers({"vaingloryRelated.teamProfile.name": team_name, "vaingloryRelated.teamProfile.region": team_region})

            # FOR DEBUGGING
            print("TEAM PROFILES: " + str(profiles))

            if profiles == False:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                return

            teamProfile = {}
            for profile in profiles:
                # FOR DEBUGGING
                print("TEAM PROFILE LOOP: " + str(profile))
                teamProfile = profile["vaingloryRelated"]["teamProfile"]
                break

            # FOR DEBUGGING
            print("TEAM PROFILE: " + str(teamProfile))

            try:

                await self.bot.send_message(info["destination"], info["mention"], embed=await self.teamProfile(teamProfile))

            except:
                await self.bot.send_message(info["destination"], languages.noProfile(info["language"], info["mention"], "team"))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    async def playerProfile(self, profile):
        """Create an embed out of a player profile.

        :arguments profile: Profile dictionary, of a player.
        :returns: Embed object.

        """

        try:

            embed = discord.Embed(
                title=profile["player"]["name"] + ", " + profile["player"]["shardId"] + ", Profile",
                url=config.bot_server,
                description=profile["description"]
            )

            embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

            embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

            roles = ""
            for role in profile["roles"]:
                roles += role + " "

            times = ""
            for time in profile["primeTime"]:
                times += time + " "

            embed.add_field(name="About", value="Does Voice: " + str(profile["voice"]) + "Prime Time: " + times + "\nPlays: " + roles + "|Fav. Role: " + profile["favRole"] + "\nFav. Power: " + profile["favPower"] + " |Fav. Game Mode: " + profile["favGameMode"])

            embed.add_field(name="Stats", value="Skill Tier: " + tools.giveFormat(profile["player"]["skillTier"], "skillTier") + " |Karma: " + tools.giveFormat(profile["player"]["karmaLevel"], "karma") + "\nWin Rate: " + str(round((profile["player"]["wins"] / profile["player"]["played"]) * 100, 2)))

            return embed

        except:
            # FOR DEBUGGING
            print("ERROR CREATING PLAYER PROFILE EMBED: " + str(format_exc()))

            return False

    async def guildProfile(self, profile):
        """Create an embed out of a guild profile.

        :arguments profile: Profile dictionary, of a guild.
        :returns: Embed object.

        """

        try:

            embed = discord.Embed(
                title=str(profile["name"]) + "[" + str(profile["tag"]) + "], " + str(profile["region"]) + ", Profile",
                url=config.bot_server,
                description=str(profile["description"])
            )

            embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

            embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

            times = ""
            for time in profile["primeTime"]:
                times += str(time) + " "

            embed.add_field(name="About", value="Prime Time: " + str(times) + "\nLanguage: " + str(profile["language"]) + "\nType: " + str(profile["type"]))

            embed.add_field(name="Stats", value="Level: " + str(profile["level"]) + "\nRecruiting:" + str(profile["recruiting"]))

            embed.add_field(name="About", value="Contact: " + str(profile["contact"]))

            return embed

        except:
            # FOR DEBUGGING
            print("ERROR CREATING GUILD PROFILE EMBED: " + str(format_exc()))

            return False

    async def teamProfile(self, profile):
        """Create an embed out of a team profile.

        :arguments profile: Profile dictionary, of a team.
        :returns: Embed object.

        """

        try:

            embed = discord.Embed(
                title=str(profile["name"]) + ", " + str(profile["region"]) + ", Profile",
                url=config.bot_server,
                description=str(profile["description"])
            )

            embed.set_author(name=config.bot_name, url=config.bot_server, icon_url=config.bot_icon)

            embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

            roles = ""
            for role in profile["roles"]:
                roles += str(role) + " "

            times = ""
            for time in profile["primeTime"]:
                times += str(time) + " "

            embed.add_field(name="About", value="Prime Time: " + str(times) + "\nLanguage: " + str(profile["language"]) + "\nType: " + str(profile["type"]))

            msg = "Skill Tier: " + str(tools.giveFormat(profile["skillTier"], "skillTier")) + "\nRecruiting:" + str(profile["recruiting"])

            if roles != "":
                msg += "\nLooking For: " + str(roles)

            embed.add_field(name="Stats", value=msg)

            embed.add_field(name="About", value="Contact: " + str(profile["contact"]))

            return embed

        except:
            # FOR DEBUGGING
            print("ERROR CREATING TEAM PROFILE EMBED: " + str(format_exc()))

            return False

    async def getInfo(self, message, req=[], check=""):
        """Gives info needed to function related to Vainglory.

            :param req: A list, containg Strings, of everything needed. Options: userData, serverData, mention, textAd, destination, language, compact, emojis
            :param check: Check if this value effects the outcome of the data.
            :returns: Information required to function.

        """

        # FOR DEBUGGING
        # print("---INPUT:\nMESSAGE: " + str(message) + "\nREQ: " + str(req) + "\nCHECK: " + str(check) + "\n---")

        if req == []:
            return {"error": "REQ IS EMPTY"}

        # Values to give when all goes wrong
        defaults = {
            "userData": False,
            "serverData": False,
            "mention": str(message.author),
            "textAd": "Thank you for choosing ComputerBot :3",
            "destination": message.author,
            "language": "english",
            "compact": False,
            "emojis": True
        }

        result = {}  # What's going to be sent
        try:

            # If communication pipe is private, Example: private messages
            if message.channel.is_private == True:
                try:

                    if "mention" in req:
                        result["mention"] = defaults["mention"]

                    if "textAd" in req:
                        try:

                            result["textAd"] = ads.giveTextAds()

                            if result["textAd"] in [None, False]:
                                result["textAd"] = defaults["textAd"]

                        except:
                            result["textAd"] = defaults["textAd"]

                    # Fetch data on user
                    data = db.discordUserDictionary(message.author.id)

                    # FOR DEBUGGING
                    # print("USER DATA:   " + str(data))

                    # If no data is found relative to the user return the default settings
                    if data in [False, None]:

                        if "userData" in req:
                            result["userData"] = defaults["userData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

                    # Data relative to the user was found
                    else:

                        if "userData" in req:
                            result["userData"] = data

                        if "language" in req:
                            try:

                                result["language"] = data["general"]["language"]

                            except:  # Set to default if not found
                                result["language"] = defaults["language"]

                        if "compact" in req:
                            try:

                                result["compact"] = data["vaingloryRelated"]["compact"]

                            except:  # Set to default if not found
                                result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            try:

                                result["emojis"] = data["vaingloryRelated"]["emojis"]

                            except:  # Set to default if not found
                                result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = message.author

                # In-case of a huge error return default settings
                except:
                        if "userData" in req:
                            result["userData"] = defaults["userData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

            # If communication pipe isn't private, Example: server/guild
            else:
                try:

                    if "mention" in req:
                        try:
                            result["mention"] = str((await self.bot.get_user_info(message.author.id)).mention)

                        except:
                            result["mention"] = defaults["mention"]

                    if "textAd" in req:
                        try:

                            result["textAd"] = ads.checkTextAds(message.server.id)

                            if result["textAd"] in [None, False]:
                                result["textAd"] = defaults["textAd"]

                        except:
                            result["textAd"] = defaults["textAd"]

                    # Fetch data on discord server
                    data = db.discordServerDictionary(message.server.id)

                    # FOR DEBUGGING
                    # print("SERVER DATA:   " + str(data))

                    # If no data is found relative to the server return the default settings
                    if data in [False, None]:

                        if "serverData" in req:
                            result["serverData"] = defaults["serverData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            if (message.server.get_member(self.bot.user.id)).server_permissions.external_emojis == False:
                                result["emojis"] = False
                                result["error-emojis"] = True  # State that emojis can't be sent because of set up

                            else:
                                result["emojis"] = defaults["emojis"]

                        if "destination" in req:
                            result["destination"] = message.channel

                    # If the value, check, given is not permitted on this communication pipe then give from user data instead
                    elif check != "" and check in data["general"]["commandBans"]:
                        try:

                            userData = db.discordUserDictionary(message.author.id)

                            # FOR DEBUGGING
                            # print("USER DATA:   " + str(userData))

                            # If no data is found relative to the user return the default settings
                            if userData in [False, None]:

                                if "userData" in req:
                                    result["userData"] = defaults["userData"]

                                if "serverData" in req:
                                    result["serverData"] = data

                                if "language" in req:
                                    result["language"] = defaults["language"]

                                if "compact" in req:
                                    result["compact"] = defaults["compact"]

                                if "emojis" in req:
                                    result["emojis"] = defaults["emojis"]

                                if "destination" in req:
                                    result["destination"] = message.author

                            # Data relative to the user was found
                            else:

                                if "userData" in req:
                                    result["userData"] = userData

                                if "serverData" in req:
                                    result["serverData"] = data

                                if "language" in req:
                                    try:

                                        result["language"] = userData["general"]["language"]

                                    except:  # Set to default if not found
                                        result["language"] = defaults["language"]

                                if "compact" in req:
                                    try:

                                        result["compact"] = userData["vaingloryRelated"]["compact"]

                                    except:  # Set to default if not found
                                        result["compact"] = defaults["compact"]

                                if "emojis" in req:
                                    try:

                                        result["emojis"] = userData["vaingloryRelated"]["emojis"]

                                    except:  # Set to default if not found
                                        result["emojis"] = defaults["emojis"]

                                if "destination" in req:
                                    result["destination"] = message.author

                        # In-case of a huge error return default settings
                        except:
                                if "userData" in req:
                                    result["userData"] = defaults["userData"]

                                if "serverData" in req:
                                    result["serverData"] = data

                                if "language" in req:
                                    result["language"] = defaults["language"]

                                if "compact" in req:
                                    result["compact"] = defaults["compact"]

                                if "emojis" in req:
                                    result["emojis"] = defaults["emojis"]

                                if "destination" in req:
                                    result["destination"] = defaults["destination"]

                    # Data relative to the server was found
                    else:
                        if "serverData" in req:
                            result["serverData"] = data

                        if "language" in req:
                            try:

                                result["language"] = data["general"]["language"]

                            except:  # Set to default if not found
                                result["language"] = defaults["language"]

                        if "compact" in req:
                            try:

                                result["compact"] = data["vaingloryRelated"]["compact"]

                            except:  # Set to default if not found
                                result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            try:

                                result["emojis"] = data["vaingloryRelated"]["emojis"]

                            except:  # Set to default if not found
                                result["emojis"] = defaults["emojis"]

                            if result["emojis"] == True and (message.server.get_member(self.bot.user.id)).server_permissions.external_emojis == False:
                                result["emojis"] = False
                                result["error-emojis"] = True  # State that emojis can't be sent because of set up

                        if "destination" in req:
                            try:

                                # Get the channels ID or state(False/None if nothing is set)
                                result["destination"] = data["general"]["botChannel"]

                                # If bot channel is not set for the server then send to the same channel
                                if result["destination"] in [False, None]:
                                    result["destination"] = message.channel

                                # If bot channel is set do the following
                                else:
                                    # Get a channel object from what's in bot channel
                                    result["destination"] = self.bot.get_channel(result["destination"])

                                    # If discord couldn't find this channel then set to default
                                    if result["destination"] in [False, None]:
                                        result["destination"] = message.channel

                            except:  # Set to default  if not found
                                result["destination"] = message.channel

                except:  # In-case of a huge error return default settings
                        if "serverData" in req:
                            result["serverData"] = defaults["serverData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "compact" in req:
                            result["compact"] = defaults["compact"]

                        if "emojis" in req:
                            result["emojis"] = defaults["emojis"]

                            if result["emojis"] == True and (message.server.get_member(self.bot.user.id)).server_permissions.external_emojis == False:
                                result["emojis"] = False
                                result["error-emojis"] = True  # State that emojis can't be sent because of set up

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

                if "userData" in req and "userData" not in result:
                    try:

                        result["userData"] = db.discordUserDictionary(message.author.id)

                        if result["userData"] in [False, None]:
                            result["userData"] = defaults["userData"]

                    except:
                        result["userData"] = defaults["userData"]

                if "serverData" in req and "serverData" not in result:
                    try:

                        result["serverData"] = db.discordServerDictionary(message.server.id)

                        if result["serverData"] in [False, None]:
                            result["serverData"] = defaults["serverData"]

                    except:
                        result["serverData"] = defaults["serverData"]

            # FOR DEBUGGING
            # print("---OUTPUT:\nINFO: " + str(result) + "\n---")

            return result

        except:
            # FOR DEBUGGING
            print("ERROR INFORMATION GATHERING:   " + str(format_exc()))

            return {"error": str(format_exc())}


def setup(bot):
    """Adds commands to the bot_work on load of this module."""

    bot.add_cog(Vainglory(bot))
    bot.add_cog(Matching(bot))
