from unittest import TestCase
import pytest
import cryptowatch as cw
from datetime import datetime


class TestListMarkets(TestCase):
    """Test class for /markets endpoint."""

    def test_list_all_markets_return(self):
        """Check return of /markets endpoint returns all markets for all exchanges."""

        # make api call to /markets
        markets = cw.markets.list()

        assert markets._http_response.status_code == 200
        assert type(markets.markets) == type(list())

    def test_list_exchange(self):
        """Check return of /markets?exchanges=kraken."""

        # make api call to /markets?exchanges=kraken
        markets = cw.markets.list(exchange='kraken')

        assert markets._http_response.status_code == 200

        assert markets.markets[0].exchange == 'kraken'

    def test_list_exchange_error(self):
        """Pass a nonexistent exhange to check error"""

        # make api call to /markets?exchanges=cephalopod
        with pytest.raises(cw.errors.APIResourceNotFoundError):
            markets = cw.markets.list(exchange='cephalopod')
