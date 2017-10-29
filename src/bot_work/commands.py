import discord
from discord.ext import commands
import config
from src.mongo_work import core as db
from src.vainglory_work import checks as vgc
from src.bot_work import languages, ads, lottery, checks, core
from discord.ext.commands.cooldowns import BucketType
from src.extra import tools
from traceback import format_exc
import json
import pickle
import datetime


def storeMemberCount():
    member_count = config.member_count

    try:

        with open(config.directory + "//pickle-db//memberCount.pickle", "wb") as handler:
            pickle.dump(member_count, handler, protocol=pickle.HIGHEST_PROTOCOL)

        # FOR DEBUGGING
        # print("MEMBER COUNT:   " + str(member_count))

    except Exception as e:
        print("!!!COULDN'T SAVE MEMBER COUNT!!!\n" + str(e))


class Bot():

    def __init__(self, bot):
        """At creation of this objects setup what's needed."""

        self.bot = bot  # Create a bots instance in this object

    # Gives a LINK from where one CAN add THIS BOT
    @commands.command(pass_context=True)
    async def invite(self, raw):
        """When you want to invite this bot to another server."""

        try:

            data = db.discordUserDictionary(raw.message.author.id)

            # FOR DEBUGGING
            # print("USER DATA:   " + str(data))

            if data == False or data == None:
                language = "english"

            else:
                language = data["general"]["language"]

        except:
            language = "english"

        await self.bot.say(languages.inviteLineOne(language))

    # Gives a LINK from where one CAN add THIS BOT
    @commands.command(pass_context=True)
    async def lottery(self, raw):
        """Look at the bot's lottery."""

        try:

            if raw.message.channel.is_private == True:
                try:

                    data = db.discordUserDictionary(raw.message.author.id)

                    # FOR DEBUGGING
                    # print("USER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.author

                    else:
                        language = data["general"]["language"]
                        destination = raw.message.author

                except:
                    language = "english"
                    destination = raw.message.author

            else:
                try:
                    data = db.discordServerDictionary(raw.message.server.id)

                    # FOR DEBUGGING
                    # print("SERVER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.channel

                    else:
                        try:
                            language = data["general"]["language"]

                            if language == False or language == None:
                                language = "english"

                        except:
                            language = "english"

                        try:
                            destination = data["general"]["botChannel"]

                            if destination == False or destination == None:
                                destination = raw.message.channel

                            else:
                                destination = self.bot.get_channel(destination)
                                if destination == None or destination == False:
                                    destination = raw.message.channel

                        except:
                            destination = raw.message.channel

                except:
                    language = "english"
                    destination = raw.message.channel

        except:
            language = "english"
            destination = raw.message.author

        embed = discord.Embed(title=languages.lotteryTitleOne(language), colour=discord.Colour.gold(), url=str(config.bot_server), description=languages.lotteryDescriptionOne(language))

        embed.set_author(name=str(config.bot_name), url=str(config.bot_server), icon_url=str(config.bot_icon))

        embed.set_image(url="https://vaingloryhack.com/wp-content/uploads/2017/03/download.png")

        embed.set_footer(text="Thank you for supporting us :3 | Contact us!")

        await self.bot.send_message(destination, embed=embed)

    @commands.command(pass_context=True)
    async def about(self, raw):
        """About ComputerBot"""

        try:

            if raw.message.channel.is_private == True:
                try:
                    data = db.discordUserDictionary(raw.message.author.id)

                    # FOR DEBUGGING
                    # print("USER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.author
                    else:
                        language = data["general"]["language"]
                        destination = raw.message.author
                except:
                    language = "english"
                    destination = raw.message.author
            else:
                try:
                    data = db.discordServerDictionary(raw.message.server.id)

                    # FOR DEBUGGING
                    # print("SERVER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.channel

                    else:
                        try:
                            language = data["general"]["language"]
                            if language == False or language == None:
                                language = "english"
                        except:
                            language = "english"

                        try:
                            destination = data["general"]["botChannel"]
                            if destination == False or destination == None:
                                destination = raw.message.channel
                            else:
                                destination = self.bot.get_channel(destination)
                                if destination == None or destination == False:
                                    destination = raw.message.channel
                        except:
                            destination = raw.message.channel

                except:
                    language = "english"
                    destination = raw.message.channel

            # FOR DEBUGGING
            # print("LANGUAGE:   " + language)
            # print("DESTINATION:   " + str(destination))

            embed = discord.Embed(title=languages.aboutTitle(language), url=config.bot_server, description=languages.aboutDescription(language))

            embed.set_author(name=config.bot_name, url=config.bot_invite, icon_url=config.bot_icon)

            embed.set_footer(text=config.bot_embed_footer, icon_url=config.bot_icon)

            embed.add_field(name=languages.aboutFieldOneTitle(language), value=languages.aboutFieldOne(language, str(self.bot.command_prefix[0])))

            embed.add_field(name=languages.aboutFieldTwoTitle(language), value=languages.aboutFieldTwo(language, str(self.bot.command_prefix[0])))

            # embed.add_field(name=languages.aboutFieldThreeTitle(language), value=languages.aboutFieldThreeV1(language, str(len(self.bot.servers))))

            embed.add_field(name=languages.aboutFieldThreeTitle(language), value=languages.aboutFieldThreeV2(language, str(len(self.bot.servers)), str(config.member_count["count"])))

            embed.add_field(name=languages.aboutFieldFourTitle(language), value=languages.aboutFieldFour(language))

            await self.bot.send_message(destination, embed=embed)

            # FOR DEBUGGING
            # print("UPDATED MEMBER COUNT BEFORE: " + str(config.member_count["updated"]))
            # print("TIME DIFFERENCE: " + str(((datetime.datetime.now() - config.member_count["updated"]).seconds / 60)))

            # Check if it's been over half a day since last member count or if no member count had been done yet
            # if config.member_count["updated"] == None:
            #     config.member_count["updated"] = datetime.datetime.now()
            #
            #     # FOR DEBUGGING
            #     # print("UPDATED MEMBER COUNT AFTER: " + str(config.member_count["updated"]))
            #
            #     member_list = []
            #     for member in self.bot.get_all_members():
            #         if str(member) in member_list:
            #             continue
            #
            #         member_list.append(str(member))
            #
            #         # FOR DEBUGGING
            #         # print(member)
            #
            #     # FOR DEBUGGING
            #     # print("MEMBER SIZE: " + str(len(member_list)) + "\nMEMBER LIST: " + str(member_list))
            #
            #     config.member_count["count"] = len(member_list)
            #     storeMemberCount()

            if config.member_count["updated"] == None or ((datetime.datetime.now() - config.member_count["updated"]).seconds / 60) > 720:
                config.member_count["updated"] = datetime.datetime.now()

                # FOR DEBUGGING
                # print("!!!CALCULATING MEMBER COUNT!!!")
                # print("UPDATED MEMBER COUNT AFTER: " + str(config.member_count["updated"]))

                member_list = []
                for member in self.bot.get_all_members():
                    if str(member) in member_list:
                        continue

                    member_list.append(str(member))

                    # FOR DEBUGGING
                    # print(member)

                # FOR DEBUGGING
                # print("MEMBER SIZE: " + str(len(member_list)) + "\nMEMBER LIST: " + str(member_list))

                config.member_count["count"] = len(member_list)
                storeMemberCount()

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @commands.command(pass_context=True)
    async def donate(self, raw):
        """Get information on how you can support ComputerBot."""

        try:

            if raw.message.channel.is_private == True:
                try:
                    data = db.discordUserDictionary(raw.message.author.id)

                    # FOR DEBUGGING
                    # print("USER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.author
                    else:
                        language = data["general"]["language"]
                        destination = raw.message.author
                except:
                    language = "english"
                    destination = raw.message.author
            else:
                try:
                    data = db.discordServerDictionary(raw.message.server.id)

                    # FOR DEBUGGING
                    # print("SERVER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.channel

                    else:
                        try:
                            language = data["general"]["language"]
                            if language == False or language == None:
                                language = "english"
                        except:
                            language = "english"

                        try:
                            destination = data["general"]["botChannel"]
                            if destination == False or destination == None:
                                destination = raw.message.channel
                            else:
                                destination = self.bot.get_channel(destination)
                                if destination == None or destination == False:
                                    destination = raw.message.channel
                        except:
                            destination = raw.message.channel

                except:
                    language = "english"
                    destination = raw.message.channel

            # FOR DEBUGGING
            # print("LANGUAGE:   " + language)
            # print("DESTINATION:   " + str(destination))

            embed = discord.Embed(title=languages.donateTitle(language), url=str(config.bot_donation), colour=discord.Colour(0x33FF58), description=languages.donateDescription(language))

            await self.bot.send_message(destination, embed=embed)

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    # Used to SEND a COMPLAINT
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3600, BucketType.user)
    async def report(self, raw, *, message=""):
        """Report an instance involving the ComputerBot.

                >report (message)
            message   ~   Message being sent to us

            Example:
                >report Bot isn't showing embeds in my pms!

        """

        try:

            data = db.discordUserDictionary(raw.message.author.id)

            # FOR DEBUGGING
            # print("USER DATA:   " + str(data))

            if data == False or data == None:
                language = "english"

            else:
                language = data["general"]["language"]

        except:
            language = "english"

        # FOR DEBUGGING
        # print("MESSAGE:   " + str(message))

        if len(str(message)) < 15:
            await self.bot.say(raw.message.author, languages.reportSize(language))
            return

        report = "FROM: " + str(raw.message.author) + " | SERVER: " + str(raw.message.server) + "\nMSG:   " + str(message)

        # FOR DEBUGGING
        # print("REPORT:   " + str(report))

        try:

            await self.bot.send_message(self.bot.get_channel(config.discord_reports_channel), report)
            await self.bot.send_message(raw.message.author, languages.reportLineOne(language, message))

        except:
            await self.bot.send_message(raw.message.author, languages.reportLineTwo(language))

