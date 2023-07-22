import requests
import html
import os
from dotenv import dotenv_values

cwd = os.getcwd()
API_Key = dotenv_values(f"{cwd}\\.env")['GOOGLE_TOKEN']

def getLatestVideo(Channel_ID):
    Max_Results = 1

    Request_URL = f'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={Channel_ID}&maxResults={Max_Results}&key={API_Key}&order=date'

    Response = requests.get(Request_URL)
    Response_Data = Response.json()

    vid_titleRAW = Response_Data["items"][0]["snippet"]["title"]

    vid_title = html.unescape(vid_titleRAW)
    vid_thumbnail = Response_Data["items"][0]["snippet"]["thumbnails"]["medium"]["url"]

    vid_link_id = Response_Data["items"][0]["id"]["videoId"]
    vid_link = f"https://www.youtube.com/watch?v={str(vid_link_id)}"


    return [vid_title, vid_link, vid_thumbnail]