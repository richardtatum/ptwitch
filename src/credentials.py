from datetime import datetime, timedelta
import json
from types import SimpleNamespace
import requests

TWITCH_OAUTH_URL = "https://id.twitch.tv/oauth2/token"
CONFIG_PATH = "config/config.json"
AUTH_PATH = "config/auth.json"

class Credentials:
    def __init__(self) -> None:
        self.__get_config()
        self.authorize()

    @property
    def headers(self):
        if not self.valid:
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

    @property
    def valid(self):
        return datetime.now() < self.expires

    def __get_config(self):
        with open(CONFIG_PATH, "r") as config_file:
            file = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))
            self.client_id = file.client_id
            self.client_secret = file.client_secret
            self.grant_type = file.grant_type

    def __get_auth(self):
        try:
            with open(AUTH_PATH, "r") as auth_file:
                # print("Loading from file")
                file = json.load(auth_file, object_hook=lambda d: SimpleNamespace(**d))

                # Date is stored as a string
                self.expires = datetime.strptime(file.expires, "%Y-%m-%d %H:%M:%S.%f")
                self.access_token = file.access_token
        except FileNotFoundError:
                # print("File not found")
                return False

        # Confirm the file loaded correctly
        return self.access_token is not None and self.expires is not None

    def __set_auth(self, access_token, expires_in):
        # print("Setting auth values")
        self.access_token = access_token
        self.expires = self.__get_expiry_date(expires_in)

        auth = {
            "access_token": self.access_token,
            "expires": self.expires
        }

        with open(AUTH_PATH, "w") as auth_file:
            # Default function just outputs the date as a string
            json.dump(auth, auth_file, default=lambda d: d.__str__())

    def __get_expiry_date(self, expires_in):
        return datetime.now() + timedelta(seconds=expires_in)

    def authorize(self):
        loaded_from_file = self.__get_auth()

        # print("Loaded from file: ", loaded_from_file)
        # print("Valid: ", self.valid)
        if loaded_from_file and self.valid:
            return

        # print("Obtaining values from twitch")
        request = requests.post(TWITCH_OAUTH_URL, self.data)
        response = request.json()

        access_token = response["access_token"]
        expires_in = response["expires_in"]
        
        self.__set_auth(access_token, expires_in)
