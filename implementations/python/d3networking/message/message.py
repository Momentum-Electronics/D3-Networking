from dataclasses import dataclass
from ..exceptions.exceptions import InvalidMessageException


def _append_bytes(msg_as_bytes: bytearray, data: int, size: int = 4):
    """
    Appends bytes to the end of the message.
    The data is inserted LSB first (little endian).

    :param msg_as_bytes: bytearray to append to.
    :param data: bytes to append as a 32 bits integer
    :param size: size (in bytes) of the data to append.
    :return: None
    """
    if size > 4:
        raise ValueError("size must be less than 5")

    for i in range(size):
        msg_as_bytes.append((data >> (i * 8)) & 0xFF)


def _read_bytes(msg_as_bytes: bytearray, start_idx: int, size: int = 4) -> int:
    """ Read bytes from a bytearray to form a 32 bits signed integer.

    The integer is assumed to be stored LSbyte-first.

    :param msg_as_bytes: A bytearray representation of a message.
    :param start_idx: The index from which to start reading the integer.
    :param size: The size of the integer. Should be a value from 1 to 4 inclusively.
    :return: An integer loaded from the bytearray.
    """
    if size > 4:
        raise ValueError("size must be less than 5")

    value: int = 0

    for i in range(start_idx, start_idx + size):
        value += (msg_as_bytes[i] & 0xFF) << ((i - start_idx) * 8)

    return value


@dataclass
class AvailablePayloadMessage:
    """ Messages that are send by the server to communicate the size of the available payload.
    """
    team_id: int
    """ Team's identifier as an 8 bit unsigned integer.
    """
    payload_size: int
    """ Size of the payload as an 8 bit unsigned integer. 
    """
    seq_num: int = 0
    """ Sequence number of the packet. Used to validate that the packets arrive in order.
    """
    sig_size: int = 0
    """ Size of the signature. There is no signature if the size is 0.
    """
    signature: bytearray = bytearray()
    """ Bytearray representation of the signature.
    """

    def as_bytes(self) -> bytes:
        """
        Bytes representation of the message

        Includes all fields.

        :return: The current object represented by a group of 10 to 508 bytes.
        """

        unsigned_msg = bytearray(self.as_unsigned_bytes())
        _append_bytes(unsigned_msg, self.sig_size)  # 4 bytes signature length
        if self.is_signed():
            unsigned_msg += self.signature

        if len(unsigned_msg) > 508:
            raise ValueError("Message does not fit in a 508 bytes UDP payload.")

        return bytes(unsigned_msg)

    def as_unsigned_bytes(self) -> bytes:
        """
        Bytes representation of an unsigned message. Includes the following fields:

        - team id
        - payload size
        - sequence number

        This is the part of the message included for the signature.

        :return: A bytes representation of a part of the message.
        """
        msg_as_bytes: bytearray = bytearray()
        msg_as_bytes.append(self.team_id)
        msg_as_bytes.append(self.payload_size)
        _append_bytes(msg_as_bytes, self.seq_num)  # 4 bytes sequence number

        return bytes(msg_as_bytes)

    def is_signed(self) -> bool:
        """ Checks if the size of the signature is greater than 0.
        :return: Whether the size of the signature is greater than 0.
        """
        if self.sig_size > 0:
            return True
        return False

    @staticmethod
    def from_bytes(msg_as_bytes: bytes):
        """
        Creates a Message object from a group of bytes.

        :param msg_as_bytes: Bytes representation of a message.
        :return: The group of bytes interpreted as an AvailablePayloadMessage object.
        """
        msg_as_bytes = bytearray(msg_as_bytes)
        team_id = msg_as_bytes[0]
        payload_size = msg_as_bytes[1]
        seq_num = _read_bytes(msg_as_bytes, 2)
        sig_size = _read_bytes(msg_as_bytes, 6)
        signature = bytearray()
        if sig_size > 0:
            if len(msg_as_bytes) < 10 + 3 + sig_size + 1:
                raise InvalidMessageException("Signature does not fit in message length.")
            signature = msg_as_bytes[10: 10 + 3 + sig_size]

        msg_from_bytes = AvailablePayloadMessage(
            team_id=team_id,
            payload_size=payload_size,
            seq_num=seq_num,
            sig_size=sig_size,
            signature=signature
        )

        return msg_from_bytes
