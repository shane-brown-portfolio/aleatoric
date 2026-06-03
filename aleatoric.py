import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate aleatoric music."
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Write generated audio to WAV file instead of playing."
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("Aleatoric Music Generator")

    if args.output:
        print(f"Output file: {args.output}")
    else:
        print("Playback mode")


if __name__ == "__main__":
    main()