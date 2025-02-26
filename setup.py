from setuptools import setup, find_packages
import config

setup(
    name=config.PROJECT_NAME,         # Package name
    version="1.0.0",                  # Package version
    packages=find_packages(),         # Automatically find all packages
    include_package_data=True,        # Include non-Python files specified in MANIFEST.in
    package_data={
        "AircashCurrencies": ["references/*.json"],     # Include JSON files in the AircashCurrencies package
    },
    description="Python package built around making currency operations easier to handle.",  # Short description
    author="Kiah Jane Seki",                                           # Author's name
    author_email="kiah.jane.jones@aircash.eu",                         # Author's email
    license="MIT",                                                     # Package license
    url="https://github.com/KiahJane/AircashCurrencies.git",                  # URL to the package repository (optional)
    install_requires=[],                                               # List of dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=f">={config.PYTHON_VERSION}",          # Minimum Python version
)
