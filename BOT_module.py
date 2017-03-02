# Body Module:
# Things that give a bot meaning!

# IMPORTS
import asyncio
import TOOL_module as tools

# MANAGES functions in the BOT module
async def commandBOT(bot, author, channel, part1, part2):
    if part1 == "catch":
        await catchMsgBOT(bot, author, channel)

    elif part1 == "sleep":
        await sleepBOT(bot, part2)

    else:
        await bot.say("**>bot" + str(part1) + str(part2) + "** *isn't a valid command!*")  # When no PARTS are MATCHED

# Tells AUTHOR how many MSGs he has in THIS channel
async def catchMsgBOT(bot, author, channel):
    msgs = 0
    msg = await bot.send_message(channel, "Calculating messages...")
    async for log in bot.logs_from(channel, limit=100):
            if log.author == author:
                msgs += 1

    if msgs == 100:  # BOT SAYS that you have over 100 MESSAGES
        await bot.edit_message(msg, "You have over 100 messages!")

    else:  # BOT SAYS number of MESSAGES you HAVE
        await bot.edit_message(msg, "You have " + str(msgs) + " messages!")


# Tells BOT to sleep for NUM of SECONDS
async def sleepBOT(bot, seconds):
    if isinstance(seconds, int) == False:
        await bot.say(str(seconds) + " isn't a valid number!")

    else:
        seconds = int(seconds)

        if seconds > 3600:
            seconds = 3600
        elif seconds <= 0:
            seconds = 1

        await bot.say("Going to sleep for " + str(seconds) + " seconds good night... :sleeping:")
        await asyncio.sleep(seconds)
        await bot.say("Done sleeping! :raised_hands:")
