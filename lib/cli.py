# lib/cli.py

from helpers import (
    exit_program,
    view_members,
    get_member,
    view_tasks,
    tasks_by_id,
    seed,
    add_task,
    pick_member,
    update_member_info,
    delete_member,
    search_by_family_member,
    search_by_description,
    del_task

)


def main():
    seed()
    main_menu()



def main_menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View family members")
    print("2. View tasks")
    print("3. Search tasks")
    choice = input(">")
    if choice == "0":
        exit_program()
    elif choice == "1":
        family_menu()
    elif choice == "2":
        view_tasks()
        task_menu()
    elif choice == "3":
        search_menu()        
    else:
        print("Invalid choice")
        main_menu()

def family_menu():
    print("please enter the number for the family member you want to select")
    print("0. Back to main menu")
    view_members()
    choice = input(">")
    if choice == "0":
        main_menu()
    else:
        family_member_menu(choice)

def family_member_menu(id):
    get_member(id)
    print("0. Return to main menu")
    print("1. View tasks")
    print("2. Add task")
    print("3. Update information")
    print("4. Delete member D:!!!")
    choice = input(">")
    if choice == "0":
        main_menu()
    elif choice == "1":
        tasks_by_id(id)
        family_member_menu(id)
    elif choice == "2":
        add_task(id)
        family_member_menu(id)
    elif choice == "3":
        update_member_info(id)
        family_member_menu(id)
    elif choice == "4":
        delete_member(id)
        main_menu()
    else:
        print("Invalid choice")
        family_member_menu(id)

def task_menu():
    print("0. Back to main menu")
    print("1. Add task")
    print("2. Delete task")
    choice = input(">")
    if choice == "0":
        main_menu()
    elif choice == "1":
        id = pick_member()
        add_task(id)
        task_menu()
    elif choice == "2":
        del_task_menu()
    else:
        print("Invalid choice")
        task_menu()

def search_menu():
    print("Search tasks by:")
    print("1. Description")
    print("2. Family Member")
    choice = input(">")
    if choice == "1":
        description = input("Enter the description to search: ")
        search_by_description(description)
        main_menu()
    elif choice == "2":
        view_members()
        id = input("Enter the family member ID to search: ")
        search_by_family_member(id)
        main_menu()
    else:
        print("Invalid choice")
        search_menu()

def del_task_menu():
    print("0. Back to main menu")
    view_tasks()
    choice = input("Enter the number of the task to delete (or 0 to cancel): ")
    if choice == "0":
        main_menu()
    else:
        del_task(choice)
        task_menu()
    

if __name__ == "__main__":
    main()

