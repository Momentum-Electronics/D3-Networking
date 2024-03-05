from nacl.signing import SigningKey, VerifyKey
from ..key_storage.key_pair import KeyPair


class KeyGenerator:
    """ Class to generate Ed25519 key pairs.
    """
    @staticmethod
    def generate_keypair() -> KeyPair:
        """
        Generates a new key pair and returns it as a KeyPair object.
        :return: A named tuple  containing the private key and the public key.
        """
        private_key: SigningKey = SigningKey.generate()
        pubic_key: VerifyKey = private_key.verify_key

        return KeyPair(private_key=private_key, public_key=pubic_key)
