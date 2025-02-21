# lib/helpers.py
from models.family_members import Family_Member
from models.tasks import Task

def view_members():
    # display family members in numbered list
    print("***Family Members***")
    members = Family_Member.get_all()
    for i, member in enumerate(members, start=1):
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
    tasks = Task.all_tasks_for_id(id)
    for i, task in enumerate(tasks, start=1):
        print(f"{i}.{task.description}")

def view_tasks():
    # display all tasks in numbered list
    print("***Tasks***")
    tasks = Task.get_all()
    for i, task in enumerate(tasks, start=1):
        member = Family_Member.find_by_id(task.family_member_id)
        print(f"{i}.{task.description} to be done by {member.name}")
    print("***********")

def exit_program():
    # toodles
    print("Goodbye!")
    exit()

def seed():
    # set up database
    # wipe and set up tables
    if not len(Family_Member.get_all()) > 0:
    ####################
    # uncomment drops for testing
    ####################
        Family_Member.drop_table()
        Task.drop_table()
        Family_Member.create_table()
        Task.create_table()
    # build local dicts from db
    
        #Task.get_all()
        # add family
        Aj = Family_Member("AJ", 5, "Son")
        Lauren = Family_Member("Lauren", 7, "Daughter")
        Violet = Family_Member("Violet", 2, "Daughter")
        Katie = Family_Member("Katie", 35, "Wife")
        Arthur = Family_Member("Arthur", 29, "Me")
        # add tasks
        Dishes = Task("Wash Dishes", 4)
        Cooking = Task("Cook Dinner", 5)
        Laundry = Task("Laundry", 4)
        Pickup = Task("Pickup toys", 2)
        Washcar = Task("Wash Car", 5)

def add_task(id):
    # add a new task for a specific family member by id
    description = input("Enter the description of the task: ")
    Task(description, int(id))
    print("Task added!")

def pick_member():
    # select a family member by number
    view_members()
    choice = input("Enter the number of the family member you want to add a task for: ")
    return int(choice)

def update_member_info(id):
    # update a family member's information by id
    name = input("Enter the new name: ")
    age = input("Enter the new age: ")
    title = input("Enter the new title: ")
    Family_Member.update(id, name, int(age), title)
    print("Member information updated!")

def delete_member(id):
    # delete a family member by id
    member = Family_Member.find_by_id(id)
    if member:
        # verify cruelty
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
    #search tasks by family member and print list 
    family_member = Family_Member.find_by_id(id)
    if family_member:
        print(f"Tasks for {family_member.name}:")
        tasks = Task.all_tasks_for_id(id)
        for i, task in enumerate(tasks, start=1):
            print(f"{task.description}")
    else:
        print("Family member not found.")

def search_by_description(description):
    #search tasks by description and print
    tasks = Task.find_by_description(description)
    if tasks:
        for task in tasks:
            print(f"{task.description} to be done by {Family_Member.find_by_id(task.family_member_id).name}")
    else:
        print("No tasks found matching the description.")

def del_task(choice):
    # delete a task by number
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

def new_family_member():
    # add a new family member
    name = input("Enter the name of the new family member: ")
    age = input("Enter the age of the new family member: ")
    title = input("Enter the title of the new family member: ")
    Family_Member(name, int(age), title)
    print("Family member added!")