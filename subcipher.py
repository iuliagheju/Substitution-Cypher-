#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

DEFAULT_KEY = "default-key"
BUFFER_SIZE = 65536


def translate_file(
    input_path: Path, output_path: Path, key_bytes: bytes, encrypt: bool
) -> None:
    key_len = len(key_bytes)
    key_index = 0

    with input_path.open("rb") as input_file, output_path.open("wb") as output_file:
        while True:
            chunk = input_file.read(BUFFER_SIZE)
            if not chunk:
                break
            transformed = bytearray(len(chunk))
            for i, value in enumerate(chunk):
                key_value = key_bytes[key_index]
                key_index += 1
                if key_index == key_len:
                    key_index = 0
                if encrypt:
                    transformed[i] = (value + key_value) & 0xFF
                else:
                    transformed[i] = (value - key_value) & 0xFF
            output_file.write(transformed)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Vigenere cipher for 8-bit bytes (encrypt/decrypt)."
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-e", "--encrypt", action="store_true", help="Encrypt input."
    )
    mode_group.add_argument(
        "-d", "--decrypt", action="store_true", help="Decrypt input."
    )
    parser.add_argument("input_file", help="Input file path.")
    parser.add_argument(
        "-o", "--output", required=True, help="Output file path."
    )
    parser.add_argument(
        "-k",
        "--key",
        default=DEFAULT_KEY,
        help="Key string (default is a built-in demo key).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    input_path = Path(args.input_file)
    output_path = Path(args.output)

    if not input_path.is_file():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    key_bytes = args.key.encode("utf-8")
    if not key_bytes:
        print("Key must not be empty.", file=sys.stderr)
        return 2

    translate_file(input_path, output_path, key_bytes, args.encrypt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
