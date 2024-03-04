from pathlib import Path
from typing import Dict

from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from nacl.exceptions import TypeError


def _add_public_key_to_file(public_key: VerifyKey, store_path: Path):
    if not store_path.exists():
        raise IOError("Privided store path does not exist.")
    with open(store_path, "wb") as stream:
        stream.write(public_key.encode())

    print(f"Added public key to {str(store_path.resolve())}.")


def _validate_not_exists(path: Path):
    if path.exists():
        raise IOError("Provided store path already exists.")


def store_public_key(public_key: VerifyKey, store_path: Path, overwrite: bool = False):
    if not overwrite:
        _validate_not_exists(store_path)
    with open(store_path, "ab") as stream:
        stream.write(public_key.encode(encoder=HexEncoder))
    print(f"Public key saved at {str(store_path.resolve())}.")


def load_public_key(store_path: Path) -> VerifyKey:
    if not store_path.exists():
        raise IOError("Provided store path does not exist.")

    with open(store_path, "rb") as stream:
        key_bytes = stream.read()

    return VerifyKey(key_bytes, encoder=HexEncoder)


def store_keymap(keymap: Dict[int, VerifyKey], store_path: Path, overwrite: bool = False):
    if not overwrite:
        _validate_not_exists(store_path)

    if store_path.exists():
        store_path.unlink()
    store_path.touch()

    for _, value in sorted(keymap.items()):
        _add_public_key_to_file(value, store_path)

    print(f"Stored keymap at {str(store_path.resolve())}")


def load_keymap(store_path: Path, keys_amount: int = 6, key_size: int = 32) -> Dict[int, VerifyKey]:
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
