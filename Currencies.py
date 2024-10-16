import json
from forex_python.converter import CurrencyRates


class Currencies:

    CURRENCIES_FILE = r"currencies.json"
    currencies = json.load(open(CURRENCIES_FILE))

    currency_lookup = {
        "id_to_code": dict(zip(currencies["currency_ids"], currencies["currency_codes"])),
        "code_to_id": {code: id_ for id_, code in zip(currencies["currency_ids"], currencies["currency_codes"])},
        "id_to_name": dict(zip(currencies["currency_ids"], currencies["currency_names"])),
        "name_to_id": {name: id_ for id_, name in zip(currencies["currency_ids"], currencies["currency_names"])},
        "code_to_name": dict(zip(currencies["currency_codes"], currencies["currency_names"])),
        "name_to_code": {name: code for code, name in zip(currencies["currency_codes"], currencies["currency_names"])},
    }

    @classmethod
    def get_conversion_rate_to_eur(cls, currency_input):
        c = CurrencyRates()

        # Currency ID
        if isinstance(currency_input, int):
            currency_code = cls.get_currency_code_from_id(currency_input)
            if currency_code is None:
                raise ValueError(f"Invalid currency ID: {currency_input}")
        # Currency code
        elif isinstance(currency_input, str) and len(currency_input) == 3:
            currency_code = currency_input.upper()
        # Currency name
        elif isinstance(currency_input, str) and len(currency_input) > 3:
            currency_code = cls.get_currency_code_from_name(currency_input)
            if currency_code is None:
                raise ValueError(f"Invalid currency name: {currency_input}")
        else:
            raise ValueError("Invalid currency input format.")

        # Fetch and return the conversion rate to EUR rounded to 2 decimals
        try:
            rate = c.get_rate(currency_code, 'EUR')
            return round(rate, 2)
        except Exception as e:
            print(f"Error fetching conversion rate: {e}")
            return None

    @classmethod
    def get_currency_id_from_code(cls, currency_code):
        """Returns the currency ID for a given currency code."""
        return cls.currency_lookup['code_to_id'].get(currency_code.upper(), "Currency code not found")
    @classmethod
    def get_currency_id_from_name(cls, currency_name):
        """Returns the currency ID for a given currency name."""
        return cls.currency_lookup['name_to_id'].get(currency_name, "Currency name not found")

    @classmethod
    def get_currency_name_from_code(cls, currency_code):
        """Returns the currency name for a given currency code."""
        return cls.currency_lookup['code_to_name'].get(currency_code.upper(), "Currency code not found")
    @classmethod
    def get_currency_name_from_id(cls, currency_id):
        """Returns the currency name for a given currency ID."""
        return cls.currency_lookup['id_to_name'].get(currency_id, "Currency ID not found")

    @classmethod
    def get_currency_code_from_id(cls, currency_id):
        """Returns the currency code for a given currency ID."""
        return cls.currency_lookup['id_to_code'].get(currency_id, "Currency ID not found")
    @classmethod
    def get_currency_code_from_name(cls, currency_name):
        """Returns the currency code for a given currency name."""
        return cls.currency_lookup['name_to_code'].get(currency_name, "Currency name not found")


if __name__ == '__main__':
    # USD to EUR
    conversion_rate = Currencies.get_conversion_rate_to_eur(191)
    print("Conversion rate to EUR:", conversion_rate)