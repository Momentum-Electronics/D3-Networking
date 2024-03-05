""" Server implementation of D3 Networking.

Sends dummy data to a multicast group. The dummy data is signed using a pre-generated
private key.

DO NOT USE THE SAME KEY FOR YOUR IMPLEMENTATION.
"""
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from time import sleep
from d3networking.transport.transport import AvailablePayloadServer, AvailablePayloadMessage

SIGNING_KEY = b'd3d0ad95d720c6cf564210a3531d329577c72f763675adbd7dfd3ce2b23208c8'

server = AvailablePayloadServer(SigningKey(SIGNING_KEY, encoder=HexEncoder), proto=6)

seq_num: int = 0
while True:
    message = AvailablePayloadMessage(
        team_id=1,
        payload_size=2
    )

    server.send_message(message)
    sleep(5)
