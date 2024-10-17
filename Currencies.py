import json


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
        "id_to_conversion_rate": dict(zip(currencies["currency_ids"], currencies["conversion_rates_to_eur_20241016"])),
        "code_to_conversion_rate": dict(zip(currencies["currency_codes"], currencies["conversion_rates_to_eur_20241016"])),
        "name_to_conversion_rate": dict(zip(currencies["currency_names"], currencies["conversion_rates_to_eur_20241016"]))
    }

    @classmethod
    def get_conversion_rate_to_eur(cls, currency_input):
        """
                Returns the conversion rate to EUR based on the input type
                (currency_id, currency_code, or currency_name).
                """
        # Currency ID
        if isinstance(currency_input, int):
            rate = cls.currency_lookup["id_to_conversion_rate"].get(currency_input)
            if rate is None:
                raise ValueError(f"Invalid currency ID: {currency_input}")
        # Currency code
        elif isinstance(currency_input, str) and len(currency_input) == 3:
            rate = cls.currency_lookup["code_to_conversion_rate"].get(currency_input.upper())
            if rate is None:
                raise ValueError(f"Invalid currency code: {currency_input}")
        # Currency name
        elif isinstance(currency_input, str) and len(currency_input) > 3:
            rate = cls.currency_lookup["name_to_conversion_rate"].get(currency_input)
            if rate is None:
                raise ValueError(f"Invalid currency name: {currency_input}")
        else:
            raise ValueError("Invalid currency input format.")

        return rate

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
    currency_ids = [
    191,
    203,
    208,
    348,
    752,
    756,
    826,
    840,
    946,
    949,
    975,
    977,
    978,
    985
  ]
    for currency_id in currency_ids:
        conversion_rate = Currencies.get_conversion_rate_to_eur(currency_id)
        print(f"Conversion rate to EUR for {currency_id}:", conversion_rate)

