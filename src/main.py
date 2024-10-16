"""
Enter amount of ppl in Hotel : 132
Enter amount of ppl/car/boat/spaceship : 100/100/10/1
Enter amount of ppl : 128
100260

คนเก่าอยู่ 132 คน
มาใหม่ 100ppl/car, 100car/boat, 10boat/spaceship
and 1 spaceship totall
มาใหม่ mamual = 128
รวม 100260 ห้อง
"""

from hotel import Hotel

manrood = Hotel()
manrood.initialize()
print(manrood.last_room)
manrood.manual_insert()
print(manrood.last_room)

#manrood.export_csv('export.csv')

#manrood.print_room_inorder()
#manrood.print_missing_rooms_inorder()
