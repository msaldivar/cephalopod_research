# cephalopod_research

To run the test file `test_markets_api.py` cd into `cephalopod_research` and execute:

```
python -m unittest tests.markets.test_markets_api.TestListMarkets
```

I created a simple wrapper for the `/markets` endpoint to easily pass in params and to init the request object
by reading the `API_KEY` from the config file

Be sure to update the `API_KEY` with a personal key in the `config.py` file

### Notes - areas of improvements:
* I didn't test every possible param, in a real environment every possible param would be tested.
* I tested several error cases it's important to test more edge cases and rainyday paths within the api
* Mocking data/using test data can also be used to confirm correct values are returned from the api
* The api wrapper could be extended to include custom error handling 