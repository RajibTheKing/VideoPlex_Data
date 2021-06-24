
from YoutubeAPI import YoutubeAPI
import sys
import json
from json import decoder

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






def main(argv):
    print("JSONModifier Started with ARG: ", argv)
    jm = JSONModifier()
    jsonData = jm.readJSON("Video.json")
    if jsonData != None:
        jm.writeJSON(jsonData, "Video_modified.json")

    
    if len(argv) == 2:
        #Means we have video Link and Category
        videoLink = argv[0]
        category = argv[1]
        youtubeAPI = YoutubeAPI()
        videoDetails = youtubeAPI.fetchVideoDetails(videoLink)


if __name__ == "__main__":
    main(sys.argv[1:])