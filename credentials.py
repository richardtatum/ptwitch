from datetime import datetime, timedelta
import json
from types import SimpleNamespace
import requests

TWITCH_OAUTH_URL = "https://id.twitch.tv/oauth2/token"
CONFIG_PATH = "config.json"

class Credentials(object):
    def __init__(self) -> None:
        self.load_from_file()
        self.authorize()

    @property
    def headers(self):
        if not self.valid():
            print("Access token expired. Re-authorizing")
            self.authorize()

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }

    @property
    def data(self):
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': self.grant_type
        }

    def load_from_file(self):
        with open(CONFIG_PATH, "r") as config_file:
            file = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))
            self.client_id = file.client_id
            self.client_secret = file.client_secret
            self.grant_type = file.grant_type

    def authorize(self):
        request = requests.post(TWITCH_OAUTH_URL, self.data)
        response = request.json()

        expires_in = response["expires_in"]
        self.access_token = response["access_token"]
        self.expires = datetime.now() + timedelta(seconds=expires_in)

    def valid(self):
        return datetime.now() < self.expires
