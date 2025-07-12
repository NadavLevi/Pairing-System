# Pairing System
[![codecov](https://codecov.io/gh/NadavLevi/Pairing-System/branch/main/graph/badge.svg)](https://codecov.io/gh/NadavLevi/Pairing-System)

This project implements a lightweight provider pairing and ranking system, designed to match **network providers** with **consumer policies** based on location, stake, and feature capabilities.


## Features

- **Location Matching & Scoring**
  - Exact (strict) or flexible (geographic proximity) matching using `geopy`
  - Location score based on physical distance with configurable max distance

- **Stake Filtering & Normalization**
  - Filters providers by minimum stake
  - Ranks providers using normalized stake score

- **Feature Filtering & Scoring**
  - Ensures all required features are present
  - Rewards providers with additional useful features

- **Configurable Pairing Engine**
  - Multi-pass filtering pipeline
  - Ranking logic using weighted scores
  - ThreadPool-based scoring for performance

## Running Tests

Tests are written using `pytest`.

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest
```

Includes:
- Parametrized success cases
- `xfail` scenarios for negative testing
- Geolocation tolerance ranges

## CLI Usage

A command-line interface is available via `main.py`:

```bash
python main.py --location "US" \
                           --features "f1" "f2" \
                           --min-stake 50 \
                           --strict
```

This will search for the exact location of "US" with at least both "f1" and "f2" features with at least 50 stake.

```bash
python main.py --location "US" \
                           --features "f1" "f2" \
                           --min-stake 50 \
                           --max-distance 6000
```

This will search for a location far from "US" with maximum distance of 6000 KM with at least both "f1" and "f2" features with at least 50 stake.

## Dependencies

- `geopy` - for location scoring
- `pytest` - for testing
- `pytest-cov` - for coverage testing

## Example Output

```
🌐 Top Matched Providers:
-----------------------------------
1. Address  : A
   Stake     : 100
   Location  : US
   Features  : feature1, feature2
   Score     : 0.94
   Components: {'stake_score': 0.8333333333333334, 'feature_score': 1.0, 'location_score': 1.0}

2. Address  : E
   Stake     : 120
   Location  : US
   Features  : feature1
   Score     : 0.83
   Components: {'stake_score': 1.0, 'feature_score': 0.5, 'location_score': 1.0}
```

---


## FYI - Country Codes are based on the following link
https://www.iban.com/country-codes