import json
from types import SimpleNamespace
from unicodedata import name
import requests
import mpv
import typer

from credentials import Credentials

player = mpv.MPV(ytdl=True, hwdec="auto")
app = typer.Typer()
credentials = Credentials()

@app.command()
def top(stream_count: int, game_id: str = "", language: str = "en"):
    url = f"https://api.twitch.tv/helix/streams?first={stream_count}&language={language}"
    if game_id:
        url += f"&game_id={game_id}"

    request = requests.get(url, headers=credentials.headers)

    data = request.json()["data"]
    top_streams = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
    streams = dict([(index, stream) for index, stream in enumerate(top_streams)])
    
    if len(streams) == 0:
        print("No streams found!")
        return

    print(f"Top {stream_count} Twitch Streams")
    for index in streams:
        stream = streams[index]
        streamer = stream.user_name
        game = stream.game_name
        print(f"[{language}] {index+1}: {streamer} - {game}")

    selected = int(input("Select stream to play: "))
    streamer = streams[selected-1].user_name

    player.play(f"https://twitch.tv/{streamer}")
    player.wait_for_playback()

@app.command()
def stream(user):
    player.play(f"https://twitch.tv/{user}")
    player.wait_for_playback()

@app.command()
def game(game_name: str, stream_count: int = 10,  language: str = "en"):
    request = requests.get(f"https://api.twitch.tv/helix/games?name={game_name}", headers=credentials.headers)

    data = request.json()["data"]
    matching_games = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
    games = dict([(index, game) for index, game in enumerate(matching_games)])

    if len(games) == 0:
        print("No matching games found.")
        return

    # Assign the id from the first game
    game_id = games[0].id

    if len(games) > 1:
        print(f"Matching games:")
        for index in games:
            game = games[index]
            print(f"{index+1}: {game.name} - {game.id}")

        selected = int(input("Select the game: "))
        game_id = games[selected-1].id

    top(stream_count, game_id, language)

if __name__ == "__main__":
    app()