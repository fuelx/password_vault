#!/usr/bin/env python3

import argparse
from vault.authenticator import TOTP

def main():
    parser = argparse.ArgumentParser(prog="vault", description="Local Password Vault")
    sub = parser.add_subparsers(dest="cmd")

    totp_cmd = sub.add_parser("totp", help="Generate TOTP")
    totp_cmd.add_argument("secret", help="Base32 secret")

    args = parser.parse_args()

    if args.cmd == "totp":
        totp = TOTP(args.secret)
        print(totp.generate())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
