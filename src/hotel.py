from math import prod
from typing import List
from tree.bplus import BPlusTree

class Hotel:
    def __init__(self, order: int = 5):
        self.tree = BPlusTree(order)
        self.last_room: int = 0
        self.ex_guest: int = 0
        self.ex_guest_start: None | int = None
        self.manual_guest_start: None | int = None
        self.checkin_channels: List[int] = []

    def insert_room(self):
        self.last_room += 1
        self.tree.insert(self.last_room, None)

    def show_tree(self):
        self.tree.show_bfs()
        print(self.last_room)

    def initialize(self):
        self.ex_guest = int(input("Enter amount of peoples already in the hotel : "))
        inp = input("Enter amount of peoples/car/boat/spaceship : ")
        guest, car, boat, spaceship = map(int, inp.split("/"))
        print(f"Guests: {guest}, Cars: {car}, Boats: {boat}, Spaceships: {spaceship}")
        self.checkin_channels = [guest, car, boat, spaceship]

        self.ex_guest_start = guest * car * boat * spaceship
        self.manual_guest_start = (guest * car * boat * spaceship) + self.ex_guest

        for _ in range((guest * car * boat * spaceship) + self.ex_guest):
            self.insert_room()

        # return "Done"

    def manual_insert(self):
        amount = int(input("Enter amount of peoples : "))
        for _ in range(amount):
            self.insert_room()
            # print("room", self.last_room, "add!")

    def export_csv(self, filename: str):
        def room_to_csv(room: int) -> str:
            manual = False
            if not self.manual_guest_start:
                raise AttributeError
            if room <= self.ex_guest:
                manual = True
                channels_output = [0] * len(self.checkin_channels)
            elif room > self.manual_guest_start:
                manual = True
                channels_output = [0] * len(self.checkin_channels)
            else:
                channels_output = self.get_checkin_channels_from_room(room_index=room)

            return f'{room},{manual},{','.join(map(str, channels_output))}\n'

        rooms = self.tree.get_list()

        with open(filename, "w", encoding='utf-8') as file:
            channels_header = [f'channel{i+1}' for i in range(len(self.checkin_channels))]
            file.write(f'room_number,is_manual_checkin,{','.join(channels_header)}\n')

            for room in rooms:
                file.write(room_to_csv(room=room))

    def get_checkin_channels_from_room(self, room_index) -> List[int]:
        # room number starts with 1
        room_index -= 1
        # print(self.checkin_channels)
        if not self.ex_guest_start:
            raise AttributeError
        total_rooms = self.ex_guest_start

        if room_index < self.ex_guest:
            return []

        room_index -= self.ex_guest

        if room_index >= total_rooms:
            return []

        checkin_channels: List[int] = [room_index % self.checkin_channels[0]]
        # print(checkin_channels)

        for channel_index, _ in enumerate(self.checkin_channels[1:-1:], 1):
            current_total_seats = prod(self.checkin_channels[:channel_index:])
            next_total_seats = prod(self.checkin_channels[:channel_index+1:])
            current_channel_index = (room_index % next_total_seats) // current_total_seats
            checkin_channels.append(current_channel_index)
            # print(self.checkin_channels[0:channel_index:], self.checkin_channels[0:channel_index+1:])
            # print(current_total_seats, next_total_seats)
            # print(checkin_channels)

        checkin_channels.append(room_index // prod(self.checkin_channels[:-1:]))

        # normalized to start with 1
        normalized_checkin_chennels = list(map(lambda i: i+1, checkin_channels))
        return normalized_checkin_chennels

    # function returns the origin of the room based on its index.
    def get_room_origin(self, room_index, tt_room, tt_space, tt_boat, tt_car):
        if room_index > tt_room:
            if room_index > tt_room + self.ex_guest_start:
                return f"Room {room_index} from manual"
            return f"Room {room_index} from 0 (Ex_Guest)"

        spaceship_index = room_index // tt_space
        boat_index = (room_index % tt_space) // tt_boat
        car_index = (room_index % tt_boat) // tt_car
        guest_index = room_index % tt_car

        if guest_index == 0:
            guest_index = tt_car

        return f"Room {room_index} comes from: spaceship {spaceship_index+1}, boat {boat_index+1}, car {car_index+1}, guest {guest_index}"

    # 4) function return linked list from b+tree -> inorder
    def inorder_traversal(self) -> list:
        node = self.tree.get_leftmost_leaf()
        if not node:
            return []

        arr = []

        total_rooms = self.checkin_channels[0] * self.checkin_channels[1] * self.checkin_channels[2] * self.checkin_channels[3]
        total_seats_per_spaceship = self.checkin_channels[0] * self.checkin_channels[1] * self.checkin_channels[2]
        total_seats_per_boat = self.checkin_channels[0] * self.checkin_channels[1]
        total_seats_per_car = self.checkin_channels[0]

        while node:
            for node_key in node.keys:
                arr.append((node_key, self.get_room_origin(node_key, total_rooms, total_seats_per_spaceship, total_seats_per_boat, total_seats_per_car)))
            node = node.next_leaf

        return arr

    # 6) function return linked list from b+tree -> reverse order
    def reverseorder_traversal(self) -> list:
        return list(reversed(self.inorder_traversal()))