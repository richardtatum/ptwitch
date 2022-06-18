import requests
import mpv

from credentials import Credentials

player = mpv.MPV(ytdl=True, hwdec="auto")
credentials = Credentials()

request = requests.get("https://api.twitch.tv/helix/streams?first=20", headers=credentials.headers)
top_streams = request.json()["data"]

streams = dict([(index, stream["user_login"]) for index, stream in enumerate(top_streams)])

print("Top 20 Twitch Streams")
for index in streams:
    print(f"{index+1}: {streams[index]}")

selected = int(input("Select stream to play: "))

streamer = streams[selected-1]

player.play(f"https://twitch.tv/{streamer}")
player.wait_for_playback()
