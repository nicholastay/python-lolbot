# -*- coding: utf-8 -*-




###########################################################
# XMPP League of Legends ChatBot
# by n2468txd
#
# SleekXMPP and JSON is required
# Template config file is in the repo
# Command listings on GitHub
#
# Username and Password for bot account required
# Main Account Summoner ID is required to message main account debug info if necessary and use admin commands
# Status format for XMPP can be found online with a quick google search
# Riot developer API key required, a development key will work just as well unless the bot is highly used
# IP prefrably in number format, just nslookup your region's xmpp server
# This bot is tested on Oceania region, untested on others.
# Was built against: OCE, OC1, SummonerVer=1.4, StaticDataVer=1.2, LeagueVer=2.5 for API modules in the Riot API
#
# http://github.com/n2468txd
###########################################################







############### Library / Module Imports ##################

# log module
import logging

# xmpp module
import sleekxmpp
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

# ssllib
import ssl

# json
import json

# requests
import requests

# if file exist
import os.path

# sys
import sys
###########################################################




################### VARS ##########################
# open json config
if os.path.exists('lolbotConfig.json'):
        with open('lolbotConfig.json') as data_file:
                data = json.load(data_file)
else:
        print "config does not exist"
        sys.exit()

riotApiKey = data["apiKey"]
riotApiRegion = data["apiRegion"]
riotApiRegionID = data["apiRegionSpectateID"]
riotApiSummonerVer = data["apiSummonerVer"]
riotApiStaticDataVer = data["apiStaticDataVer"]
riotApiLeagueVer = data["apiLeagueVer"]
xmppLoLUsername = data["username"]
xmppLoLPassword = data["password"]
xmppLoLIP = data["ip"]
xmppLoLPort = data["port"]
xmppStatus = data["status"]
mainAcc = data["mainAccountID"]
welcomeMessage = data["welcomeMessage"]
autoSendMessage = []
####################################################

################### Classes #######################

