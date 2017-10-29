from discord.ext import commands
import config
import json
from traceback import format_exc
from src.mongo_work import core
import random
import os

class Bot():

    def __init__(self, bot):
        """At creation of this objects setup what's needed."""

        self.bot = bot  # Create a bots instance in this object

    @commands.group(pass_context=True, hidden=True)
    async def mongo(self, raw):
        """Commands used by developers for MongoDB. You'll need to be in owners to use these commands."""
        pass

    # @mongo.command(pass_context=True)
    # async def (self, raw):
    #     """
    #
    #             >mongo
    #
    #         Example:
    #             >mongo
    #
    #     """
    #     if raw.message.author.id not in config.owners:  # Check if author is owner
    #         return

    @mongo.command(pass_context=True)
    async def mongoSize(self, raw):
        """List the size of mongo db.

                >mongo mongoSize

            Example:
                >mongo mongoSize

        """

        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        await self.bot.say(core.dataBaseSize())

    @mongo.command(pass_context=True)
    async def getMongo(self, raw, db_name="", collection_name="", db_filter=""):
        """List the size of mongo db.

                >mongo getMongo (db_name) (collection) (db_filter)
            db_name           -   Database name.
            collection_name   -   Database collection name.
            db_filter         -   Database filter, a dictionary used to filter results with.

            Example:
                >mongo getMongo test test_name {"_id": "id"}

        """

        if raw.message.author.id not in config.owners:  # Check if author is owner
            return

        if db_name == "":
            await self.bot.say("You must give a **db name**... :sweat_smile:")
            return

        if collection_name == "":
            await self.bot.say("You must give a **collection name**... :sweat_smile:")
            return

        if db_filter == "":
            db_filter = {}

        result = core.getFromMongo(str(db_name), str(collection_name), str(db_filter))
        path = config.directory + "//temp//" + str(random.randrange(1, 9999999999)) + ".json"

        with open(path, "w") as handler:
            json.dump(result, handler)

        # FOR DEBUGGING
        # print("PATH: " + str(path))

        try:

            msg = await self.bot.say("Sending result this make take a while... :eyes:")
            await self.bot.send_file(raw.message.channel, path)

            await self.bot.edit_message(msg, "File has been sent :hugging:")

        except:
            await self.bot.say("Error occurred... :confused:\n" + str(format_exc()))

        try:
            if path != None:
                os.remove(path)

                # FOR DEBUGGING
                # print("REMOVED JSON AT:\n" + str(path))

        except:
            await self.bot.send_message(self.bot.get_channel(config.discord_logs_channel), "FROM: " + str(config.bot_name) + "```Couldn't removed file at:\n" + str(path) + "```")

def setup(bot):
    """Adds commands to the bot_work on load of this module."""

    bot.add_cog(Bot(bot))