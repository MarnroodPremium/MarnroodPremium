from math import prod
from typing import List, Tuple
from tree.bplus import BPlusTree
from track import track


class Hotel:
    def __init__(self, channels: List[int], order: int = 5):
        self.tree = BPlusTree(order)
        self.last_room: int = 0
        self.ex_guest: int = channels.pop()
        self.ex_guest_start: int = prod(channels) + 1
        self.new_guest_start: int = 1
        self.checkin_channels: List[int] = channels

        self.initialize()

    def insert_room(self):
        self.last_room += 1
        self.tree.insert(self.last_room, self.last_room)

    def show_tree(self):
        self.tree.show_bfs()
        print(self.last_room)

    def room_to_text(self, room: int) -> str:
        if not self.new_guest_start:
            raise AttributeError

        # manual check-in
        if room < self.new_guest_start:
            return f"{room}_manual\n"

        # ex-guest
        if room >= self.ex_guest_start:
            channels_output = [0] * len(self.checkin_channels)
            channels_output.append(1)
        # from main channels
        else:
            channels_output = self.get_checkin_channels_from_room(room_index=room)
            channels_output.append(0)

        return f"{room}_{'_'.join(map(str, channels_output))}\n"

    @track
    def initialize(self):
        guest, car, boat, spaceship = self.checkin_channels
        self.checkin_channels = [guest, car, boat, spaceship]

        self.ex_guest_start = (guest * car * boat * spaceship) + 1
        self.new_guest_start = 1

        for _ in range((guest * car * boat * spaceship) + self.ex_guest):
            self.insert_room()

    @track
    def manual_insert(self, amount: int) -> List[int]:
        for _ in range(amount):
            self.insert_room()
            self.ex_guest_start += 1
            self.new_guest_start += 1
            # print("room", self.last_room, "add!")
        return list(range(1, amount + 1))

    @track
    def export_as_file(self, filename: str):
        rooms = self.tree.get_list()

        with open(filename, "w", encoding="utf-8") as file:
            for room in rooms:
                file.write(self.room_to_text(room=room))

    def get_checkin_channels_from_room(self, room_index) -> List[int]:
        # room number starts with 1
        room_index -= self.new_guest_start
        # print(self.checkin_channels)
        total_rooms = self.ex_guest_start - self.new_guest_start

        if room_index >= total_rooms:
            return []

        checkin_channels: List[int] = [room_index % self.checkin_channels[0]]
        # print(checkin_channels)

        for channel_index, _ in enumerate(self.checkin_channels[1:-1:], 1):
            current_total_seats = prod(self.checkin_channels[:channel_index:])
            next_total_seats = prod(self.checkin_channels[: channel_index + 1 :])
            current_channel_index = (
                room_index % next_total_seats
            ) // current_total_seats
            checkin_channels.append(current_channel_index)
            # print(self.checkin_channels[0:channel_index:], self.checkin_channels[0:channel_index+1:])
            # print(current_total_seats, next_total_seats)
            # print(checkin_channels)

        checkin_channels.append(room_index // prod(self.checkin_channels[:-1:]))

        # normalized to start with 1
        normalized_checkin_chennels = list(map(lambda i: i + 1, checkin_channels))
        return normalized_checkin_chennels

    # 4) การจัดเรียงลำดับหมายเลขห้อง
    @track
    def get_all_rooms(self) -> None | List[int]:
        node = self.tree.get_leftmost_leaf()
        if not node:
            return None

        rooms: List[int] = []
        while node:
            for value in node.values:
                if value is not None and isinstance(value, list):
                    rooms.extend(value)
            node = node.next_leaf
        return rooms

    # 6) การแสดงจำนวนหมายเลขห้องที่ไม่มีแขกเข้าพัก (ให้ห้องพักหมายเลขมากที่สุดเป็นห้องสุดท้าย)
    @track
    def get_empty_rooms(self) -> None | List[int]:
        node = self.tree.get_leftmost_leaf()
        if not node:
            return None

        rooms: List[int] = []
        while node:
            for value in node.values:
                if value is None:
                    rooms.append(node.keys[node.values.index(value)])
            node = node.next_leaf

        return rooms

    @track
    def delete(self, room_idx: int) -> bool:
        node, i = self.tree.retrieve(room_idx)
        if node is not None:
            node.values[i] = None  # type: ignore
            return True
        else:
            return False

    @track
    def search(self, room_idx: int) -> None | Tuple[bool, List[int]]:
        node, i = self.tree.retrieve(room_idx)
        if node is not None:
            value = node.values[i]
            if value is not None:
                manual = True
                if room_idx < self.new_guest_start:
                    channels_output = [0] * len(self.checkin_channels)
                elif room_idx >= self.ex_guest_start:
                    manual = False
                    channels_output = [0] * len(self.checkin_channels)
                else:
                    manual = False
                    channels_output = self.get_checkin_channels_from_room(
                        room_index=room_idx
                    )
                return (manual, channels_output)
        # print("{room_idx} -> Not Found")
        return None
