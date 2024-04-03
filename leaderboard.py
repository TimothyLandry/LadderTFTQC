from api import Api
from stats import Stats
import time

def getProfiles():
    with open("players.txt", "r") as file:
        playerList = []
        for p in file:
            p = p.replace('\n','')
            playerList.append(p)

    startEpoch = 1710932400 # Wed Mar 20 2024 11:00:00 GMT+0000
    endEpoch = 1712142000 # Wed Apr 03 2024 11:00:00 GMT+0000
    api = Api(startEpoch, endEpoch) 
    output=[]
    for fullTag in playerList:
        name,tag = fullTag.split('#')
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - getMatches() {name}")

        matches = api.getMatches(name, tag)
        if(len(matches)>0):
            puuid = api.getSummonerPuuid(name, tag)

            stats = Stats(puuid, matches)
            data = stats.getPlayerData()

            profile = api.getSummonerProfile(puuid)
            
            if(len(profile)>0):
                jsonProfile = {
                    "name": name,
                    "tier": profile[0]['tier'],
                    "rank": profile[0]['rank'], 
                    "leaguePoints": profile[0]['leaguePoints'],
                    "recombobulator": stats.countRecombobulator(data),
                    "threeStars": stats.countThreeStarUnits(data),
                    "featherknight": stats.countGamesAsFeatherknight(data)
                }
                output.append(jsonProfile)
    return output

def getFeatherknightLeaderboard(jsonProfiles):
    sortedProfiles = sortByFeatherknight(jsonProfiles)
    leaderboard = "Ladder de games en tant que Pengu:"
    for p in sortedProfiles:
        if(p["featherknight"] >0):
            leaderboard += f"\n{p['name']} - {p['featherknight']} games"

    if(leaderboard == "Ladder de games en tant que Pengu:"):
        leaderboard += "\nNone...\nPengu va pleurer ce soir se couchant...\n"
    return leaderboard

def getRankLeaderboard(jsonProfiles):
    sortedProfiles = sortByRank(jsonProfiles)
    leaderboard = "Ladder (rank):"
    for p in sortedProfiles:
        leaderboard += f"\n{p['name']} - {p['tier']} {p['rank']} {p['leaguePoints']} lp"
        
    if(leaderboard == "Ladder (rank):"):
        leaderboard += "\nNone...\nPersonne aime le set11...\n"
    return leaderboard

def getRecombobulatorLeaderboard(jsonProfiles):
    sortedProfiles = sortByRecombobulator(jsonProfiles)
    leaderboard = "Ladder des gigachads:"
    for p in sortedProfiles:
        if(p["recombobulator"]>0):
            leaderboard += f"\n{p['name']} - {p['recombobulator']} recombobulator(s)"

    if(leaderboard == "Ladder des gigachads:"):
        leaderboard += "\nNone...\nChekko est pas fier...\n"
    return leaderboard

def getThreeStarsLeaderboard(jsonProfiles):
    sortedProfiles = sortByThreeStars(jsonProfiles)
    leaderboard = "Ladder des rerollers:"
    for p in sortedProfiles:
        if(p["threeStars"]>0):
            leaderboard += f"\n{p['name']} - {p['threeStars']} three stars units"

    if(leaderboard == "Ladder des rerollers:"):
        leaderboard += "\nNone...\nAppuyez dont sur D siboire...\n"
    return leaderboard

def sortByFeatherknight(jsonProfiles):
    sortedProfiles = sorted(jsonProfiles, key=lambda k: k['featherknight'],reverse=True)
    return sortedProfiles

def sortByRank(jsonProfiles):
    jsonProfiles = sorted(jsonProfiles, key=lambda k: k['leaguePoints'],reverse=True)
    sortedProfiles= []
    for tier in ["CHALLENGER", "GRANDMASTER", "MASTER", "DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]:
        for rank in ["I", "II", "III", "IV"]:
            for profile in jsonProfiles:
                if(profile['tier'] == tier and profile['rank'] == rank):
                    sortedProfiles.append(profile)
    return sortedProfiles

def sortByRecombobulator(jsonProfiles):
    sortedProfiles = sorted(jsonProfiles, key=lambda k: k['recombobulator'],reverse=True)
    return sortedProfiles

def sortByThreeStars(jsonProfiles):
    sortedProfiles = sorted(jsonProfiles, key=lambda k: k['threeStars'],reverse=True)
    return sortedProfiles
