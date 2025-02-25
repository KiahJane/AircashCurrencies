import logging
from typing import Dict, Union, List
import config
from utils import load_currencies, build_currency_lookup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Currencies:
    """Handles currency mappings, conversions, and lookup functions."""

    def __init__(self, conversion_rates_key: Union[str, None] = None):
        self.currencies:Dict[str, List] = load_currencies(config.CURRENCIES_FILE_PATH)
        self.conversion_rates_key = conversion_rates_key if conversion_rates_key else (
            max((key for key in self.currencies.keys() if key.startswith("conversion_rates_to_eur_")), default=None))
        self.currency_lookup:Dict[str, Dict] = build_currency_lookup(self.currencies, self.conversion_rates_key)

        if self.conversion_rates_key:
            logging.info(f"Using conversion rates from: {self.conversion_rates_key}")
        else:
            logging.error(f"Conversion rates were not retrievable from: {config.CURRENCIES_FILE_PATH}.")
            raise ValueError("No valid conversion rates key found in the JSON file")

    ### Methods for Conversions ###
    def get_conversion_rate_to_eur(self, currency_input: Union[int, str]) -> float:
        """Returns the conversion rate to EUR for a currency ID, ISO code, or name.
        :param currency_input: Currency ID (int), ISO code (str), or name (str).
        :return: Conversion rate to EUR.
        :raises ValueError: If currency_input is invalid.
        """
        logging.info(f"Retrieving conversion rate for: {currency_input}")
        lookup = self.currency_lookup
        rate = None

        if isinstance(currency_input, int):
            rate = lookup["id_to_conversion_rate"].get(currency_input)
        elif isinstance(currency_input, str) and len(currency_input) == 3:
            rate = lookup["code_to_conversion_rate"].get(currency_input.upper())
        elif isinstance(currency_input, str) and len(currency_input) > 3:
            rate = lookup["name_to_conversion_rate"].get(currency_input)

        if rate is None:
            logging.warning(f"Invalid currency input: {currency_input}")
            raise ValueError(f"Invalid currency input: {currency_input}")

        logging.info(f"Conversion rate for {currency_input}: {rate}")
        return rate

    def convert_to_eur(self, currency_iso_code: str, amount: float) -> float:
        """Converts an amount to EUR based on the currency ISO code.
        :param currency_iso_code: Currency ISO code.
        :param amount: Amount in the given currency.
        :return: Converted amount in EUR.
        :raises ValueError: If currency code is invalid.
        """
        logging.info(f"Converting {amount} {currency_iso_code} to EUR")
        conversion_rate = self.currency_lookup["code_to_conversion_rate"].get(currency_iso_code.upper())

        if conversion_rate is None:
            logging.error(f"Invalid currency code: {currency_iso_code}")
            raise ValueError(f"Invalid currency code: {currency_iso_code}")

        logging.info(f"{amount} {currency_iso_code} = {amount * conversion_rate} EUR at rate {conversion_rate}")
        return amount * conversion_rate

    ### Methods for Mapping ###
    def get_currency_id_from_code(self, currency_iso_code: str) -> Union[int, str]:
        """Returns the currency ID for a given currency code."""
        logging.debug(f"Getting currency ID for ISO code: {currency_iso_code}")
        return self.currency_lookup['code_to_id'].get(currency_iso_code.upper(), "Currency code not found")
    def get_currency_id_from_name(self, currency_name: str) -> Union[int, str]:
        """Returns the currency ID for a given currency name."""
        logging.debug(f"Getting currency ID for name: {currency_name}")
        return self.currency_lookup['name_to_id'].get(currency_name, "Currency name not found")

    def get_currency_name_from_code(self, currency_iso_code: str) -> Union[int, str]:
        """Returns the currency name for a given currency code."""
        logging.debug(f"Getting currency name for ISO code: {currency_iso_code}")
        return self.currency_lookup['code_to_name'].get(currency_iso_code.upper(), "Currency code not found")
    def get_currency_name_from_id(self, currency_id: int) -> Union[int, str]:
        """Returns the currency name for a given currency ID."""
        logging.debug(f"Getting currency name for ID: {currency_id}")
        return self.currency_lookup['id_to_name'].get(currency_id, "Currency ID not found")

    def get_currency_iso_code_from_id(self, currency_id: int) -> str:
        """Returns the currency ISO code for a given currency ID."""
        logging.debug(f"Getting currency ISO code for ID: {currency_id}")
        return self.currency_lookup['id_to_code'].get(currency_id, "Currency ID not found")
    def get_currency_iso_code_from_name(self, currency_name: str) -> str:
        """Returns the currency ISO code for a given currency name."""
        logging.debug(f"Getting currency ISO code for name: {currency_name}")
        return self.currency_lookup['name_to_code'].get(currency_name, "Currency name not found")


if __name__ == '__main__':
    currencies = Currencies()

    currency_ids = [
        946,
        949
      ]
    for curr_id in currency_ids:
        currency_conversion_rate = currencies.get_currency_iso_code_from_id(curr_id)
        logging.info(f"Conversion rate to EUR for {curr_id}: {currency_conversion_rate}")
        print(f"Conversion rate to EUR for {curr_id}: {currency_conversion_rate}")
