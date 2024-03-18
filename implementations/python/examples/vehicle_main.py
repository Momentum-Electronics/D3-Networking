""" Vehicle implementation for D3 networking

Example of a vehicle implementation using the D3 networking library.
"""
from d3networking.message.message import AvailablePayloadMessage
from d3networking.vehicle.vehicle import listen_for_drop_point_infos

NB_SECONDS_TO_LISTEN = 3

decision_picked = False
while not decision_picked:
    received_infos: list[AvailablePayloadMessage] = listen_for_drop_point_infos(NB_SECONDS_TO_LISTEN)
    
    if len(received_infos) == 0:
        continue

    # Example of a simple decision making process, we take the one with the max payload size
    chosen_msg = max(received_infos, key=lambda msg: msg.payload_size)
    print(f"Chosen drop point: ZC{chosen_msg.team_id}")
    
    # Exit the loop and let the vehicle go to the chosen drop point
    decision_picked = True
    

