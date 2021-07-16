
from YoutubeAPI import YoutubeAPI
import sys
import json
from json import decoder
import datetime
import time
from rapidApi import RapidApi

class JSONModifier:
    def __init__(self):
        print("Inside JSONModifier Constructor")
    
    def readJSON(self, fileName):
        try:
            with open(fileName, encoding='UTF-8') as json_file:
                data = json.load(json_file)
                #str = json.dumps(data, indent=4)
                #print(str)
                return data
        except:
            return None
    
    def writeJSON(self, jsonData, fileName):
        encodedStr = json.dumps(jsonData, indent=4, ensure_ascii=False).encode('UTF-8')
        decodedStr = encodedStr.decode()
        

        file = open(fileName, "w+", encoding="UTF-8")
        file.write(decodedStr)
        file.close()


    def updateVideoItem(self, jsonData, videoDetails, videoUrl, imdbDetail):
        for x in jsonData["VideoData"]:
            if x["URL"] == videoUrl:
                if videoDetails == None:
                    jsonData["VideoData"].remove(x)
                else:
                    x["ID"] = videoDetails["id"]
                    # x["Title"]        --> Untouched
                    # x["Category"]     --> Untouched
                    # x["Cast"]    --> Untouched
                    x["Thumbnail_URL"] = videoDetails["snippet"]["thumbnails"]
                    x["PublishedAt"] = videoDetails["snippet"]["publishedAt"]
                    x["ViewCount"] = videoDetails["statistics"]["viewCount"]
                
                    if "likeCount" in videoDetails["statistics"].keys():
                        x["LikeCount"] = videoDetails["statistics"]["likeCount"]
                    else:
                        x["LikeCount"] = "0"
                    
                    if "dislikeCount" in videoDetails["statistics"].keys():
                        x["DislikeCount"] = videoDetails["statistics"]["dislikeCount"]
                    else:
                        x["DislikeCount"] = "0"

                    # x["URL"]          --> Untouched
                    x["Duration"] = videoDetails["contentDetails"]["duration"]
                    # x["Genre"]        --> Untouched
                    x["Quality"] = videoDetails["contentDetails"]["definition"]
                    x["Country"] = []
                    # x["Language"]     --> Untouched
                    # x["Director"]     --> Untouched
                    # x["Producer"]     --> Untouched
                    x["ChannelTitle"] = videoDetails["snippet"]["channelTitle"]
                    x["UpdatedAt"] = str(time.time())
                    # x["Ratings"]       --> Untouched
                    if x["Category"] == "Movie":
                        x["Title"] = imdbDetail["Title"]
                        x["Year"] = imdbDetail["Year"]
                        x["Released"] = imdbDetail["Released"]
                        x["Writer"] = imdbDetail["Writer"]
                        x["Plot"]  = imdbDetail["Plot"]
                        x["Poster"] = imdbDetail["Poster"]
                        x["IMDBId"] =  imdbDetail["imdbID"]
                        x["BoxOffice"] =  imdbDetail["BoxOffice"]
                        x["Production"]= imdbDetail["Production"]
                        x["Cast"] = imdbDetail["cast"]
                        x["Genre"] = imdbDetail["Genre"]
                        x["Director"] = imdbDetail["Director"]
                        x["Language"] = imdbDetail["Language"]
                        x["Country"] = imdbDetail["Country"]
                        x["Ratings"] = imdbDetail["Ratings"]



        return jsonData

    
    def insertVideoItem(self, jsonData, videoDetails, videoUrl, title, category, imdbDetail):
        if videoDetails == None:
            return
        x = dict()
        x["ID"] = videoDetails["id"]
        x["Title"] = title
        x["Category"] = category
        x["Cast"] = []
        x["Thumbnail_URL"] = videoDetails["snippet"]["thumbnails"]
        x["PublishedAt"] = videoDetails["snippet"]["publishedAt"]
        x["ViewCount"] = videoDetails["statistics"]["viewCount"]

        if "likeCount" in videoDetails["statistics"].keys():
            x["LikeCount"] = videoDetails["statistics"]["likeCount"]
        else:
            x["LikeCount"] = "0"
        
        if "dislikeCount" in videoDetails["statistics"].keys():
            x["DislikeCount"] = videoDetails["statistics"]["dislikeCount"]
        else:
            x["DislikeCount"] = "0"

        x["URL"] = videoUrl
        x["Duration"] = videoDetails["contentDetails"]["duration"]
        x["Genre"] = []
        x["Quality"] = videoDetails["contentDetails"]["definition"]
        x["Country"] = []
        x["Language"] = []
        x["Director"] = []
        x["Producer"] = []
        x["ChannelTitle"] = videoDetails["snippet"]["channelTitle"]
        x["UpdatedAt"] = str(time.time())
        x["Ratings"] = []

        x["Year"] = ""
        x["Released"] = ""
        x["Writer"] = []
        x["Plot"]  = ""
        x["Poster"] = ""
        x["IMDBId"] =  ""
        x["BoxOffice"] =  ""
        x["Production"]= []

        if category == "Movie":
            x["Title"] = imdbDetail["Title"]
            x["Year"] = imdbDetail["Year"]
            x["Released"] = imdbDetail["Released"]
            x["Writer"] = imdbDetail["Writer"]
            x["Plot"]  = imdbDetail["Plot"]
            x["Poster"] = imdbDetail["Poster"]
            x["IMDBId"] =  imdbDetail["imdbID"]
            x["BoxOffice"] =  imdbDetail["BoxOffice"]
            x["Production"]= imdbDetail["Production"]
            x["Cast"] = imdbDetail["cast"]
            x["Genre"] = imdbDetail["Genre"]
            x["Director"] = imdbDetail["Director"]
            x["Language"] = imdbDetail["Language"]
            x["Country"] = imdbDetail["Country"]
            x["Ratings"] = imdbDetail["Ratings"]
            

        jsonData["VideoData"].append(x)
        return jsonData

