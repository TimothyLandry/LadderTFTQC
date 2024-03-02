import requests
import json
from time import sleep

class Api:
    def __init__(self, startTime):
        # API Key
        f = open("./config.json")
        apiKey = json.load(f)["apiKey"]
        # Headers
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
    
    def getSummonerPuuid(self, summonerName):
        return (self.abstractApiCall("na1",f"tft/summoner/v1/summoners/by-name/{summonerName}", None))["puuid"]
    
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
    
    def getMatches(self, name):
        puuid = self.getSummonerPuuid(name)
        matchIds = self.getMatchIds(puuid)
        matches = []
        for m in matchIds:
            matches.append(self.getMatch(m))
            sleep(1)