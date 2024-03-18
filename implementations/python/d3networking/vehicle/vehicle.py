import datetime

from ..transport.transport import AvailablePayloadClient, AvailablePayloadMessage


def listen_for_drop_point_infos(nb_seconds: int) -> list[AvailablePayloadMessage]:
    """
    Listen for drop point infos from the server for a given amount of time.

    :param nb_seconds: The number of seconds to listen for drop point infos.
    """

    # Start client on IPv6
    validate_keys = []
    client = AvailablePayloadClient(validate_keys, proto=6)

    received_infos: dict[int, AvailablePayloadMessage] = {}

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=nb_seconds)
    while datetime.datetime.now() <= end_time:
        msg: AvailablePayloadMessage = client.recv_message(validate=False)
        
        # Check if message was received properly
        if msg is None:
            continue

        # Check if message content is valid
        if msg.team_id < 0 or msg.team_id > 99:
            print("Invalid message content received")
            continue
        
        received_infos[msg.team_id] = msg
    
    client.close_connection()

    return list(received_infos.values())
        

        