# SERVER COMMANDS   <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    @commands.group(pass_context=True)
    async def server(self, raw):
        """Commands used by server owners and administrators to configure bots usage."""
        pass

    # @server.command(pass_context=True)
    # async def nothing(self, raw):
    #     """"""
    #
    #     # TODO 1- X 2- X 3- X 4- X 5- MODERATION COMMANDS 6- VAINGLORY REGION OF SERVER 7- X 8- X 9- X 10- X 11- SERVER LANGUAGE
    #
    #     pass

    @commands.command(pass_context=True)
    async def serverInfo(self, raw):
        """Info on the current server.

                >server serverInfo

            Example:
                >server serverInfo

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            # FOR DEBUGGING
            # print("SERVER DATA:   " + str(data))

            if data == False or data == None:
                await self.bot.say("We **don't have** any **data** on **" + str(raw.message.server) + "**... :confused:")
                return

            else:
                try:

                    if "serverInfo" in data["general"]["commandBans"]:
                        try:
                            data = db.discordUserDictionary(raw.message.author.id)

                            # FOR DEBUGGING
                            # print("USER DATA:   " + str(data))

                            if data == False or data == None:
                                language = "english"
                                destination = raw.message.author
                            else:
                                language = data["general"]["language"]
                                destination = raw.message.author
                        except:
                            language = "english"
                            destination = raw.message.author

                    else:
                        try:
                            language = data["general"]["language"]
                            if language == False or language == None:
                                language = "english"
                        except:
                            language = "english"

                        try:
                            destination = data["general"]["botChannel"]
                            if destination == False or destination == None:
                                destination = raw.message.channel
                            else:
                                destination = self.bot.get_channel(destination)
                                if destination == None or destination == False:
                                    destination = raw.message.channel
                        except:
                            destination = raw.message.channel

                except:
                    language = "english"
                    destination = raw.message.author

            # FOR DEBUGGING
            # print("LANGUAGE:   " + language)
            # print("DESTINATION:   " + str(destination))

            try:  # Support for old data

                emojis = str(data["vaingloryRelated"]["emojis"])

            except Exception as e:

                # FOR DEBUGGING
                # print("ERROR: " + str(e))

                emojis = True

            embed = discord.Embed(title=languages.serverInfoTitle(language,
                                  str(raw.message.server)),
                                  colour=discord.Colour(0x354b),
                                  url=config.bot_server,
                                  description=languages.serverInfoDescription(language, str(raw.message.server)))

            embed.set_author(name=config.bot_name, url=config.bot_invite, icon_url=config.bot_icon)

            embed.set_footer(text=config.bot_embed_footer, icon_url=config.bot_icon)

            embed.add_field(name=languages.serverInfoFieldOneTitle(language), value=languages.serverInfoFieldOne(language, str(data["tournamentRelated"]["defaultGame"]), str(data["general"]["notify"]), str(data["general"]["notifyOwner"]), str(data["general"]["botChannel"])))

            embed.add_field(name=languages.serverInfoFieldTwoTitle(language), value=languages.serverInfoFieldTwo(language, str(data["general"]["commandBans"])))

            embed.add_field(name=languages.serverInfoFieldThreeTitle(language), value=languages.serverInfoFieldThree(language, str(data["vaingloryRelated"]["defaultRegion"]), str(data["vaingloryRelated"]["guildName"]), str(data["vaingloryRelated"]["guildTag"]), str(data["vaingloryRelated"]["teamName"]), str(data["vaingloryRelated"]["teamTag"]), str(data["vaingloryRelated"]["compact"]), str(emojis)))

            embed.add_field(name=languages.serverInfoFieldFourTitle(language), value=languages.serverInfoFieldFour(language))

            await self.bot.send_message(destination, embed=embed)

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def prefix(self, raw, prefix=str(config.default_prefix)):
        """Change this servers command prefix.

                >server prefix (prefix)
            prefix   -   New prefix   -   Default: $; No blank spaces in prefixes

            Example:
                >server prefix !

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                # FOR DEBUGGING
                # print(data)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            # FOR DEBUGGING
            # print(data)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            # FOR DEBUGGING
            # print("LANGUAGE:   " + str(language))

            permissions = raw.message.author.permissions_in(raw.message.channel)

            # FOR DEBUGGING
            # print("PERMISSIONS:   " + str(permissions))
            # print("IS ADMINISTRATOR:   " + str(permissions.administrator))

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "prefix"))
                return

            if db.updateDiscordServer(raw.message.server.id,{"general.prefix": str(prefix)}) == True:
                await self.bot.say("This **servers prefix** has been **updated** to __**" + str(prefix) + "**__ :blush:")
                return

            else:
                await self.bot.say("Sorry but I **wasn't able** to **update** this **servers prefix** :confused:")
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def languageS(self, raw, server_language="english"):
        """Change the bots language on this server.

                >server languageS (server_language)
            serverLanguage   -   Language   -   Default: english; Options: english, spanish

            Example:
                >server languageS spanish

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server language"))
                return

            server_language = str(server_language).lower()
            if server_language not in ["english", "spanish"]:
                await self.bot.say(languages.notLanguage(language, server_language))
                return

            if db.updateDiscordServer(raw.message.server.id, {"general.language": str(server_language)}) == True:
                await self.bot.say(languages.serverLanguageChangeLineOne(language, str(raw.message.server),server_language))
                return

            else:
                await self.bot.say(languages.serverLanguageChangeLineTwo(language, str(raw.message.server), server_language))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def vaingloryRegion(self, raw, region="na"):
        """Set the servers Vainglory region for vainglory_work commands.

                >server vaingloryRegion (region)
            region   -   Region   -   Default: na; Options: na, eu, sg or sea, ea, sa

            Example:
                >server vaingloryRegion eu

        """

        try:

            permissions = raw.message.author.permissions_in(raw.message.channel)

            # FOR DEBUGGING
            # print("PERMISSIONS:   " + str(permissions))
            # print("IS ADMINISTRATOR:   " + str(permissions.administrator))

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server language"))
                return

            region = vgc.giveRegion(region)

            if region == "sea":
                region = "sg"

            if db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.defaultRegion": str(region)}) == True:
                await self.bot.say(languages.serverRegionChangeLineOne(language, str(raw.message.server), region))
                return

            else:
                await self.bot.say(languages.serverRegionChangeLineTwo(language, str(raw.message.server), region))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def vaingloryGuild(self, raw, guild_tag="None", guild_name="Unknown"):
        """If this server represents a in-game guild associate them with this command.

                >server vaingloryGuild (guild_tag) (guild_name)
            guild_tag    -   Tag of Vainglory guild    -   Default: None
            guild_name   -   Name of Vainglory guild   -   Default: Unknown; Replace blank spaces with _ or surround name with ""

            Example 1:
                >server vaingloryGuild TKHG "Kings Home"
            Example 2:
                >server vaingloryGuild TKHG Kings_Home

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server vainglory_work guild"))
                return

            if vgc.giveCommunityTag(guild_tag) == False:
                await self.bot.say(languages.notVgGuildTag(language, guild_tag))
                return

            guild_name = str(guild_name).replace("_", " ")
            if vgc.checkCommunityName(guild_name) == False:
                await self.bot.say(languages.notVgGuildTag(language, guild_name))
                return

            if db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.guildName": str(guild_name)}) == True and db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.guildTag": str(guild_tag)}):
                await self.bot.say(languages.serverVgGuildChangeLineOne(language, str(raw.message.server), guild_name, guild_tag))
                return

            else:
                await self.bot.say(languages.serverVgGuildChangeLineTwo(language, str(raw.message.server), guild_name, guild_tag))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def vaingloryTeam(self, raw, team_tag="None", team_name="Unknown"):
        """If this server represents a in-game team associate them with this command.

                >server vaingloryTeam (team_name)
            team_tag    -   Tag of the Vainglory team    -   Default: None
            team_name   -   Name of the Vainglory team   -   Default: Unknown; Replace blank spaces with _ or surround name with ""

            Example 1:
                >server vaingloryTeam TTKK "Thy True Kings"
            Example 2:
                >server vaingloryTeam TTKK Thy_True_Kings

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server vainglory_work guild"))
                return

            if vgc.giveCommunityTag(team_tag) == False:
                await self.bot.say(languages.notVgTeamTag(language, team_tag))
                return

            team_name = str(team_name).replace("_", " ")
            if vgc.checkCommunityName(team_name) == False:
                await self.bot.say(languages.notVgTeamName(language, team_name))
                return

            if db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.teamName": str(team_name)}) == True and db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.teamTag": str(team_tag)}) == True:
                await self.bot.say(languages.serverVgTeamChangeLineOne(language, str(raw.message.server), team_name, team_tag))
                return

            else:
                await self.bot.say(languages.serverVgTeamChangeLineTwo(language, str(raw.message.server), team_name, team_tag))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def defaultGame(self, raw, game_name="Vainglory"):
        """What game do you use this bot for primarily.

                >server defaultGame (team_name)
            defaultGame   -   Name of Vainglory team   -   Default: Vainglory; Replace blank spaces with _ or surround name with ""

            Example 1:
                >server defaultGame Vainglory

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server default game"))
                return

            game_name = str(game_name).lower().replace("_", " ")
            if game_name not in ["vainglory_work"]:
                await self.bot.say(languages.notGame(language, game_name))
                return

            if db.updateDiscordServer(raw.message.server.id, {"tournamentRelated.defaultGame": str(game_name)}) == True:
                await self.bot.say(languages.serverGameChangeLineOne(language, str(raw.message.server), game_name))
                return

            else:
                await self.bot.say(languages.serverGameChangeLineTwo(language, str(raw.message.server), game_name))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")


    @server.command(pass_context=True)
    async def notifyServer(self, raw, setting=True):
        """If server should be notified when a developer notice is sent out. If a channel is specified on the server for the bot then notice will be sent there; else the notice will be sent to the servers general channel.

                >server notifyServer (send)
            send   -   Setting, True to send or False to not send   -   Default: True; Options: True or False

            Example:
                >server notifyServer False

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server default game"))
                return

            setting = str(setting).lower()
            if setting not in ["true", "false"]:
                await self.bot.say(languages.notBool(language, setting))
                return

            if setting == "true":
                setting = True

            else:
                setting = False

            # FOR DEBUGGING
            # print("SEND SETTING:   " + str(setting))

            if db.updateDiscordServer(raw.message.server.id, {"general.notify": setting}) == True:
                if setting == False:
                    await self.bot.say(languages.serverNotifyLineOne(language, str(raw.message.server)))
                    return

                else:
                    await self.bot.say(languages.serverNotifyLineTwo(language, str(raw.message.server)))
                    return

            else:
                await self.bot.say(languages.serverNotifyLineThree(language, str(raw.message.server)))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")


    @server.command(pass_context=True)
    async def notifyOwner(self, raw, setting=True):
        """If you should be notified when a developer notice is sent out.

                >server notifyOwner (send)
            send   -   Setting, True to send or False to not send   -   Default: False; Options: True or False

            Example:
                >server notifyOwner True

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            # FOR DEBUGGING
            # print("MESSAGE AUTHOR:   " + str(raw.message.author) + "\nSERVER OWNER:   " + str(raw.message.server.owner))

            if raw.message.author != raw.message.server.owner:
                await self.bot.send_message(raw.message.author, languages.notServerOwner(language, str(raw.message.server)))
                return

            setting = str(setting).lower()
            if setting not in ["true", "false"]:
                await self.bot.say(languages.notBool(language, str(setting)))
                return

            if setting == "true":
                setting = True

            else:
                setting = False

            if db.updateDiscordServer(raw.message.server.id, {"general.notifyOwner": setting}) == True:
                if setting == False:
                    await self.bot.say(languages.serverNotifyOwnerLineOne(language, str(raw.message.server.owner), str(raw.message.server)))
                    return

                else:
                    await self.bot.say(languages.serverNotifyOwnerLineTwo(language, str(raw.message.server.owner), str(raw.message.server)))
                    return

            else:
                await self.bot.say(languages.serverNotifyOwnerLineThree(language, str(raw.message.server.owner), str(raw.message.server)))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")


    @server.command(pass_context=True)
    async def setChannel(self, raw, specific_channel=True):
        """Set the current channel as ComputerBot's channel to communicate with the server.

                >server setChannel (specific_channel)
            specific_channel   -   Setting, True to send all bot msgs to current channel or False to not send to a specific channel   -   Default: True; Options: True or False

            Example:
                >server setChannel True

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server default game"))
                return

            setting = str(specific_channel).lower()
            if setting not in ["true", "false"]:
                await self.bot.say(languages.notBool(language, str(setting)))
                return

            if setting == "true":
                setting = raw.message.channel.id

            else:
                setting = False

            if db.updateDiscordServer(raw.message.server.id, {"general.botChannel": setting}) == True:
                if setting != False:
                    await self.bot.say(languages.serverChannelLineOne(language, str(raw.message.channel), str(raw.message.server)))
                    return

                else:
                    await self.bot.say(languages.serverChannelLineTwo(language, str(raw.message.server)))
                    return


            else:
                await self.bot.say(languages.serverChannelLineThree(language, str(raw.message.server)))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")


    @server.command(pass_context=True)
    async def banCommand(self, raw, command_name, mode="disable"):
        """Ban specific or a group of commands from being used in the server.

                >server banCommand (command_name)
            command_name   -   Name of the command to ban   -   List of individual/group commands that can be banned: vaingloryGroup
            set            -   Enable or disable            -   Default: Disable, Options: Enable, Disable

            Example:
                >server banCommand vaingloryStats disable

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server default game"))
                return

            command_name = str(command_name).lower()
            if command_name not in config.commands:
                await self.bot.say(languages.notCommand(language, command_name))
                return

            mode = str(mode).lower()
            if mode not in ["disable", "enable"]:
                await self.bot.say(languages.notMode(language, command_name, mode))
                return

            # FOR DEBUGGING
            # print("COMMAND NAME:   " + str(command_name) + "\nSET:   " + str(set))

            if mode == "disable":
                if db.updateDiscordServerArray(raw.message.server.id, {"general.commandBans": str(command_name)}, "add") == True:
                    await self.bot.say(languages.serverCommandBanLineOne(language, command_name, str(raw.message.server)))
                    return

                else:
                    await self.bot.say(languages.serverCommandBanLineTwo(language, command_name, str(raw.message.server)))
                    return

            else:
                if db.updateDiscordServerArray(raw.message.server.id, {"general.commandBans": str(command_name)}, "remove") == True:
                    await self.bot.say(languages.serverCommandBanLineFour(language, command_name, str(raw.message.server)))
                    return

                else:
                    await self.bot.say(languages.serverCommandBanLineFour(language, command_name, str(raw.message.server)))
                    return


        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def compressS(self, raw, mode="disable"):
        """If this server's VainGlory related embeds should be compressed to be smaller.

                >server compressS (mode)
            mode   -   Whether to enable or disable

            Example 1:
                >server compressS disable

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "vainglory compress"))
                return

            mode = str(mode).lower()
            if mode not in ["disable", "enable"]:
                await self.bot.say(languages.notMode(language, "vaingloryCompress", mode))
                return

            if mode == "disable":
                mode = False

            else:
                mode = True

            if db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.compact": mode}) == True:
                await self.bot.say(languages.compressVainGloryLineOne(language, str(raw.message.server)))
                return

            else:
                await self.bot.say(languages.compressVainGloryLineTwo(language, str(raw.message.server)))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def emojisS(self, raw, mode="disable"):
        """If VainGlory related embeds should be sent with emojis.

                >server emojisS (mode)
            mode   -   Whether to enable or disable

            Example 1:
                >server emojisS disable

        """

        try:

            if raw.message.channel.is_private == True:
                data = db.discordUserDictionary(raw.message.author.id)

                if data == None or data == False:
                    language = "english"

                else:
                    language = data["general"]["language"]

                await self.bot.say(languages.notInServer(language))
                return

            data = db.discordServerDictionary(raw.message.server.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            permissions = raw.message.author.permissions_in(raw.message.channel)

            if permissions.administrator == False:
                await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "vainglory compress"))
                return

            mode = str(mode).lower()
            if mode not in ["disable", "enable"]:
                await self.bot.say(languages.notMode(language, "emojisS", mode))
                return

            if mode == "disable":
                mode = False

            else:
                mode = True

            if db.updateDiscordServer(raw.message.server.id, {"vaingloryRelated.emojis": mode}) == True:
                await self.bot.say(languages.emojisVainGloryLineOne(language, str(raw.message.server)))
                return

            else:
                await self.bot.say(languages.emojisVainGloryLineTwo(language, str(raw.message.server)))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def customC(self, raw, command_name="", msg="", embed="true", send_to="here"):
        """Create or edit a custom command.

                >server customC (command_name) (msg) (embed)
            command_name   -   Command name to trigger the response.
            msg            -   Response to this custom command; surround by "; /user/ represents the user name/nick name; /server/ represents the server name.   -   enter as $remove to remove custom command
            embed          -   If the response of this command will be in a embed fashion.   -   Default: true; Options: true, false
            send_to        -   Where to send this message to   -   Default: here; Options: here, sent to this servers channels or pm, sent to members pm

            Example 1:
                >server customC hello "Hello /user/, to /server/ hope you like it here!"

            Example 2:
                >server customC hello "Hello /user/, to /server/ hope you like it here!" false pm

        """

        try:

            info = dict(await self.getInfo(raw.message, ["language", "mention", "needAdmin", "needPublic", "serverData"]))

            if "error-private" in info:
                await self.bot.send_message(info["destination"], languages.notInServer(info["language"]))
                return

            elif "error-admin" in info:
                await self.bot.send_message(info["destination"], languages.notAuthorized(info["language"], str(raw.message.server), ""))
                return

            command_name = str(command_name)
            if command_name == "":
                await self.bot.say("You must enter a valid **command name**... :sweat_smile:")
                return

            elif command_name in config.commands:
                await self.bot.say("**" + command_name + " can't be used** as a **custom command**... :sweat_smile:")
                return

            elif checks.checkCustomCommandName(command_name) == False:
                await self.bot.say("**" + command_name + " isn't a valid name** for a **custom command**... :sweat_smile:")
                return

            msg = str(msg)
            if msg == "":
                await self.bot.say("You need to give a **msg**... :sweat_smile:")

            elif checks.checkResponse(msg) == False:
                await self.bot.say("What you've entered as **msg** isn't valid... :sweat_smile:")

            elif msg == "$remove":
                if db.updateDiscordServer(raw.message.server.id, {"general.customCommands." + command_name: 1}, mode="$unset") == True:
                    await self.bot.say("**" + command_name + " custom command** has been successfully **removed**... :hugging:")

                else:
                    await self.bot.say("**" + command_name + "** custom command **wasn't removed**... :confused:")

                return

            embed = str(embed).lower()
            values = {"true": True, "false": False}
            if embed not in values:
                await self.bot.say("**" + str(embed) + " isn't valid** embed option... :sweat_smile:")
                return

            else:
                embed = values[embed]

            send_to = str(send_to).lower()
            values = ["here", "pm"]
            if send_to not in values:
                await self.bot.say("**" + send_to + "** isn't a valid **send to**... :sweat_smile:")
                return

            # No server data was found
            if info["serverData"] in [False, None]:
                if db.updateDiscordServer(raw.message.server.id, {"general.customCommands." + command_name: {"embed": embed, "reason": command_name, "destination": send_to, "msg": msg}}) == True:
                    await self.bot.say("**" + command_name + " custom command** has been **created**! :hugging:")

                else:
                    await self.bot.say("**" + command_name + " custom command** couldn't be **created**... :confused:")

                return

            # Server data found and this command doesn't already exist
            if str(command_name) not in info["serverData"]["general"]["customCommands"]:
                if db.updateDiscordServer(raw.message.server.id, {"general.customCommands." + command_name: {"embed": embed, "reason": command_name, "destination": send_to, "msg": msg}}) == True:
                    await self.bot.say("**" + command_name + " custom command** has been **created**! :hugging:")

                    # Show them a preview
                    await self.bot.say("This is what the custom command will look like...", embed=core.generateAnnouncement({"embed": True, "reason": command_name, "from": str(raw.message.server), "to": str(raw.message.author), "msg": msg}))

                else:
                    await self.bot.say("**" + command_name + " custom command** couldn't be **created**... :confused:")

                return

            # Server data found and this command already exist
            else:
                if db.updateDiscordServer(raw.message.server.id, {"general.customCommands." + command_name: {"embed": embed, "msg": msg}}) == True:
                    await self.bot.say("**" + command_name + " custom command** has been **updated**! :hugging:")
                    return

                else:
                    await self.bot.say("**" + command_name + " custom command** couldn't be **updated**... :confused:")
                    return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def joinM(self, raw, msg="", embed="true", send_to="here"):
        """Setup a msg that will be sent every time someone joins the server to the current channel!

                >server (msg) (embed) (sent_to)
            msg       -   Msg to be sent; surround by "; /user/ represents the user name/nick name; /uesr/ represents the server name.   -   enter as $remove to remove join message
            embed     -   If the response of this command will be in a embed fashion.   -   Default: true; Options: true, false
            send_to   -   Where to send this message to   -   Default: here; Options: here, sent to this channel, or pm, sent to new members pm

            Example 1:
                >server Welcome, /user/, to our server /server/ hope you have a blast!

            Example 2:
                >server Welcome, /user/, to our server /server/ hope you have a blast! false pm

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "needAdmin", "needPublic", "serverData"])

            if "error-private" in info:
                await self.bot.send_message(info["destination"], languages.notInServer(info["language"]))
                return

            elif "error-admin" in info:
                await self.bot.send_message(info["destination"], languages.notAuthorized(info["language"], str(raw.message.server), ""))
                return

            msg = str(msg)
            if msg == "":
                await self.bot.say("You need to give a **msg**... :sweat_smile:")

            elif checks.checkResponse(msg) == False:
                await self.bot.say("What you've entered as **msg** isn't valid... :sweat_smile:")

            elif msg == "$remove":
                if db.updateDiscordServer(raw.message.server.id, {"general.memberJoin.announce": 1}, mode="$unset") == True:
                    await self.bot.say("**Welcome message** for new member has been successfully **removed**... :hugging:")

                else:
                    await self.bot.say("**Welcome message** for new member **wasn't removed**... :confused:")

                return

            embed = str(embed).lower()
            values = {"true": True, "false": False}
            if embed not in values:
                await self.bot.say("**" + str(embed) + " isn't valid** embed option... :sweat_smile:")
                return

            else:
                embed = values[embed]

            send_to = str(send_to).lower()
            values = {"here": str(raw.message.channel.id), "pm": "pm"}
            if send_to not in values:
                await self.bot.say("**" + send_to + "** isn't a valid **send to**... :sweat_smile:")
                return

            else:
                send_to = values[send_to]

            if db.updateDiscordServer(raw.message.server.id, {"general.memberJoin.announce": {"embed": embed, "destination": send_to, "msg": msg, "reason": "Member Joined"}}) == True:
                await self.bot.say("**Welcome msg** for new members **has been setup on** __**this channel**__! :hugging:")

                # Show them a preview
                await self.bot.say("This is what the welcome msg will look like...", embed=core.generateAnnouncement({"embed": True, "reason": "memberJoin", "from": str(raw.message.server), "to": str(raw.message.author), "msg": msg}))

                return

            else:
                await self.bot.say("**Welcome msg** for new members **wasn't set up**... :confused:")
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def joinR(self, raw, role):
        """Setup the bot to give a role upon a new member joining the server.

                >server (role)
            role   -   tag of the role to give to new members

            Example:
                >server @new-guy

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "needAdmin", "needPublic", "serverData"])

            if "error-private" in info:
                await self.bot.send_message(info["destination"], languages.notInServer(info["language"]))
                return

            elif "error-admin" in info:
                await self.bot.send_message(info["destination"], languages.notAuthorized(info["language"], str(raw.message.server), ""))
                return

            elif str(role).lower() == "$remove":
                if db.updateDiscordServer(raw.message.server.id, {"general.memberJoin.giveRole": 1}, mode="$unset") == True:
                    await self.bot.say("**Welcome role** for new member has been successfully **removed**... :hugging:")

                else:
                    await self.bot.say("**Welcome role** for new member **wasn't removed**... :confused:")

                return

            if raw.message.role_mentions == []:
                await self.bot.say("You need to **tag a role**... :sweat_smile:")
                return

            else:
                role = raw.message.role_mentions[0]

            if db.updateDiscordServer(raw.message.server.id, {"general.memberJoin.giveRole": {"role": role.id}}) == True:
                await self.bot.say("**Role, " + str(role) + ",** for new members has been **setup**! :hugging:")

                return

            else:
                await self.bot.say("**Welcome role, " + str(role) + ",** for new members **wasn't set up**... :confused:")
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @server.command(pass_context=True)
    async def leaveM(self, raw, msg="", embed="true", send_to="here"):
        """Setup a msg that will be sent every time someone leaves the server to the current channel!

                >server (msg) (embed) (sent_to)
            msg       -   Msg to be sent; surround by "; /user/ represents the user name/nick name; /server/ represents the server name.   -   enter as $remove to remove leave message
            embed     -   If the response of this command will be in a embed fashion.   -   Default: true; Options: true, false
            send_to   -   Where to send this message to   -   Default: here; Options: here, sent to this channel, or pm, sent to new members pm

            Example 1:
                >server We're sorry to see you leave, /user/, our server /server/ hope you had a blast!

            Example 2:
                >server We're sorry to see you leave, /user/, our server /server/ hope you had a blast! false pm

        """

        try:

            info = await self.getInfo(raw.message, ["language", "mention", "destination", "needAdmin", "needPublic", "serverData"])

            if "error-private" in info:
                await self.bot.send_message(info["destination"], languages.notInServer(info["language"]))
                return

            elif "error-admin" in info:
                await self.bot.send_message(info["destination"], languages.notAuthorized(info["language"], str(raw.message.server), ""))
                return

            msg = str(msg)
            if msg == "":
                await self.bot.say("You need to give a **msg**... :sweat_smile:")

            elif checks.checkResponse(msg) == False:
                await self.bot.say("What you've entered as **msg** isn't valid... :sweat_smile:")

            elif msg == "$remove":
                if db.updateDiscordServer(raw.message.server.id, {"general.memberLeave.announce": 1}, mode="$unset") == True:
                    await self.bot.say("**Leaving message** for leaving member has been successfully **removed**... :hugging:")

                else:
                    await self.bot.say("**Leaving message** for leaving member **wasn't removed**... :confused:")

                return

            embed = str(embed).lower()
            values = {"true": True, "false": False}
            if embed not in values:
                await self.bot.say("**" + str(embed) + " isn't valid** embed option... :sweat_smile:")
                return

            else:
                embed = values[embed]

            send_to = str(send_to).lower()
            values = {"here": str(raw.message.channel.id), "pm": "pm"}
            if send_to not in values:
                await self.bot.say("**" + send_to + "** isn't a valid **send to**... :sweat_smile:")
                return

            else:
                send_to = values[send_to]

            if db.updateDiscordServer(raw.message.server.id, {"general.memberLeave.announce": {"embed": embed, "destination": send_to, "msg": msg, "reason": "Meamber Left"}}) == True:
                await self.bot.say("**Leaving msg** for leaving members **has been setup on** __**this channel**__! :hugging:")

                # Show them a preview
                await self.bot.say("This is what the leaving msg will look like...", embed=core.generateAnnouncement({"embed": True, "reason": "memberLeave", "from": str(raw.message.server), "to": str(raw.message.author), "msg": msg}))

                return

            else:
                await self.bot.say("**Leaving msg** for leaving members **wasn't set up**... :confused:")
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    # @server.command(pass_context=True)
    # async def (self, raw):
    #     """
    #
    #             >server
    #
    #         Example:
    #             >server
    #
    #     """
    #
    #     try:
    #
    #         info = await self.getInfo(raw.message, ["language", "mention", "destination", "needAdmin", "needPublic", "serverData"])
    #
    #         if "error-private" in info:
    #             await self.bot.send_message(info["destination"], languages.notInServer(info["language"]))
    #             return
    #
    #         elif "error-admin" in info:
    #             await self.bot.send_message(info["destination"], languages.notAuthorized(info["language"], str(raw.message.server), ""))
    #             return
    #
    #     except:
    #         await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
    #
    #         try:
    #
    #             await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")
    #
    #         except Exception as e:
    #             await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
    #             return
    #
    #         await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