def getExistingVideoLinks(jsonData):
    urlList = []
    for x in jsonData["VideoData"]:
        urlList.append(x["URL"])
    
    return urlList

def getExistingImdbIDs(jsonData):
    imdbIds = []
    for x in jsonData["VideoData"]:
        if len(x["IMDBId"]) > 0:
            imdbIds.append(x["IMDBId"])
    
    return imdbIds

def getVideoDataByLink(jsonData, videoLink):
    for x in jsonData["VideoData"]:
        if x["URL"] == videoLink:
            return x

def main(argv):
    print("JSONModifier Started with ARG: ", argv)
    jm = JSONModifier()
    jsonData = jm.readJSON("Video.json")
    if jsonData == None:
        print("FAILED: JSON parsing failed")
        return

    instruction = argv[0]

    if instruction == "UPDATE":
        #Means we have video Link and Category
        videoLink = argv[1]

        oldVideoData = getVideoDataByLink(jsonData, videoLink)
        youtubeAPI = YoutubeAPI()
        videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
        imdbDetails = None

        if oldVideoData["Category"] == "Movie":
            rapidApi = RapidApi()
            imdbID = oldVideoData["IMDBId"]
            imdbDetails = rapidApi.fetchMovieDetail(imdbID)

        
        jsonData = jm.updateVideoItem(jsonData, videoDetails, videoLink, imdbDetails)
        jm.writeJSON(jsonData, "Video.json")
        pass
    
    elif instruction == "UPDATE_ALL":
        youtubeAPI = YoutubeAPI()
        rapidApi = RapidApi()

        for x in jsonData["VideoData"]:
            videoLink = x["URL"]
            category = x["Category"]
            imdbID = ""
            imdbDetails = None
            if category == "Movie":
                imdbID = x["IMDBId"]
                imdbDetails = rapidApi.fetchMovieDetail(imdbID)
            
            videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
            jsonData = jm.updateVideoItem(jsonData, videoDetails, videoLink, imdbDetails)
        
        jm.writeJSON(jsonData, "Video.json")


    elif instruction == "INSERT":
        category = argv[1]
        title = argv[2]
        videoLink = argv[3]
        imdbID = ""
        if category == "Movie":
            imdbID = argv[4]
        
        print("Category, Title, videoLink = ", {category, title, videoLink})

        urlList = getExistingVideoLinks(jsonData)
        imdbList = getExistingImdbIDs(jsonData)
        if videoLink in urlList:
            print("FAILED: this link is already existed in JSON")
        elif imdbID in imdbList:
            print("FAILED: this imdbID is already existed in JSON")
        else:
            youtubeAPI = YoutubeAPI()
            videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
            imdbDetails = None
            if category == "Movie" and videoDetails != None:
                rapidApi = RapidApi()
                imdbDetails = rapidApi.fetchMovieDetail(imdbID)

            jm.insertVideoItem(jsonData, videoDetails, videoLink, title, category, imdbDetails)
            jm.writeJSON(jsonData, "Video.json")
    elif instruction == "CHECK_YTD":
        videoLink = argv[1]
        youtubeAPI = YoutubeAPI()
        videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
    elif instruction == "CHECK_IMDB":
        imdbID = argv[1]
        rapidApi = RapidApi()
        movieDetails = rapidApi.fetchMovieDetail(imdbID)
    elif instruction == "isPlayable":
        videoLink = argv[1]
        youtubeAPI = YoutubeAPI()
        videoDetails = youtubeAPI.checkPlayability(videoLink)
    else:
        pass





if __name__ == "__main__":
    main(sys.argv[1:])