from types import SimpleNamespace
import requests
import mpv
import json

from credentials import Credentials

player = mpv.MPV(ytdl=True, hwdec="auto")


credentials = Credentials()

request = requests.get("https://api.twitch.tv/helix/streams?first=20", headers=credentials.headers)
top_streams = request.json()["data"]

streams = [(index, stream["user_login"]) for index, stream in enumerate(top_streams)]

print(streams)

# print(credentials.expires)
# print(credentials.as_headers())

# access_token = requests.post('https://id.twitch.tv/oauth2/token', data=credentials.as_data())
# print(access_token.json())

# print(headers)

# top_streams = requests.get("https://api.twitch.tv/helix/streams?first=20", headers=headers)
# top_streams = top_streams.json()["data"]

# user_login = [stream["user_login"] for stream in top_streams if stream["user_login"] == "fps_shaka"]
# player.play(f"https://twitch.tv/{user_login[0]}")
# player.wait_for_playback()
# del player

# print(access_token.text)

# p_headers = {
#     "access_token":"suq7ey4wvi0x52qoci7fb83jfgrx8k",
#     "expires_in":5253690,
#     "token_type":"bearer"
# }

# top_headers = {
#     "Authorization":"Bearer suq7ey4wvi0x52qoci7fb83jfgrx8k",
#     "Client-Id":"bf4o7stpox92oj5mktry8jptqj34jr"
# }

# request = requests.get("https://api.twitch.tv/helix/streams?first=20", headers=top_headers)
# response = request.json()["data"]

# user_login = [stream["user_login"] for stream in response if stream["user_login"] == "fps_shaka"]

# streamer_request = requests.get(f"https://api.twitch.tv/helix/streams?user_login={user_login[0]}", headers=top_headers)
# print(streamer_request.text)

