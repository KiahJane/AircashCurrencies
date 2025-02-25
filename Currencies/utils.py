import json
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_currencies(file_path: str) -> Dict:
    """Loads currency data from JSON, handling errors."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logging.info(f"Loaded currencies from: {file_path}")
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Currency file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {file_path}")
        return {}

def build_currency_lookup(currencies: Dict, conversion_rates_version: str) -> Dict[str, Dict]:
    """Builds mapping dictionaries for currency lookup."""
    if not currencies:
        return {}

    currency_ids = currencies.get("currency_ids", [])
    currency_codes = currencies.get("currency_iso_codes", [])
    currency_names = currencies.get("currency_names", [])
    conversion_rates = currencies.get(conversion_rates_version, [])

    logging.info("Currency lookup table successfully built.")
    return {
        "id_to_code": {id_: code for id_, code in zip(currency_ids, currency_codes)},
        "code_to_id": {code: id_ for code, id_ in zip(currency_codes, currency_ids)},
        "id_to_name": {id_: name for id_, name in zip(currency_ids, currency_names)},
        "name_to_id": {name: id_ for name, id_ in zip(currency_names, currency_ids)},
        "code_to_name": {code: name for code, name in zip(currency_codes, currency_names)},
        "name_to_code": {name: code for name, code in zip(currency_names, currency_codes)},
        "id_to_conversion_rate": {id_: rate for id_, rate in zip(currency_ids, conversion_rates)},
        "code_to_conversion_rate": {code: rate for code, rate in zip(currency_codes, conversion_rates)},
        "name_to_conversion_rate": {name: rate for name, rate in zip(currency_names, conversion_rates)}
    }
