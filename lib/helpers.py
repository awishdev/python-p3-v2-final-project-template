# lib/helpers.py
from models.family_members import Family_Member
from models.tasks import Task

def view_members():
    # display family members in numbered list
    print("***Family Members***")
    for member in Family_Member.get_all():
        print(f"{member.id}.{member.name}")

def get_member(id):
    # search for a specific family member by id
    member = Family_Member.find_by_id(id)
    # check if its me!
    if member.name == "Arthur":
        print("It's you!")
    else:
        print(f"{member.name} is {member.age} years old and is your {member.title}")

def tasks_by_id(id):
    # display tasks for a specific family member by id
    print(f"***Tasks for {Family_Member.find_by_id(id).name}***")
    for task in Task.all_tasks_for_id(id):
        print(f"{task.description}")

def view_tasks():
    # display all tasks in numbered list
    print("***Tasks***")
    for task in Task.get_all():
        member = Family_Member.find_by_id(task.family_member_id)
        print(f"{task.id}.{task.description} to be done by {member.name}")
    print("***********")

def exit_program():
    #toodles
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

def pick_member():
    view_members()
    choice = input("Enter the number of the family member you want to add a task for: ")
    return int(choice)

def update_member_info(id):
    name = input("Enter the new name: ")
    age = input("Enter the new age: ")
    title = input("Enter the new title: ")
    Family_Member.update(id, name, int(age), title)
    print("Member information updated!")

def delete_member(id):
    member = Family_Member.find_by_id(id)
    if member:
        print(f"Are you sure you want to delete {member.name} (y/n)?")
        choice = input(">")
        if choice.lower() == "y":
            member.delete()
            print(f"{member.name} has been deleted!")
        elif choice.lower() == "n":
            print("Member deletion cancelled.")
        else:
            print("Invalid choice. Member deletion cancelled.")
    else:
        print("Member not found.")

def search_by_family_member(id):
    family_member = Family_Member.find_by_id(id)
    if family_member:
        print(f"Tasks for {family_member.name}:")
        for task in Task.all_tasks_for_id(id):
            print(f"{task.description}")
    else:
        print("Family member not found.")

def search_by_description(description):
    tasks = Task.find_by_description(description)
    if tasks:
        print(f"Tasks containing '{description}':")
        for task in tasks:
            print(f"{task.description} to be done by {Family_Member.find_by_id(task.family_member_id).name}")
    else:
        print("No tasks found matching the description.")

def del_task(choice):
    try:
        task_id = int(choice)
        task = Task.find_by_id(task_id)
        if task:
            task.delete()
            print("Task deleted!")
        else:
            print("Task not found.")
    except ValueError:
        print("Invalid task number.")