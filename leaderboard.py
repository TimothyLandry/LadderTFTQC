from api import Api
from stats import Stats
import json

def getLeaderboardOutput():
    api = Api(1709445434) 
    #summonerNames = ["davidas", "sadivad", "hanneko", "chekko", "shawinigan", "geehess"]
    summonerNames = ["shawinigan"]
    output=[]
    for summonerName in summonerNames:
        print(summonerName)

        matches = api.getMatches(summonerName)
        puuid = api.getSummonerPuuid(summonerName)

        stats = Stats(puuid, matches)
        data = stats.getPlayerData()

        profile = api.getSummonerProfile(summonerName)
        print(profile)
        jsonProfile = {
            "profile": profile,
            "name": summonerName,
            "rank": f"{profile[0]['tier']} {profile[0]['rank']} {profile[0]['leaguePoints']} lp",
            "recombobulator": stats.countRecombobulator(data),
            "threeStars": stats.countThreeStarUnits(data),
            "featherknight": stats.countGamesAsFeatherknight(data)
        }
        output.append(jsonProfile)

    raw = json.dumps(output, indent=3)
    return raw