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
* The bot will automatically join any group chat given.

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

On the OCE (Oceania) server?
-------------
Jump right in and add 'n2468txd' as a friend in League of Legends! Feel free to use the PM commands and add the bot to your chatroom. The custom commands however, will be my own custom commands and these commands will be kept private (you can try and look for those commands :P).

A kind note: please do not abuse the commands and the system as the Riot API can only handle so many requests. If the system is abused I will be forced to restrict this bot to select people and it will not be left open to public.






Riot API disclaimer
--------------
'n2468txd-lolbot' isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.