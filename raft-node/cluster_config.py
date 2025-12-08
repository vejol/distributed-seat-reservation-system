import argparse
import json
from pathlib import Path
import sys


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--id", type=int, required=True)
    parser.add_argument(
        "--config",
        type=str,
        required=False,
        default="default",
        help="the key used in config.json",
    )
    parser.add_argument(
        "--prod",
        action="store_true",
        help="launch application in production mode with logs/snapshots saved on disk",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="launch application in development mode with the Interactive Dev Console and logs/snapshots saved in memory only"
    )

    return parser.parse_args()


def get_addresses(args):
    config_path = Path(__file__).resolve().parent / "config.json"
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    with open(config_path) as file:
        config = json.load(file)

    nodes = config[args.config]

    if args.id < 0 or args.id >= len(nodes):
        raise ValueError(
            f"Error: The provided id value ({args.id}) is out of range. Expected a value between 0 and {len(nodes) - 1}."
        )

    selfAddr = nodes[args.id]
    partners = [n for i, n in enumerate(nodes) if i != args.id]

    return selfAddr, partners
