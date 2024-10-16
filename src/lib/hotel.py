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

    # 4) การจัดเรียงลำดับหมายเลขห้อง
    def print_room_inorder(self):
        node = self.tree.get_leftmost_leaf()
        if not node:
            print('no room')
            return
        
        print('rooms inorder: ', end='')
        while node:
            print(' '.join(str(key) for key in node.keys), end=' ')
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
            for node_key in node.keys:
                if expected_key is None:
                    expected_key = node_key
                else:
                    while expected_key < node_key - 1:
                        expected_key += 1
                        print(expected_key, end=' ')
                        printed_any = True

                expected_key = node_key

            node = node.next_leaf

        if not printed_any:
            print("no room without guest")
            return
        
        print()