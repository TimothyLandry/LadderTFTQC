import requests
import json
from time import sleep

class Api:
    def __init__(self, startTime):
        f = open("./config.json")
        apiKey = json.load(f)["riotApiKey"]

        self.headers =   {
            "Accept-Language": "en,en-US;q=0.5",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": f"{apiKey}"
        }
        self.startTime = startTime

    def abstractApiCall(self, region, endpoint, params):
        url = f"https://{region}.api.riotgames.com/"
        return requests.get(f"{url}{endpoint}", headers=self.headers, params=params).json()

    def getSummonerId(self, summonerName):
        return (self.abstractApiCall("na1", f"tft/summoner/v1/summoners/by-name/{summonerName}", None))["id"]
    
    def getSummonerPuuid(self, name, tag):
        return (self.abstractApiCall("americas",f"riot/account/v1/accounts/by-riot-id/{name}/{tag}", None))["puuid"]
    
    def getSummonerProfile(self, summonerName):
        summonerId = self.getSummonerId(summonerName)
        return self.abstractApiCall("na1",f"tft/league/v1/entries/by-summoner/{summonerId}", None)
    
    def getMatchIds(self, puuid):
        params = {
            "startTime": self.startTime,
            "count": 200
        }
        return self.abstractApiCall("americas",f"tft/match/v1/matches/by-puuid/{puuid}/ids", params)
    
    def getMatch(self, id):
        return self.abstractApiCall("americas",f"tft/match/v1/matches/{id}", None)
    
    def getMatches(self, name, tag):
        puuid = self.getSummonerPuuid(name, tag)
        matchIds = self.getMatchIds(puuid)
        matches = []
        for m in matchIds:
            matches.append(self.getMatch(m))
            # 100calls/2min workaround
            sleep(1.3)
        return matches