from unittest import TestCase

from cephalopod_research.tests import config
from cephalopod_research.tests.config import cw_api


class TestListMarkets(TestCase):
    """Test class for /markets endpoint"""

    def test_list_all_markets(self):
        """Check return of /markets endpoint returns all markets for all exchanges."""

        url = config.API_BASE_URL + 'markets'
        response = cw_api.get(
            url,
            headers=config.headers,
            verify=True,
            timeout=(5, 20),
            allow_redirects=True,
        )
        rjson = response.json()

        assert response.status_code == 200
        assert rjson['result']

        # assert cursor has values
        assert 'last' in rjson['cursor']
        assert 'hasMore' in rjson['cursor']

        # assert allowance has values
        assert 'cost' in rjson['allowance']
        assert 'remaining' in rjson['allowance']
        assert 'remainingPaid' in rjson['allowance']
        assert 'account' in rjson['allowance']

        # assert an individual result has values
        assert 'id' in rjson['result'][0]
        assert 'exchange' in rjson['result'][0]
        assert 'pair' in rjson['result'][0]
        assert 'active' in rjson['result'][0]
        assert 'route' in rjson['result'][0]

    def test_list_markets_limit(self):
        """Check return of /markets?limit=2 endpoint returns all markets for all exchanges."""

        url = config.API_BASE_URL + 'markets?limit=2'
        response = cw_api.get(
            url,
            headers=config.headers,
            verify=True,
            timeout=(5, 20),
            allow_redirects=True,
        )
        rjson = response.json()

        assert response.status_code == 200
        assert len(rjson['result']) == 2

        for i in range(len(rjson['result'])):
            assert 'id' in rjson['result'][i]
            assert 'exchange' in rjson['result'][i]
            assert 'pair' in rjson['result'][i]
            assert 'active' in rjson['result'][i]
            assert 'route' in rjson['result'][i]

    def test_list_markets_limit_errors(self):
        """Check return of /markets?limit forcing errors."""

        # limit should only work between [1-20000]

        # test negative limit - 400 Bad Request
        url = config.API_BASE_URL + 'markets?limit=-1'
        response = cw_api.get(
            url,
            headers=config.headers,
            verify=True,
            timeout=(5, 20),
            allow_redirects=True,
        )
        assert response.status_code == 400

        url = config.API_BASE_URL + 'markets?limit=abc'
        response = cw_api.get(
            url,
            headers=config.headers,
            verify=True,
            timeout=(5, 20),
            allow_redirects=True,
        )
        assert response.status_code == 400

    def test_details_of_market(self):
        """"""


