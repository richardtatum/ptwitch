import json
from types import SimpleNamespace
import requests
import mpv
import typer

from credentials import Credentials

player = mpv.MPV(ytdl=True, hwdec="auto")
app = typer.Typer()
credentials = Credentials()

@app.command()
def test():
    typer.echo("Test complete!")

@app.command()
def top(number_of_streams: int, language: str = "en"):
    request = requests.get(f"https://api.twitch.tv/helix/streams?first={number_of_streams}&language={language}", headers=credentials.headers)

    data = request.json()["data"]
    top_streams = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

    streams = dict([(index, stream) for index, stream in enumerate(top_streams)])

    print("Top 20 Twitch Streams")
    for index in streams:
        stream = streams[index]
        streamer = stream.user_name
        game = stream.game_name
        print(f"{index+1}: {streamer} - {game}")

    selected = int(input("Select stream to play: "))
    streamer = streams[selected-1].user_name

    player.play(f"https://twitch.tv/{streamer}")
    player.wait_for_playback()

@app.command()
def stream(user):
    player.play(f"https://twitch.tv/{user}")
    player.wait_for_playback()

if __name__ == "__main__":
    app()