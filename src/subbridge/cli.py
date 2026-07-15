from __future__ import annotations

import argparse
from pathlib import Path

from subbridge.downloader import download_subscription
from subbridge.generator import generate_mihomo_config
from subbridge.providers.liberty import parse_liberty_subscription


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subbridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert = subparsers.add_parser("convert", help="Convert a subscription to Mihomo YAML")
    convert.add_argument("--url", required=True)
    convert.add_argument("--output", required=True, type=Path)
    convert.add_argument("--provider", default="liberty", choices=["liberty"])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    raw = download_subscription(args.url)
    nodes = parse_liberty_subscription(raw)
    output = generate_mihomo_config(nodes)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Generated {args.output} with {len(nodes)} nodes")


if __name__ == "__main__":
    main()
