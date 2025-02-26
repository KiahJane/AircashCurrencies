# Currencies

###### This Python package contains the various currencies used by Aircash.
###### Each currency has an ID, code, name and various conversion rates.
###### This package is an interface to edit and retrieve currencies used at Aircash. The currency name can be retrieved from the currency ID or currency ISO code (and vice versa). The package also enables easy access to the conversion rate needed to convert the currency into Euros (updated manually).

## Methods included in the package:
### Methods for Accessing All Currencies
- `load_currencies`: Returns tupled lists of currency IDs, ISO codes and names from a JSON file if it exists.
- `currencies_by_id_asc`: Returns currencies as a dictionary sorted by currency ID in ascending order.
- `currencies_by_iso_code_alphabetical`: Returns currencies as a dictionary sorted by currency ISO code in alphabetical order.
- `currencies_by_name_alphabetical`: Returns currencies as a dictionary sorted by currency name in alphabetical order.

### Methods for Conversions
- `get_conversion_rate_to_eur`: Returns the conversion rate to EUR for a currency ID, ISO code or name.
- `convert_to_eur`: Converts a given amount to EUR using the conversion rate for the given currency ISO code.

### Methods for Currency Extraction 
- `get_currency_id_from_code`: Returns the corresponding currency ID for the given currecy ISO code. 
- `get_currency_id_from_name`: Returns the corresponding currency ID for the given currency name.
- `get_currency_name_from_code`: Returns the corresponding currency name for a given currency ISO code.
- `get_currency_name_from_id`: Returns the corresponding currency name for a given currency ID.
- `get_currency_iso_code_from_id`: Returns the corresponding currency ISO code for a given currency ID.
- `get_currency_iso_code_from_name`: Returns the corresponding currency ISO code for a given currency name.

### Functional Methods
- `update_conversion_rates`: Retrieves the latest conversion rates from https://www.exchangerate-api.com/ and updates JSON file.
- `save_currencies`: Saves the provided currency IDs, ISO codes, names and conversion rates to a JSON file.
- `add_currency`: Adds a new currency if it does not already exist.
- `delete_currency_by_id`: Deletes currency by indexing its ID.

### Method for Live Conversion Rates API Call 
- `_get_conversion_rates`: Retrieves actual currency conversion rates for a list of currency IDs.