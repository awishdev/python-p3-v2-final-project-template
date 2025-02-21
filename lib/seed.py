from models.__init__ import CONN, CURSOR
from models.family_members import Family_Member
from models.tasks import Task

Family_Member.drop_table()
Task.drop_table()
Family_Member.create_table()
Task.create_table()

Aj = Family_Member("AJ", 5, "Son")
Lauren = Family_Member("Lauren", 7, "Daughter")
Violet = Family_Member("Violet", 2, "Daughter")
Katie = Family_Member("Katie", 35, "Wife")
Arthur = Family_Member("Arthur", 29, "Me")

Dishes = Task("Wash Dishes", 4)
Cooking = Task("Cook Dinner", 5)
Laundry = Task("Laundry", 4)
Pickup = Task("Pickup toys", 2)
Washcar = Task("Wash Car", 5)