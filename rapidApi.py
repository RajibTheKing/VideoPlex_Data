import requests
import json

# querystring = {"i":"nm0451321","r":"json"}
# response = requests.request("GET", url, headers=headers, params=querystring)
# myJson = json.loads(response.text)
# jsonStr = json.dumps(myJson, indent=4, ensure_ascii=False).encode('UTF-8')
# print(jsonStr.decode())


class RapidApi:
    def __init__(self):
        print("Inside RapidApi Constructor")
        try:
            with open("C:\\Users\\rajib\\AndroidStudioProjects\\PersonalKeys\\securedKeys.json", encoding='UTF-8') as json_file:
                data = json.load(json_file)
                print(data)
                self.apiKey = data["rapid_key"]

                self.service = {
                    "IMDB_Alternative" : {
                        "url": "https://movie-database-imdb-alternative.p.rapidapi.com/",
                        "headers": {
                            'x-rapidapi-key': self.apiKey,
                            'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
                        }

                    },
                    "IMDB_Unofficial" : {
                        "url": "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/",
                        "headers": {
                            'x-rapidapi-key': self.apiKey,
                            'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
                        }

                    }
                }
        except:
            print("File read ERROR")

    
    def fetchMovieDetail(self, imdbID):
        IMDB_AlternativeData = self.fetchFromIMDB_Alternative(imdbID)
        jsonStr = json.dumps(IMDB_AlternativeData, indent=4, ensure_ascii=False).encode('UTF-8')
        print("IMDBAlternative: ", jsonStr.decode())

        IMDB_UnofficialData = self.fetchFromIMDB_Unofficial(imdbID)
        jsonStr = json.dumps(IMDB_UnofficialData, indent=4, ensure_ascii=False).encode('UTF-8')
        print("IMDB_Unofficial: ", jsonStr.decode())


        #Fix Cast Issue
        ret = self.fixCast(IMDB_AlternativeData, IMDB_UnofficialData)

        #Fix Poster Issue
        if len(IMDB_UnofficialData["poster"]) > 0:
            ret["Poster"] = IMDB_UnofficialData["poster"]


        #Fix Gnre
        ret["Genre"] = [x.strip() for x in ret["Genre"].split(",")]

        #Fix Director
        ret["Director"] = [x.strip() for x in ret["Director"].split(",")]

        #Fix Writer
        ret["Writer"] = [x.strip() for x in ret["Writer"].split(",")]

        #Fix Production
        ret["Production"] = [x.strip() for x in ret["Production"].split(",")]

        #Fix Language
        ret["Language"] = [x.strip() for x in ret["Language"].split(",")]

        #Fix Country
        ret["Country"] = [x.strip() for x in ret["Country"].split(",")]

        del ret['imdbRating']
        del ret['imdbVotes']
        del ret['Website']
        del ret['DVD']
        del ret['Type']
        del ret['Awards']
        del ret['Response']
        del ret['Rated']


        jsonStr = json.dumps(ret, indent=4, ensure_ascii=False).encode('UTF-8')
        print("ret: ", jsonStr.decode())
        return ret
        

    def fetchFromIMDB_Alternative(self, imdbID):
        querystring = {"i":imdbID,"r":"json"}
        response = requests.request("GET", self.service["IMDB_Alternative"]["url"], headers=self.service["IMDB_Alternative"]["headers"], params=querystring)
        myJson = json.loads(response.text)
        return myJson


    def fetchFromIMDB_Unofficial(self, imdbID):
        curUrl = self.service["IMDB_Unofficial"]["url"] + imdbID
        response = requests.request("GET", curUrl, headers=self.service["IMDB_Unofficial"]["headers"])
        myJson = json.loads(response.text)
        return myJson


    def fixCast(self, IMDB_AlternativeData, IMDB_UnofficialData):
        ret = IMDB_AlternativeData

        if len(IMDB_UnofficialData["cast"]) > 0:
            ret["cast"] = IMDB_UnofficialData["cast"]
        else:
            listActors = ret["Actors"].split(",")
            ret["cast"] = []
            for x in listActors:
                obj = {
                    "actor": x,
                    "actor_id": "",
                    "character": ""
                }
                ret["cast"].append(obj)
        
        del ret["Actors"]
        return ret

    

    


        


        

    
