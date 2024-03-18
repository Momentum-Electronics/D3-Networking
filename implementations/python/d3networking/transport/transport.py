import socket
import struct
from typing import Literal, Union, Dict

from ..message.message import AvailablePayloadMessage, _append_bytes
from ..processing.processing import validate_msg, validate_seq_num

from nacl.signing import VerifyKey, SigningKey, SignedMessage

V6_MULTICAST_GRP = "ff12::e01"
V4_MULTICAST_GRP = "224.0.0.70"
PORT = 36868
INT_MAX_VAL = 2_147_483_647


class AvailablePayloadServer:
    """ Server implementation for D3 networking.
    """
    def __init__(self, signing_key: Union[SigningKey, None], proto: Literal[4, 6] = 6):
        """ Instantiate an AvailablePayloadServer

        :param signing_key: The key used to sign messages. Messages won't be signed if this is set to None.
        :param proto: The network protocol to use (IPv4 or IPv6).
        """
        self._port = PORT
        if proto == 6:
            self._addr = V6_MULTICAST_GRP
        else:
            self._addr = V4_MULTICAST_GRP

        self._addr_info = socket.getaddrinfo(self._addr, None)[0]
        self._socket = socket.socket(self._addr_info[0], socket.SOCK_DGRAM)  # Use UDP
        self.signing_key = signing_key
        self.seq_num = 0

    def send_message(self, msg: AvailablePayloadMessage):
        """ Send a message to the UDP socket.

        :param msg: An unsigned message ready to be sent. This method takes care of signing the message and setting the
        key length attribute before sending.
        :return: None.
        """
        msg.seq_num = self.seq_num
        if self.signing_key is not None:
            signed_msg: SignedMessage = self.signing_key.sign(msg.as_unsigned_bytes())
            sig_length: int = len(bytearray(len(signed_msg.signature)))
            assert (sig_length <= INT_MAX_VAL)
            msg.sig_size = sig_length
            msg.signature = bytearray(signed_msg.signature)
        self._socket.sendto(msg.as_bytes(), (self._addr_info[4][0], self._port))
        self.seq_num += 1
        self.seq_num %= INT_MAX_VAL + 1


class AvailablePayloadClient:
    """ Client implementation of D3 networking.
    """
    def __init__(self, validate_keys: Dict[int, VerifyKey], scope_id: int = 0, proto: Literal[4, 6] = 6):
        """ Instantiate an AvailablePayloadClient

        :param validate_keys: Mapping between team identifiers and their public keys. This is used to validate
        message signatures.
        :param scope_id: Scope id of the network interface to use.
        :param proto: The network protocol to use (IPv4 or IPv6).
        """
        self._port = PORT
        if proto == 6:
            self._addr = V6_MULTICAST_GRP
        else:
            self._addr = V4_MULTICAST_GRP

        self._addr_info = socket.getaddrinfo(self._addr, None)[0]
        self._socket = socket.socket(self._addr_info[0], socket.SOCK_DGRAM)  # Use UDP

        self._socket.bind(("", self._port))
        self.validate_keys = validate_keys

        self._join_multicast_grp(proto, scope_id)
        self.prev_seq_num = -1

    def _join_multicast_grp(self, proto: Literal[4, 6], scope_id: int):
        grp = socket.inet_pton(self._addr_info[0], self._addr_info[4][0])

        if proto == 6:
            mreq = grp + struct.pack('@I', scope_id)
            self._socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        else:
            mreq = grp + struct.pack('=I', socket.INADDR_ANY)
            self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    @staticmethod
    def _validate_data(data: bytes) -> bool:
        if len(data) < 10:
            return False

        return True

    def close_connection(self):
        """ Close the connection to the multicast group.
        """
        self._socket.shutdown()
        self._socket.close()

    def recv_message(self, validate: bool = True) -> Union[AvailablePayloadMessage, None]:
        """ Receive a message on the UDP socket.

        This is a blocking call.

        :param validate: Whether to drop the message if it has no valid signature or not.
        :return: The message if it is valid, None otherwise.
        """
        data, _ = self._socket.recvfrom(1500)
        data.rstrip()

        if not AvailablePayloadClient._validate_data(data):
            print("Message dropped because of invalid message format.")
            return None

        parsed_message = AvailablePayloadMessage.from_bytes(data)

        if not parsed_message.is_signed() and validate:
            print("Message dropped because it was not signed.")
            return None

        if parsed_message.team_id in self.validate_keys.keys():
            validate_key = self.validate_keys[parsed_message.team_id]
        else:
            validate_key = None

        if validate and not validate_msg(parsed_message.as_unsigned_bytes(), bytes(parsed_message.signature), validate_key):
            print("Message dropped because the signature was not valid.")
            return None

        if not validate_seq_num(seq_num=parsed_message.seq_num, old_seq_num=self.prev_seq_num):
            print("Message dropped because it was expired.")
            return None  # Expired message

        self.prev_seq_num = parsed_message.seq_num
        return parsed_message
