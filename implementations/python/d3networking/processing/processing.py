from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from ..message.message import AvailablePayloadMessage


def validate_msg(msg: bytes, signature: bytes, verify_key: VerifyKey) -> bool:
    try:
        verify_key.verify(msg, signature)
    except BadSignatureError:
        return False

    return True


def validate_seq_num(seq_num: int, old_seq_num: int) -> bool:
    if seq_num == 0:
        if old_seq_num == -1:
            return True
        if old_seq_num == INT_MAX_VAL:
            return True

        return False

    return seq_num > old_seq_num
