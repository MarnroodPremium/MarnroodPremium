from math import prod
from typing import List
from tree.bplus import BPlusTree

class Hotel:
    def __init__(self, order: int = 5):
        self.tree = BPlusTree(order)
        self.last_room: int = 0
        self.ex_guest: int = 0
        self.ex_guest_start: None | int = None
        self.new_guest_start: None | int = None
        self.checkin_channels: List[int] = []

    def insert_room(self):
        self.last_room += 1
        self.tree.insert(self.last_room, self.last_room)

    def show_tree(self):
        self.tree.show_bfs()
        print(self.last_room)

    def initialize(self):
        self.ex_guest = int(input("Enter amount of peoples already in the hotel : "))
        inp = input("Enter amount of peoples/car/boat/spaceship : ")
        guest, car, boat, spaceship = map(int, inp.split("/"))
        print(f"Guests: {guest}, Cars: {car}, Boats: {boat}, Spaceships: {spaceship}")
        self.checkin_channels = [guest, car, boat, spaceship]

        self.ex_guest_start = (guest * car * boat * spaceship) + 1
        self.new_guest_start = 1

        for _ in range((guest * car * boat * spaceship) + self.ex_guest):
            self.insert_room()

        # return "Done"

    def manual_insert(self):
        amount = int(input("Enter amount of peoples : "))
        for _ in range(amount):
            self.insert_room()
            self.ex_guest_start += 1
            self.new_guest_start += 1
            # print("room", self.last_room, "add!")

    def export_csv(self, filename: str):
        def room_to_csv(room: int) -> str:
            manual = True
            if not self.new_guest_start:
                raise AttributeError
            if room < self.new_guest_start:
                channels_output = [0] * len(self.checkin_channels)
            elif room >= self.ex_guest_start:
                manual = False
                channels_output = [0] * len(self.checkin_channels)
            else:
                manual = False
                channels_output = self.get_checkin_channels_from_room(room_index=room)

            return f"{room},{manual},{','.join(map(str, channels_output))}\n"

        rooms = self.tree.get_list()

        with open(filename, "w", encoding='utf-8') as file:
            channels_header = [f'channel{i+1}' for i in range(len(self.checkin_channels))]
            file.write(f"room_number,is_manual_checkin,{','.join(channels_header)}\n")

            for room in rooms:
                file.write(room_to_csv(room=room))

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

    # 4) การจัดเรียงลำดับหมายเลขห้อง
    def print_room_inorder(self):
        node = self.tree.get_leftmost_leaf()
        if not node:
            print('no room')
            return

        print('rooms inorder: ', end='')
        while node:
            for value in node.values:
                if value != None:
                    print(*value, end=' ')
            node = node.next_leaf
        print()

    # 6) การแสดงจำนวนหมายเลขห้องที่ไม่มีแขกเข้าพัก (ให้ห้องพักหมายเลขมากที่สุดเป็นห้องสุดท้าย)
    def print_missing_rooms_inorder(self):
        node = self.tree.get_leftmost_leaf()
        if not node:
            print('no room')
            return

        expected_key = None
        printed_any = False

        print('missing rooms inorder: ', end='')
        while node:
            for value in node.values:
                if value == None:
                    printed_any = True
                    print(node.keys[node.values.index(value)], end=' ')
            node = node.next_leaf

        if not printed_any:
            print("no room without guest")
            return

        print()

    def delete(self, room_idx):
        node, i = self.tree.retrieve(room_idx)
        if node != None:
            node.values[i] = None
            print("Room Deleted")
        else:
            print("Not Found")

    def search(self, room_idx):
        node, i = self.tree.retrieve(room_idx)
        if node != None:
            value = node.values[i]
            if value != None:
                manual = True
                if room_idx < self.new_guest_start:
                    channels_output = [0] * len(self.checkin_channels)
                elif room_idx >= self.ex_guest_start:
                    manual = False
                    channels_output = [0] * len(self.checkin_channels)
                else:
                    manual = False
                    channels_output = self.get_checkin_channels_from_room(room_index=room_idx)
                print(f"{room_idx},add by manual:{manual},{','.join(map(str, channels_output))}")
                return
        print("Not Found")