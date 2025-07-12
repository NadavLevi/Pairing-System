#!/usr/bin/env python3.12

import argparse
from typing import List
from models.policy import ConsumerPolicy
from models.provider import Provider
from pairing_system.system import PairingSystem


def create_sample_providers() -> List[Provider]:
    return [
        Provider("A", 100, "US", ["feature1", "feature2"]),
        Provider("B", 60, "UK", ["feature1"]),
        Provider("C", 200, "DE", ["feature1", "feature2", "feature3"]),
        Provider("D", 80, "CA", ["feature1", "feature3"]),
        Provider("E", 120, "US", ["feature1"]),
        Provider("F", 300, "JP", ["feature1", "feature2", "feature3", "feature4"]),
        Provider("G", 250, "FR", ["feature1", "feature4"]),
        Provider("H", 150, "CA", ["feature2", "feature3"]),
    ]


def create_consumer_policy(location: str, features: List[str], min_stake: int) -> ConsumerPolicy:
    return ConsumerPolicy(
        required_location=location,
        required_features=features,
        min_stake=min_stake
    )


def print_pairing_results(providers: List[Provider]) -> None:
    print("\n🌐 Top Matched Providers:\n" + "-" * 35)
    for idx, provider in enumerate(providers, start=1):
        print(f"{idx}. Address  : {provider.address}")
        print(f"   Stake    : {provider.stake}")
        print(f"   Location : {provider.location}")
        print(f"   Features : {', '.join(provider.features)}\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Run Lava Provider Pairing CLI")
    parser.add_argument("--location", type=str, default="US", help="Required location (default: US)")
    parser.add_argument("--features", nargs="*", default=["feature1"], help="Required features (default: ['feature1'])")
    parser.add_argument("--min-stake", type=int, default=70, help="Minimum stake required (default: 70)")
    parser.add_argument("--strict", action="store_true", help="Use strict location filtering (default: False)")
    parser.add_argument("--max-distance", type=int, default=2000, help="Max distance in km for flexible location filtering")
    return parser.parse_args()


def main():
    args = parse_args()
    providers = create_sample_providers()
    policy = create_consumer_policy(args.location, args.features, args.min_stake)

    system = PairingSystem()
    best_providers = system.get_pairing_list(
        providers,
        policy,
        strict=args.strict,
        max_distance_km=args.max_distance
    )
    
    if not best_providers:
        print(f"⚠️  No matching providers found based on the given policy ({policy}).\n")
    else:
        print_pairing_results(best_providers)


if __name__ == "__main__":
    main()