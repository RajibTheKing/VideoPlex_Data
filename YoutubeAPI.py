
import requests
import json
import time
import datetime
import isodate

'''
This list shows: All Youtube Video Categories by categoryId

2 - Autos & Vehicles
1 -  Film & Animation
10 - Music
15 - Pets & Animals
17 - Sports
18 - Short Movies
19 - Travel & Events
20 - Gaming
21 - Videoblogging
22 - People & Blogs
23 - Comedy
24 - Entertainment
25 - News & Politics
26 - Howto & Style
27 - Education
28 - Science & Technology
29 - Nonprofits & Activism
30 - Movies
31 - Anime/Animation
32 - Action/Adventure
33 - Classics
34 - Comedy
35 - Documentary
36 - Drama
37 - Family
38 - Foreign
39 - Horror
40 - Sci-Fi/Fantasy
41 - Thriller
42 - Shorts
43 - Shows
44 - Trailers

'''


class YoutubeAPI:
    def __init__(self):
        print("Inside YoutubeAPI Constructor")
        self.apiKey = "AIzaSyBKwvNR4nPv60u2sU-6Q14WSWDBqog-iLs"

    def fetchVideoDetails(self, videoLink):
        try:
            urlStr = "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,id,status&id=" + self.getVideoID(videoLink) + "&key=" + self.apiKey
            response = requests.get(urlStr)
            jsonData = response.json()

            # Start: Preprocess Video Details (IMPORTANT --> for further tasks)
            jsonData = jsonData['items'][0]
            jsonData = self.removeElements(jsonData, ["tags", "localized", "liveBroadcastContent", "kind", "etag", "description"])
            jsonData = self.fixDuration(jsonData)
            jsonData = self.fixThumbnailURL(jsonData)
            # End: preprocessing

            jsonStr = json.dumps(jsonData, indent=4, ensure_ascii=False).encode('UTF-8')
            print(jsonStr.decode())
            return jsonData
        except:
            print("ERROR: fetchVideoDetails")
            return None
    
    def getVideoID(self, videoLink):
        startIndex = videoLink.find("v=") + 2
        videoLink = videoLink[startIndex: len(videoLink)]
        return videoLink
    
    def fixDuration(self, data):
        value = data['contentDetails']['duration']
        dur = isodate.parse_duration(value)
        fixedDuration = str(datetime.timedelta(seconds=dur.total_seconds()))
        data['contentDetails']['duration'] = fixedDuration
        
        return data

    def fixThumbnailURL(self, data):
        thumbnails = data['snippet']['thumbnails']
        maxRes = 0
        thumbUrl = ""
        for x in thumbnails.keys():
            curRes = thumbnails[x]['width'] * thumbnails[x]['height']
            if  curRes > maxRes:
                maxRes = curRes
                thumbUrl = thumbnails[x]['url']
        data['snippet']['thumbnails'] = thumbUrl
        return data

    def removeElementByName(self, data, element, depth):
        if type(data) != dict:
            return data

        if element in data.keys():
            del data[element]
        
        for x in data.keys():
            data[x] = self.removeElementByName(data[x], element, depth+1)

        return data
    
    def removeElements(self, data, elements):
        for x in elements:
            data = self.removeElementByName(data, x, 0)
        
        return data

        


