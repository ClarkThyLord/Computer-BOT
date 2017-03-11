# VG Commands:
# File containing all of VG commands for Discord
"""

List of Commands:
player
stats
match

"""

# IMPORTS
import gamelocker
from discord.ext import commands
import TOOL_module as tools
import VG_module
import VG_toolbox

# VG Variables--
keyVG = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4ZmZiZWRiMC1kZTI2LTAxMzQtY2E4YS0wMjQyYWMxMTAwMDYiLCJpc3MiOiJnYW1lbG9ja2VyIiwib3JnIjoiY2xhcmNrNzEtb3V0bG9vay1jb20iLCJhcHAiOiI4ZmZhMzE0MC1kZTI2LTAxMzQtY2E4OS0wMjQyYWMxMTAwMDYiLCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.wQQmGA--zf9PeIV0inIr-ZaZzsFLw_eVwHVwV1WXZCo"  # VG_API_TOKEN_HERE
apiVG = gamelocker.Gamelocker(keyVG).Vainglory()  # API OBJECT

# DISCORD EMBED VARIABLES--
botImageDISCORD = "http://i63.tinypic.com/9k6xcj.jpg"  # URL of BOTS IMAGE
signatureDISCORD = "Big Thanks to SEMC and MadGlory! Made with love ~ xoxo"  # String used in FOOTER as MESSAGE

