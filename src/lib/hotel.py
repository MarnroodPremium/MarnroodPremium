from typing import List
from .tree.bplus import BPlusTree
from .export import export_csv

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
        export_csv(tree=self.tree, filename=filename)