from .tree.bplus import BPlusTree

class Hotel:
    def __init__(self, order: int = 5):
        self.tree = BPlusTree(order)
        self.last_room = 0
        self.ex_guest_start = None
        self.manual_guest_start = None

    def insert_room(self):
        self.last_room += 1
        self.tree.insert(self.last_room, None)

    def show_tree(self):
        self.tree.show_bfs()
        print(self.last_room)

    def initialize(self):
        global ex_guest, guest, car, boat, spaceship # พอดีต้องใช้ค่าพวกนี้หาว่าคนมาจากทางไหน แต่ไม่อยากแก้โค้ดเพื่อนง่ะ
        ex_guest = int(input("Enter amount of peoples already in the hotel : "))
        inp = input("Enter amount of peoples/car/boat/spaceship : ")
        guest, car, boat, spaceship = map(int, inp.split("/"))
        print(f"Guests: {guest}, Cars: {car}, Boats: {boat}, Spaceships: {spaceship}")

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

    # function returns the origin of the room based on its index.
    def get_room_origin(self, room_index, tt_room, tt_space, tt_boat, tt_car):        
        if room_index > tt_room:
            if room_index > tt_room + ex_guest:
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

        total_rooms = guest * car * boat * spaceship
        total_seats_per_spaceship = guest * car * boat
        total_seats_per_boat = guest * car
        total_seats_per_car = guest

        while node:
            for node_key in node.keys:
                arr.append((node_key, self.get_room_origin(node_key, total_rooms, total_seats_per_spaceship, total_seats_per_boat, total_seats_per_car)))
            node = node.next_leaf
        
        return arr

    # 6) function return linked list from b+tree -> reverse order
    def reverseorder_traversal(self) -> list:
        return list(reversed(self.inorder_traversal()))