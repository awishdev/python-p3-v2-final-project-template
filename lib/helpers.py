# lib/helpers.py
from models.family_members import Family_Member
from models.tasks import Task
#from seed import seeder

def view_members():
    print("***Family Members***")
    for member in Family_Member.get_all():
        print(f"{member.id}.{member.name}")

def get_member(id):
    member = Family_Member.find_by_id(id)
    if member.name == "Arthur":
        print("It's you!")
    else:
        print(f"{member.name} is {member.age} years old and is your {member.title}")

def tasks_by_id(id):
    print(f"***Tasks for {Family_Member.find_by_id(id).name}***")
    for task in Task.all_tasks_for_id(id):
        print(f"{task.description}")

def view_tasks():
    print("***Tasks***")
    for task in Task.get_all():
        member = Family_Member.find_by_id(task.family_member_id)
        print(f"{task.description} to be done by {member.name}")
    print("***********")

def exit_program():
    print("Goodbye!")
    exit()

def seed():
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

def add_task(id):
    description = input("Enter the description of the task: ")
    Task(description, int(id))
    print("Task added!")