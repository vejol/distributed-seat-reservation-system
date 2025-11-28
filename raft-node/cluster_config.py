import argparse
import json
from pathlib import Path
import sys


def get_addresses():
    config_path = Path(__file__).resolve().parent / "config.json"
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    with open(config_path) as file:
        config = json.load(file)

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument(
        "--config",
        type=str,
        required=False,
        default="default",
        help="the key of the configuration used in the config.json file",
    )
    args = parser.parse_args()

    nodes = config[args.config]

    if args.id < 0 or args.id >= len(nodes):
        raise ValueError(
            f"Error: The provided id value ({args.id}) is out of range. Expected a value between 0 and {len(nodes) - 1}."
        )

    selfAddr = nodes[args.id]
    partners = [n for i, n in enumerate(nodes) if i != args.id]

    return selfAddr, partners
