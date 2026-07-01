#!/usr/bin/env python3

"""
BGroundRemover
Professional AI Background Removal Tool
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="bground", description="Professional AI Background Removal Tool"
    )

    parser.add_argument("input", nargs="?", help="Input image or folder")

    parser.add_argument("-o", "--output", default="output", help="Output folder")

    parser.add_argument(
        "--engine", default="birefnet", choices=["birefnet"], help="AI Engine"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("BGroundRemover")
    print("=" * 50)
    print(f"Input : {args.input}")
    print(f"Output: {args.output}")
    print(f"Engine: {args.engine}")
    print()
    print("Engine loading... (coming soon)")


if __name__ == "__main__":
    main()
