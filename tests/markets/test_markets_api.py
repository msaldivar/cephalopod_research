import logging
import numbers
from unittest import TestCase

# from cephalopod_research.tests.config import cw_api
from cephalopod_research.api.markets_api import CryptowatchMarketsAPIWrapper

logger = logging.getLogger(__name__)


class TestListMarkets(TestCase):
    """Test class for /markets endpoint"""
    cw_api = CryptowatchMarketsAPIWrapper()

    def test_list_all_markets(self):
        """Check return of /markets endpoint returns all markets for all exchanges."""

        logger.debug('Test list all markets')
        response = self.cw_api.get(
            params='markets'
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

        logger.debug('Test limit 2 markets')
        response = self.cw_api.get(
            params='markets?limit=2'
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
        """Check return of /markets?limit - forcing errors."""

        logger.debug('Test negative int value for limit - expect status code 400')
        response = self.cw_api.get(
            params='markets?limit=-1'
        )
        assert response.status_code == 400

        logger.debug('Test non-int value, abc - expect status code 400')
        response = self.cw_api.get(
            params='markets?limit=abc'
        )
        assert response.status_code == 400

    def test_details_of_market(self):
        """"""

        exchange = 'kraken'
        pair = 'btcusd'
        logger.debug(f'Get the market details for the exchange:{exchange} and pair:{pair}')
        response = self.cw_api.get(
            params=f'markets/{exchange}/{pair}'
        )
        rjson = response.json()

        assert response.status_code == 200, rjson

        assert rjson['result']['id'] == 87
        assert rjson['result']['exchange'] == exchange
        assert rjson['result']['pair'] == pair
        assert rjson['result']['active']
        assert len(rjson['result']['routes']) == 5

    def test_details_of_market_error(self):
        """Test 404 error by passing a fake pair - using Bioshock currency value Adam."""

        exchange = 'kraken'
        pair = 'btcadam'
        logger.debug(f'Get the market details for the exchange:{exchange} and nonexistent pair:{pair}')

        response = self.cw_api.get(
            params=f'markets/{exchange}/{pair}'
        )
        rjson = response.json()

        assert response.status_code == 404, rjson
        assert rjson['error'] == 'Instrument not found', rjson['error']

    def test_current_market_price(self):
        """Test getting current market price of btcusd on kraken"""

        exchange = 'kraken'
        pair = 'btcusd'
        logger.debug(f'Get the price for {pair} on exchange {exchange}')
        response = self.cw_api.get(
            params=f'markets/{exchange}/{pair}/price'
        )
        rjson = response.json()

        assert response.status_code == 200, rjson
        assert isinstance(rjson['result']['price'], numbers.Number)

    def test_market_trades_with_limit(self):
        """Test getting the most recent trades."""

        exchange = 'kraken'
        pair = 'btcusd'
        limit = 'limit=1'
        response = self.cw_api.get(
            params=f'markets/{exchange}/{pair}/trades?{limit}'
        )
        rjson = response.json()

        assert response.status_code == 200, rjson
        assert len(rjson['result']) == 1
        assert len(rjson['result'][0]) == 4

    def test_market_24H_summary(self):
        """Test getting the markets summary from Kraken for btcusd"""

        exchange = 'kraken'
        pair = 'btcusd'
        response = self.cw_api.get(
            params=f'markets/{exchange}/{pair}/summary'
        )
        rjson = response.json()

        assert response.status_code == 200, rjson

        assert len(rjson['result']) == 3
        assert len(rjson['result']['price']) == 4
        assert len(rjson['result']['price']['change']) == 2

        assert isinstance(rjson['result']['price']['last'], numbers.Number)
        assert isinstance(rjson['result']['price']['high'], numbers.Number)
        assert isinstance(rjson['result']['price']['low'], numbers.Number)

        assert isinstance(rjson['result']['price']['change']['percentage'], numbers.Number)
        assert isinstance(rjson['result']['price']['change']['absolute'], numbers.Number)

        assert isinstance(rjson['result']['volume'], numbers.Number)
        assert isinstance(rjson['result']['volumeQuote'], numbers.Number)