# # USER COMMANDS   <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    @commands.group(pass_context=True)
    async def user(self, raw):
        """Commands used by a user to configure bots usage. You'll need to be the owner of current server."""
        pass

#     @user.command(pass_context=True)
#     async def nothing(self, raw):
#         """"""
#
#         # TODO 1- 2- 3- 4-
#
#         pass

    @commands.command(pass_context=True)
    async def userInfo(self, raw, user_mention=""):
        """Info on discord user relevant to the ComputerBot.

                >userInfo(user_mention)
            user_mention   -   When looking at another players

            Example 1:
                $userInfo

            Example 2:
                $userInfo @ClarkthyLord #7042

        """

        try:

            if raw.message.channel.is_private == True:
                try:
                    data = db.discordUserDictionary(raw.message.author.id)

                    # FOR DEBUGGING
                    # print("USER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.author
                    else:
                        language = data["general"]["language"]
                        destination = raw.message.author
                except:
                    language = "english"
                    destination = raw.message.author
            else:
                try:
                    data = db.discordServerDictionary(raw.message.server.id)

                    # FOR DEBUGGING
                    # print("SERVER DATA:   " + str(data))

                    if data == False or data == None:
                        language = "english"
                        destination = raw.message.channel

                    elif "userInfo" in data["general"]["commandBans"]:
                        try:
                            data = db.discordUserDictionary(raw.message.author.id)

                            # FOR DEBUGGING
                            # print("USER DATA:   " + str(data))

                            if data == False or data == None:
                                language = "english"
                                destination = raw.message.author

                            else:
                                language = data["general"]["language"]
                                destination = raw.message.author

                        except:
                            language = "english"
                            destination = raw.message.author

                    else:
                        try:
                            language = data["general"]["language"]
                            if language == False or language == None:
                                language = "english"
                        except:
                            language = "english"

                        try:
                            destination = data["general"]["botChannel"]
                            if destination == False or destination == None:
                                destination = raw.message.channel

                            else:
                                destination = self.bot.get_channel(destination)
                                if destination == None or destination == False:
                                    destination = raw.message.channel
                        except:
                            destination = raw.message.channel

                except:
                    language = "english"
                    destination = raw.message.author

            # FOR DEBUGGING
            # print("LANGUAGE:   " + language)
            # print("DESTINATION:   " + str(destination))

            if user_mention != "":

                try:

                    user_name = str(raw.message.mentions[0])
                    user = raw.message.mentions[0]

                    # FOR DEBUGGING
                    # print("USER:   " + str(user))
                    # print("USER ID:   " + str(user.id))

                except:

                    # FOR DEBUGGING
                    # print("!!!NOPE!!!")

                    user_name = str(raw.message.author)
                    user = raw.message.author

            else:
                user_name = str(raw.message.author)
                user = raw.message.author

            user = db.discordUserDictionary(user.id)

            if user == False or user == None:
                await self.bot.send_message(destination, languages.userInfoLineOne(language, user_name))
                return

            # FOR DEBUGGING
            # print("USER DATA:   " + str(user))

            try:

                emojis = user["vaingloryRelated"]["emojis"]

            except:
                emojis = True

            embed = discord.Embed(title=languages.userInfoTitle(language), colour=discord.Colour(0x354b), url=config.bot_server, description=languages.userInfoDescription(language, str(user_name)))

            embed.set_author(name=config.bot_name, url=config.bot_invite, icon_url=config.bot_icon)

            embed.set_footer(text=config.bot_embed_footer, icon_url=config.bot_icon)

            embed.add_field(name=languages.userInfoFielOneTitle(language), value=languages.userInfoFieldOne(language))

            embed.add_field(name=languages.userInfoFieldTwoTitle(language), value=languages.userInfoFieldTwo(language, str(user["vaingloryRelated"]["quickName"]), str(user["vaingloryRelated"]["quickRegion"]), str(user["vaingloryRelated"]["verifiedName"]), str(user["vaingloryRelated"]["verifiedRegion"]), str(user["vaingloryRelated"]["compact"]), str(emojis)))

            embed.add_field(name=languages.userInfoFieldThreeTitle(language), value=languages.userInfoFieldThree(language))

            # Send message to the correct channel
            await self.bot.send_message(destination, embed=embed)

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @user.command(pass_context=True)
    async def languageU(self, raw, user_language="english"):
        """Change the bots language in private messages.

                >user languageU (user_language)
            userLanguage   -   Language   -   Default: english; Options: english, spanish

            Example:
                >user languageU spanish

        """

        try:

            data = db.discordUserDictionary(raw.message.author.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            user_language = str(user_language).lower()
            if user_language not in ["english", "spanish"]:
                await self.bot.send_message(raw.message.author, languages.notLanguage(language, user_language))
                return

            if db.updateDiscordUser(raw.message.author.id, {"general.language": str(language)}) == True:
                await self.bot.send_message(raw.message.author, languages.userLanguageLineOne(language, user_language))
                return

            else:
                await self.bot.send_message(raw.message.author, languages.userLanguageLineTwo(language, user_language))
                return

        except Exception as e:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")
            
            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @user.command(pass_context=True)
    async def compressU(self, raw, mode="disable"):
        """If VainGlory related embeds should be compressed to be smaller.

                >user compressU (mode)
            mode   -   Whether to enable or disable

            Example 1:
                >user compressU disable

        """

        try:

            data = db.discordUserDictionary(raw.message.author.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            mode = str(mode).lower()
            if mode not in ["disable", "enable"]:
                await self.bot.send_message(raw.message.author, languages.notMode(language, "vaingloryCompress", mode))
                return

            if mode == "disable":
                mode = False

            else:
                mode = True

            if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.compact": mode}) == True:
                await self.bot.send_message(raw.message.author, languages.compressVainGloryLineOne(language, str(raw.message.author)))
                return

            else:
                await self.bot.send_message(raw.message.author, languages.compressVainGloryLineTwo(language, str(raw.message.author)))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

    @user.command(pass_context=True)
    async def emojisU(self, raw, mode="disable"):
        """If VainGlory related embeds should be sent with emojis..

                >user emojisU (mode)
            mode   -   Whether to enable or disable

            Example 1:
                >user emojisU disable

        """

        try:

            data = db.discordUserDictionary(raw.message.author.id)

            if data == None or data == False:
                language = "english"

            else:
                language = data["general"]["language"]

            mode = str(mode).lower()
            if mode not in ["disable", "enable"]:
                await self.bot.send_message(raw.message.author, languages.notMode(language, "emojisU", mode))
                return

            if mode == "disable":
                mode = False

            else:
                mode = True

            if db.updateDiscordUser(raw.message.author.id, {"vaingloryRelated.emojis": mode}) == True:
                await self.bot.send_message(raw.message.author, languages.emojisVainGloryLineOne(language, str(raw.message.author)))
                return

            else:
                await self.bot.send_message(raw.message.author, languages.emojisVainGloryLineTwo(language, str(raw.message.author)))
                return

        except:
            await self.bot.say("Sorry an **error** has **occurred**... :sweat_smile:")

            try:

                await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(raw.message.author) + "```" + str(format_exc()) + "```")

            except Exception as e:
                await self.bot.say("A **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + str(e) + "```")
                return

            await self.bot.say("A **report** has been successfully sent to the developers! :hugging:")

# DEVELOPER COMMANDS   <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    @commands.group(pass_context=True, hidden=True)
    async def dev(self, raw):
        """Commands used by developers. You'll need to be in owners to use these commands."""
        pass

    @dev.command(pass_context=True)
    async def notice(self, raw, *, message=""):
        """Sends a notice to all the servers and owners the bot is on."""

        if raw.message.author.id not in config.owners:
            await self.bot.say("**You aren't a developer** so you **can't use** this **command** :stuck_out_tongue:")
            return

        if message == "":
            await self.bot.say("**That msg is empty!**")
            return

        # results = ""
        owners = []
        results = []
        for server in self.bot.servers:
            try:

                serverData = db.discordServerDictionary(server.id)

                # FOR DEBUGGING
                # print("SERVER DATA FOR " + str(server).upper() + ":   " + str(serverData))

                result = ""
                if serverData == None or serverData == False:
                    try:

                        await self.bot.send_message(server, message)
                        result = "TRUE = " + str(server) + "  <->  FALSE = " + str(server.owner)

                    except:
                        result = "FALSE = " + str(server) + "  <->  FALSE = " + str(server.owner)

                else:
                    try:

                        if serverData["general"]["notify"] == True:
                            destination = self.bot.get_channel(serverData["general"]["botChannel"])
                            await self.bot.send_message(destination, message)
                            result += "TRUE = " + str(server)

                        else:
                            result += "FALSE = " + str(server)
                    except:

                        try:

                            await self.bot.send_message(server, message)
                            result += "TRUE = " + str(server)

                        except:

                            result += "FALSE = " + str(server)
                    try:

                        if serverData["general"]["notifyOwner"] == True:
                            if server.owner not in owners:
                                await self.bot.send_message(server.owner, message)
                                owners.append(str(server.owner))
                                result += "  <->  TRUE = " + str(server.owner)
                            else:
                                result += "  <->  DONE = " + str(server.owner)
                        else:
                            result += "  <->  FALSE = " + str(server.owner)

                    except:

                        result += "  <->  FALSE = " + str(server.owner)
            except:

                result = "FALSE = " + str(server) + "  <->  FALSE = " + str(server.owner)

            # FOR DEBUGGING
            # print(result)

            results.append(result)

        # FOR DEBUGGING
        # print("RESULTS:\n" + str(results))

        # with open("result", "w") as handler:
        #     handler.write(results)

        # print("\n\n!!!DONE SENDING NOTICES!!!")

        await self.bot.say("**Notice** sent to all possible server! :hugging:")

        try:

            with open("result.json", "w") as handler:
                json.dump(results, handler)

            await self.bot.send_file(raw.message.channel, "result.json")

        except Exception as e:
            await self.bot.say("Couldn't send **result**... :sweat_smile:```" + str(e) + "```")

    @dev.command(pass_context=True)
    async def listEmojis(self, raw):
        """List all the info on custom emojis in the current server."""

        if raw.message.author.id not in config.owners:
            await self.bot.say("**You aren't a developer** so you **can't use** this **command** :stuck_out_tongue:")
            return

        try:

            emojis = raw.message.server.emojis

        except Exception as e:
            await self.bot.say("Something went wrong... :sweat_smile:```" + str(e) + "```")
            return

        for emoji in emojis:
            await self.bot.say(str(emoji) + " **|** ``<:" + str(emoji.name) + ":" + str(emoji.id) + ">``")

    @dev.command(pass_context=True)
    async def listPerm(self, raw, permission=""):
        """List all the permissions the bot has on this server.

                >dev listPerm (permission)

            permission - Check if this permission is true

        """

        if raw.message.author.id not in config.owners:
            await self.bot.say("**You aren't a developer** so you **can't use** this **command** :stuck_out_tongue:")
            return

        ans = raw.message.server.get_member(self.bot.user.id)

        await self.bot.say("**USER:** " + str(ans) + " **|NICK NAME:** " + str(ans.nick) + "\n**SERVER:** " + str(ans.server) + " **|JOINED:** " + str(ans.joined_at))

        # FOR DEBUGGING
        # print("ROLES: " + str(ans.roles))

        msg = "__**ROLES:**__\n"
        for role in ans.roles:
            msg += str(role) + "\n"

        await self.bot.say(msg)

        # FOR DEBUGGING
        # print("PERMISSIONS: " + str(ans.server_permissions))

        msg = "__**PERMISSIONS:**__\n"
        for permission in ans.server_permissions:
            msg += str(permission) + "\n"

        await self.bot.say(msg)

        # permissions = raw.message.author.permissions_in(raw.message.channel)
        #
        # if permissions.administrator == False:
        #     await self.bot.say(languages.notAuthorized(language, str(raw.message.server), "server default game"))
        #     return

        if permission != "":
            if permission in ans.server_permissions:
                if ans.server_permissions[permission] == True:
                    await self.bot.say("TRUE")

                else:
                    await self.bot.say("FALSE")

    @dev.command(pass_context=True)
    async def userNum(self, raw):
        """Number of users the bot is serving."""

        if raw.message.author.id not in config.owners:
            await self.bot.say("**You aren't a developer** so you **can't use** this **command** :stuck_out_tongue:")
            return

        msg = await self.bot.say("Counting users this might take a while... :eyes:")

        user_list = []
        for member in self.bot.get_all_members():
            if str(member) in user_list:  # This user has all ready been counted
                continue

            user_list.append(str(member))

            # FOR DEBUGGING
            # print(member)

        # FOR DEBUGGING
        # print("USER SIZE: " + str(len(member_list)) + "\nUSER LIST: " + str(member_list))

        await self.bot.edit_message(msg, "Number Of Users: " + str(len(user_list)))

# ADS COMMANDS   <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    @commands.group(pass_context=True, hidden=True)
    async def ads(self, raw):
        """Commands used by developers for ads. You'll need to be in owners to use these commands."""
        pass

    @ads.command(pass_context=True)
    async def addEA(self, raw, ad_id, views, time, title, description, url, image):
        """Add an embed add to the system.

                >ads addEA (ad_id) (time) (title) (description) (url) (image)
            ad_id         -   ID of ad
            views         -   The amount of time this add must be sent before being removed
            time          -   The break time server will get from ads after receiving this add   -   In minutes
            title         -   The title of the embed
            description   -   The embeds description
            url           -   Url to ads page
            image         -   Url of image used in ad

            Example:
                >ads addEA Computer 3000 30 "Computer Organization" "Join the Computer organization!" http://discord.me/ComputerBot http://i64.tinypic.com/2q24gsj.jpg

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        ad_id = str(ad_id)
        views = ads.giveViewsAds(views)
        time = ads.giveTimeAds(time)
        if time == False:
            time = 30

        title = str(title)
        description = str(description)
        url = str(url)
        image = str(image)

        if ads.checkIfAds("embed", ad_id) == True:
            await self.bot.say("**" + str(ad_id) + "** is already an **embed ad**... :sweat_smile:")
            return

        if ads.addEmbedAds(ad_id, views, time, title, description, url, image) == True:
            await self.bot.say("**" + str(ad_id) + "** has been **added** to the **embed ads**... :eyes:")

            embed = ads.makeEmbedAds(ad_id)
            await self.bot.send_message(raw.message.channel, content="This is what **" + str(ad_id) + "** looks like... :eyes:", embed=embed)
            return

        else:
            await self.bot.say("Sorry I wan't able to **add " + str(ad_id) + "** to **embed ads**... :pensive:")
            return

    @ads.command(pass_context=True)
    async def removeEA(self, raw, ad_id):
        """Remove an embed add from the system.

                >ads removeEA (ad_id)
            ad_id   -   ID of ad

            Example:
                >ads removeEA Computer

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if ads.checkIfAds("embed", ad_id) == True:
            if ads.removeAds("embed", ad_id) == True:
                await self.bot.say("**" + str(ad_id) + "** has been **removed** from **embed ads**... :eyes:")
                return

            else:
                await self.bot.say("Sorry I wasn't able to **remove " + str(ad_id) + "** from **embed ads**... :pensive:")
                return

        else:
            await self.bot.say("**" + str(ad_id) + "** ins't an **embed ad**... :sweat_smile:")
            return

    @ads.command(pass_context=True)
    async def addTA(self, raw, ad_id, views, text):
        """Add a text add to the system.

                >ads addTA (ad_id) (time) (title) (description) (url) (image)
            ad_id   -   ID of ad
            views   -   The amount of time this add must be sent before being removed
            text    -   The ads content

            Example:
                >ads addTA Computer 3000 Thank you for choosing ComputerBot :3

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        ad_id = str(ad_id)
        views = ads.giveViewsAds(views)
        text = str(text)

        if ads.checkIfAds("text", ad_id) == True:
            await self.bot.say("**" + str(ad_id) + "** is already an **text ad**... :sweat_smile:")
            return

        if ads.addTextAds(ad_id, views, text) == True:
            await self.bot.say("**" + str(ad_id) + "** has been **added** to the **text ads**... :eyes:")

            await self.bot.send_message(raw.message.channel, content="This is what **" + str(ad_id) + "** looks like... :eyes:\n" + str(config.ads_text[ad_id]))
            return

        else:
            await self.bot.say("Sorry I wan't able to **add " + str(ad_id) + "** to **text ads**... :pensive:")
            return

    @ads.command(pass_context=True)
    async def removeTA(self, raw, ad_id):
        """Remove a text ad from the system.

                >ads removeTA (ad_id)
            ad_id   -   ID of ad

            Example:
                >ads removeTA Computer

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if ads.checkIfAds("text", ad_id) == True:
            if ads.removeAds("text", ad_id) == True:
                await self.bot.say("**" + str(ad_id) + "** has been **removed** from **text ads**... :eyes:")
                return

            else:
                await self.bot.say("Sorry I wasn't able to **remove " + str(ad_id) + "** from **text ads**... :pensive:")
                return

        else:
            await self.bot.say("**" + str(ad_id) + "** ins't a **ad** from **text ads**... :sweat_smile:")
            return

    @ads.command(pass_context=True)
    async def listA(self, raw, extension_command):
        """List of all ads data.

                >ads listA (extension _commands)
            extension_command   -   What you would like to list   -   embed_ads, text_ads, queue, excluded

            Example:
                >ads listA

        """

        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if extension_command == "embed_ads":

            msg = "**Embed Ads:**\n"
            for ad in config.ads_embed.keys():
                msg += "**Name:**   *" + str(ad) + "* **|Views Left:**   *" + str(config.ads_embed[ad]["views"]) + "* **|Ad Break Given:** *" + str(config.ads_embed[ad]["time"]) + "*\n"

            await self.bot.say(msg)

        elif extension_command == "text_ads":

            msg = "**Text Ads:**\n"
            for ad in config.ads_text.keys():
                msg += "**Name:**   *" + str(ad) + "* **|Views Left**   *" + str(config.ads_text[ad]["views"]) + "*\n"

                await self.bot.say(msg)

        elif extension_command == "queue":

            msg = "**Server Ad Break Queue:**\n"
            for server in config.ads_queue.keys():
                msg += "**Server ID:**   *" + str(server) + "* **|Break:**    *" + str(config.ads_queue[server]["expires"]) + "*\n"

            await self.bot.say(msg)

        elif extension_command == "excluded":

            msg = "**Servers Excluded From Ads:**\n"
            for server in config.ads_queue.keys():
                msg += "**Server ID:**   *" + str(server) + "* **|Excluded For:**    *" + str(config.ads_queue[server]["expires"]) + "*\n"

            await self.bot.say(msg)

        else:
            await self.bot.say("Sorry didn't catch that... :sweat_smile:")

    @ads.command(pass_context=True)
    async def testA(self, raw, ad_id):
        """Test a add.

                >ads testA (ad_id)
            ad_id   -   Id of ad

            Example:
                >ads testA Computer

        """

        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if ads.checkIfAds("embed", ad_id) == True:
            embed = ads.makeEmbedAds(ad_id)

            await self.bot.send_message(raw.message.channel, embed=embed)

        else:
            await self.bot.say("**" + str(ad_id) + "** ins't an **ad**... :sweat_smile:")
            return

    @ads.command(pass_context=True)
    async def excludeSA(self, raw, server_id, time="False"):
        """Exclude a server, by their id, from the ad system.

            >ads excludeSA (server_id) (time)
            ad_server   -   Id of server
            time    -    Time to exclude server from ads for in days   -   False if exclude forever

            Example:
                >ads excludeSA 31231973 440

        """

        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if time == "False":
            time = False

        elif time in ["True", True]:
            time = 30

        time = ads.giveTimeAds(time)

        # FOR DEBUGGING
        # print("TIME:   " + str(time))

        if ads.checkServerExcludeAds(server_id) == True:
            await self.bot.say("This server is already **excluded**... :sweat_smile:")
            return

        if ads.excludeServerAds(server_id, time) == True:
            msg = "**" + str(server_id) + "** has be **excluded** from **ads** for"

            if time != False:
                msg += " the next **" + str(time) + " days**"

            else:
                msg += " **forever**"

            msg += "... :eyes:"

            await self.bot.say(msg)
            return

        else:
            await self.bot.say("Sorry I wasn't able to **exclude " + str(server_id) + "**... :pensive:")
            return

    @ads.command(pass_context=True)
    async def includeSA(self, raw, server_id):
        """Include a server that was excluded, by their id, from the ad system.

            >ads includeSA (server_id)
            server_id   -   Id of server

            Example:
                >ads includeSA 31231973

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if ads.checkServerExcludeAds(server_id) == False:
            await self.bot.say("This server isn't **excluded**... :sweat_smile:")
            return

        if ads.includeServerAds(server_id) == True:
            await self.bot.say("**" + str(server_id) + "** has been **included** into **ads** again... :eyes:")
            return

        else:
            await self.bot.say("Sorry I wasn't able to **include " + str(server_id) + "**... :pensive:")
            return

    # LOTTERY COMMANDS   <-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    @commands.group(pass_context=True, hidden=True)
    async def lotteryE(self, raw):
        """Commands used by developers for lottery. You'll need to be in owners to use these commands."""
        pass

    @lotteryE.command(pass_context=True)
    async def lotteryState(self, raw, state="true"):
        """Turn lottery on and off.

                >lottery lotteryState (state)
            state   -   State of the lottery   -   true, lottery will be on; false, lottery will be off.

            Example:
                >lottery lotteryState false

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        try:
            state = str(state).lower()

            if state == "false":
                config.lottery_settings["on"] = False

                await self.bot.say("Lottery is **off**... :eyes:")

            else:
                config.lottery_settings["on"] = True

                await self.bot.say("Lottery is **on**... :eyes:")

            lottery.storeSettings()

        except Exception as e:
            await self.bot.say("**Lottery state wasn't effected**... :confused:```" + str(e) + "```")

    @lotteryE.command(pass_context=True)
    async def lotteryIceC(self, raw, chance="1000"):
        """Change the chances of hitting the ICE lottery.

                >lottery lotteryIce (chance)
            chance   - chance the lottery will hit, 1 out of chance   -   A number; decimals will be rounded up.

            Example:
                >lottery lotteryIce 999

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if tools.isInt(chance) == False:
            await self.bot.say("**" + str(chance) + "** isn't a valid number... :sweat_smile:")
            return

        chance = int(chance)

        if chance < 1:
            await self.bot.say("**" + str(chance) + "** is smaller then **1** needs to be bigger... :sweat_smile:")
            return

        try:

            config.lottery_settings["iceRate"] = chance

            await self.bot.say("**1** out of a **" + str(chance) + "** is the new **ICE lottery chance**... :eyes:")

            lottery.storeSettings()

        except Exception as e:
            await self.bot.say("**ICE lottery chance wasn't effected**... :confused:```" + str(e) + "```")


    @lotteryE.command(pass_context=True)
    async def lotteryIceA(self, raw, amount="100"):
        """Change the amount of ICE won.

                >lottery lotteryIce (chance)
            chance   - chance the lottery will hit, 1 out of chance   -   A number; decimals will be rounded up.

            Example:
                >lottery lotteryIce 999

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if tools.isInt(amount) == False:
            await self.bot.say("**" + str(amount) + "** isn't a valid number... :sweat_smile:")
            return

        amount = int(amount)

        if amount < 1:
            await self.bot.say("**" + str(amount) + "** is smaller then **1** needs to be bigger... :sweat_smile:")
            return

        try:

            config.lottery_settings["iceAmount"] = amount

            await self.bot.say("**" + str(amount) + "** is now the quantity of ICE won from the lottery... :eyes:")

            lottery.storeSettings()

        except Exception as e:
            await self.bot.say("**ICE lottery amount wasn't effected**... :confused:```" + str(e) + "```")


    @lotteryE.command(pass_context=True)
    async def lotteryCooldown(self, raw, time=1000):
        """Lottery cool down.

                >lottery lotteryCooldown (time)
            time   -   Time, in minutes, each lottery cool down is.   -   A number; decimals will be rounded up.

            Example:
                >lottery lotteryCooldown 60

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if tools.isInt(time) == False:
            await self.bot.say("**" + str(time) + "** isn't a valid number... :sweat_smile:")
            return

        time = int(time)

        if time < 1:
            await self.bot.say("**" + str(time) + "** is smaller then **1** needs to be bigger... :sweat_smile:")
            return

        try:

            config.lottery_settings["timeOut"] = time

            await self.bot.say("Lottery cool down has been updated to **" + str(time) + "**... :eyes:")

            lottery.storeSettings()

        except Exception as e:
            await self.bot.say("**Lottery cool down wasn't effected**... :confused:```" + str(e) + "```")

    @lotteryE.command(pass_context=True)
    async def excludeUL(self, raw, discord_user_id):
        """Remove a user from the lottery by their ID.

            >lottery removeUL (discord_user_id)

            Example:
                >lottery removeUL 332331312312

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if discord_user_id in config.lottery_excludes:
            await self.bot.say("**" + str(discord_user_id) + "** is **already excluded from the lottery**... :sweat_smile:")
            return

        try:

            config.lottery_excludes.append(discord_user_id)

            await self.bot.say("**" + str(discord_user_id) + "** has been removed from the lottery... :eyes:")

            lottery.storeLottery()

        except Exception as e:
            await self.bot.say("**" + str(discord_user_id) + " wasn't successfully excluded from the lottery**... :confused:```" + str(e) + "```")

    @lotteryE.command(pass_context=True)
    async def includeUL(self, raw, discord_user_id):
        """Include a user from the lottery by their ID.

            >lottery includeUL (discord_user_id)

            Example:
                >lottery includeUL 332331312312

        """
        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if discord_user_id not in config.lottery_excludes:
            await self.bot.say("**" + str(discord_user_id) + " isn't excluded from the lottery**... :sweat_smile:")
            return

        try:

            config.lottery_excludes.pop(discord_user_id)

            await self.bot.say("**" + str(discord_user_id) + "** has been added to the lottery... :eyes:")

            lottery.storeSettings()

        except Exception as e:
            await self.bot.say("**" + str(discord_user_id) + " wasn't successfully added to the lottery**... :confused:```" + str(e) + "```")

    async def getInfo(self, message, req=[], check=""):
        """Gives info needed to function related to General.

            :param req: A list, containing Strings of everything needed. Options: userData, serverData, needPublic, needPrivate, needAdmin, isPrivate, isAdmin, mention, destination, language
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
            "destination": message.author,
            "language": "english"
        }

        result = {}  # What's going to be sent
        try:

            # If communication pipe is private, Example: private messages
            if message.channel.is_private == True:
                try:

                    if "needPublic" in req:
                         result["error-public"] = True

                    if "isPrivate" in req:
                        result["isPrivate"] = True

                    if "mention" in req:
                        result["mention"] = defaults["mention"]

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

                        if "destination" in req:
                            result["destination"] = message.author

                # In-case of a huge error return default settings
                except:
                        if "userData" in req:
                            result["userData"] = defaults["userData"]

                        if "language" in req:
                            result["language"] = defaults["language"]

                        if "destination" in req:
                            result["destination"] = defaults["destination"]

            # If communication pipe isn't private, Example: server/guild
            else:
                try:

                    if "needPrivate" in req:
                        result["error-private"] = True

                    if "isPrivate" in req:
                        result["isPrivate"] = False

                    if "mention" in req:
                        try:
                            result["mention"] = str((await self.bot.get_user_info(message.author.id)).mention)

                        except:
                            result["mention"] = defaults["mention"]

                    if "isAdmin" in req:
                        result["isAdmin"] = (message.author.permissions_in(message.channel)).administrator

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

    bot.add_cog(Bot(bot))
