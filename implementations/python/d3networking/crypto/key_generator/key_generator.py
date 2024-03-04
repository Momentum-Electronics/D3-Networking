from nacl.signing import SigningKey, VerifyKey
from ..key_storage.key_pair import KeyPair


class KeyGenerator:

    @staticmethod
    def generate_keypair() -> KeyPair:
        private_key: SigningKey = SigningKey.generate()
        pubic_key: VerifyKey = private_key.verify_key

        return KeyPair(private_key=private_key, public_key=pubic_key)
