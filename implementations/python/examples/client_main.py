"""

Receives messages, validates their signatures and prints message information
on the standard output.
"""

from pathlib import Path

from d3networking.crypto.key_storage.storage import load_keymap
from d3networking.transport.transport import AvailablePayloadClient, AvailablePayloadMessage

validate_keys = load_keymap(store_path=Path("./demo.keys"), keys_amount=1)

client = AvailablePayloadClient(validate_keys, proto=6)

while True:
    msg: AvailablePayloadMessage = client.recv_message(validate=True)  # Drops messages with no valid signature
    if msg is not None:
        print(f"Team {msg.team_id} has {msg.payload_size} containers available.")
