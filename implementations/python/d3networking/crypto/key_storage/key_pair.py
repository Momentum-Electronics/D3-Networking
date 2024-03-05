from typing import NamedTuple
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey


class KeyPair(NamedTuple):
    """ Represents a pair of Ed25519 public and private keys.
    """
    public_key: VerifyKey
    """ The public key. This can be share with anyone.
    
    Used to verify signatures.
    """
    private_key: SigningKey
    """ The private key. This cannot be shared with anyone!
    
    Used to sign messages.
    """


def print_keypair(keypair: KeyPair):
    """ Display a pair of keys to the standard output.

    :param keypair: A pair of private and public keys to display to the standard
    output.
    :return: None
    """
    print(f"Private key: {keypair.private_key.encode(encoder=HexEncoder)}")
    print(f"Public key: {keypair.public_key.encode(encoder=HexEncoder)}")
    print("Keep the private key PRIVATE.")
