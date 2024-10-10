from typing import List
from tree.bplus import BPlusTree

def export_csv(filename: str, tree: BPlusTree, channels: List[int], manual_start: int):
    def room_to_csv(room: int) -> str:
        manual = False
        if room >= manual_start:
            manual = True

        channels_output = map(lambda channel_count: str(room % channel_count), channels)
        return f'{room},{manual},{','.join(channels_output)}\n'

    rooms = tree.get_list()

    with open(filename, "w", encoding='utf-8') as file:
        for room in rooms:
            file.write(room_to_csv(room=room))
