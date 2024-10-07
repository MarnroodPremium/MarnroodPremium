from .tree.bplus import BPlusTree

class Hotel(BPlusTree):
    def __init__(self, order = 5):
        super().__init__(order)
        self.last_room = 0
        self.ex_guest_start = None
        self.manual_guest_start = None

    def insert_room(self):
        self.last_room += 1
        self.insert(self.last_room, None)

    def printHotel(self):
        self.show_bfs()
        print(self.last_room)

    def invite_stack(self):
        ex_guest = int(input("Enter amount of ppl in Hotel : "))
        inp = input("Enter amount of ppl/car/boat/spaceship : ")
        guest, car, boat, spaceship = map(int, inp.split("/"))
        print(f"Guests: {guest}, Cars: {car}, Boats: {boat}, Spaceships: {spaceship}")

        self.ex_guest_start = guest * car * boat * spaceship
        self.manual_guest_start = (guest * car * boat * spaceship) + ex_guest

        for i in range((guest * car * boat * spaceship) + ex_guest):
            self.insert_room()

        #return "Done"

    def manual_insert(self):
        amount = int(input("Enter amount of ppl : "))
        for i in range(amount):
            self.insert_room()
            #print("room", self.last_room, "add!")
            