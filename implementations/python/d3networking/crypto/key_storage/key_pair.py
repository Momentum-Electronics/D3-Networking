from typing import NamedTuple
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey


class KeyPair(NamedTuple):
    public_key: VerifyKey
    private_key: SigningKey


def print_keypair(keypair: KeyPair):
    print(f"Private key: {keypair.private_key.encode(encoder=HexEncoder)}")
    print(f"Public key: {keypair.public_key.encode(encoder=HexEncoder)}")
    print("Keep the private key PRIVATE.")
