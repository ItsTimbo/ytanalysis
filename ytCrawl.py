from googleapiclient.discovery import build
import pprint as p
import wordAnalysis
import configparser as cfp

config = cfp.ConfigParser()
config.read('config.ini')

API_KEY = config['Api']['key']
MAX_RESULTS = config['Settings']['results']

youtube = build('youtube', 'v3', developerKey=API_KEY)

def getChannelID(channelname):
    request = youtube.search().list(
        type='channel',
        part='snippet',
        q = channelname,
        maxResults=1
    )

    result = request.execute()

    return result['items'][0]['id']['channelId']

def getVideoIDs(channelID):
    request = youtube.search().list(
        part='snippet',
        channelId=channelID,
        maxResults=MAX_RESULTS,
        order='date',
        type='video'
    )
    
    result = request.execute()['items']

    if not result:
        return False
    
    videoIDs = []
    for video in result:
        videoIDs.append(video['id']['videoId'])
    
    return videoIDs

def getVideoDetails(channelID):
    videoIDs = getVideoIDs(channelID)
    
    videoDetails = []
    for videoID in videoIDs:
        request = youtube.videos().list(
            part='snippet',
            id=videoID
        )
        results = request.execute()['items']
        
        p.pprint(results[0])
        print("="*50)
        
        if not results:
            return False
        
        videoDetails.append(results[0]['snippet']['description'][:500])
    
    return videoDetails

def getChannelDescription(channelID):
    request = youtube.channels().list(
        part='snippet,contentDetails',
        id=channelID
    )
    
    result = request.execute()
    
    if result['items']:
        return result['items'][0]['snippet']['description']
    else:
        return False

if __name__ == "__main__":
    usernames = ['HandOfUncut']

    channelID = getChannelID(usernames[0])
    
    result = []
    result.append(getChannelDescription(channelID))
    result.append(getVideoDetails(channelID))