import json

class Stats:
    def __init__(self, puuid, raw):
        self.puuid = puuid
        self.raw = raw
        config = json.load(open("./config/config.json"))
        self.currentSet = config["currentSet"]

    def getPlayerData(self):
        data = []
        for i in self.raw:
            try:
                for p in i["info"]["participants"]:
                    if(p["puuid"] == self.puuid):
                        data.append(p)
            except(KeyError):
                print(i)
        return data
    
    def getMostGoldOnDeath(self, data):
        highest = 0
        for d in data:
            if(highest <= d["gold_left"]):
                highest=d["gold_left"]
        return highest
    
    def countFithPlaces(self, data):
        count = 0
        for d in data:
            if(d["placement"] == 5):
                count+=1
        return count
    
    def countThreeStarUnits(self, data):
        count = 0
        for d in data:
            for u in d["units"]:
                if(u["tier"] == 3):
                    count+=1
        return count
    
    def countGamesAsFeatherknight(self, data):
        count = 0
        for d in data:
            if(d["companion"]["species"] == "PetPenguKnight"):
                count+=1
        return count