class LolBot(ClientXMPP):

        def __init__(self, jid, password):
                ClientXMPP.__init__(self, jid, password)

                self.add_event_handler("session_start", self.session_start)
                self.add_event_handler("message", self.message)

                self.add_event_handler("changed_status", self.changed_status)

                self.add_event_handler("got_online", self.got_online)

                #group chats
                self.add_event_handler("groupchat_invite", self.accept_invite)
                self.add_event_handler("groupchat_message", self.muc_message)

                self.ssl_version = ssl.PROTOCOL_SSLv3

                self.auto_authorize = True
                self.auto_subscribe = True


        def changed_status(self, status):
                if ('inGame' in str(status)) and (str(str(status['from']).split('@', 1)[0]).strip('sum') in autoSendMessage):
                        returnMessage = RiotApiGameInfo(str(str(status['from']).split('@', 1)[0]).strip('sum'))
                        self.send_message(mto=((str(status['from']).split('/', 1)[0]) + '/xiff'), mbody=returnMessage, mtype='chat')
                        print 'Sent auto message to: ' + ((str(status['from']).split('/', 1)[0]) + '/xiff')

        def got_online(self, presence):
                if ((str(presence['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc) and (welcomeMessage.lower() == 'true'):
                        self.send_message(mto="sum" + mainAcc + "@pvp.net/xiff", mbody="Welcome back, " + mainAccName + "!", mtype='chat')
        
        def session_start(self, event):
                self.send_presence(pstatus=xmppStatus, pshow='chat')
                self.get_roster()
                #tell self online
                self.send_message(mto="sum" + mainAcc + "@pvp.net/xiff", mbody="(--> chatbot online)", mtype='chat')

        def accept_invite(self, inv):
                self.plugin['xep_0045'].joinMUC(inv["from"], xmppLoLUsername, wait=True)
                print("Invite from %s to %s" %(inv["from"], inv["to"]))

        def muc_message(self, msg):
                if msg['mucnick'] != xmppLoLUsername:
                        
                        parsedMsg = msg['body'].split()
                        firstWord = parsedMsg[0]
            
                        if "!hello" in firstWord:
                                self.send_message(mto=msg['from'].bare, mbody="Hello!", mtype='groupchat')
            
                        if "!ping" in firstWord:
                                self.send_message(mto=msg['from'].bare, mbody="Pong!", mtype='groupchat')

                        elif "!level" in firstWord:
                                theName = msg['body']
                                if len(theName) > 6:
                                        returnMessage = theName[6:] + " is Level " + str(RiotApiLevel(theName[6:]))
                                        self.send_message(mto=msg['from'].bare, mbody=str(returnMessage), mtype='groupchat')
                                else:
                                        self.send_message(mto=msg['from'].bare, mbody="Invalid summoner.", mtype='groupchat')

                        elif "!rank" in firstWord:
                                theName = msg['body']
                                if len(theName) > 5:
                                        summonerID = RiotApiGetID(theName[5:])
                                        if summonerID == 0:
                                                returnMessage = "Invalid / having issues at the bot right now."
                                        else:
                                                returnMessage = theName[5:] + " is in " + str(RiotApiGetRank(summonerID)) + " for ranked solo"
                                        self.send_message(mto=msg['from'].bare, mbody=str(returnMessage), mtype='groupchat')
                                else:
                                        self.send_message(mto=msg['from'].bare, mbody="Invalid summoner.", mtype='groupchat')
                                        
                        elif "!gameinfo" in firstWord:
                                theName = msg['body']
                                returnMessage = ""
                                if len(theName) > 9:
                                        summonerID = str(RiotApiGetID(theName[9:]))
                                        if summonerID == 0:
                                                returnMessage = "Invalid / having issues at the bot right now."
                                        else:
                                                returnMessage = RiotApiGameInfo(summonerID)
                                else:
                                        returnMessage = RiotApiGameInfo((str(msg['from']).strip('sum')).strip('@pvp.net/xiff'))
                                self.send_message(mto=msg['from'].bare, mbody=str(returnMessage), mtype='groupchat')

                        elif "!help" in firstWord:
                                self.send_message(mto=msg['from'].bare, mbody="---\nCommands available:\n!hello - bot will reply hello\n!ping - ping test bot\n!level [summoner name] - checks level of player\n!rank [summoner name] - checks SOLO rank of a player\n!gameinfo <optional player> - checks current game info", mtype='groupchat')

                        else:
                                # Load custom commands
                                commandsFile = open('lolbotCommands.txt', 'r')
                                commands = []
                                for line in commandsFile:
                                    thisCommand = []
                                    thisCommand.append((line.split())[0])
                                    thisCommand.append(line[((len((line.split())[0]))+1):])
                                    if thisCommand[1].endswith('\n'):
                                            thisCommand[1] = thisCommand[1][:-1]
                                    commands.append(thisCommand)

                                #returnMessage = '0'
                                for command in commands:
                                        if str(command[0]) == str(firstWord):
                                                #returnMessage = str(command[1])
                                                self.send_message(mto=msg['from'].bare, mbody=str(command[1]), mtype='groupchat')
                                                break

                                        
        
        def message(self, msg):
                if msg['type'] in ('chat', 'normal'):
                        
                        parsedMsg = msg['body'].split()
                        firstWord = parsedMsg[0]
                        
                        if "hello" in firstWord:
                                msg.reply("Hello!").send()
                                
                        elif "ping" in firstWord:
                                msg.reply("Pong!").send()
                                
                        elif ("offline" in firstWord) and ((str(msg['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc):
                                msg.reply("Bot is going down...").send()
                                self.disconnect(wait=True)
                                
                        elif "level" in firstWord:
                                theName = msg['body']
                                if len(theName) > 6:
                                        returnMessage = theName[6:] + " is Level " + str(RiotApiLevel(theName[6:]))
                                        msg.reply(str(returnMessage)).send()
                                else:
                                        msg.reply("Invalid summoner.").send()

                        elif "rank" in firstWord:
                                theName = msg['body']
                                if len(theName) > 5:
                                        summonerID = RiotApiGetID(theName[5:])
                                        if summonerID == 0:
                                                returnMessage = "Invalid / having issues at the bot right now."
                                        else:
                                                returnMessage = theName[5:] + " is in " + str(RiotApiGetRank(summonerID)) + " for ranked solo"
                                        msg.reply(str(returnMessage)).send()
                                else:
                                        msg.reply("Invalid summoner.").send()
                                        
                        elif "gameinfo" in firstWord:
                                theName = msg['body']
                                returnMessage = ""
                                if len(theName) > 9:
                                        summonerID = str(RiotApiGetID(theName[9:]))
                                        if summonerID == 0:
                                                returnMessage = "Invalid / having issues at the bot right now."
                                        else:
                                                returnMessage = RiotApiGameInfo(summonerID)
                                else:
                                        returnMessage = RiotApiGameInfo((str(msg['from']).strip('sum')).strip('@pvp.net/xiff'))
                                msg.reply(str(returnMessage)).send()

                        elif ("addcom" in firstWord) and ((str(msg['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc):
                                if len(str(msg['body']).split()) < 3:
                                        msg.reply("Not enough arguments.").send()
                                else:
                                        writeCommandFile = open('lolbotCommands.txt', 'a')
                                        writeCommandFile.write(((msg['body'])[7:]) + '\n')
                                        msg.reply('Command ' + ((msg['body']).split())[1] + " has been added.").send()

                        elif ("listauto" in firstWord) and ((str(msg['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc):
                                msg.reply(str(autoSendMessage)).send()

                        elif ("addauto" in firstWord) and ((str(msg['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc):
                                summonerID = str(RiotApiGetID(str((msg['body'])[8:])))
                                autoSendMessage.append(summonerID)
                                msg.reply(str((msg['body'])[8:]) + " (" + summonerID + ")" + " has been added to auto monitoring list.").send()

                        elif ("removeauto" in firstWord) and ((str(msg['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc):
                                summonerID = str(RiotApiGetID(str((msg['body'])[11:])))
                                autoSendMessage.remove(summonerID)
                                msg.reply(str((msg['body'])[11:]) + " (" + summonerID + ")" + " has been removed from auto monitoring list.").send()

                        elif ("idlookup" in firstWord) and ((str(msg['from']).strip('sum')).strip('@pvp.net/xiff') == mainAcc):
                                summonerID = str((msg['body'])[9:])
                                summonerName = str(RiotApiGetName(summonerID))
                                msg.reply(summonerID + " --> " + summonerName).send()

                        elif "auto" in firstWord:
                                if (str(msg['from']).strip('sum')).strip('@pvp.net/xiff') in autoSendMessage:
                                        autoSendMessage.remove((str(msg['from']).strip('sum')).strip('@pvp.net/xiff'))
                                        msg.reply("Auto mode disabled.").send()
                                else:
                                        autoSendMessage.append((str(msg['from']).strip('sum')).strip('@pvp.net/xiff'))
                                        msg.reply("Auto mode enabled.").send()

                        elif "help" in firstWord:
                                msg.reply("---\nCommands available:\nhello - bot will reply hello\nping - ping test bot\nlevel [summoner name] - checks level of player\nrank [summoner name] - checks SOLO rank of a player\ngameinfo <optional player> - checks current game info\nauto - enables auto mode").send()

################### Functions #######################

def RiotApiGetID(summonerName):
        r = requests.get('https://' + riotApiRegion + '.api.pvp.net/api/lol/' + riotApiRegion + '/v' + riotApiSummonerVer + '/summoner/by-name/' + summonerName + '?api_key=' + riotApiKey)
        if r.status_code != 200:
                return 0
        summonerID = r.json()[summonerName.lower().replace(" ", "")]["id"]
        return summonerID
        
def RiotApiGetChampionByID(championID):
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + riotApiRegion + '/v' + riotApiStaticDataVer + '/champion/' + str(championID) + '?api_key=' + riotApiKey)
        if r.status_code != 200:
                return 0
        championName = r.json()["name"]
        return championName

def RiotApiGetChampionList():
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + riotApiRegion + '/v' + riotApiStaticDataVer + '/champion?dataById=true&api_key=' + riotApiKey)
        return r.json()

def RiotApiGetName(summonerID):
        r = requests.get('https://' + riotApiRegion + '.api.pvp.net/api/lol/' + riotApiRegion + '/v' + riotApiSummonerVer + '/summoner/' + summonerID + '/name?api_key=' + riotApiKey)
        if r.status_code != 200:
                return 0
        summonerName = r.json()[summonerID]
        return str(summonerName)

def RiotApiLevel(summonerName):
        r = requests.get('https://' + riotApiRegion + '.api.pvp.net/api/lol/' + riotApiRegion + '/v' + riotApiSummonerVer + '/summoner/by-name/' + summonerName + '?api_key=' + riotApiKey)
        if r.status_code != 200:
                return "Invalid / having issues at the bot right now."
        summonerLevel = r.json()[(summonerName.lower()).replace(" ", "")]["summonerLevel"]
        return str(summonerLevel)

def RiotApiGetRank(summonerID):
        r = requests.get('https://' + riotApiRegion + '.api.pvp.net/api/lol/' + riotApiRegion + '/v' + riotApiLeagueVer + 'league/by-summoner/' + str(summonerID) + '/entry?api_key=' + riotApiKey)
        if r.status_code != 200:
                return "Invalid / having issues at the bot right now."
        returnMessage = ''
        if str(summonerID) not in r.text:
                return "Summoner is below level 30, or unranked / having issues at the bot right now."
        elif "RANKED_SOLO_5x5" not in str(r.json()[str(summonerID)]):
                return "Summoner has not played solo ranked / having issues at the bot right now."
        else:
                return str(str(r.json()[str(summonerID)][0]["tier"]).title() + " " + str(r.json()[str(summonerID)][0]["entries"][0]["division"]) + " (" + str(r.json()[str(summonerID)][0]["entries"][0]["leaguePoints"]) + " LP)")
        
def RiotApiGameInfo(summonerID):
        gameMode = ''
        finalGameInfo = ''
                                                                      
        r = requests.get('https://' + riotApiRegion + '.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/' + riotApiRegionID + '/' + str(summonerID) + '?api_key=' + riotApiKey)
        if r.status_code != 200:
                return "Invalid / having issues at the bot right now."
        if r.json()["gameMode"] == 'CLASSIC':
                gameMode = "Summoner's Rift 5v5"
        elif r.json()["gameMode"] == 'ARAM':
                gameMode = "ARAM 5v5"
        elif r.json()["gameMode"] == 'ONEFORALL':
                gameMode = "URF 5v5"
        else:
                gameMode = 0
        if gameMode == 0:
               return "Invalid game mode, bot cannot handle"

        if r.json()["gameType"] != 'MATCHED_GAME':
                return "You are not in a matched game, bot cannot handle"

        summonerNames = []
        summonerLevels = []
        summonerChampIDs = []
        summonerChampNames = []
        summonerIDs = []
        summonerRanks = []

        # Add names to array
        for x in range(0, 10):
                summonerNames.append(str(r.json()["participants"][x]["summonerName"]))

        # Get levels in bulk and add level to array
        rLevels = requests.get('https://' + riotApiRegion + '.api.pvp.net/api/lol/' + riotApiRegion + '/v' + riotApiSummonerVer + '/summoner/by-name/' + ",".join(summonerNames) + '?api_key=' + riotApiKey)
        for x in summonerNames:
                summonerLevels.append(str(rLevels.json()[(str(x).lower()).replace(" ", "")]["summonerLevel"]))

        # Get champion id and add to array
        for x in range(0, len(summonerNames)):
                summonerChampIDs.append(str(r.json()["participants"][x]["championId"]))

        # Use data list to lookup champion and add to array
        for x in range(0, len(summonerChampIDs)):
                summonerChampNames.append(str(championListByID['data'][str(summonerChampIDs[x])]['name']))

        # Get ranks
        # levels request has id data too
        for x in range(0, len(summonerNames)):
                summonerIDs.append(str(rLevels.json()[(str(summonerNames[x]).lower()).replace(" ", "")]["id"]))
        rRank = requests.get('https://' + riotApiRegion + '.api.pvp.net/api/lol/' + riotApiRegion + '/v' + riotApiLeagueVer + '/league/by-summoner/' + ",".join(summonerIDs) + '/entry?api_key=' + riotApiKey)
        for x in range(0, len(summonerNames)):
                if summonerLevels[x] == '30':
                        if summonerIDs[x] not in rRank.text:
                                summonerRanks.append('Unranked')
                        elif "RANKED_SOLO_5x5" not in str(rRank.json()[summonerIDs[x]]):
                                summonerRanks.append('Unranked')
                        else:
                                summonerRanks.append(str(str(rRank.json()[summonerIDs[x]][0]["tier"]).title() + " " + str(rRank.json()[summonerIDs[x]][0]["entries"][0]["division"]) + " (" + str(rRank.json()[summonerIDs[x]][0]["entries"][0]["leaguePoints"]) + " LP)"))
                else:
                        summonerRanks.append('0')
                        
                
        # return str(gameMode + "\n---\n" + summonerNames[0] + " | Level " + summonerLevels[0] + " | " + summonerChampNames[0] + "\n" + summonerNames[1] + " | Level " + summonerLevels[1] + " | " + summonerChampNames[1] + "\n" + summonerNames[2] + " | Level " + summonerLevels[2] + " | " + summonerChampNames[2] + "\n" + summonerNames[3] + " | Level " + summonerLevels[3] + " | " + summonerChampNames[3] + "\n" + summonerNames[4] + " | Level " + summonerLevels[4] + " | " + summonerChampNames[4] + "\n-vs-\n" + summonerNames[5] + " | Level " + summonerLevels[5] + " | " + summonerChampNames[5] + "\n" + summonerNames[6] + " | Level " + summonerLevels[6] + " | " + summonerChampNames[6] + "\n" + summonerNames[7] + " | Level " + summonerLevels[7] + " | " + summonerChampNames[7] + "\n" + summonerNames[8] + " | Level " + summonerLevels[8] + " | " + summonerChampNames[8] + "\n" + summonerNames[9] + " | Level " + summonerLevels[9] + " | " + summonerChampNames[9] + "\n")
                
        finalGameInfo = str(gameMode + "\n---\n")
        for x in range(0, (len(summonerNames)/2)):
                finalGameInfo+=str(summonerNames[x] + " | Level " + summonerLevels[x] + " | " + summonerChampNames[x])
                if summonerRanks[x] != '0':
                        finalGameInfo+=str(" | " + summonerRanks[x])
                finalGameInfo+=str(" // \n")
        finalGameInfo+=str("--vs--\n")
        for x in range((len(summonerNames)/2), len(summonerNames)):
                finalGameInfo+=str(summonerNames[x] + " | Level " + summonerLevels[x] + " | " + summonerChampNames[x])
                if summonerRanks[x] != '0':
                        finalGameInfo+=str(" | " + summonerRanks[x])
                finalGameInfo+=str(" // \n")
                
        return str(finalGameInfo)


if __name__ == '__main__':

        logging.basicConfig(level=logging.DEBUG,
                                                format='%(levelname)-8s %(message)s')

        xmpp = LolBot((xmppLoLUsername + '@pvp.net'), ('AIR_' + xmppLoLPassword))

        xmpp['feature_mechanisms'].unencrypted_plain = True
        xmpp.register_plugin('xep_0045')

        # Get champion list as json, one time on startup
        championListByID = RiotApiGetChampionList()

        # Get admin's name
        mainAccName = RiotApiGetName(mainAcc)
        
        if xmpp.connect((xmppLoLIP, xmppLoLPort), use_ssl=True):
                xmpp.process(block=True)
                print("Done")
        else:
                print("Unable to connect.")
