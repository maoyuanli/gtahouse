# for security reason the tokens used for the project is saved somewhere else and is not uploaded to GitHub.
# this utility class help to fetch it

import json
import os


class TokenFetcher():

    def __init__(self, token_file):
        self.token_file = token_file

    def fetch_token(self, key):
        cur_path = os.path.dirname(__file__)
        par_path = os.path.dirname(os.path.dirname(cur_path))
        while os.path.isfile(os.path.join(par_path, self.token_file)) == False:
            par_path = os.path.dirname(os.path.dirname(par_path))
        token = json.load(open(os.path.join(par_path, self.token_file), 'r'))
        return token[key]
