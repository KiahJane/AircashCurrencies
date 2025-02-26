import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

try:
    # load environment variables from .env file
    EXCHANGE_RATE_API_KEY = Path(os.getenv("EXCHANGE_RATE_API_KEY"))

    # Project Info
    PROJECT_DIR = Path(__file__).resolve().parent
    PROJECT_NAME = "AircashCurrencies"
    PYTHON_VERSION = 3.10

    # Data file paths
    REFERENCE_DIR = PROJECT_DIR / "references"
    CURRENCIES_FILE_PATH = REFERENCE_DIR / "currencies.json"

    # Check if the required files exist (Optional)
    required_files = [CURRENCIES_FILE_PATH]
    missing_files = [str(file) for file in required_files if not file.exists()]

    if missing_files:
        print(f"⚠️ Warning: The following files are missing: {', '.join(missing_files)}")

except Exception as e:
    print(f"❌ Error loading configuration: {e}")

else:
    print("✅ Configuration variables loaded successfully!")
