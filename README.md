# Vigenere Cipher CLI

This project provides a command-line tool that performs a byte-level Vigenere
cipher (8-bit ASCII). It supports encryption and decryption on any binary file.

## Requirements

- Python 3.8 or newer

## Usage

```bash
python subcipher.py -e input.bin -o encrypted.bin -k "my key"
python subcipher.py -d encrypted.bin -o decrypted.bin -k "my key"

Arguments can appear in any order. Use the same key for encryption and decryption.
If no key is provided, the tool uses the key `default-key`.

## Implementation notes

- The key string is encoded as UTF-8 and repeated across the input bytes.
- Encryption adds each key byte modulo 256; decryption subtracts it modulo 256.
- The program processes files in chunks to handle large inputs efficiently.

## Test data

Sample files are included in `tests/`:

- `tests/sample_input.bin` (10 KB ASCII sample data repeating: "Message for encryption")
- `tests/expected_encrypted.bin` (encrypted with `default-key`)

Verify encryption:

```bash
python subcipher.py -e tests/sample_input.bin -o tests/out_encrypted.bin
fc /b tests\\expected_encrypted.bin tests\\out_encrypted.bin
```

Verify decryption:

```bash
python subcipher.py -d tests/expected_encrypted.bin -o tests/out_decrypted.bin
fc /b tests\\sample_input.bin tests\\out_decrypted.bin
```
