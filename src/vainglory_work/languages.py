import config


# GENERAL LINES
def profileTest(language, mention, profileType):
    msg ={
    "english": mention + ", this is what your **" + profileType + " profile** looks like... :eyes:",
    "spanish": mention + ", esto es lo que su **prefil de " + profileType + "** se parece... :eyes:"
    }

    return msg.get(language, mention + ", this is what your **" + profileType + " profile** looks like... :eyes:")

def noProfile(language, mention, profileType):
    msg = {
    "english": mention + ", no **" + profileType + " profile** related to you was found... :confused:",
    "spanish": mention + ", no hay un **" + profileType + " perfil** relacionado con usted... :confused:"
    }

    return msg.get(language, mention + ", no **" + profileType + " profile** related to you was found... :confused:")

def notVerified(language, mention, botPrefix):
    msg = {
    "english": mention + ", you're not **verified** with us, **" + config.bot_name + "**, so you can't make use of this feature! :sweat_smile:\nPlease look at **" + botPrefix + "help verify** for more :hugging:",
    "spanish": mention + ", No se ha **verificado** con nosotros, **" + config.bot_name + "**, por lo que no puede hacer uso de esta característica! :sweat_smile:\nPor favor mire **" + botPrefix + "help verify** para más :hugging:"
    }

    return msg.get(language, mention + ", you aren't **verified** with us, **" + config.bot_name + "**, so you can't make use of this feature! :sweat_smile:\nPlease look at **" + botPrefix + "help verify** for more :hugging:")


def noInput(language, mention, inputType):
    msg = {
    "english": mention + ", you need to give a valid **" + inputType + "**... :sweat_smile:",
    "spanish": mention + ", necesita dar un nombre válido **" + inputType + "**... :sweat_smile:"
    }

    return msg.get(language, mention + ", you need to give a valid **" + inputType + "**... :sweat_smile:")


def invalidInput(language, mention, input, inputType):
    msg = {
    "english": mention + ", **" + input + "** isn't a valid **" + inputType + "**... :sweat_smile:",
    "spanish": mention + ", **" + input + "** no es un válido **" + inputType + "**... :sweat_smile:"
    }

    return msg.get(language, mention + ", **" + input + "** isn't a valid **" + inputType + "**... :sweat_smile:")


def noEmojisAllowed(language):
    msg = {
    "english": "It seems that **" + str(config.bot_name) + "** can't use __**External Emojis**__ in this server! Notify a server admin to allow __**External Emojis**__ :hugging:",
    "spanish": "Parece que **" + str (config.bot_name) + "** no puede usar __**Emojis Externo**__ en este servidor! Notifica a un administrador del servidor para permitir uso __**Emojis Externo**__ :hugging:"
    }

    return msg.get(language, "It seems that **" + str(config.bot_name) + "** can't use __**External Emojis**__ in this server! Notify a server admin to allow __**External Emojis**__ :hugging:")

def unSentFile(language, mention):
    msg = {
    "english": mention + ", sorry we can't send the file at the moment :sob:",
    "spanish": mention + ", lo sentimos no pudimos enviar el archivo en este momento :sob:"
    }

    return msg.get(language, mention + ", sorry we can't send the file at the moment :sob:")


def sentFile(language, mention):
    msg = {
    "english": mention + ", file has been sent :blush:",
    "spanish": mention + ", El archivo ha sido enviado :blush:"
    }

    return msg.get(language, mention + ", file has been sent :blush:")


def noPlayerName(language, mention):
    msg = {
    "english": mention + ", **you didn't enter a player name...** :sweat_smile:",
    "spanish": mention + ", **no ingresaste el nombre de un jugador...** :sweat_smile:"
    }

    return msg.get(language, mention + ", **you didn't enter a player name...** :sweat_smile:")


def noRegion(language, mention):
    msg = {
    "english": mention + ", **you didn't enter a region...** :sweat_smile:",
    "spanish": mention + ", **no ingresaste el nombre de la región...** :sweat_smile:"
    }

    return msg.get(language, mention + ", **you didn't enter a region...** :sweat_smile:")


def invalidPlayerName(language, mention, playerName):
    msg = {
    "english": mention + ", **" + playerName + " isn't a valid player name...** :sweat_smile:",
    "spanish": mention + ", **" + playerName + " no es un nombre de valido para un jugador...** :sweat_smile:"
    }

    return msg.get(language, mention + ", **" + playerName + " isn't a valid player name...** :sweat_smile:")

def noMatchId(language, mention):
    msg = {
    "english": mention + "**, you'll need a valid match id...** :sweat_smile:",
    "spanish": mention + ", necesitas ingresar un ID de un partido válido... :sweat_smile:"
    }

    return msg.get(language, mention + "**, you'll need a valid match id...** :sweat_smile:")

def noTopElement(langauge, mention):
    msg = {
    "english": mention + ", no **top element** was given... :sweat_smile:",
    "spanish": mention + ", no se ha dado ningún elemento... :sweat_smile:"
    }

    return msg.get(langauge, mention + ", no **top element** was given... :sweat_smile:")

def invalidTopElement(language, mention, topElement):
    msg = {
    "english": mention + ", **" + topElement + "** isn't a valid element to check for... :sweat_smile:",
    "spanish": mention + ", **" + topElement + "** No es un elemento válido para comprobar... :sweat_smile:"
    }

    return msg.get(language, mention + ", **" + topElement + "** isn't a valid element to check for... :sweat_smile:")

def matchNotFound(language, mention, matchId, region):
    msg = {
    "english": mention + ", I didn't find  the match , **" + matchId + "**, in the **" + region + "** region... :confused:",
    "spanish": mention + ", no encontré el partido , **" + matchId + "**, en la **" + region + "** región... :confused:"
    }

    return msg.get(language, mention + ", I didn't find  the match , **" + matchId + "**, in the **" + region + "** region... :confused:")

