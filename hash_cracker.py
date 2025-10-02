#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import argparse
import sys
import time
from multiprocessing import Pool, cpu_count
from functools import partial

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN, RED, YELLOW, CYAN = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN
except ImportError:
    GREEN = RED = YELLOW = CYAN = ""

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, *args, **kwargs):
        return iterable

HASH_LENGTHS = {
    32: 'md5',
    40: 'sha1',
    64: 'sha256',
    96: 'sha384',
    128: 'sha512'
}


def display_banner():
    banner = f"""{CYAN}
    #########################################
    #                                       #
    #      Python Hash Cracker              #
    # (Auto-Detect, Salt, File Output)      #
    #     Github="AhmetGultekin0"           #
    #                                       #
    #########################################
    """
    print(banner)


def check_password(password, target_hash, algorithm, salt, salt_position):
    if salt:
        if salt_position == 'prefix':
            password_to_hash = salt + password
        else:
            password_to_hash = password + salt
    else:
        password_to_hash = password

    hasher = hashlib.new(algorithm)
    hasher.update(password_to_hash.encode('utf-8'))
    hashed_password = hasher.hexdigest()

    if hashed_password.lower() == target_hash.lower():
        return password
    return None


def main():
    display_banner()

    parser = argparse.ArgumentParser(
        description="Advanced Hash Cracker. It auto-detects hash types and supports salt and file output.",
        epilog="Example: python hash_cracker.py <HASH> <WORDLIST>"
    )

    parser.add_argument("target_hash", help="The hash string to be cracked.")
    parser.add_argument("wordlist", help="Path to the wordlist file containing passwords to try.")
    parser.add_argument("-a", "--algorithm",
                        help="The hash algorithm. If not specified, it will be guessed based on hash length.")
    parser.add_argument("-p", "--processes", type=int, default=cpu_count(),
                        help=f"Number of CPU cores to use (default: {cpu_count()}).")
    parser.add_argument("-s", "--salt", help="The salt value to be used during hashing.")
    parser.add_argument("--salt-position", choices=['prefix', 'suffix'], default='prefix',
                        help="Position of the salt: before (prefix) or after (suffix) the password.")
    parser.add_argument("-o", "--output-file", help="Output file to save the found passwords.")

    args = parser.parse_args()

    if not args.algorithm:
        hash_len = len(args.target_hash)
        if hash_len in HASH_LENGTHS:
            args.algorithm = HASH_LENGTHS[hash_len]
            print(f"{YELLOW}[*] Hash length ({hash_len}) detected. Algorithm set to: {args.algorithm.upper()}")
        else:
            print(f"{RED}[-] Could not auto-detect hash type. Please specify it manually using the '-a' flag.")
            sys.exit(1)

    print(f"{YELLOW}[*] Initializing...")
    print(f"{YELLOW}[*] Target Hash: {args.target_hash}")
    print(f"{YELLOW}[*] Algorithm: {args.algorithm.upper()}")
    if args.salt:
        print(f"{YELLOW}[*] Salt: '{args.salt}' ({args.salt_position})")
    print(f"{YELLOW}[*] Wordlist: {args.wordlist}")
    print(f"{YELLOW}[*] CPU Cores: {args.processes}\n")

    start_time = time.time()

    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f]
            total_passwords = len(passwords)
            if total_passwords == 0:
                print(f"{RED}[-] Wordlist is empty or could not be read.")
                sys.exit(1)
    except FileNotFoundError:
        print(f"{RED}[-] Error: Wordlist file not found at '{args.wordlist}'")
        sys.exit(1)

    worker_func = partial(check_password, target_hash=args.target_hash, algorithm=args.algorithm, salt=args.salt,
                          salt_position=args.salt_position)

    found_password = None

    with Pool(processes=args.processes) as pool:
        with tqdm(total=total_passwords, desc=f"{CYAN}Cracking", unit=" passwords") as pbar:
            for result in pool.imap_unordered(worker_func, passwords):
                pbar.update(1)
                if result:
                    found_password = result
                    pool.terminate()
                    break

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n" + "=" * 50)
    if found_password:
        print(f"{GREEN}[+] SUCCESS: Password found!")
        print(f"{GREEN}[+] Hash: {args.target_hash}")
        print(f"{GREEN}[+] Password: {found_password}")
        if args.output_file:
            try:
                with open(args.output_file, 'a') as f:
                    f.write(f"{args.target_hash}:{found_password}\n")
                print(f"{GREEN}[*] Result saved to '{args.output_file}'.")
            except IOError as e:
                print(f"{RED}[-] Could not write to the output file: {e}")
    else:
        print(f"{RED}[-] FAILURE: Password not found in the wordlist.")

    print("=" * 50)
    hashes_per_second = total_passwords / elapsed_time if elapsed_time > 0 else 0
    print(f"{YELLOW}[*] Total Time: {elapsed_time:.2f} seconds")
    print(f"{YELLOW}[*] Performance: {hashes_per_second:.2f} hashes/second")
    print("=" * 50)


if __name__ == "__main__":
    main()
