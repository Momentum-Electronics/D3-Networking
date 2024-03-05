from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from ..message.message import AvailablePayloadMessage


def validate_msg(msg: bytes, signature: bytes, verify_key: VerifyKey) -> bool:
    """ Validate that the message is properly signed.

    :param msg: The message to validate. Use the unsigned bytes message representation.
    :param signature: The message's signature.
    :param verify_key: The message's public key.
    :return: Whether the message is properly signed or not.
    """
    try:
        verify_key.verify(msg, signature)
    except BadSignatureError:
        return False

    return True


def validate_seq_num(seq_num: int, old_seq_num: int) -> bool:
    """ Validate that the sequence number comes after the old sequence number.

    :param seq_num: A sequence number to validate.
    :param old_seq_num: The previous sequence number.
    :return: Whether the sequence number was probably send after the old one.
    """
    if seq_num == 0:
        if old_seq_num == -1:
            return True
        if old_seq_num == INT_MAX_VAL:
            return True

        return False

    return seq_num > old_seq_num
