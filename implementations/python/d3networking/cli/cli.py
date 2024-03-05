from pathlib import Path
from typing import Dict

import click
from d3networking.crypto.key_generator.key_generator import KeyGenerator
from d3networking.crypto.key_storage.key_pair import print_keypair, KeyPair
from d3networking.crypto.key_storage.storage import store_keymap
from nacl.signing import VerifyKey


def _bad_key_err() -> None:
    print("Bad key format.")
    print("Operation cancelled")
    exit(1)


@click.group()
def app():
    """ Utility script to generate and store signing keys.
    """
    pass


@click.command()
def generate_keypair():
    """Generate a public and a private key for message signing.
    
    Keep the private key private and share your public key with the recipients
    of your messages.
    """
    keys: KeyPair = KeyGenerator.generate_keypair()
    print_keypair(keys)


@click.command()
@click.option('--amount', default=1, help="Amount of keys to store.")
@click.argument("path", type=click.Path())
def store_sign_keys(amount, path):
    """Prompts the user for a certain amount of keys and stores them to the provided path.
    
    Keys should be provided in hexadecimal encoding.
    """
    keys: Dict[int, VerifyKey] = {}

    for i in range(1, amount + 1):
        key_as_str = input(f"Key for team {i}: ")
        try:
            key = VerifyKey(bytes.fromhex(key_as_str))
            keys[i] = key
        except TypeError:
            _bad_key_err()
        except ValueError:
            _bad_key_err()

    store_keymap(keys, store_path=Path(path), overwrite=True)


app.add_command(generate_keypair)
app.add_command(store_sign_keys)


def main():
    app()
