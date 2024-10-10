from math import prod
from typing import List
from tree.bplus import BPlusTree
from export import export_csv

class Hotel:
    def __init__(self, order: int = 5):
        self.tree = BPlusTree(order)
        self.last_room: int = 0
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
        ex_guest = int(input("Enter amount of peoples already in the hotel : "))
        inp = input("Enter amount of peoples/car/boat/spaceship : ")
        guest, car, boat, spaceship = map(int, inp.split("/"))
        print(f"Guests: {guest}, Cars: {car}, Boats: {boat}, Spaceships: {spaceship}")
        self.checkin_channels = [guest, car, boat, spaceship]

        self.ex_guest_start = guest * car * boat * spaceship
        self.manual_guest_start = (guest * car * boat * spaceship) + ex_guest

        for _ in range((guest * car * boat * spaceship) + ex_guest):
            self.insert_room()

        # return "Done"

    def manual_insert(self):
        amount = int(input("Enter amount of peoples : "))
        for _ in range(amount):
            self.insert_room()
            # print("room", self.last_room, "add!")

    def export_csv(self, filename: str):
        if not self.manual_guest_start:
            raise AttributeError
        export_csv(filename=filename, tree=self.tree, channels=self.checkin_channels, manual_start=self.manual_guest_start)

    def get_checkin_channels_from_room(self, room_index) -> List[int]:
        # room number starts with 1
        room_index -= 1
        # print(self.checkin_channels)
        total_rooms = self.ex_guest_start

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
