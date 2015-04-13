# n2468txd-lolbot

The basic rundown
-------------

A chatbot that runs on XMPP, that connects to the League of Legends chat server.

The Riot API reference is here: https://developer.riotgames.com/api/methods
Be sure to configure the config file properly, using the template.

PM Commands:
-------------
* hello - Responds with 'Hello'.
* ping - Responds with 'Pong!'.
* level [summoner name] - Responds with the specified summoner's level.
* rank [summoner name] - Responds with the specified summoner's solo queue rank.
* gameinfo [optional summoner name] - Responds with the ingame info, if no summoner name is specified the sender is assumed.
* auto - Enabled Auto Mode (covered below).
* help - Responds with the above.

Group Chat Commands:
-------------
* All the above commands, with an exclamation point in front, eg hello = !hello.
* Any custom commands added with the addcom command (covered below). The custom commands will just return with text.

Admin Commands:
-------------
* addcom [new command name] [command output] - Add a custom group chat command. Add an exclamation point in front if you want the command to have an exclamation point, this is not added automatically. (use carefully! does not check if command already exists, unintended results can occur if this happens. There is no delete command for now, remove from the txt file manually)
* addauto [summoner name] - Adds specified summoner to the Auto list
* removeauto [summoner name] - Removes specified summoner from Auto
* listauto - Lists summoner IDs of summoners with Auto enabled
* idlookup [summoner ID] - looks up specified summoner ID and returns with name

What is Auto Mode?
-------------
When a summoner goes in game and they have registered themselved (or the admin has registered them as an auto user), and they are friends with the bot, the summoner will automatically be messaged gameinfo for their game.