# CLASS containing ALL COMMANDS for THIS MODULE
class Vg():
    """All the commands in relation to Vainglory.

            Made with love and some Vainglory api, python - gamelocker.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, player_name="", server="na", days="7", game_type="any", auto="False"):
        """Gets a players performance in the past days.

                >stats (player_name) (server) (days) (game_type)
            player_name   ~   name of player to search for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            days          ~   day range to search from                     ~   default: 7, requirements: maximum: 93, minimum: 1
            game_type     ~   game type you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz

            example:
                >stats player1 na 10 casual

        """
        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WASTE OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # MESSAGE the USER if NO NAME was GIVEN
        if player_name == "":
            await self.bot.say("You need to give a player's name at least...")
            return

        # MESSAGE the USER if NAME GIVEN is TOO SHORT
        if len(str(player_name)) < 3:
            await self.bot.say("That isn't a valid name... :sweat_smile:")
            return

        # MESSAGE the USER if a NUMBER was GIVEN
        if tools.isIntTOOL(player_name) == True:
            await self.bot.say(str(player_name) + " isn't a valid name... :sweat_smile:")
            return

        notice = "Looking at matches for " + str(player_name)

        # Check that SERVER is VALID
        if VG_toolbox.isServerVG(server) == True:
            if str(server) == "sea":
                server = "sg"

            notice += " in " + str(server) + " servers"

        else:
            await self.bot.say(str(server) + " isn't a valid server name... :sweat_smile:")
            return

        # CHECK DAYS to be a VALID NUMBER
        if tools.isIntTOOL(days) == True:
            days = int(days)  # Convert DAYS to INT to prevent ERRORS

            if days > 93:
                days = 93  # MAKE DAYS a VALID RANGE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

            elif days <= 0:
                days = 1  # MAKE DAYS a VALID RANGE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

            else:  # LEAVE DAYS ALONE
                notice += " from the past " + str(days) + " days"  # ADD to NOTICE that DATE

        else:  # DATE is INVALID so THEN MESSAGE USER
            await self.bot.say("Sorry but " + str(days) + " isn't a valid number... :sweat_smile:")  # If DAYS is an INVALID number TELL USER
            return

        # Check that GAMETYPE is VALID
        if game_type != "" and tools.isIntTOOL(game_type) == False:

            if VG_toolbox.isGameModeVG(game_type) == True:  # GAMETYPE is VALID
                notice += " from " + game_type + " games"

                # If GAMETYPE is ANY turn to BLANK
                if game_type == "any":
                    game_type = ""

            else:  # GAMETYPE isn't VALID
                await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
                return

        # If GAMETYPE is VALID then MESSAGE user
        if game_type != "" and tools.isIntTOOL(game_type) == True:
            await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
            return

        # END of NOTICE
        notice += "... :eyes:"

        # Converts AUTO to it's proper BOOLEAN
        if auto == "False" or auto == "false":
            auto = False
        elif auto == "True" or auto == "true":
            auto = True
            notice += " - AUTO: True"

        else:
            await self.bot.say("That isn't a valid secret!")
            return

        # NOTICE USER that THEIR COMMAND is being PROCESSED
        msg = await self.bot.say(notice)
        # RUNS PERFORMANCE FETCH and UPDATES MESSAGE once DONE
        
        output = VG_module.getPlayerPerformanceVG(player_name, server, days, game_type, auto)
        if type(output) == str:
                await self.bot.edit_message(msg, output)
        else:
            await self.bot.edit_message(msg, embed=output)

    @commands.command()
    async def player(self, player_name="", server="na", mode="user", auto="False"):
        """Checks if player exist in vainglory.

                >player (player_name) (server) (mode)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            mode          ~   user or dev mode                             ~   default: user, options: user, dev

            Example:
                >player player1 na user

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        notice = "Looking for "  # DEFAULT NOTICE SENT to USER!

        # Check that a NAME was GIVEN
        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        # Check that NAME is VALID
        if tools.isIntTOOL(player_name) == True or len(player_name) < 3:
            await self.bot.say(str(player_name) + " isn't a valid name!")

        notice += str(player_name)

        # Check that SERVER is VALID
        if VG_toolbox.isServerVG(server) == True:
            if str(server) == "sea":
                server = "sg"
            notice += " in " + str(server) + " servers"

        else:
            await self.bot.say(str(server) + " isn't a valid server name... :sweat_smile:")
            return

        notice += "... :eyes:"

        # Check that MODE is VALID
        if mode == "user" or mode == "dev":
            pass

        else:
            await self.bot.say(str(mode) + " isn't a valid mode... :sweat_smile:")
            return


        # Converts AUTO to it's proper BOOLEAN
        if auto == "False" or auto == "false":
            auto = False

        elif auto == "True" or auto == "true":
            auto = True

            notice += " - AUTO: True"

        else:
            await self.bot.say("That isn't a valid secret!")
            return

        player_name = str(player_name)  # Convert PLAYER_NAME to STRING to prevent errors

        msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
        output = VG_module.getPlayerInfoVG(player_name, server, mode, auto)
        if type(output) == str:
                await self.bot.edit_message(msg, output)
        else:
            await self.bot.edit_message(msg, embed=output)  # RUNS ID TEST


    @commands.command()
    async def match(self, player_name="", server="na", game_type="any", auto="False"):
        """Fetched the latest Vainglory match.

                >player (player_name) (server) (game_type)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            game_type     ~   game type you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz

            Example:
                >match player1 na casual

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        notice = "Looking for the latest match of "  # DEFAULT NOTICE SENT to USER!

        # Check that a NAME was GIVEN
        if player_name == "":
            await self.bot.say("You need to give a players name... :sweat_smile:")
            return

        # Check that NAME is VALID
        if tools.isIntTOOL(player_name) == True or len(player_name) < 3:
            await self.bot.say(str(player_name) + " isn't a valid name!")

        notice += str(player_name)

        # Check that SERVER is VALID
        if VG_toolbox.isServerVG(server) == True:
            if str(game_type) == "sea":
                game_type = "sg"

            notice += " in " + str(server) + " servers"

        else:
            await self.bot.say(str(server) + " isn't a valid server name... :sweat_smile:")
            return

        # Check that GAMETYPE is VALID
        if game_type != "" and tools.isIntTOOL(game_type) == False:

            if VG_toolbox.isGameModeVG(game_type) == True:  # GAMETYPE is VALID
                notice += " from " + str(game_type) + " games"

                # If GAMETYPE is ANY turn to BLANK
                if game_type == "any":
                    game_type = ""

            else:  # GAMETYPE isn't VALID
                await self.bot.say("Sorry but " + str(game_type) + " isn't a valid game type... :sweat_smile:")
                return

            # Converts AUTO to it's proper BOOLEAN
            if auto == "False" or auto == "false":
                auto = False
            elif auto == "True" or auto == "true":
                auto = True
                notice += " - AUTO: True"

            else:
                await self.bot.say("That isn't a valid secret!")
                return

            notice += "... :eyes:"

            msg = await self.bot.say(notice)
            output = VG_module.getLatestMatchVG(player_name, server, game_type, auto)
            if type(output) == str:
                await self.bot.edit_message(msg, output)

            else:
                await self.bot.edit_message(msg, embed=output)


def setup(bot):
    bot.add_cog(Vg(bot))
