import requests
import mpv

from credentials import Credentials

player = mpv.MPV(ytdl=True, hwdec="auto")
credentials = Credentials()

# request = requests.get("https://api.twitch.tv/helix/streams?first=20", headers=credentials.headers)
# top_streams = request.json()["data"]

# streams = [(index, stream["user_login"]) for index, stream in enumerate(top_streams)]

# print(streams)