def notVgGuildName(language, mention, name):
    msg = {
    "english": mention  + "**" + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:",
    "spanish": mention + "**" + name + "** no es un **válido** nombre para un **gremio de Vainglory** ...: sweat_smile:"
    }

    return msg.get(language, "**" + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:")


def notVgTeamName(language, mention, name):
    msg = {
    "english": mention + "**, " + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:",
    "spanish": mention + "**, " + name + "** no es un **válido** nombre para un **equipo de Vainglory** ...: sweat_smile:"
    }

    return msg.get(language, mention + "**, " + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:")

def noQuickData(language, mention, botPrefix):
    msg = {
    "english": mention + ", you'll have to save data to your discord account **before using VainGlory related commands without arguments**... :stuck_out_tongue:\nEnter **" + botPrefix + "help savevg** for more information! :hugging:",
    "spanish": mention + ", tendrás que guardar datos en tu cuenta de discord **antes de usar comandos relacionados con VainGlory sin argumentos**... :stuck_out_tongue:\nEnter **" + botPrefix + "help savevg** para más información! :hugging:"
    }

    return msg.get(language, mention + ", you'll have to save data to your discord account **before using VainGlory related commands without arguments**... :stuck_out_tongue:\nEnter **" + botPrefix + "help savevg** for more information! :hugging:")

def noQuickDataOnMention(language, mention, mentioned):
    msg = {
    "english": mention + ", no **user data** was found on **" + mentioned + "**... :sweat_smile:",
    "spanish": mention + ", no hay **datos del usuario " + mentioned + "**... :sweat_smile:"
    }

    return msg.get(language, mention + ", no **user data** was found on **" + mentioned + "**... :sweat_smile:")

def duplicateIgn(language, mention):
    msg = {
    "english": mention + "**, you can't use the same ign twice in a command...** :sweat:",
    "spanish": mention + "**, no puedes usar el mismo ign dos veces en un comando...** :sweat:"
    }

    return msg.get(language, mention + "**, you can't use the same ign twice in a command...** :sweat:")

def playerNotFound(language, mention, ign, region):
    msg = {
    "english": mention + ", nothing was found on **" + ign + "** in **" + region + "**... :confused:",
    "spanish": mention + ", no se encontró nada de **" + ign + "** en **" + region + "**... :confused:"
    }

    return msg.get(language, mention + ", nothing was found on **" + ign + "** in **" + region + "**... :confused:")

# CUSTOM LINES
def playerDescription(language, name, createdAt):
    msg = {
    "english": "__**Vainglory Career for " + name + "**__\n**Last Match Played:** *" + createdAt + "*",
    "spanish": "__**Carrera de Vainglory para "+ name +"**__\n**Último Partido Jugado:** *"+ createdAt + "*"
    }

    return msg.get(language, "__**Vainglory Career for " + name + "**__\n**Last Match Played:** *" + createdAt + "*")


def playerLineOne(language, mention, playerName, region):
    msg = {
    "english": mention + ", looking for **" + playerName + "** in **" + region + "**... :eyes:",
    "spanish": mention + ", buscando **" + playerName + "** en **" + region + "**... :eyes:"
    }

    return msg.get(language, "Looking for **" + playerName + "** in **" + region + "**... :eyes:")


def playerLineTwo(language, mention, playerName, region):
    msg = {
    "english": mention + ", couldn't find anything on **" + playerName + "** in **" + region +"**... :confused:",
    "spanish": mention + ", no encontró nada de **" + playerName +"** en **" + region + " **... :confused:"
    }

    return msg.get(language, mention + ", couldn't find anything on **" + playerName + "** in **" + region +"**... :confused:")


def playerEmbedFieldOneTitle(language):
    msg = {
    "english": "__Career:__",
    "spanish": "__Carrera:__"
    }

    return msg.get(language, "__Career:__")


def playerEmbedFieldOne(language, winRate, wins, loss, matches, winStreak, lossStreak, gold):
    msg = {
    "english": "**Win Rate:** *" + winRate + "*\n**Total Wins:** *" + wins + "*  **|Total Loss:** *" + loss + "*  **|Total Matches:** *" + matches + "*\n**Win Streak:** *" + winStreak + "*  **|Loss Streak:** *" + lossStreak + "*\n**Life Time Gold:** *" + gold + "*",
    "spanish": "**Gana:** *" + winRate + "*\n**Total de Victorias:** *" + wins + "* **|Total de Perdidas:** *" + loss + "* **|Total de Juegos** *" + matches + "*\n**Racha:** *" + lossStreak + "* **|Racha de pérdidas:** *" + lossStreak + "*\n**Total de Oro:** *" + gold + "*"
    }

    return msg.get(language, "**Win Rate:** *" + winRate + "*\n**Total Wins:** *" + wins + "*  **|Total Loss:** *" + loss + "*  **|Total Matches:** *" + matches + "*\n**Win Streak:** *" + winStreak + "*  **|Loss Streak:** *" + lossStreak + "*\n**Life Time Gold:** *" + gold + "*")


def playerEmbedFieldTwoTitle(language):
    msg = {
    "english": "__ELO Career:__",
    "spanish": "__Carrera De ELO:__"
    }

    return msg.get(language, "__ELO Career:__")


def comparePlayersLineOne(language):
    msg = {
    "english": "**More then one in-game name must be given...** :sweat_smile:",
    "spanish": "**Se debe de dar dos o más nombres de juegadores...** :sweat_smile:"
    }

    return msg.get(language, "**More then one in-game name must be given...** :sweat_smile:")


def comparePlayersDescription(language, size, region):
    msg = {
    "english": "Comparing **" + size + "** players in the **" + region + "** region!",
    "spanish": "Comparando **" + size + "** jugadores en la **" + region + "** región!"
    }

    return msg.get(language, "Comparing **" + size + "** players in the **" + region + "** region!")


def comparePlayersFieldOneTitle(language):
    msg = {
    "english": "__Biggest Level__",
    "spanish": "__El Nivel Mas Grande__"
    }

    return msg.get(language, "__Biggest Level__")


def comparePlayersFieldTwoTitle(language):
    msg = {
    "english": "__Most Xp__",
    "spanish": "__Más Xp__"
    }

    return msg.get(language, "__Most Xp__")


def comparePlayersFieldThreeTitle(language):
    msg = {
    "english": "__Most Gold__",
    "spanish": "__Más Oro__"
    }

    return msg.get(language, "__Most Xp__")


def comparePlayersFieldFourTitle(language):
    msg = {
    "english": "__Highest Win Rate__",
    "spanish": "__Porcentaje de Ganancias__"
    }

    return msg.get(language, "__Highest Win Rate__")


def comparePlayersFieldFiveTitle(language):
    msg = {
    "english": "__Total Wins__",
    "spanish": "__Total de Victorias__"
    }

    return msg.get(language, "__Total Wins__")


def comparePlayersFieldSixTitle(language):
    msg = {
    "english": "__Total Losses__",
    "spanish": "__Pérdidas totales__"
    }

    return msg.get(language, "__Total Losses__")


def comparePlayersFieldSevenTitle(language):
    msg = {
    "english": "__Biggest Win Streak__",
    "spanish": "__Mayor Racha de Victorias__"
    }

    return msg.get(language, "__Biggest Win Streak__")


def comparePlayersFieldEightTitle(language):
    msg = {
    "english": "__Biggest Lost Streak__",
    "spanish": "__Mayor Racha de Pérdidas__"
    }

    return msg.get(language, "__Biggest Lost Streak__")


def saveVGLineOne(language, mention, playerName, region, guildName, teamName):
    msg = {
    "english": mention + ", saving ign, **" + playerName + "**, region, **" + region + "**, guild name, **" + guildName + "**, team name, **" + teamName + "**, to your discord account... :eyes:",
    "spanish": mention + ", guardano ign, **" + playerName + "**, región, **" + region + "**, nombre del gremio, **" + guildName + "**, nombre del equipo, **" + teamName + "**, a tu cuenta de discord.. :eyes:"
    }

    return msg.get(language, mention + ", saving ign, **" + playerName + "**, region, **" + region + "**, guild name, **" + guildName + "**, team name, **" + teamName + "**, to your discord account... :eyes:")


def saveVGLineTwo(language, mention, playerName, region, guildName, teamName):
    msg = {
    "english": mention + ", ign, **" + playerName + "**, region, **" + region + "**, guild name, **" + guildName + "**, team name, **" + teamName + "**, have been saved to your discord account... :hugging:",
    "spanish": mention + ", ign, **" + playerName + "**, región, **" + region + "**, nombre del gremio, **" + guildName + "**, nombre del equipo, **" + teamName + "**, se han salvado a tu cuenta de discord.. :hugging:"
    }

    return msg.get(language, mention + ", ign, **" + playerName + "**, region, **" + region + "**, guild name, **" + guildName + "**, team name, **" + teamName + "**, have been saved to your discord account... :hugging:")


def saveVGLineThree(language, mention, playerName, region, guildName, teamName):
    msg = {
    "english": mention + ", ign, **" + playerName + "**, region, **" + region + "**, guild name, **" + guildName + "**, team name, **" + teamName + "**, wasn't saved to your discord account... :confused:",
    "spanish": mention + ", ign, **" + playerName + "**, región, **" + region + "**, nombre del gremio, **" + guildName + "**, nombre del equipo, **" + teamName + "**, no se guardó a tu cuenta de discord.. :confused:"
    }

    return msg.get(language, mention + ", ign, **" + playerName + "**, region, **" + region + "**, guild name, **" + guildName + "**, team name, **" + teamName + "**, wasn't saved to your discord account... :confused:")

def compareUniquePlayersDescription(language, size, regionOne, regionTwo):
    msg = {
    "english": "Comparing **" + size + "** players in the **" + regionOne + "** and **" + regionTwo + "** region!",
    "spanish": "Comparando **" + size + "** jugadores en la **" + regionOne + "** y **" + regionTwo + "** región!"
    }

    return msg.get(language, "Comparing **" + size + "** players in the **" + regionOne + "** and **" + regionTwo + "** region!")

def compareUniquePlayersLineOne(language, mention, ignOne, regionOne, ignTwo, regionTwo):
    msg = {
    "english": mention + ", looking at **" + ignOne + ", " + regionOne + ",** and **" + ignTwo + ", " + regionTwo +"**... :eyes:",
    "spanish": mention + ", mirando a **" + ignOne + ", " + regionOne + ",** y **" + ignTwo + ", " + regionTwo +"**... :eyes:"
    }

    return msg.get(language, mention + ", looking at **" + ignOne + ", " + regionOne + ",** and **" + ignTwo + ", " + regionTwo +"**... :eyes:")

def compareUniquePlayersFieldOneTitle(language):
    msg = {
    "english": "__Highest Skill Tier__",
    "spanish": "__Nivel de Habilidad Más Alto__"
    }

    return msg.get(language, "__Highest Skill Tier__")

def compareUniquePlayersFieldTwoTitle(language):
    msg = {
    "english": "__Highest Karma Level__",
    "spanish": "__Mas Grande Nivel de Karma__"
    }

    return msg.get(language, "__Highest Karma Level__")

def compareUniquePlayersFieldThreeTitle(language):
    msg = {
    "english": "__Biggest Level__",
    "spanish": "__El Nivel Mas Grande__"
    }

    return msg.get(language, "__Biggest Level__")

def compareUniquePlayersFieldFourTitle(language):
    msg = {
    "english": "__Most Xp__",
    "spanish": "__Más Xp__"
    }

    return msg.get(language, "__Most Xp__")

def compareUniquePlayersFieldFiveTitle(language):
    msg = {
    "english": "__Most Gold__",
    "spanish": "__Más Oro__"
    }

    return msg.get(language, "__Most Gold__")

def compareUniquePlayersFieldSixTitle(language):
    msg = {
    "english": "__Highest Win Rate__",
    "spanish": "__Porcentaje de Ganancias__"
    }

    return msg.get(language, "__Highest Win Rate__")

def compareUniquePlayersFieldSevenTitle(language):
    msg = {
    "english": "__Total Wins__",
    "spanish": "__Total de Victorias__"
    }

    return msg.get(language, "__Total Wins__")


def compareUniquePlayersFieldEightTitle(language):
    msg = {
    "english": "__Total Losses__",
    "spanish": "__Pérdidas totales__"
    }

    return msg.get(language, "__Total Losses__")


def compareUniquePlayersFieldNineTitle(language):
    msg = {
    "english": "__Biggest Lost Streak__",
    "spanish": "__Mayor Racha de Pérdidas__"
    }

    return msg.get(language, "__Biggest Lost Streak__")


def compareUniquePlayersFieldTenTitle(language):
    msg = {
    "english": "__Biggest Lost Streak__",
    "spanish": "__Mayor Racha de Pérdidas__"
    }

    return msg.get(language, "__Biggest Lost Streak__")


def statsLineOne(language, mention, playerName, region, gameMode, days):
    msg = {
    "english": mention + ", looking at stats of **" + gameMode + "** in the past **" + days + "** days for **" + playerName + "** in **" + region + "**... :eyes:",
    "spanish": mention + ", mirando las estadísticas de **" + gameMode + "** en los pasados **" + days + "** dias para **" + playerName + "** en **" + region + "**... :eyes:"
    }

    return msg.get(language, mention + ", looking at stats of **" + gameMode + "** in the past **" + days + "** days for **" + playerName + "** in **" + region + "**... :eyes:")


def statsTitle(language, ign, region, gameMode):
    msg = {
    "english": "Stats of " + ign + ", " + region + ", in " + gameMode,
    "spanish": "Stats de " + ign + ", " + region + ", en " + gameMode
    }

    return msg.get(language, ign + ", " + region + ", stats in " + gameMode)

def statsDescription(language, samplesAmount, gameMode):
    msg = {
    "english": "Sampling **" + samplesAmount + " " + gameMode + "** matches...",
    "spanish": "Muestreo de **" + samplesAmount + " " + gameMode + "** coincidencias..."
    }

    return msg.get(language, "Sampling **" + samplesAmount + " " + gameMode + "** matches...")

def statsFieldOneTitle(language):
    msg = {
    "english": "__Latest Match__",
    "spanish": "__Último Partido__"
    }

    return msg.get(language, "__Latest Match__")

def statsFieldOne(language, latestMatchDate, latestMatchGameMode):
    msg = {
    "english": "**Game Mode:** *" + latestMatchGameMode + "*\n**Date:** *" + latestMatchDate + "*",
    "spanish": "**Modo De Juego:** *" + latestMatchGameMode + "*\n**Fecha:** *" + latestMatchDate + "*"
    }

    return msg.get(language, "**Game Mode:** *" + latestMatchGameMode + "*\n**Date:** *" + latestMatchDate + "*")

def mostFrequentlyPlayedGameModes(language):
    msg = {
    "english": "__Game Mode__",
    "spanish": "__Modo de Juego__"
    }

    return msg.get(language, "__Game Mode__")

def mostFrequentlyUsedActors(language):
    msg = {
    "english": "__Favorite Heroes__",
    "spanish": "__Héroes Favoritos__"
    }

    return msg.get(language, "__Favorite Heroes__")

def mostFrequentlyUsedSkins(language):
    msg = {
    "english": "__Favorite Skins__",
    "spanish": "__Pieles Favoritas__"
    }

    return msg.get(language, "__Favorite Skins__")

def mostFrequentlyBoughtItems(language):
    msg = {
    "english": "__Frequent Items__",
    "spanish": "__Artículos Frecuentes__"
    }

    return msg.get(language, "__Frequent Items__")

def mostFrequentlyUsedItemsTitle(language):
    msg = {
    "english": "__Frequently Used Items__",
    "spanish": "__Artículos Más Utilizados__"
    }

    return msg.get(language, "__Frequently Used Items__")

def statsFieldSevenTitle(language):
    msg = {
    "english": "__General View__",
    "spanish": "__vista General__"
    }

    return msg.get(language, "__General View__")


def statsFieldSeven(language, winRate, afkRate, skillTierMean, skillTierMax, karmaLevelMean, karmaLevelMax):
    msg = {
    "english": "**Win Rate:** *" + winRate + "%* **|AFK Rate:** *" + afkRate + "%*\n**Highest Skill Tier:** *" + skillTierMax + "* **|Avg. Skill Tier:** *" + skillTierMean + "*\n**Highest Karma:** *" + karmaLevelMax + "* **|Avg. Karma:** *" + karmaLevelMean + "*",
    "spanish": "**Ratio De Victorias:** *" + winRate + "%* **|Ratio De AFK:** *" + afkRate + "%*\n**Nivel De Habilidad Más Alto:** *" + skillTierMax + "* **|Promedio De Habilidades:** *" + skillTierMean + "*\n**Karma Más Alta:** *" + karmaLevelMax + "* **|Promedio De Karma:** *" + karmaLevelMean + "*"
    }

    return msg.get(language, "**Win Rate:** *" + winRate + "%* **|AFK Rate:** *" + afkRate + "%*\n**Highest Skill Tier:** *" + skillTierMax + "* **|Avg. Skill Tier:** *" + skillTierMean + "*\n**Highest Karma:** *" + karmaLevelMax + "* **|Avg. Karma:** *" + karmaLevelMean + "*")


def statsFieldEightTitle(language):
    msg = {
    "english": "__General In-game View__",
    "spanish": "__Vista General De Juegos__"
    }

    return msg.get(language, "__General In-game View__")


def statsFieldEight(language, killsMean, killsTotal, assistsMean, assistsTotal, deathsMean, deathsTotal, minionKillsMean, minionKillsTotal):
    msg = {
    "english": "**Avg. Kills:** *" + killsMean + "* **|Kills Sum:** *" + killsTotal + "*\n**Avg. Assists:** *" + assistsMean + "* **|Assists Sum:** *" + assistsTotal + "*\n**Avg. Deaths:** *" + deathsMean + "* **|Deaths Sum:** *" + deathsTotal + "*\n**Avg. Minions:** *" + minionKillsMean + "* **|Minion Kills Sum:** *" + minionKillsTotal + "*",
    "spanish": "**Promedio De Asesinatos:** *" + killsMean + "* **|Total De Asesinatos:** *" + killsTotal + "*\n**Promedio De Asistencias:** *" + assistsMean + "* **|Total De Asistencias:** *" + assistsTotal + "*\n**Promedio De Muertes:** *" + deathsMean + "* **|Total De Muertes:** *" + deathsTotal + "*\n**Promedio De Minion Asesinatos:** *" + minionKillsMean + "* **|Sumna De Minions:** *" + minionKillsTotal + "*"
    }

    return msg.get(language, "**Avg. Kills:** *" + killsMean + "* **|Kills Sum:** *" + killsTotal + "*\n**Avg. Assists:** *" + assistsMean + "* **|Assists Sum:** *" + assistsTotal + "*\n**Avg. Deaths:** *" + deathsMean + "* **|Deaths Sum:** *" + deathsTotal + "*\n**Avg. Minions:** *" + minionKillsMean + "* **|Minion Kills Sum:** *" + minionKillsTotal + "*")


def statsFieldNineTitle(language):
    msg = {
    "english": "__View Of Scores__",
    "spanish": "__Vista De Las Puntuaciones__"
    }

    return msg.get(language, "__View Of Scores__")


def statsFieldNine(language, goldMean, goldTotal, goldMax, farmMean, farmTotal, farmMax):
    msg = {
    "english": "**Avg. Gold:** *" + goldMean + "* **|Gold Sum:** *" + goldTotal + "* **|Most Gold Earned:** *" + goldMax + "*\n**Avg. Farm:** *" + farmMean + "* **|Farm Sum:** *" + farmTotal + "* **|Most Farm Earned:** *" + farmMax + "*",
    "spanish": "**Promedio De Oro:** *" + goldMean + "* **|Oro Total:** *" + goldTotal + "* **|El Más Oro Ganado:** *" + goldMax + "*\n**Promedio De Farm:** *" + farmMean + "* **|Total De Farm:** *" + farmTotal + "* **|El Más Farm Ganado:** *" + farmMax + "*"
    }

    return msg.get(language, "**Avg. Gold:** *" + goldMean + "* **|Gold Sum:** *" + goldTotal + "* **|Most Gold Earned:** *" + goldMax + "*\n**Avg. Farm:** *" + farmMean + "* **|Farm Sum:** *" + farmTotal + "* **|Most Farm Earned:** *" + farmMax + "*")


def statsFieldTenTitle(language):
    msg = {
    "english": "__Turrets Statistics__",
    "spanish": "__Turrets Estadísticas__"
    }

    return msg.get(language, "__Turrets Statistics__")


def statsFieldTen(language, turretMean, turretRate, turretTotal):
    msg = {
    "english": "**Avg. Turret Captures:** *" + turretMean + "*\n**All Turrets Captured Rate:** *" + turretRate + "%*\n**Total Turrets Captured:** *" + turretTotal + "*",
    "spanish": "**Promedio De Torres Capturadas:** *" + turretMean + "*\n**Ratio De Capturar Todas Las Torres:** *" + turretRate + "%*\n**Total De Torres Capturadas:** *" + turretTotal + "*"
    }

    return msg.get(language, "**Avg. Turret Captures:** *" + turretMean + "*\n**All Turrets Captured Rate:** *" + turretRate + "%*\n**Total Turrets Captured:** *" + turretTotal + "*")


def statsFieldElevenTitle(language):
    msg = {
    "english": "__Crystal Miner Statistics__",
    "spanish": "__Minero De Cristal Estadísticas__"
    }

    return msg.get(language, "__Crystal Miner Statistics__")


def statsFieldEleven(language, crystalMinerMean, crystalMinerRate, crystalMinerTotal):
    msg = {
    "english": "**Avg. Crystal Miner:** *" + crystalMinerMean + "*\n**Crystal Miner Rate:** *" + crystalMinerRate + "%*\n**Crystal Miners Sum:** *" + crystalMinerTotal + "*",
    "spanish": "**Promedio De Minero De Cristal:** *" + crystalMinerMean + "*\n**Tasa De Minero De Cristal:** *" + crystalMinerRate + "%*\n**Total De Minero De Cristal:** *" + crystalMinerTotal + "*"
    }

    return msg.get(language, "**Avg. Crystal Miner:** *" + crystalMinerMean + "*\n**Crystal Miner Rate:** *" + crystalMinerRate + "%*\n**Crystal Miners Sum:** *" + crystalMinerTotal + "*")


def statsFieldTwelveTitle(language):
    msg = {
    "english": "__Gold Miner Statistics__",
    "spanish": "__Minero De Oro Estadísticas__"
    }

    return msg.get(language, "__Gold Miner Statistics__")


def statsFieldTwelve(language, goldMinerMean, goldMinerRate, goldMinerTotal, goldMinerMax):
    msg = {
    "english": "**Avg. Gold Miners:** *" + goldMinerMean + "*\n**Gold Miner Rate:** *" + goldMinerRate + "%*\n**Total Gold Miner:** *" + goldMinerTotal + "*\n**Most Gold Miners:** *" + goldMinerMax + "*",
    "spanish": "**Promedio De Minero De Oro:** *" + goldMinerMean + "*\n**Tasa De Minero De Oro:** *" + goldMinerRate + "%*\n**Total De Minero De Oro:** *" + goldMinerTotal + "*\n**Maximo Asesinatos Del Minero De Oro:** *" + goldMinerMax + "*"
    }

    return msg.get(language, "**Avg. Gold Miners:** *" + goldMinerMean + "*\n**Gold Miner Rate:** *" + goldMinerRate + "%*\n**Total Gold Miner:** *" + goldMinerTotal + "*\n**Most Gold Miners:** *" + goldMinerMax + "*")


def statsFieldThirteenTitle(language):
    msg = {
    "english": "__Kraken Statistics__",
    "spanish": "__Kraken Estadísticas__"
    }

    return msg.get(language, "Turrets Statistics")


def statsFieldThirteen(language, krakenMean, krakenRate, krakenTotal, krakenMax):
    msg = {
    "english": "**Avg. Krakens Captured:** *" + krakenMean + "*\n**Kraken Capture Rate:** *" + krakenRate + "%*\n**Total Kraken Captures:** *" + krakenTotal + "*\n**Maximum Amount Of Kraken Captures:** *" + krakenMax + "*",
    "spanish": "**Promedio De Capturas Del Kraken:** *" + krakenMean + "*\n**Tasa De Capturas Del Kraken:** *" + krakenRate + "%*\n**Total Capturas De Kraken:** *" + krakenTotal + "*\n**Máxima Capturas De Kraken:** *" + krakenMax + "*"
    }

    return msg.get(language, "**Avg. Krakens Captured:** *" + krakenMean + "*\n**Kraken Capture Rate:** *" + krakenRate + "%*\n**Total Kraken Captures:** *" + krakenTotal + "*\n**Maximum Amount Of Kraken Captures:** *" + krakenMax + "*")


def statsFieldFourteenTitle(language):
    msg = {
    "english": "__In-Game View__",
    "spanish": "__Vista De Juegos__"
    }

    return msg.get(language, "In-Game View__")


def statsFieldFourteen(language, killsMean, assistsMean, deathsMean, minionKillsMean, farmMean, turretsTotal, crystalMinersTotals, goldMinerTotals, krakenCapturesTotal):
    msg = {
    "english": "**Avg. Kills:** *" + killsMean + "*\n**Avg. Assists:** *" + assistsMean + "*\n**Avg. Deaths** *" + deathsMean + "*\n**Avg. Minions:** *" + minionKillsMean + "*\n**Avg. Farm:** *" + farmMean + "*\n**Turrets Destroyed:** *" + turretsTotal + "*\n**Crystal Miners Killed:** *" + crystalMinersTotals + "*\n**Gold Miners Killed:** *" + goldMinerTotals + "*\n**Krakens Captured:** *" + krakenCapturesTotal + "*",
    "spanish": "**Promedio De Asesinatos:** *" + killsMean + "*\n**Promedio De Asistencias:** *" + assistsMean + "*\n**Promedio De Muertes** *" + deathsMean + "*\n**Promedio De Asesinatos De Minion:** *" + minionKillsMean + "*\n**Promedio De Farm:** *" + farmMean + "*\n**Torres Destruidas:** *" + turretsTotal + "*\n**Mineros De Cristal Asesinados:** *" + crystalMinersTotals + "*\n**Mineros De Oro Asesinados:** *" + goldMinerTotals + "*\n**Kraken Capturados:** *" + krakenCapturesTotal + "*"
    }

    return msg.get(language, "**Average Kills:** *" + killsMean + "*\n**Average Assists:** *" + assistsMean + "*\n**Average Deaths** *" + deathsMean + "*\n**Average Minion Kills:** *" + minionKillsMean + "*\n**Average Farm:** *" + farmMean + "*\n**Turrets Destroyed:** *" + turretsTotal + "*\n**Crystal Miners Killed:** *" + crystalMinersTotals + "*\n**Gold Miners Killed:** *" + goldMinerTotals + "*\n**Kraken Captures:** *" + krakenCapturesTotal + "*")


def compareStatsLineOne(language, mention, ignOne, ignTwo, regionOne, regionTwo, gameMode, days):
    msg = {
    "english": mention + ", comparing stats of **" + ignOne + ", " + regionOne + ",** and **" + ignTwo + ", " + regionTwo + ",** for **" + gameMode + "** matches in the past **" + days + "** days... :eyes:",
    "spanish": mention + ", comparando las estadísticas de **" + ignOne + ", " + regionOne + ",** y **" + ignTwo + ", " + regionTwo + ",** para **" + gameMode + "** juegos en los últimos **" + days + "** días... :eyes:"
    }

    return msg.get(language, mention + ", comparing stats of **" + ignOne + ", " + regionOne + ",** and **" + ignTwo + ", " + regionTwo + ",** for **" + gameMode + "** matches in the past **" + days + "** days... :eyes:")


def compareStatsDescription(language, ignOne, ignTwo, regionOne, regionTwo, gameMode, days, samplesNum):
    msg = {
    "english": "Looking at stats of **" + ignOne + ", " + regionOne + ",** and **" + ignTwo + ", " + regionTwo + ",** in **" + gameMode + "** matches from the past **" + days + "** days.\nSampled **" + samplesNum + "** matches...",
    "spanish": "Mirando las estadísticas de **" + ignOne + ", " + regionOne + ",** y **" + ignTwo + ", " + regionTwo + ",** en **" + gameMode + "** partidos en los pasados **" + days + "** días.\n Muestreó de **" + samplesNum + "** coincidencias..."
    }

    return msg.get(language, "Looking at stats of **" + ignOne + ", " + regionOne + ",** and **" + ignTwo + ", " + regionTwo + ",** in **" + gameMode + "** matches from the past **" + days + "**.\nSampled **" + samplesNum + "** matches...")


def compareStatsFieldOneTitle(language, ign):
    msg = {
    "english": "__Latest Match Of " + ign + "__",
    "spanish": "__Último Partido De " + ign + " __"
    }

    return msg.get(language, "__Latest Match of " + ign + "__")


def compareStatsFieldOne(language, latestSkillTier, latestKarma, latestMatchDate, latestMatchGameMode):
    msg = {
    "english": "**ST:** *" + latestSkillTier + "* **|K:** *" + latestKarma + "*\n**Game Mode:** *" + latestMatchGameMode + "*\n**Date:** *" + latestMatchDate + "*",
    "spanish": "**ST:** *" + latestSkillTier + "* **|K:** *" + latestKarma + "*\n**Modo De Juego:** *" + latestMatchGameMode + "*\n**Fecha:** *" + latestMatchDate + "*"
    }

    return msg.get(language, "**ST:** *" + latestSkillTier + "* **|K:** *" + latestKarma + "*\n**Game Mode:** *" + latestMatchGameMode + "*\n**Date:** *" + latestMatchDate + "*")


def compareStatsFieldTwoTitle(language, ign):
    msg = {
    "english": "__General View Of " + ign + "__",
    "spanish": "__Vista General De " + ign + "__"
    }

    return msg.get(language, "__General View Of " + ign + "__")


def compareStatsFieldTwo(language, killsMean, killsTotal, assistsMean, assistsTotal, deathsMean, deathsTotal):
    msg = {
    "english": "**Avg. Kills:** *" + killsMean + "* **|Total Kills:** *" + killsTotal + "*\n**Avg. Assists:** *" + assistsMean + "* **|Total Assists:** *" + assistsTotal + "*\n**Avg. Deaths:** *" + deathsMean + "* **|Total Deaths:** *" + deathsTotal + "*",
    "spanish": "**Promedio De Asesinatos:** *" + killsMean + "* **|Total De Asesinatos:** *" + killsTotal + "*\n**Promedio De Asistencias:** *" + assistsMean + "* **|Total De Asistencias:** *" + assistsTotal + "*\n**Promedio De Muertes:** *" + deathsMean + "* **|Total De Muertes:** *" + deathsTotal + "*"
    }

    return msg.get(language, "**Average Kills:** *" + killsMean + "* **|Total Kills:** *" + killsTotal + "*\n**Average Assists:** *" + assistsMean + "* **|Total Assists:** *" + assistsTotal + "*\n**Average Deaths:** *" + deathsMean + "* **|Total Deaths:** *" + deathsTotal + "*")


def compareStatsFieldThreeTitle(language, ign):
    msg = {
    "english": "__In-Game View Of " + ign + "__",
    "spanish": "__Vista Dentro Del Juego " + ign + "__"
    }

    return msg.get(language, "__In-Game View Of " + ign + "__")


def compareStatsFieldThree(language, turretRate, crystalMinerRate, goldMinerRate, krakenRate):
    msg = {
    "english": "**Capturing All Turrets Rate:** *" + turretRate + "*\n**Crystal Miner Rate:** *" + crystalMinerRate + "*\n**Gold Miner Rate:** *" + goldMinerRate + "*\n**Kraken Capture Rate:** *" + krakenRate + "*\n",
    "spanish": "**Captura De Todas Las Torres:** *" + turretRate + "*\n**Tase De Minero De Cristal:** *" + crystalMinerRate + "*\n**Tase De Minero De Gold:** *" + goldMinerRate + "*\n**Captura Del Kraken:** *" + krakenRate + "*\n"
    }

    return msg.get(language, "**Capturing All Turrets Rate:** *" + turretRate + "*\n**Killing Crystal Miner Rate:** *" + crystalMinerRate + "*\n**Killing Gold Miner Rate:** *" + goldMinerRate + "*\n**Kraken Capture Rate:** *" + krakenRate + "*\n")


def compareStatsFieldFourTitle(language, ign):
    msg = {
    "english": "__Game Statistics Of" + ign + "__",
    "spanish": "__Estadísticas De Juegos De " + ign + "__"
    }

    return msg.get(language, "__Game Statistics Of" + ign + "__")


def compareStatsFieldFour(language, winRate, afkRate):
    msg = {
    "english": "**Win Rate:** *" + winRate + "* **|AFK Rate:** *" + afkRate + "*",
    "spanish": "**Tasa de Ganancia:** *" + winRate + "* **|Tase de AFK:** *" + afkRate + "*"
    }

    return msg.get(language, "**Win Rate:** *" + winRate + "* **|AFK Rate:** *" + afkRate + "*")


def compareStatsFieldFiveTitle(language, ignOne, ignTwo):
    msg = {
    "english": "__" + ignOne + " vs " + ignTwo + "__",
    "spanish": "__" + ignOne + " vs "+ ignTwo + "__"
    }

    return msg.get(language, "__" + ignOne + " vs " + ignTwo + "__")


def compareStatsFieldFive(language, ignOne, ignTwo, rate):
    msg = {
    "english": "**" + ignOne + "** has a **" + rate + "%** of beating **" + ignTwo + "**",
    "spanish": "**" + ignOne + "** tiene un **" + rate + "%** de probabilidades de vencer a **" + ignTwo + "**"
    }

    return msg.get(language, "**" + ignOne + "** has a **" + rate + "%** of beating **" + ignTwo + "**")


def latestLineOne(language, mention, gameMode, ign, region):
    msg = {
    "english": mention + ", looking for the latest **" + gameMode + "** match of **" + ign + "** in the **" + region + "**... :eyes:",
    "spanish": mention + ", buscando el último juego **" + gameMode + "** de **" + ign + "** en la **" + region + "**... :eyes:"
    }

    return msg.get(language, mention + ", looking for the latest **" + gameMode + "** match of **" + ign + "** in the **" + region + "**... :eyes:")

def latestDescription(language, ign, region, gameMode, matchId):
    msg = {
    "english": "Looking at the latest **" + gameMode + "** match of **" + ign + "** in **" + region + "** region.\n**Match ID:** *" + matchId + "*",
    "spanish": "Mirando el último **" + gameMode + "** partido de **" + ign + "** en la **" + region + "** región.\n**ID Del Partido:** *" + matchId + "*"
    }

    return msg.get(language, "Looking at the latest **" + gameMode + "** match of **" + ign + "** in **" + region + "** region.\n**Match ID:** *" + matchId + "*")


def latestFieldOneTitle(language, title):
    msg = {
    "english": "left",
    "spanish": "izquierda"
    }

    title.replace("left", msg.get(language, "left"))

    msg = {
    "english": "right",
    "spanish": "derecho"
    }

    title.replace("right", msg.get(language, "right"))

    msg = {
    "english": "Winner",
    "spanish": "Ganador"
    }

    title.replace("Winner", msg.get(language, "Winner"))

    msg = {
    "english": "True",
    "spanish": "Cierto",
    }

    title.replace("True", msg.get(language, "True"))

    msg = {
    "english": "False",
    "spanish": "Falso",
    }

    title.replace("False", msg.get(language, "False"))

    return title


def playerMatchInfo(language, skillTier, karma, kills, assists, deaths, farm, actor, items):
    msg = {
    "english": "**" + actor + "** | **" + skillTier + "** | **" + karma + "** *|K/D/A:* **" + kills + "** */* **" + deaths + "** */* **" + assists + "** *-Farm:* **" + farm + "**\n**Build:** " + items,
    "spanish": "**" + actor + "** | **" + skillTier + "** | **" + karma + "** *|K/D/A:* **" + kills + "** */* **" + deaths + "** */* **" + assists + "** *-Farm:* **" + farm + "**\n**Equipo:** " + items
    }

    return msg.get(language, "**" + actor + "** | **" + skillTier + "** | **" + karma + "** *|K/D/A:* **" + kills + "** */* **" + deaths + "** */* **" + assists + "** *-Farm:* **" + farm + "**\n**Build:** " + items)


def playerMatchInfoCompact(language, kills, assists, deaths, farm, actor):
    msg = {
    "english": "**" + actor + "** |K/D/A: **" + kills + "** / **" + deaths + "** / **" + assists + "** *- Farm:* **" + farm + "**",
    "spanish": "**" + actor + "** |K/D/A: **" + kills + "** / **" + deaths + "** / **" + assists + "** *- Farm:* **" + farm + "**"
    }

    return msg.get(language, "**" + actor + "** |K/D/A: **" + kills + "** / **" + deaths + "** / **" + assists + "** *- Farm:* **" + farm + "**")


def playerTelemetryMatchInfo(language, ign, skillTier, karma, kills, assists, deaths, farm, actor, items):
    msg = {
    "english": "**" + ign + "** | **" + actor + "** | **" + skillTier + "** | **" + karma + "** *|K/D/A:* **" + kills + "** */* **" + deaths + "** */* **" + assists + "** *- Farm:* **" + farm + "**\n**Build:** " + items,
    "spanish": "**" + ign + "** | **" + actor + "** | **" + skillTier + "** | **" + karma + "** *|K/D/A:* **" + kills + "** */* **" + deaths + "** */* **" + assists + "** *- Farm:* **" + farm + "**\n**Equipo:** " + items
    }

    return msg.get(language, "**" + ign + "** | **" + actor + "** | **" + skillTier + "** | **" + karma + "** *|K/D/A:* **" + kills + "** */* **" + deaths + "** */* **" + assists + "** *-Farm:* **" + farm + "**\n**Build:** " + items)


def playerTelemetryMatchInfoCompact(language, ign, kills, assists, deaths, farm, actor):
    msg = {
    "english": "**" + ign + "** | **" + actor + "** |K/D/A: **" + kills + "** / **" + deaths + "** / **" + assists + "** - Farm: **" + farm + "**",
    "spanish": "**" + ign + "** | **" + actor + "** |K/D/A: **" + kills + "** / **" + deaths + "** / **" + assists + "** - Farm: **" + farm + "**"
    }

    return msg.get(language, "**" + ign + "** | **" + actor + "** |K/D/A: **" + kills + "** / **" + deaths + "** / **" + assists + "** - Farm: **" + farm + "**")


def matchLineOne(language, mention, matchId, region):
    msg = {
    "english": mention + ", searching for match **" + matchId + "** in the **" + region + "**... :eyes:",
    "spanish": mention + ", buscando el partido **" + matchId + "** en la **" + region + "**... :eyes:"
    }

    return msg.get(language, mention + ", searching for match **" + matchId + "** in the **" + region + "**... :eyes:")


def matchDescription(language, matchId):
    msg = {
    "english": "Looking at **" + matchId + "** match.",
    "spanish": "Mirando el **" + matchId + "** partido"
    }

    return msg.get(language, "Looking at **" + matchId + "** match.")

def matchesTitle(language, ign, region, gameMode):
    msg = {
    "english": str(gameMode).title() + " match of " + ign + ", " + region,
    "spanish": str(gameMode).title() + " partido de " + ign + ", " + region
    }

    return msg.get(language, str(gameMode).title() + " match of " + ign + ", " + region)

def matchesDescription(language, matchDate, matchId, pageNum, pagesMax):
    msg = {
    "english": "**Match Date:** *" + matchDate + "*\n**Match ID:** *" + matchId + "*\nMatch *" + pageNum + "* of *" + pagesMax + "*",
    "spanish": "**Fecha Del Partido:** *" + matchDate + "*\n**ID Del Paritdo:** *" + matchId + "*\nPartido *" + pageNum + "* de *" + pagesMax + "*"
    }

    return msg.get(language, "**Match Date:** *" + matchDate + "*\n**Match ID:** *" + matchId + "\nMatch *" + pageNum + "* of *" + pagesMax + "*")


def matchDescriptionOne(language, matchDate, matchId):
    msg = {
    "english": "**Match Date:** *" + matchDate + "*\n**Match ID:** *" + matchId + "*",
    "spanish": "**Fecha Del Partido:** *" + matchDate + "*\n**ID Del Paritdo:** *" + matchId + "*"
    }

    return msg.get(language, "**Match Date:** *" + matchDate + "*\n**Match ID:** *" + matchId + "*")


def matchesLineOne(language, mention, ign, region, gameMode):
    msg = {
    "english": mention + ", looking for recent matches of **" + ign + "** in the **" + region + "** region about **" + gameMode + "** matches... :eyes:",
    "spanish": mention + ", buscando reciente partidos de **" + ign + "** en la **" + region + "** región sobre **" + gameMode + "** partidos... :eyes:"
    }

    return msg.get(language, mention + ", looking for recent matches of **" + ign + "** in the **" + region + "** region about **" + gameMode + "** matches... :eyes:")

def telemetryLineOne(language, mention):
    msg = {
    "english": mention + "**, processing match's telemetry data...**",
    "spanish": mention + "**, procesando los datos de telemetría del partido...**"
    }

    return msg.get(language, mention + "**, processing match's telemetry data...**")

def telemetryLineTwo(language, mention):
    msg = {
    "english": mention + "**, you aren't viewing a valid minute of the match...** :sweat_smile:",
    "spanish": mention + "**, no estás viendo un minuto válido del partido...** :sweat_smile:"
    }

    return msg.get(language, mention + "**, you aren't viewing a valid minute of the match...** :sweat_smile:")

def telemetryLineThree(language, mention, minute, matchId):
    msg = {
    "english": mention + "**, done dictating events** from minute **" + minute + "** in match, **" + matchId + "**... :blush:",
    "spanish": mention + "**, hecho dictando eventos** de minuto **" + minute + "** en el partido, **" + matchId + "**... :blush:"
    }

    return msg.get(language, mention + "**, done dictating events** from minute **" + minute + "** in match, **" + matchId + "**... :blush:")

def telemetryTitle(language, matchId):
    msg={
    "english": "Telemetry for " + matchId,
    "spanish": "Telemetría para" + matchId
    }

    return msg.get(language, "Telemetry for " + matchId)


def telemetryDescription(language, ign, sectionNum, sectionMax, eventMax, gameMode, matchId):
    msg = {
    "english": "Looking at **" + ign + "**. At **" + sectionNum + " , " + eventMax + "** events, of **" + sectionMax + "** sections in a **" + gameMode + "** match.\nMatch ID: *" + matchId + "*",
    "spanish": "Mirando a **" + ign + "**. En la **" + sectionNum + " , " + eventMax + "** eventos, de **" + sectionMax + "** secciones, en un **" + gameMode + "** partido.\nID del partido: *" + matchId + "*"
    }

    return msg.get(language, "Looking at **" + ign + "**. At **" + sectionNum + " , " + eventMax + "** events, of **" + sectionMax + "** sections in a **" + gameMode + "** match.\nMatch ID: *" + matchId + "*")


def telemetryHeroKillHero(language, teamEmoji, actorOne, teamOne, actorTwo, teamTwo):
    msg = {
    "english": ":skull: " + teamEmoji + " **" + actorOne + " (" + teamOne + ")** killed **" + actorTwo + " (" + teamTwo + ")**\n",
    "spanish": ":skull: " + teamEmoji + " **" + actorOne + " (" + teamOne + ")** asesino **" + actorTwo + " (" + teamTwo + ")**\n"
    }

    return msg.get(language, ":skull: " + teamEmoji + " **" + actorOne + " (" + teamOne + ")** killed **" + actorTwo + " (" + teamTwo + ")**\n")


def telemetryHeroKillTurret(language, teamEmoji, actor, team):
    msg = {
    "english": ":fire: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed a **enemy turret**\n",
    "spanish": ":fire: " + teamEmoji + " **" + actor + " (" + team + ")** ha destruido una **torreta enemiga**\n"
    }

    return msg.get(language, ":fire: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed a **enemy turret**\n")


def telemetryHeroKillGoldMiner(language, teamEmoji, actor, team):
    msg = {
    "english": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **gold miner**\n",
    "spanish": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** ha matado al **minero de oro**\n"
    }

    return msg.get(language, ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **gold miner**\n")


def telemetryHeroKillCrystalMiner(language, teamEmoji, actor, team):
    msg = {
    "english": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy crystal miner**\n",
    "spanish": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** ha matado al **minero de cristal enemigo**\n"
    }

    return msg.get(language, ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy crystal miner**\n")


def telemetryHeroCaptureKraken(language, teamEmoji, actor, team):
    msg = {
    "english": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has captured the **kraken**\n",
    "spanish": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** ha capturado el **kraken**\n"
    }

    return msg.get(language, ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has captured the **kraken**\n")


def telemetryHeroKillKraken(language, teamEmoji, actor, team):
    msg = {
    "english": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy kraken**\n",
    "spanish": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** ha matado al **kraken enemigo**\n"
    }

    return msg.get(language, ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy kraken**\n")


def telemetryHeroKillVainCrystal(language, teamEmoji, actor, team):
    msg = {
    "english": ":gem: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed the **enemy crystal**\n",
    "spanish": ":gem: " + teamEmoji + " **" + actor + " (" + team + ")** ha destruido el **cristal enemigo**\n"
    }

    return msg.get(language, ":gem: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed the **enemy crystal**\n")


def telemetryNpcKillHero(language, teamEmoji, actorOne, teamOne, actorTwo, teamTwo):
    msg = {
    "english": ":skull: " + teamEmoji + " **" + actorOne + " (" + teamOne + ")** has killed **" + actorTwo + " (" + teamTwo + ")**\n",
    "spanish": ":skull: " + teamEmoji + " **" + actorOne + " (" + teamOne + ")** ha matado **" + actorTwo + " (" + teamTwo + ")**\n"
    }

    return msg.get(language, ":skull: " + teamEmoji + " **" + actorOne + " (" + teamOne + ")** has killed **" + actorTwo + " (" + teamTwo + ")**\n")


def telemetryNpcKillTurret(language, teamEmoji, actor, team):
    msg = {
    "english": ":fire: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed a **enemy turret**\n",
    "spanish": ":fire: " + teamEmoji + " **" +actor + " (" + team + ")** ha destruido una **torreta enemiga**\n"
    }

    return msg.get(language, ":fire: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed a **enemy turret**\n")


def telemetryNpcKillGoldMiner(language, teamEmoji, actor, team):
    msg = {
    "english": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **gold miner**\n",
    "spanish": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** ha matado al **minero de oro**\n"
    }

    return msg.get(language, ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **gold miner**\n")


def telemetryNpcKillCrystalMiner(language, teamEmoji, actor, team):
    msg = {
    "english": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy crystal miner**\n",
    "spanish": ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** ha matado al **miner de cristal del enemigo**\n"
    }

    return msg.get(language, ":pick: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy crystal miner**\n")


def telemetryNpcCapturedKraken(language, teamEmoji, actor, team):
    msg = {
    "english": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has captured the **kraken**\n",
    "spanish": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** Ha capturado el **kraken**\n"
    }

    return msg.get(language, ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has captured the **kraken**\n")


def telemetryNpcKillKraken(language, teamEmoji, actor, team):
    msg = {
    "english": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy kraken**\n",
    "spanish": ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** ha matado el **kraken del enemigo**\n"
    }

    return msg.get(language, ":japanese_ogre: " + teamEmoji + " **" + actor + " (" + team + ")** has killed the **enemy kraken**\n")


def telemetryNpcKillVainCrystal(language, teamEmoji, actor, team):
    msg = {
    "english": ":gem: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed the **enemies crystal**\n",
    "spanish": ":gem: " + teamEmoji + " **" + actor + " (" + team + ")** ha destruido el **cristal enemigo**\n"
    }

    return msg.get(language, ":gem: " + teamEmoji + " **" + actor + " (" + team + ")** has destroyed the **enemies crystal**\n")


def telemetryHeroLevelUp(language, teamEmoji, actor, team, level):
    msg = {
    "english": ":arrow_up: " + teamEmoji + " **" + actor + " (" + team + ")** has **leveled up to " + level + "**\n",
    "spanish": ":arrow_up: " + teamEmoji + " **" + actor + " (" + team + ")** se ha **nivelado a " + level + "**\n"
    }

    return msg.get(language, ":arrow_up: " + teamEmoji + " **" + actor + " (" + team + ")** has **leveled up to " + level + "**\n")


def telemetryHeroAbilityUse(language, teamEmoji, actor, team, ability):
    msg = {
    "english": ":star: " + teamEmoji + " **" + actor + " (" + team + ")** has used the **" + ability + " hero ability**\n",
    "spanish": ":star: " + teamEmoji + " **" + actor + " (" + team + ")** ha utilizado **" + ability + " habilidad de héroe**\n"
    }

    return msg.get(language, ":star: " + teamEmoji + " **" + actor + " (" + team + ")** has used the **" + ability + " hero ability**\n")


def telemetryItemAbilityUse(language, teamEmoji, actor, team, ability):
    msg = {
    "english": ":purse: " + teamEmoji + " **" + actor + " (" + team + ")** has used the **" + ability + " item ability**\n",
    "spanish": ":purse: " + teamEmoji + " **" + actor + " (" + team + ")** ha utilizado **" + ability + " habilidad de artículo**\n"
    }

    return msg.get(language, ":purse: " + teamEmoji + " **" + actor + " (" + team + ")** has used the **" + ability + " item ability**\n")


def telemetrySellItem(language, teamEmoji, actor, team, item):
    msg = {
    "english": ":regional_indicator_b: " + teamEmoji + " **" + actor + " (" + team + ")** has sold **" + item + "**\n",
    "spanish": ":regional_indicator_b: " + teamEmoji + " **" + actor + " (" + team + ")** ha vendido **" + item + "**\n"
    }

    return msg.get(language, ":regional_indicator_b: " + teamEmoji + " **" + actor + " (" + team + ")** has sold **" + item + "**\n")


def telemetryBuyItem(language, teamEmoji, actor, team, item):
    msg = {
    "english": ":regional_indicator_s: " + teamEmoji + " **" + actor + " (" + team + ")** has bought **" + item + "**\n",
    "spanish": ":regional_indicator_s: " + teamEmoji + " **" + actor + " (" + team + ")** ha comprado **" + item + "**\n"
    }

    return msg.get(language, ":regional_indicator_s: " + teamEmoji + " **" + actor + " (" + team + ")** has bought **" + item + "**\n")


def telemetryBanHero(language, teamEmoji, actor, team):
    msg = {
    "english": ":negative_squared_cross_mark: " + teamEmoji + " **" + team + "**  has banned **" + actor + "**\n",
    "spanish": ":negative_squared_cross_mark: " + teamEmoji + " **" + team + "** ha prohibido **" + actor + "**\n"
    }

    return msg.get(language, ":negative_squared_cross_mark: " + teamEmoji + " **" + team + "**  has banned **" + actor + "**\n")


def telemetrySelectHero(language, teamEmoji, player, actor):
    msg = {
    "english": ":raising_hand: " + teamEmoji + " **" + player + "** has selected **" + actor + "**\n",
    "spanish": ":raising_hand: " + teamEmoji + " **" + player + "** ha seleccionado **" + actor + "**\n"
    }

    return msg.get(language, ":raising_hand: " + teamEmoji + " **" + player + "** has selected **" + actor + "**\n")


def telemetrySelectSkin(language, teamEmoji, actor, skin):
    msg = {
    "english": ":dress: " + teamEmoji + " **" + actor + "** has selected the **" + skin + "** skin\n",
    "spanish": ":dress: " + teamEmoji + " **" + actor + "** Ha seleccionado el **" + skin + "** piel\n"
    }

    return msg.get(language, ":dress: " + teamEmoji + " **" + actor + "** has selected the **" + skin + "** skin\n")


def telemetrySwapHero(language, teamEmoji, actorOne, actorTwo):
    msg = {
    "english": ":left_right_arrow: " + teamEmoji + " **" + actorOne + "** and **" + actorTwo + "** have swapped heroes\n",
    "spanish": ":left_right_arrow: " + teamEmoji + " **" + actorOne + "** y **" + actorTwo + "** han cambiado héroes\n"
    }

    return msg.get(language, ":left_right_arrow: " + teamEmoji + " **" + actorOne + "** and **" + actorTwo + "** have swapped heroes\n")


def topListLineOne(language, mention, topElements, ign, region, gameMode, days):
    msg = {
    "english": mention + ", looking at top **" + topElements + "** in **" + gameMode + "** matches of **" + ign + "** in the **" + region + "** from the past **" + days + "**... :eyes:",
    "spanish": mention + ", mirando los elementos superiores **" + topElements + "** en **" + gameMode + " partidos de **" + ign + "** en la región **" + region + "** en los últimos **" + days + " días... :eyes:"
    }

    return msg.get(language, mention + ", looking at top **" + topElements + "** in **" + gameMode + "** matches for **" + ign + "** in the **" + region + "** from the past **" + days + "**... :eyes:")


def topListDescription(language, ign, region, topElements):
    msg = {
    "english": "Looking at the top **" + topElements + "** of **" + ign + "** in the **" + region + "** region.",
    "spanish": "Mirando los elementos superiores **" + topElements + "** de **" + ign + "** en la **" + region + "** región."
    }

    return msg.get(language, "Looking at the top **" + topElements + "** of **" + ign + "** in the **" + region + "** region.")


def matchGeneralViewTitle(language):
    msg = {
    "english": "__General View__",
    "spanish": "__Vista General__"
    }

    return msg.get(language, "__General View__")


def matchGeneralView(language, gold, kills, aces, turrets, krakens):
    msg = {
    "english": "**Gold:** *" + gold + "* **|Kills:** *" + kills + "* **|Aces:** *" + aces + "* **|Turrets:** *" + turrets + "* **|Krakens Captured:** *" + krakens + "*",
    "spanish": "**Oro:** *" + gold + "* **|Asessinatos:** *" + kills + "** **Ases:** *" + aces + "* **|Torretas:** *" + turrets + "* **|Krakens Capturados:* **" + krakens + "*"
    }

    return msg.get(language, "**Gold:** *" + gold + "* **|Kills:** *" + kills + "* **|Aces:** *" + aces + "* **|Turrets:** *" + turrets + "* **|Krakens Captured:** *" + krakens + "*")


def leaderboardFilterOneNotReal(language, mention, filterOne):
    msg = {
    "english": mention + ", **" + filterOne + "** isn't a **valid first filter**... :sweat_smile:",
    "spanish": mention + ", **" + filterOne + "** no es un primer filtro válido.. :sweat_smile:"
    }

    return msg.get(language, mention + ", **" + filterOne + "** isn't a **valid first filter**... :sweat_smile:")


def leaderboardFilterTwoNotReal(language, mention, filterTwo):
    msg = {
    "english": mention + ", **" + filterTwo + "** isn't a **valid second filter**... :sweat_smile:",
    "spanish": mention + ", **" + filterTwo + "** no es un segundo filtro válido.. :sweat_smile:"
    }

    return msg.get(language, mention + ", **" + filterTwo + "** isn't a **valid second filter**... :sweat_smile:")


def leaderboardLineOne(language, mention, filterOne, filterTwo, playerName):
    msg = {
    "english": mention + ", looking at **" + filterOne + " " + filterTwo + "** for **" + playerName + "**... :eyes:",
    "spanish": mention + ", mirando a **" + filterOne + " " + filterTwo + "** para **" + playerName + "**... :eyes:"
    }

    return msg.get(language, mention + ", looking at **" + filterOne + " " + filterTwo + "** for **" + playerName + "**... :eyes:")


def leaderboardDescription(language, filterOne, filterTwo, playerName):
    msg = {
    "english": "Looking at **" + filterOne + " " + filterTwo + "** for **" + playerName + "**.",
    "spanish": "Mirando a **" + filterOne + " " + filterTwo + "** para **" + playerName + "**."
    }

    return msg.get(language, "Looking at **" + filterOne + " " + filterTwo + "** for **" + playerName + "**.")


def gifLineOne(language, mention):
    msg = {
    "english": mention + ", generating match's GIF... :eyes:",
    "spanish": mention + ", generando GIF del partido... :eyes:"
    }

    return msg.get(language, mention + ", generating match's GIF... :eyes:")


def gifLineTwo(language, mention):
    msg = {
    "english": mention + ", sending match's GIF, this may take a while... :stuck_out_tongue:",
    "spanish": mention  + ", enviando GIF del partido, esto podría tomar un tiempo... :stuck_out_tongue:"
    }

    return msg.get(language, mention + ", sending match's GIF, this may take a while... :stuck_out_tongue:")


def gifLineThree(language, mention):
    msg = {
    "english": mention + ", you took too long to respond :confused:",
    "spanish": mention + ", tomó demasiado tiempo para responder :confused:"
    }

    return msg.get(language, mention + ", you took too long to respond :confused:")


def verifyLineOne(language, mention, ign, region):
    msg = {
    "english": mention + ", seeing if requirements have been meet to verify **" + ign + "**, **" + region + "**... :eyes:",
    "spanish": mention + ", viendo si los requisitos se han cumplido para verificar a **"+ ign + "**, **" + region + "**... :eyes:"
    }

    return msg.get(language, mention + ", seeing if requirements have been meet to verify **" + ign + "**, **" + region + "**... :eyes:")


def verifyLineTwo(language, mention, ign, region):
    msg = {
    "english": mention + ", no **blitz** matches on **" + ign + "**, **" + region + "** has been found... :sweat_smile:",
    "spanish": mention + ", no se han encontrado partidos de **blitz** de **" + ign + "**, **" + region + "**... :sweat_smile:"
    }

    return msg.get(language, mention + ", no **blitz** matches on **" + ign + "**, **" + region + "** has been found... :sweat_smile:")


def verifyLineThree(language, mention, ign, region):
    msg = {
    "english": mention + ", **" + ign + "**, **" + region + "**, has been verified to __**this account**__! :hugging:",
    "spanish": mention + ", **" + ign + "**, **" + region + "**, se ha verificado en __**esta cuenta**__! :hugging:"
    }

    return msg.get(language, mention + ", **" + ign + "**, **" + region + "**, has been verified to __**this account**__! :hugging:")


def verifyLineFour(language, mention, ign):
    msg = {
    "english": mention + ", this ign, **" + ign + "**, has all ready been verified to another discord account!\nNeed help? Talk to the devs at __**" + str(config.bot_server) + "**__!",
    "spanish": mention + ", este ign, **" + ign + "**, se ha sido verificado a otra cuenta de Discord!\nNecesita ayuda? Hable con los desarrolladores en ___**" + str(config.bot_server) + "**__!"
    }

    return msg.get(language, mention + ", this ign, **" + ign + "**, has all ready been verified to another discord account!\nNeed help? Talk to the devs at __**" + str(config.bot_server) + "**__!")


def verifyLineFive(language, mention):
    msg = {
    "english": mention + ", fixing everything up for you... :eyes:",
    "spanish": mention + ", arreglando todo para ti... :eyes:"
    }

    return msg.get(language, mention + ", fixing everything up for you... :eyes:")


def verifyLineSix(language, ign, region, items, prefix):
    msg = {
    "english": "Buy the following items at the beginning of **" + ign + "**, **" + region + "**, __**next blitz**__ match, order does not matter; you can sell these items right after buying them for the gold.\n**" + items + "**\nAfter finishing your blitz match immediately do the **" + prefix + "verify** command to check if you've been verified!\nEnter **" + prefix + "verify $cancel** if wish to cancel your verification!",
    "spanish": "Compre los siguientes elementos al principio del __**siguiente juego de blitz**__ de **" + ign + "**, **" + region + "**, no tiene que comprarlos en ningún orden, puede vender estos artículos inmediatamente después de comprarlos.\n**" + items + "**\nDespués de finalizar su partida de blitz haga inmediatamente el comando **"+ prefix +" verify** para verificar si ha sido verificado!\nIngrese ** "+ prefix +"verify $cancel ** si desea cancelar su verificación! "
    }

    return msg.get(language, "Buy the following items at the beginning of **" + ign + "**, **" + region + "**, __**next blitz**__ match, order does not matter; you can sell these items right after buying them for the gold.\n**" + items + "**\nAfter finishing your blitz match immediately do the **" + prefix + "verify** command to check if you've been verified!\nEnter **" + prefix + "verify $cancel** if wish to cancel your verification!")


def verifyLineSeven(language, mention):
    msg = {
    "english": mention + ", you took too long to verify!",
    "spanish": mention + ", tomaste demasiado tiempo para verificar!"
    }

    return msg.get(language, mention + ", you took too long to verify!")

def verifyLineEight(language, mention):
    msg = {
    "english": mention + ", your **verification process** has been **cancelled**! :eyes:",
    "spanish": mention + ",  su **proceso de verificación** ha sido **cancelado**! :eyes:"
    }

    return msg.get(language, mention + ", your **verification process** has been **cancelled**! :eyes:")

def profileAdded(language, mention, profileType):
    msg ={
    "english": mention + ", your **" + profileType + " profile** has been added! :hugging:",
    "spanish": mention + ", tu **" + profileType + " perfil** se ha añadido! :hugging:"
    }

    return msg.get(language, mention + ", your **" + profileType + " profile** has been added! :hugging:")

def profileNotAdded(language, mention, profileType):
    msg ={
    "english": mention + ", your **" + profileType + " profile** has not been added! :confused:",
    "spanish": mention + ", tu **" + profileType + " perfil** no se ha añadido! :confused:"
    }

    return msg.get(language, mention + ", your **" + profileType + " profile** has not been added! :confused:")

def profileRemoving(language, mention, profileType):
    msg = {
        "english": mention + ", removing your **" + profileType + " profile**... :eyes:",
        "spanish": mention + ", quitado tu **perfil de " + profileType + "**... :eyes:"
    }

    return msg.get(language, mention + ", removing your **" + profileType + " profile**... :eyes:")

def profileRemoved(language, mention, profileType):
    msg ={
    "english": mention + ", your **" + profileType + " profile** has been removed! :hugging:",
    "spanish": mention + ", tu **" + profileType + " prefil** se ha eliminado! :hugging:"
    }

    return msg.get(language, mention + ", your **" + profileType + " profile** has been removed! :hugging:")

def profileNotRemoved(language, mention, profileType):
    msg ={
    "english": mention + ", your **" + profileType + " profile** has not been removed! :confused:",
    "spanish": mention + ", tu **" + profileType + " prefil** no ha sido eliminado! :confused:"
    }

    return msg.get(language, mention + ", your **" + profileType + " profile** has not been removed! :confused:")

def profileSectionUpdated(language, mention, section, profileType):
    msg = {
    "english": mention + ", **" + section + "** has been updated in your **" + profileType + " profile**! :hugging:",
    "spanish": mention + ", **" + section + "** se ha actualizado en tu **" + profileType + " perfil**! :hugging:"
    }

    return msg.get(language, mention + ", **" + section + "** has been updated in your **" + profileType + " profile**! :hugging:")

def profileSectionNotUpdated(language, mention, section, profileType):
    msg = {
    "english": mention + ", **" + section + "** has not been updated in your **" + profileType + " profile**! :confused:",
    "spanish": mention + ", **" + section + "** no se ha actualizado en tu **" + profileType + " perfil**! :confused:"
    }

    return msg.get(language, mention + ", **" + section + "** has not been updated in your **" + profileType + " profile**! :confused:")

def settingUpProfile(language, mention, profileType):
    msg = {
    "english": mention + ", setting up your **" + profileType + " profile**... :eyes: ",
    "spanish": mention + ", configurando su **perfil de " + profileType + "**.. :eyes:"
    }

    return msg.get(language, mention + ", setting up your **" + profileType + " profile**... :eyes: ")

def settingUpProfileErrorLineOne(language, mention, profileType):
    msg = {
        "english": mention + ", sorry an **error** has **occurred** while setting up your **" + profileType + " profile**... :sweat_smile:",
        "spanish": mention + ", lo sentimos un **error** se ha producido al configurar su **perfil de " + profileType + "**... :sweat_smile:"
    }

    return msg.get(language, mention + ", sorry an **error** has **occurred** while setting up your **" + profileType + " profile**... :sweat_smile:")

def settingUpProfileErrorLineTwo(language, mention, error):
    msg = {
        "english": mention + ", a **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + error + "```",
        "spanish": mention + ", un **informe** no fue enviado con éxito a los desarrolladores! :cold_sweat:\n```" + error + "```"
    }

    return msg.get(language, mention + ", a **report** wasn't successfully sent to the developers! :cold_sweat:\n```" + error + "```")

def settingUpProfileErrorLineThree(language, mention):
    msg = {
        "english": mention + ", a **report** has been successfully sent to the developers! :hugging:",
        "spanish": mention + ", un **informe** ha sido enviado con éxito a los desarrolladores! :hugging:"
    }

    return msg.get(language, mention + ", a **report** has been successfully sent to the developers! :hugging:")

def settingUpProfileDone(language, mention, profileType):
    msg = {
    "english": mention + ", your **" + profileType + " profile** has been setup! :hugging:",
    "spanish": mention + ", tu **perfil de " + profileType + "** se ha configurado! :hugging:"
    }

    return msg.get(language, mention + ", your **" + profileType + " profile** has been setup! :hugging:")

def settingUpProfileNotDone(language, mention, profileType):
    msg = {
    "english": mention + ", your **" + profileType + " profile** has not been setup! :confused:",
    "spanish": mention + ", tu **perfil de " + profileType + "** no se ha configurado! :confused:"
    }

    return msg.get(language, mention + ", your **" + profileType + " profile** has been setup! :confused:")

def verifyReqNot(language, mention, ign, region):
    msg = {
    "english": mention + ", you haven't meet the requirements to verify **" + ign + "**, **" + region + "**, please buy what you need!... :cold_sweat:",
    "spanish": mention + ", no ha cumplido los requisitos para verificar **" + ign + "**, **" + region + "**, por favor, compre lo que necesita!... :cold_sweat:"
    }

    return msg.get(language, mention + ", you haven't meet the requirements to verify **" + ign + "**, **" + region + "**, please buy what you need to buy!... :cold_sweat:")

# def telemetry(language, teamEmoji, ):
#     msg = {
#     "english": "",
#     "spanish": ""
#     }
#
#     return msg.get(language, "")
