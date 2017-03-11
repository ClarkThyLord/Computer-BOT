# Body Commands:
# File containing all of the BOT commands for Discord
"""

List of Commands:
developer   ~   extension commands: servers
invite
bot

"""

# IMPORTS
import discord
from discord.ext import commands

# BOT VARIABLES
nameBOT = "Computer"

# CLASS containing ALL COMMANDS for THIS MODULE
class Bot():
    """Basic bot Commands.

            Made using Discord.py

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # pass_context=True
    async def developer(self, command=""):
        """A command used by developers."""

        # author = msg.message.author  # Get the AUTHOR of the MESSAGE
        # channel = msg.message.channel  # Get the CHANNEL of the MESSAGE

        if command == "":
            await self.bot.say("You need to input an extension command... :sweat_smile:")
            return

        if command == "servers":
            msg = await self.bot.say("Running " + str(command) + "... :eyes:")

            notice = "I'm in **" + str(len(self.bot.servers)) + "** servers total!\nNames are the Following:\n"

            for server in self.bot.servers:
                notice += str(server.name)

            await self.bot.edit_message(msg, notice)


        else:
            await self.bot.say(str(command) + " isn't a valid extension command... :sweat_smile:")

    @commands.command()
    async def invite(self):
        """When you want to invite this bot to another server."""

        await self.bot.say("You can invite me to any server at:\nhttps://discordapp.com/oauth2/authorize?client_id=284430926648442890&scope=bot&permissions=0x00004000")

    @commands.command()
    async def bot(self):
        """Gives you some info on this bot."""

        await self.bot.say("Hi, I'm *" + str(nameBOT) + "*, and I've been developed in Python and have grown with lots of love. You can see a list of our commands with the **help** command!")

def setup(bot):
    bot.add_cog(Bot(bot))
