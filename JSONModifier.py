
from YoutubeAPI import YoutubeAPI
import sys
import json
from json import decoder
import datetime
import time

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


    def updateVideoItem(self, jsonData, videoDetails, videoUrl):
        for x in jsonData["VideoData"]:
            if x["URL"] == videoUrl:
                if videoDetails == None:
                    jsonData["VideoData"].remove(x)
                else:
                    x["ID"] = videoDetails["id"]
                    # x["Title"]        --> Untouched
                    # x["Category"]     --> Untouched
                    # x["Artist_ID"]    --> Untouched
                    x["Thumbnail_URL"] = videoDetails["snippet"]["thumbnails"]
                    x["PublishedAt"] = videoDetails["snippet"]["publishedAt"]
                    x["ViewCount"] = videoDetails["statistics"]["viewCount"]
                    x["LikeCount"] = videoDetails["statistics"]["likeCount"]
                    x["DislikeCount"] = videoDetails["statistics"]["dislikeCount"]
                    # x["URL"]          --> Untouched
                    x["Duration"] = videoDetails["contentDetails"]["duration"]
                    # x["Genre"]        --> Untouched
                    x["Quality"] = videoDetails["contentDetails"]["definition"]
                    # x["Country"]      --> Untouched
                    # x["Language"]     --> Untouched
                    # x["Director"]     --> Untouched
                    # x["Producer"]     --> Untouched
                    x["ChannelTitle"] = videoDetails["snippet"]["channelTitle"]
                    x["UpdatedAt"] = str(time.time())
                    # x["Rating"]       --> Untouched


        return jsonData

    
    def insertVideoItem(self, jsonData, videoDetails, videoUrl, title, category):
        if videoDetails == None:
            return
        x = dict()
        x["ID"] = videoDetails["id"]
        x["Title"] = title
        x["Category"] = category
        x["Artist_ID"] = []
        x["Thumbnail_URL"] = videoDetails["snippet"]["thumbnails"]
        x["PublishedAt"] = videoDetails["snippet"]["publishedAt"]
        x["ViewCount"] = videoDetails["statistics"]["viewCount"]
        x["LikeCount"] = videoDetails["statistics"]["likeCount"]
        x["DislikeCount"] = videoDetails["statistics"]["dislikeCount"]
        x["URL"] = videoUrl
        x["Duration"] = videoDetails["contentDetails"]["duration"]
        x["Genre"] = []
        x["Quality"] = videoDetails["contentDetails"]["definition"]
        x["Country"] = ""
        x["Language"] = ""
        x["Director"] = []
        x["Producer"] = []
        x["ChannelTitle"] = videoDetails["snippet"]["channelTitle"]
        x["UpdatedAt"] = str(time.time())
        x["Rating"] = []

        jsonData["VideoData"].append(x)
        return jsonData

def getExistingVideoLinks(jsonData):
    urlList = []
    for x in jsonData["VideoData"]:
        urlList.append(x["URL"])
    
    return urlList


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
        youtubeAPI = YoutubeAPI()
        videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
        jsonData = jm.updateVideoItem(jsonData, videoDetails, videoLink)
        jm.writeJSON(jsonData, "Video.json")
    
    elif instruction == "UPDATE_ALL":
        youtubeAPI = YoutubeAPI()
        urlList = getExistingVideoLinks(jsonData)

        for videoLink in urlList:
            videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
            jsonData = jm.updateVideoItem(jsonData, videoDetails, videoLink)
            jm.writeJSON(jsonData, "Video.json")


    elif instruction == "INSERT":
        category = argv[1]
        title = argv[2]
        print("Category, Title = ", {category, title})
        videoLink = argv[3]
        urlList = getExistingVideoLinks(jsonData)
        if videoLink in urlList:
            print("FAILED: this link is already existed in JSON")
        else:
            youtubeAPI = YoutubeAPI()
            videoDetails = youtubeAPI.fetchVideoDetails(videoLink)
            jm.insertVideoItem(jsonData, videoDetails, videoLink, title, category)
            jm.writeJSON(jsonData, "Video.json")




if __name__ == "__main__":
    main(sys.argv[1:])