import config

# Common Lines:
def notInServer(language):
    msg = {
    "english": "You can't use **server commands** outside a **server**... :stuck_out_tongue:",
    "spanish": "No puede utilizar **comandos de servidor** fuera de un **servidor** ...: stuck_out_tongue:"
    }

    return msg.get(language, "You can't use **server commands** outside a **server**... :stuck_out_tongue:")


def notAuthorized(language, server_name, command_name):
    msg = {
    "english": "You **aren't** an **administrator** to the server, **" + server_name + "**, so you **don't have access to** the **" + command_name + " commmand**... :sweat_smile:",
    "spanish": "**No eres administrador** del servidor, **" + server_name + "**, asique no tienes acesso al **commando " + command_name + "**... :sweat_smile:"
    }

    return msg.get(language, "You **aren't** an **administrator** to the server, **" + server_name + "**, so you **don't have access to** the **" + command_name + " commmand**... :sweat_smile:")

def notLanguage(language, new_language):
    msg = {
    "english": "**" + new_language + "** isn't a **supported language**... :sweat_smile:",
    "spanish": "**" + new_language + "** no es un **lenguaje soportado**... :sweat_smile:"
    }

    return msg.get(language, "**" + language + "** isn't a **supported language**... :sweat_smile:")

def notVgGuildName(language, name):
    msg = {
    "english": "**" + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:",
    "spanish": "**" + name + "** no es un **válido** nombre para un **gremio de Vainglory** ...: sweat_smile:"
    }

    return msg.get(language, "**" + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:")

def notVgGuildTag(language, tag):
    msg = {
    "english": "**" + tag + "** isn't a valid **Vainglory guild tag**... :sweat_smile:",
    "spanish": "**" + tag + "** no es un **válida** etiqueta para un **gremio de Vainglory**... :sweat_smile:"
    }

    return msg.get(language, "**" + tag + "** isn't a valid **Vainglory team tag**... :sweat_smile:")

def notVgTeamName(language, name):
    msg = {
    "english": "**" + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:",
    "spanish": "**" + name + "** no es un **válido** nombre para un **equipo de Vainglory** ...: sweat_smile:"
    }

    return msg.get(language, "**" + name + "** isn't a valid **Vainglory guild name**... :sweat_smile:")

def notVgTeamTag(language, tag):
    msg = {
    "english": "**" + tag + "** isn't a valid **Vainglory guild tag**... :sweat_smile:",
    "spanish": "**" + tag + "** no es un **válida** etiqueta para una **equipo de Vainglory**... :sweat_smile:"
    }

    return msg.get(language, "**" + tag + "** isn't a valid **Vainglory team tag**... :sweat_smile:")

def notGame(language, game_name):
    msg = {
    "english": "**" + game_name + "** isn't supported by **ComputerBot**... :confused:",
    "spanish": "**" + game_name + "** no es compatible con **ComputerBot**... :confused:"
    }

    return msg.get(language, "**" + game_name + "** isn't supported by **ComputerBot**... :confused:")

def notBool(language, value):
    msg = {
    "english": "**" + value + " isn't valid** please use **True** or **False**... :sweat_smile:",
    "spanish": "**" + value + "no es válido ** use **True** o **False**... :sweat_smile:"
    }

    return msg.get(language, "**" + value + " isn't valid** please use **True** or **False**... :sweat_smile:")

def notServerOwner(language, server_name):
    msg = {
    "english": "You **aren't** the **owner** of **" + server_name + "** so you **don't have access**... :sweat_smile:",
    "spanish": "Usted **no es el propietario  del servidor, " + server_name + ",** por lo que **no tienes acceso**... :sweat_smile:"
    }

    return msg.get(language, "You **aren't** the **owner** of **" + server_name + "** so you **don't have access**... :sweat_smile:")

# Custom Lines:
# ABOUT LINES
def aboutTitle(language):
    msg = {
    "english": "About",
    "spanish": "Sobre"
    }

    return msg.get(language, "About")


def aboutDescription(language):
    msg = {
    "english": "Hi, I'm **" + config.bot_name + "**, developed by Halcyon Hackers with love, python, and VG API. I'm a growing community bot that has new features added regularly. For now I control VG soon I will control the world. :smiley:",
    "spanish": "Hola, soy **" + config.bot_name + "**, desarrollado por Halcyon Hackers con amor, python y VG API. Soy un bot de comunidad en crecimiento que tiene nuevas características agregadas regularmente. Por ahora controlo VG pronto voy a controlar el mundo. :smiley:"
    }

    return msg.get(language, "Hi, I'm **" + config.bot_name + "**, developed by Halcyon Hackers with love, python, and VG API. I'm a growing community bot that has new features added regularly. For now I control VG soon I will control the world. :smiley:")

def aboutFieldOneTitle(language):
    msg = {
    "english": "What can I do?",
    "spanish": "¿Que puedo hacer?"
    }

    return msg.get(language, "What can I do?")

def aboutFieldOne(language, server_prefix):
    msg = {
    "english": "For a look at what I can do type **" + server_prefix + "help**, for a detailed list please check the [docs](" + config.bot_docs + ").",
    "spanish": "Para una vistazo a lo que puedo hacer, escriba **" + server_prefix + "help**, para una lista detallada por favor revise [docs](" + config.bot_docs + ")."
    }

    return msg.get(language, "For a look at what I can do type **" + server_prefix + "help**, for a detailed list please check the [docs](" + config.bot_docs + ").")

def aboutFieldTwoTitle(langugage):
    msg = {
    "english": "Talk To My Developers!",
    "Spanish": "¡Habla Con Mis Desarrolladores!"
    }

    return msg.get(langugage, "Talk To My Developers!")

def aboutFieldTwo(language, bot_prefix):
    msg = {
    "english": "**Developers: ClarkthyLord, SpiesWithin, physiX, Kashz**\nCome join us [here](" + config.bot_server + "). If you believe you’ve found a bug, error, or need to report something contact us via the **" + str(bot_prefix) + "report message** command; **Fair Warning**, use this too much and you will lose it.",
    "spanish": "**Desarrolladores: ClarkthyLord, SpiesWithin, physiX, Kashz**\nVenga con nosotros [aquí](" + config.bot_server + "). Si cree que encontró un error o necesidad de informar algo, hágalo vía mensaje de informe con **" + str(bot_prefix) + "report message**; Advertencia, use esto demasiado y lo perderá."
    }

    return msg.get(language, "**Developers: ClarkthyLord, SpiesWithin, physiX, Kashz**\nCome join us [here](" + config.bot_server + "). If you believe you’ve found a bug, error, or need to report something contact us via the **" + str(bot_prefix) + "report message** command; **Fair Warning**, use this too much and you will lose it.")

def aboutFieldThreeTitle(language):
    msg = {
    "english": "Bot Status:",
    "spanish": "Estado Del Bot:"
    }

    return msg.get(language, "Bot Status:")

def aboutFieldThreeV1(language, server_num):
    msg = {
    "english": "Servers I'm In: *" + server_num + "*",
    "spanish": "Servidores En Los Que Estoy: *" + server_num + "*"
    }

    return msg.get(language, "Servers I'm In: *" + server_num + "*")

def aboutFieldThreeV2(language, server_num, member_num):
    msg = {
    "english": "Servers I'm In: *" + server_num + "*\nUsers Serving: *" + member_num + "*",
    "spanish": "Servidores En Los Que Estoy: *" + server_num + "*\nUsuarios Que Servimos: *" + member_num + "*"
    }

    return msg.get(language, "Servers I'm In: *" + server_num + "*\nUsers Serving: *" + member_num + "*")

def aboutFieldFourTitle(language):
    msg = {
    "english": "Donations!",
    "spanish": "¡Donaciones!"
    }

    return msg.get(language, "Donations!")

def aboutFieldFour(language):
    msg = {
    "english": "To support us with donations please go [here](" + config.bot_donation + ")!",
    "spanish": "Para apoyarnos con donaciones, por favor vaya [aquí](" + config.bot_donation + ")!"
    }

    return msg.get(language, "To support us with donations please go [here](" + config.bot_donation + ")!")

def userInfoLineOne(language, user_name):
    msg ={
    "english": "We **don't have** any **data** on **" + user_name + "**... :confused:",
    "spanish": "**No tenemos** ningún **dato** sobre **" + user_name + "**... :confused:"
    }

    return msg.get(language, "We **don't have** any **data** on **" + user_name + "**... :confused:")


# USER INFO LINES
def userInfoTitle(language):
    msg = {
    "english": "About User",
    "spanish": "Sobre Usuario"
    }

    return msg.get(language, "About User")

def userInfoDescription(language, user_name):
    msg = {
    "english": "Information on  **" + user_name + "**, a discord user using ComputerBot :hugging:",
    "spanish": "Informacion sobre **" + user_name + "**, un usario the discord utilizando ComputerBot :hugging:"
    }

    return msg.get(language, "Information on you, **" + user_name + "**, relating to the ComputerBot :hugging:")

def userInfoFielOneTitle(language):
    msg = {
    "english": "General View:",
    "spanish": "Vista General:"
    }

    return msg.get(language, "General View:")

def userInfoFieldOne(language):
    msg = {
    "english": "**Language:** *" + language + "*",
    "spanish": "**Idioma:** *" + language + "*"
    }

    return msg.get(language, "**Language:** *" + language + "*")

def userInfoFieldTwoTitle(language):
    msg = {
    "english": "Vainglory Related:",
    "spanish": "Vainglory Relacionado:"
    }

    return msg.get(language, "Vainglory Related:")

def userInfoFieldTwo(language, quick_name, quick_region, verified_name, verified_region, compress, emojis):
    msg = {
    "english": "**Compress Embeds:** *" + compress + "*\n**Send Emojis:** *" + emojis + "*\n**Quick IGN:** *" + quick_name + "* **|Quick Region:** *" + quick_region + "*\n**Verified IGN:** *" + verified_name + "* **|Verified Region:** *" + verified_region + "*",
    "spanish": "**Comprimir Embeds:** *" + compress + "*\n**Mandar Emojis:** *" + emojis + "*\n**Quick IGN:** *" + quick_name + "* **|Quick Region:** *" + quick_region + "*\n**IGN Verificado:** *" + verified_name + "* **|Region Verificada:** *" + verified_region + "*"
    }

    return msg.get(language, "**Compress Embeds:** *" + compress + "*\n**Send Emojis:** *" + emojis + "*\n**Quick IGN:** *" + quick_name + "* **|Quick Region:** *" + quick_region + "*\n**Verified IGN:** *" + verified_name + "* **|Verified Region:** *" + verified_region + "*")

def userInfoFieldThreeTitle(language):
    msg ={
    "english": "Tournament Related:",
    "spanish": "Relacionado Con El Torneo:"
    }

    return msg.get(language, "Tournament Related:")

def userInfoFieldThree(language):
    msg = {
    "english": "Coming Soon",
    "spanish": "Próximamente"
    }

    return msg.get(language, "Coming Soon")

# DONATE LINES
def donateTitle(language):
    msg = {
    "english": "Support Us By Donating!",
    "spanish": "¡Apóyanos donando!"
    }

    return msg.get(language, "Support Us By Donating!")

def donateDescription(language):
    msg = {
    "english": "If you would like to help support us please go [here](" + config.bot_donation + "). Donators may get cookies, well cool stuff anyways! :smiley:",
    "spanish": "Si quieres ayudarnos por favor vaya [aquí](" + config.bot_donation + "). Los donadores pueden obtener galletas :smiley:"
    }

    return msg.get(language, "If you would like to help support us please go [here](" + config.bot_donation + "). Donators may get cookies, well cool stuff anyways! :smiley:")


def serverInfoTitle(language, server_name):
    msg = {
    "english": "About " + server_name,
    "spanish": "Sobre " + server_name
    }

    return msg.get(language, "About " + server_name)


def serverInfoDescription(language, server_name):
    msg = {
    "english": "Information on **" + server_name + "** a discord server using *ComputerBot* :hugging:",
    "spanish": "Información sobre **" + server_name + "** un servidor de Discord usando *ComputerBot* :hugging:"
    }

    return msg.get(language, "**Information on " + server_name + "** a discord server using *ComputerBot* :hugging:")


def serverInfoFieldOneTitle(language):
    msg = {
    "english": "General View:",
    "spanish": "Vista general:"
    }

    return msg.get(language, "General View:")


def serverInfoFieldOne(language, default_game, notify_server, notify_owner, channel):
    msg = {
    "english": "**Default Game:** *" + default_game + "* **|Language:** *" + language + "*\n**Notify Server:** *" + notify_server + "* **|Notify Owner:** *" + notify_owner + "*\n**Bots Channel:** *" + channel + "*",
    "spanish": "**Juego Predeterminado:** *" + default_game + "* **|Idioma:** *" + language + "*\n**Notificar Al Servidor:** *" + notify_server + "* **|Notificar Al Propietario:** *" + notify_owner + "*\n**Bots Channel:** *"+ channel + "*"
    }

    return msg.get(language, "**Default Game:** *" + default_game + "* **|Language:** *" + language + "*\n**Notify Server:** *" + notify_server + "* **|Notify Owner:** *" + notify_owner + "*\n**Bots Channel:** *" + channel + "*")


def serverInfoFieldTwoTitle(language):
    msg = {
    "english": "Server Command Bans:",
    "spanish": "Prohibiciones De Comandos En El Servidor:"
    }

    return msg.get(language, "Server Command Bans:")


def serverInfoFieldTwo(language, command_bans):
    if command_bans != []:
        msg = ""
        for command in command_bans:
            msg += "*" + str(command) + "*\n"

    else:
        msg = {
        "english": "No Command Bans",
        "spanish": "No Hay Prohibiciones De Comando"
        }

        msg = msg.get(language)

    return msg

def serverInfoFieldThreeTitle(language):
    msg = {
    "english": "Vainglory Related:",
    "spanish": "Relacionado A Vainglory:"
    }

    return msg.get(language, "Vainglory Related:")

def serverInfoFieldThree(language, region, guildN, guildT, teamN, teamT, compress, emojis):
    msg = {
    "english": "**Compress Embeds:** *" + compress + "*\n**Send Emojis:** *" + emojis + "*\n**Region:** *" + region + "*\n**Guild:** *" + guildN + "* **|** *" + guildT + "*\n**Team:** *" + teamN + "* **|** *" + teamT + "*",
    "spanish": "**Comprimir Embeds:** *" + compress + "*\n**Mandar Emojis:** *" + emojis + "**\n**Región:** *" + region + "*\n**Gremio:** *" + guildN + "* **|** *" + guildT + "*\n**Equipo:** *" + teamN + "* **|** *" + teamT + "*"
    }

    return msg.get(language, "**Compress Embeds:** *" + compress + "*\n**Send Emojis:** *" + emojis + "*\n**Region:** *" + region + "*\n**Guild:** *" + guildN + "* **|** *" + guildT + "*\n**Team:** *" + teamN + "* **|** *" + teamT + "*")

def serverInfoFieldFourTitle(language):
    msg = {
    "english": "Tournament Related:",
    "spanish": "Relacionado Con Torneos:"
    }

    return msg.get(language, "Tournament Related")

def serverInfoFieldFour(language):
    msg = {
    "english": "Coming Soon",
    "spanish": "Próximamente"
    }

    return msg.get(language, "Coming Soon")

def serverPrefixLineOne(language, prefix):
    msg = {
    "english": "This **servers prefix** has been **updated** to __**" + prefix + "**__ :blush:",
    "spanish": "El **prefijo de este servidor** ha sido **actualizado** a __**" + prefix + "**__ :blush:"
    }

    return msg.get(language, "This **servers prefix** has been **updated** to __**" + prefix + "**__ :blush:")

def serverPrefixLineTwo(language, prefix):
    msg = {
    "english": "Sorry but I **wasn't able** to **update** this **servers prefix** to __**" + prefix + "**__ :confused:",
    "spanish": "Lo siento, pero **no pude actualizar** el **prefijo** de este **servidor** a __**" + prefix + "**__ :confused:"
    }

    return msg.get(language, "Sorry but I **wasn't able** to **update** this **servers prefix** to __**" + prefix + "**__ :confused:")

def serverLanguageChangeLineOne(language, server_name, new_language):
    msg = {
    "english": "This **servers, " + server_name + ", bot language** has been **updated** to __**" + new_language + "** __ :blush:",
    "spanish": "El **idioma** de el bot en este servidor, **" + server_name + "**, ha sido **actualizado** a __**" + new_language + "**__ :blush:"
    }

    return msg.get(new_language, "This **servers, " + server_name + ", bot language** has been **updated** to __**" + new_language + "** __ :blush:")

def serverLanguageChangeLineTwo(language, name, new_language):
    msg = {
    "english": "Sorry, but I **wasn't able** to **update** this **server's, " + name + ", bot language** to __**" + new_language + "**__ :confused:",
    "spanish": "Lo siento, pero **no pude actualizar** el **idioma del bot** en este servirdor, **" + name + ",** a __**" + new_language + "**__ :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **update** this **server's, " + name + ", bot language** to __**" + new_language + "**__ :confused:")

def serverRegionChangeLineOne(language, name, region):
    msg = {
    "english": "This **server's, " + name + ", vainglory_work region** has been **updated** to __**" + region + "**__ :blush:",
    "spanish": "La **vainglory_work región de este servidor, " + name + ",** ha sido **actualizado** a __**" + region + "**__ :blush:"
    }

    return msg.get(language, "This **server's, " + name + ", vainglory_work region** has been **updated** to __**" + region + "**__ :blush:")

def serverRegionChangeLineTwo(language, name, region):
    msg = {
    "english": "Sorry, but I **wasn't able** to **update** this **servers, " + name + ", vainglory_work region to __**" + region + "**__ :confused:",
    "spanish": "Lo siento, pero **no fue capaz de actualizar** la **vainglory_work región de este servidor, " + name + ",** a __**" + region + "**__ :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **update** this **servers, " + name + ", vainglory_work region to __**" + region + "**__ :confused:")

def serverVgGuildChangeLineOne(language, server_name, guild_name, guild_tag):
    msg = {
    "english": "This **server , " + server_name + ",** has been **associated** to __**" + guild_name +"(" + guild_tag + ")**__ a Vainglory guild :blush:",
    "spanish": "Este servidor **," + server_name + ",** ha sido **asociado** a __**" + guild_name + "(" + guild_tag + ")** __ a Vainglory guild :blush:"
    }

    return msg.get(language, "This **server , " + server_name + ",** has been **associated** to __**" + guild_name +"(" + guild_tag + ")**__ a vainglory_work guild :blush:")

def serverVgGuildChangeLineTwo(language, server_name, guild_name, guild_tag):
    msg = {
    "english": "Sorry, but I **wasn't able** to **associate " + guild_name + "(" + guild_tag + ")** with **" + server_name + "** :confused:",
    "spanish": "Lo siento, pero **no pude asociar " + guild_name + "(" + guild_tag + ")** con **" + server_name + "** :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **associate " + guild_name + "(" + guild_tag + ")** with **" + server_name + "** :confused:")

def serverVgTeamChangeLineOne(language, server_name, team_name, team_tag):
    msg = {
    "english": "This **server , " + server_name + ",** has been **associated** to __**" + team_name + "(" + team_tag + ")**__ a Vainglory team :blush:",
    "spanish": "Este servidor **," + server_name + ",** ha sido **asociado** a __**" + team_name + "(" + team_tag + ")** __ un equipo de Vainglory :blush:"
    }

    return msg.get(language, "This **server , " + server_name + ",** has been **associated** to __**" + team_name + "(" + team_tag + ")**__ a Vainglory guild :blush:")

def serverVgTeamChangeLineTwo(language, server_name, team_name, team_tag):
    msg = {
    "english": "Sorry, but I **wasn't able** to **associate " + team_name + "(" + team_tag + ")** with **" + server_name + "** :confused:",
    "spanish": "Lo siento, pero **no pude asociar " + team_name + "(" + team_tag + ")** con **" + server_name + "** :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **associate " + team_name + "(" + team_tag + ")** with **" + server_name + "** :confused:")

def serverGameChangeLineOne(language, server_name, game_name):
    msg = {
    "english": "This **server's , " + server_name + ", default game** has been **set to** __**" + game_name + "**__ :blush:",
    "spanish": "El **juego predeterminado** ha sido **establecido** a __ **" + game_name + "** __ en el **servidor, " + server_name + "** :blush:"
    }

    return msg.get(language, "This **server's , " + server_name + ", default game** has been **set to** __**" + game_name + "**__ :blush:")

def serverGameChangeLineTwo(language, server_name, game_name):
    msg = {
    "english": "Sorry, but I **wasn't able** to set **" + game_name + "** as the **servers ," + server_name + "** default game :confused:",
    "spanish": "Lo siento, pero **no pude** establecer **" + game_name + "** como el juego predeterminado del  **servidor ," + server_name + "** :confuso:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to set **" + game_name + "** as the **servers ," + server_name + "** default game :confused:")

def serverNotifyLineOne(language, server_name):
    msg = {
    "english": "**Notifications** will not be sent to **" + server_name + "** anymore... :eyes:",
    "spanish": "**Notificaciones** no serán enviadas a **" + server_name + "** más... :eyes:"
    }

    return msg.get(language, "**Notifications** will not be sent to **" + server_name + "** anymore... :eyes:")

def serverNotifyLineTwo(language, server_name):
    msg = {
    "english": "**Notifications** will be sent to **" + server_name + "** from now on... :eyes:",
    "spanish": "**Notificaciones** serán enviadas a **" + server_name + "** a partir de ahora... :eyes:"
    }

    return msg.get(language, "**Notifications** will be sent to **" + server_name + "** from now on... :eyes:")

def serverNotifyLineThree(language, server_name):
    msg = {
    "english": "Sorry but I **wasn't able** to **change** this **server's, " + server_name + ", notification setting**... :confused:",
    "spanish": "Lo siento, pero **no fue capaz** de **cambiar** la **configuración de notificación en** este servidor , **" + server_name + "**... :confused:"
    }

    return msg.get(language, "Sorry but I **wasn't able** to **change** this **server's, " + server_name + ", notification setting**... :confused:")

def serverChannelLineOne(language, server_channel, server_name):
    msg = {
    "english": "From now on I'll **send most of my messages** into **this channel, " + server_channel + "**, no matter where I'm called from within **" + server_name + "**... :hugging:",
    "spanish": "A partir de ahora **enviaré la mayoría de mis mensajes a este canal," + server_channel + "**, no importa desde donde me llamen dentro de **" + server_name + "**.. :hugging:"
    }

    return msg.get(language, "From now on I'll **send most of my messages** into **this channel, " + server_channel + "**, no matter where I'm called from within **" + server_name + "**... :hugging:")

def serverChannelLineTwo(language, server_name):
    msg = {
    "english": "From now on I'll **respond** to users from **wherever I'm called** in **" + server_name + "**... :hugging:",
    "spanish": "A partir de ahora **responderé** a los usuarios de **dondequiera que me llamen** en **" + server_name + "**... :hugging:"
    }

    return msg.get(language, "From now on I'll **respond** to users from **wherever I'm called** in **" + server_name + "**... :hugging:")

def serverChannelLineThree(language, server_name):
    msg = {
    "english": "Sorry, but I **wasn't able** to **setup** a **channel** for myself in **" + server_name + "**... :confused:",
    "spanish": "Lo siento, pero **no pude configurar** un **canal** para mí en **" + server_name + "**... :confused:"
    }

    return msg.get(language, "Sorry but I **wasn't able** to **setup** a **channel** for myself in **" + str(server_name) + "**... :confused:")

def serverNotifyOwnerLineOne(language, server_owner, server_name):
    msg = {
    "english": "**" + server_owner + " the owner** of **" + server_name + " won't be sent bot notifications**... :eyes:",
    "spanish": "**" + server_owner + " el propietario** de **" + server_name + "no será enviado notificaciones sobre bot ** ...: ojos:"
    }

    return msg.get(language, "**" + server_owner + " the owner** of **" + server_name + " won't be sent bot notifications**... :eyes:")

def serverNotifyOwnerLineTwo(language, server_owner, server_name):
    msg = {
    "english": "**" + server_owner + " the owner** of **" + server_name + " will be sent bot notifications**... :eyes:",
    "spanish": "**" + server_owner + "el propietario** de **" + server_name + " se le enviará notificaciones sobre el bot**... :ojos:"
    }

    return msg.get(language, "**" + server_owner + " the owner** of **" + server_name + " will be sent bot notifications**... :eyes:")

def serverNotifyOwnerLineThree(language, server_owner, server_name):
    msg = {
    "english": "Sorry, but I **wasn't able** to **change** if you the **server owner, " + server_owner + ", of " + server_name +" receives bot notifications**... :confused:",
    "spanish": "Lo siento, pero **no fue capaz** de cambiar **si el propietario, " + server_owner + ", del servidor " + server_name + " recibe notificaciones sobre el bot**... :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **change** if you the **server owner, " + server_owner + ", of " + server_name +" receives bot notifications**... :confused:")

def notCommand(language, command):
    msg = {
    "english": "**" + command + " isn't a valid command name/group** please enter a **valid command name/group**... :sweat_smile:",
    "spanish": "**" + command + " no es un nombre/grupo de comando válido** por favor **ingrese un nombre/grupo de comando válido**... :sweat_smile:"
    }

    return msg.get(language, "**" + command + " isn't a valid command name/group** please enter a **valid command name/group**... :sweat_smile:")

def notMode(language, command, mode):
    msg = {
    "english": "**" + command + " can't be set to " + mode + "**... :sweat_smile:",
    "spanish": "**" + command + " no puede ser establecido a " + mode + "**... :sweat_smile:"
    }

    return msg.get(language, "**" + command + " can't be set to " + mode + "**... :sweat_smile:")

def serverCommandBanLineOne(language, command, server_name):
    msg = {
    "english": "**" + command + "** has been **disabled** in **" + server_name + "**... :eyes:",
    "spanish": "**" + command + "** ha sido **desactivado** en **" + server_name + "**... :eyes:"
    }

    return msg.get(language, "**" + command + "** has been **disabled** in **" + server_name + "**... :eyes:")

def serverCommandBanLineTwo(language, command, server_name):
    msg = {
    "english": "Sorry, but I **wasn't able** to **disable " + command + "** in the server **" + server_name + "**... :confused:",
    "spanish": "Lo siento, pero **no he podido deshabilitar" + command + "** en el servidor, **" + server_name + "**... :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **disable " + command + "** in **" + server_name + "**... :confused:")

def serverCommandBanLineThree(language, command, server_name):
    msg = {
    "english": "**" + command + "** has been **enabled** in **" + server_name + "**... :eyes:",
    "spanish": "**" + command + "** ha sido **habilitado** en **" + server_name + "**... :eyes:"
    }

    return msg.get(language, "**" + command + "** has been **enabled** in **" + server_name + "**... :eyes:")

def serverCommandBanLineFour(language, command, server_name):
    msg = {
    "english": "Sorry, but I **wasn't able** to **enable " + command + "** in **" + server_name + "**... :confused:",
    "spanish": "Lo siento, pero **no fue capaz** de habilitar " + command + "** en **" + server_name + "**... :confused:"
    }

    return msg.get(language, "Sorry, but I **wasn't able** to **enable " + command + "** in **" + server_name + "**... :confused:")

def userLanguageLineOne(language, new_language):
    msg = {
    "english": "**Your bot's language** has been **updated** to __**" + new_language + "**__ :blush:",
    "spanish": "**El idioma de tu bot** ha sido **actualizado** a __**" + new_language + "**__ :blush:"
    }

    return msg.get(new_language, "**Your bot's language** has been **updated** to __**" + new_language + "**__ :blush:")

def userLanguageLineTwo(language, new_language):
    msg = {
    "english": "Sorry but I **wasn't able** to **update your bots language to " + new_language + "** :confused:",
    "spanish": "Lo siento, pero **no fue capaz** de **actualizar el lenguaje bot a " + new_language + "** :confused:"
    }

    return msg.get(language, "Sorry but I **wasn't able** to **update your bots language to " + new_language + "** :confused:")


def compressVainGloryLineOne(language, entityName):
    msg = {
    "english": "**I was able to update vainglory embed compression for " + entityName + "...** :hugging:",
    "spanish": "**He podido actualizar la compresión de incrustación de vainglory para " + entityName + "...** :hugging:"
    }

    return msg.get(language, "**I was able to update vainglory embed compression for " + entityName + "...** :hugging:")


def compressVainGloryLineTwo(language, entityName):
    msg = {
    "english": "**I wasn't able to update vainglory embed compression for " + entityName + "...** :confused:",
    "spanish": "**No pude actualizar la compresión de embeds para vainglory para " + entityName + "...** :confused:"
    }

    return msg.get(language, "**I wasn't able to update vainglory compress for " + entityName + "...** :confused:")


def emojisVainGloryLineOne(language, entityName):
    msg = {
    "english": "**I was able to update vainglory emojis for " + entityName + "...** :hugging:",
    "spanish": "**He podido actualizar el utilizo de emojis de vainglory para " + entityName + "...** :hugging:"
    }

    return msg.get(language, "**I was able to update vainglory embed compression for " + entityName + "...** :hugging:")


def emojisVainGloryLineTwo(language, entityName):
    msg = {
    "english": "**I wasn't able to update vainglory emojis for " + entityName + "...** :confused:",
    "spanish": "**No pude actualizar el utilizo de emojis para vainglory para " + entityName + "...** :confused:"
    }

    return msg.get(language, "**I wasn't able to update vainglory compress for " + entityName + "...** :confused:")


def reportLineOne(language, message):
    msg = {
    "english": "Report sent :ok_hand:\nContent:```" + message + "```",
    "spanish": "Reporte enviado :ok_hand:\nContenido:```" + message + "```"
    }

    return msg.get(language, "Report sent :ok_hand:\nContent:```" + message + "```")


def reportLineTwo(language):
    msg = {
    "english": "Sorry, **something went wrong** while **sending** your **report**... :confused:\nTry again later :blush:",
    "spanish": "Lo sentimos, **algo a salió mal** mientras **enviamos** su **reporte**... :confused:\nInténtalo de nuevo más tarde :blush:"
    }

    return msg.get(language, "Sorry, **something went wrong** while **sending** your **report**... :confused:\nTry again later :blush:")


def lotteryTitle(language, name):
    msg = {
    "english": name + ", you've just won the ComputerBot ICE lottery!",
    "spanish": "¡" + name + ", acabas de ganar la lotería de ComputerBot de ICE!"
    }

    return msg.get(language, name + ", you've just won the ComputerBot ICE lottery!")


def lotteryDescription(language):
    msg = {
    "english": "With a **1** in **" + str(config.lottery_settings["iceRate"]) + "** chance you've won **" + str(config.lottery_settings["iceAmount"]) + " VainGlory ICE**!\nPlease go [here](" + str(config.bot_server) + "), " + str(config.bot_server) + ", to claim your ICE!",
    "spanish": "Con un **1** en **" + str(config.lottery_settings["iceRate"]) + "** oportunidad has ganado **" + str(config.lottery_settings["iceAmount"]) + " VainGlory ICE**!\nVaya [aquí](" + str(config.bot_server) + "), " + str(config.bot_server) + ", para reclamar su ICE!"
    }

    return msg.get(language, "With a **1** in **" + str(config.lottery_settings["iceRate"]) + "** chance you've won **" + str(config.lottery_settings["iceAmount"]) + " VainGlory ICE**!\nPlease go [here](" + str(config.bot_server) + "), " + str(config.bot_server) + ", to claim your ICE!")

def lotteryTitleOne(language):
    msg = {
    "english": "ComputerBot Lottery",
    "spanish": "ComputerBot Lotería"
    }

    return msg.get(language, "ComputerBot Lottery")

def lotteryDescriptionOne(language):
    msg = {
    "english": "Win the lottery at random from simple things like using ComputerBot commands!\n*ICE Amount:* **" + str(config.lottery_settings["iceAmount"]) + "**",
    "spanish": "¡Gana la lotería al azar desde cosas simples como usar comandos ComputerBot!\n*Cantidad De ICE:* **" + str(config.lottery_settings["iceAmount"]) + "**"
    }

    return msg.get(language, "Win the lottery from simple things like using ComputerBot commands!\n*Current ICE Pot:* **" + str(config.lottery_settings["iceAmount"]) + "**")

def inviteLineOne(language):
    msg = {
    "english": "You can invite me, ComputerBot, to any server at:\nhttp://Computergg.com/bot",
    "spanish": "Puedes invitarme, ComputerBot, a cualquier servidor en:\nhttp://Computergg.com/bot"
    }

    return msg.get(language, "You can invite me, ComputerBot, to any server at:\nhttp://Computergg.com/bot")

def reportSize(language):
    msg = {
    "english": "You'll have to write something longer then that to report it! :sweat_smile:",
    "spanish": "Tendrás que escribir algo más que eso para reportalo :sweat_smile:"
    }

    return msg.get(language, "You'll have to write something longer then that to report it! :sweat_smile:")

# def (language):
#     msg = {
#     "english": ,
#     "spanish":
#     }
#
#     return msg.get(language, )
