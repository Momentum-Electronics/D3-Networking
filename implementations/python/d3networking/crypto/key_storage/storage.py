from pathlib import Path
from typing import Dict

from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from nacl.exceptions import TypeError


def _add_public_key_to_file(public_key: VerifyKey, store_path: Path):
    if not store_path.exists():
        raise IOError("Provided store path does not exist.")
    with open(store_path, "wb") as stream:
        stream.write(public_key.encode())

    print(f"Added public key to {str(store_path.resolve())}.")


def _validate_not_exists(path: Path):
    if path.exists():
        raise IOError("Provided store path already exists.")


def store_public_key(public_key: VerifyKey, store_path: Path, overwrite: bool = False):
    """ Writes a single public key to a key storage file.

    :param public_key: The public key to store as a VerifyKey object.
    :param store_path: The path towards where the public key should be saved.
    :param overwrite: If the file already exists, whether to overwrite the file's
    contents with the key. Default is False
    :return: None
    """
    if not overwrite:
        _validate_not_exists(store_path)
    with open(store_path, "wb") as stream:
        stream.write(public_key.encode())
    print(f"Public key saved at {str(store_path.resolve())}.")


def load_public_key(store_path: Path) -> VerifyKey:
    """ Load a single public key from a file.
    :param store_path: A binary file where the key is stored.
    :return: The key as a newly instanced VerifyKey object.
    """
    if not store_path.exists():
        raise IOError("Provided store path does not exist.")

    with open(store_path, "rb") as stream:
        key_bytes = stream.read()

    return VerifyKey(key_bytes)


def store_keymap(keymap: Dict[int, VerifyKey], store_path: Path, overwrite: bool = False):
    """ Store a map of keys.

    The map of keys is a dictionary that maps each key with a team identifier.

    The dictionary has the following structure:

        {
            1: VerifyKey
            2: VerifyKey
        }

    There should be an entry for each team identifier you plan to receive messages from.

    :param keymap: The keymap to store.
    :param store_path: A path towards a file where the keys will be stored.
    :param overwrite: Whether to overwrite the file's contents if it already exists. Default is False
    :return: None
    """
    if not overwrite:
        _validate_not_exists(store_path)

    if store_path.exists():
        store_path.unlink()
    store_path.touch()

    for _, value in sorted(keymap.items()):
        _add_public_key_to_file(value, store_path)

    print(f"Stored keymap at {str(store_path.resolve())}")


def load_keymap(store_path: Path, keys_amount: int = 6, key_size: int = 32) -> Dict[int, VerifyKey]:
    """
    Load keymap from a binary file.

    See the store_keymap documentation for more information on the file structure.

    This method assumes that the keys are stored in order starting with team identifier 1.

    :param store_path: Where to load the keymap from. Must be a binary file.
    :param keys_amount: The amount of keys to load from the file. The method makes
    no checks on the validity of this value. Default is 6 as there are 6 teams.
    :param key_size: The size of each key stored in the file. Defaults to 32 bytes as
    it is the size of an Ed25519 verify key.
    :return: A dictionary that maps each VerifyKey with its corresponding team id.
    """
    if not store_path.exists():
        raise IOError("Provided store path does not exist.")

    keymap: Dict[int, VerifyKey] = {}

    with open(store_path, "rb") as stream:
        try:
            for i in range(1, keys_amount + 1):
                key_bytes = stream.read(key_size)
                keymap[i] = VerifyKey(key_bytes)
        except TypeError:
            raise IOError("Bad format for provided store path file.")
    
    return keymap
