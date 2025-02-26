import logging
import requests
from datetime import datetime
from typing import Dict, Union, List, Tuple, Optional
import config
from utils import load_json, build_currency_lookup, save_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Currencies:
    """Handles currency mappings, conversions, and lookup functions."""

    def __init__(self, conversion_rates_key: Union[str, None] = None):
        self.api_key = config.EXCHANGE_RATE_API_KEY
        self.api_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/EUR"
        self.currency_file = config.CURRENCIES_FILE_PATH

        self.currencies:Dict[str, List] = load_json(self.currency_file)
        self.conversion_rates_key = conversion_rates_key if conversion_rates_key else (
            max((key for key in self.currencies.keys() if key.startswith("conversion_rates_to_eur_")), default=None))
        self.currency_lookup:Dict[str, Dict] = build_currency_lookup(self.currencies, self.conversion_rates_key)

        if self.conversion_rates_key:
            logging.info(f"Using conversion rates from: {self.conversion_rates_key}")
        else:
            logging.error(f"Conversion rates were not retrievable from: {self.currency_file}.")
            raise ValueError("No valid conversion rates key found in the JSON file")

    ### Methods for Accessing All Currencies ###
    def load_currencies(self) -> Tuple[List[int], List[str], List[str]]:
        """Loads currencies (ID, ISO code, name) from JSON."""
        currencies = (
             self.currencies.get("currency_ids", []),
             self.currencies.get("currency_iso_codes", []),
             self.currencies.get("currency_names", [])
        )
        return currencies

    def load_conversion_rates(self) -> List[float]:
        """Loads currency conversion rates for the "conversion_rates_key"."""
        return self.currencies.get(self.conversion_rates_key, [])

    def currencies_by_id_asc(self) -> Dict[int, Tuple[str, str]]:
        """Returns currencies sorted by their IDs in ascending order."""
        ids, iso_codes, names = self.load_currencies()
        return dict(sorted(zip(ids, zip(iso_codes, names))))

    def currencies_by_iso_code_alphabetical(self) -> Dict[str, Tuple[int, str]]:
        """Returns currencies sorted by their ISO codes in alphabetical order."""
        ids, iso_codes, names = self.load_currencies()
        return dict(sorted(zip(iso_codes, zip(ids, names))))

    def currencies_by_name_alphabetical(self) -> Dict[str, Tuple[int, str]]:
        """Returns currencies sorted by their names in alphabetical order."""
        ids, iso_codes, names = self.load_currencies()
        return dict(sorted(zip(names, zip(ids, iso_codes))))

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
        return round(amount * conversion_rate, 2)

    ### Methods for Currency Extraction ###
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

    ### Functional Methods ###
    def update_conversion_rates(self):
        """Retrieves the latest conversion rates."""
        ids, iso_codes, names = self.load_currencies
        self.save_currencies(ids, iso_codes, names)

    def save_currencies(self, ids: List[int], iso_codes: List[str], names: List[str], rates: List[float] = None):
        """Saves the given currencies to JSON."""
        if not rates:
            save_json({"currency_ids": ids,
                            "currency_iso_codes": iso_codes,
                            "currency_names": names,
                            f"conversion_rates_to_eur_{datetime.now().strftime("%Y%m%d")}": self._get_conversion_rates(ids)},
                       self.currency_file)
        else:
            save_json({"currency_ids": ids,
                       "currency_iso_codes": iso_codes,
                       "currency_names": names,
                       f"{self.conversion_rates_key}": rates},
                      self.currency_file)

    def add_currency(self, id_: int, iso_code: str, name: str):
        """Adds a new curency if it does not already exist. Anytime a new currency is added, the conversion rates are
        automatically updated."""
        ids, iso_codes, names = self.load_currencies()

        if id_ in ids:
            logging.error(f"Currency already exists for ID: {id_}")
            raise ValueError(f"Currency already exists for ID: {id_}")
        if iso_code in iso_codes:
            logging.error(f"Currency already exists for ID: {iso_code}")
            raise ValueError(f"Currency already exists for ID: {iso_code}")
        if name in names:
            logging.error(f"Currency already exists for ID: {name}")
            raise ValueError(f"Currency already exists for ID: {name}")

        ids.append(id_)
        iso_codes.append(iso_code)
        names.append(name)
        self.save_currencies(ids, iso_codes, names)
        logging.info(f"Currency added successfully: {id_} - {iso_code} - {name}")
        self.currency_lookup = build_currency_lookup(self.currencies, self.conversion_rates_key)

    def delete_currency_by_id(self, id_: int):
        """Deletes currency by indexing by its ID."""
        ids, iso_codes, names = self.load_currencies()
        rates = self.load_conversion_rates()

        if id_ in ids:
            index = ids.index(id_)
            ids.pop(index)
            iso_codes.pop(index)
            names.pop(index)
            rates.pop(index)
            self.save_currencies(ids, iso_codes, names, rates)
            logging.info(f"Currency {id_} deleted successfully.")
        else:
            logging.error(f"Currency {id_} not found.")

    ### Method for Live Conversion Rates API Call ###
    def _get_conversion_rates(self, ids: List[int]) -> List[Optional[float]]:
        """Retrieves actual currency conversion rates for a list of currency IDs."""
        if not ids:
            return []

        iso_codes = [self.get_currency_iso_code_from_id(id_) for id_ in ids]
        iso_codes = list(filter(None, iso_codes))
        if not iso_codes:
            return [None]

        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()  # Raise an error for bad HTTP responses (4xx, 5xx)
            data = response.json()

            rates = data.get("conversion_rates", {})
            logging.info(f"Conversion rates retrieved the currencies: {ids}")
            return [rates.get(iso_code.upper(), None) for iso_code in iso_codes]

        except requests.RequestException as e:
            logging.error(f"Failed to fetch exchange rates: {e}")
            return [None]


if __name__ == '__main__':
    currency_handler = Currencies()

    currency_ids = [
        946,
        949
      ]
    for curr_id in currency_ids:
        currency_conversion_rate = currency_handler.get_currency_iso_code_from_id(curr_id)
        logging.info(f"Conversion rate to EUR for {curr_id}: {currency_conversion_rate}")
        print(f"Conversion rate to EUR for {curr_id}: {currency_conversion_rate}")
