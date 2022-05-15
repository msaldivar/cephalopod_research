import requests

from cephalopod_research.tests import config


class CryptowatchMarketsAPIWrapper:
    """A simple wrapper for the cryptowatch /markets endpoint"""

    def __init__(self):
        self.url = config.API_BASE_URL + 'markets'
        self.cw_api = requests.Session()

        if config.API_KEY == 'replace_me':
            raise ValueError('Add api key to config.py')

        self.headers = {
            "Accept": "application/json",
            "X-CW-API-Key": config.API_KEY,
        }

    def get(self, params=''):
        """Perform the request.get call based on the passed in params"""

        url = self.url + params
        response = self.cw_api.get(
            url,
            headers=self.headers,
            verify=True,
            timeout=(5, 20),
            allow_redirects=True,
        )

        return response
