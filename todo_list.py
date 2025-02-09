import os
import json
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for Windows
init()

class TodoList:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()
        
    def load_tasks(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    self.tasks = json.load(file)
        except Exception as e:
            print(f"{Fore.RED}Error loading tasks: {e}{Style.RESET_ALL}")
            self.tasks = []
            
    def save_tasks(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            print(f"{Fore.RED}Error saving tasks: {e}{Style.RESET_ALL}")
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_menu(self):
        self.clear_screen()
        print(f"\n{Fore.CYAN}╔══════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║    My Fancy Todo List    ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════╝{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Add Task")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} View Tasks")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Mark Task as Complete")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Delete Task")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Exit")
        
    def get_priority_color(self, priority):
        colors = {
            'high': Fore.RED,
            'medium': Fore.YELLOW,
            'low': Fore.GREEN
        }
        return colors.get(priority.lower(), Fore.WHITE)
        
    def add_task(self):
        self.clear_screen()
        print(f"\n{Fore.CYAN}=== Add New Task ==={Style.RESET_ALL}")
        task = input(f"{Fore.WHITE}Enter your task: {Style.RESET_ALL}")
        
        while True:
            priority = input(f"{Fore.WHITE}Enter priority (high/medium/low): {Style.RESET_ALL}").lower()
            if priority in ['high', 'medium', 'low']:
                break
            print(f"{Fore.RED}Invalid priority! Please try again.{Style.RESET_ALL}")
        
        while True:
            due_date = input(f"{Fore.WHITE}Enter due date (YYYY-MM-DD) or press Enter to skip: {Style.RESET_ALL}")
            if not due_date:
                due_date = "No due date"
                break
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                break
            except ValueError:
                print(f"{Fore.RED}Invalid date format! Please use YYYY-MM-DD{Style.RESET_ALL}")
        
        task_dict = {
            "task": task,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date,
            "priority": priority,
            "completed": False
        }
        self.tasks.append(task_dict)
        self.save_tasks()
        print(f"\n{Fore.GREEN}Task added successfully!{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        
    def view_tasks(self):
        self.clear_screen()
        print(f"\n{Fore.CYAN}=== Your Tasks ==={Style.RESET_ALL}")
        if not self.tasks:
            print(f"{Fore.YELLOW}No tasks found!{Style.RESET_ALL}")
        else:
            for index, task in enumerate(self.tasks, 1):
                status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if task["completed"] else f"{Fore.RED}✗{Style.RESET_ALL}"
                priority_color = self.get_priority_color(task["priority"])
                
                print(f"\n{Fore.CYAN}Task #{index}:{Style.RESET_ALL}")
                print(f"Status: {status}")
                print(f"Description: {priority_color}{task['task']}{Style.RESET_ALL}")
                print(f"Priority: {priority_color}{task['priority'].upper()}{Style.RESET_ALL}")
                print(f"Created: {Fore.BLUE}{task['created']}{Style.RESET_ALL}")
                print(f"Due: {Fore.YELLOW}{task['due_date']}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'─' * 40}{Style.RESET_ALL}")
                
        input("\nPress Enter to continue...")
        
    def mark_complete(self):
        self.clear_screen()
        self.view_tasks()
        if not self.tasks:
            return
            
        while True:
            try:
                task_num = int(input(f"\n{Fore.WHITE}Enter task number to mark as complete (0 to cancel): {Style.RESET_ALL}"))
                if task_num == 0:
                    return
                if 1 <= task_num <= len(self.tasks):
                    self.tasks[task_num-1]["completed"] = True
                    self.save_tasks()
                    print(f"\n{Fore.GREEN}Task marked as complete!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}Invalid task number!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        
    def delete_task(self):
        self.clear_screen()
        self.view_tasks()
        if not self.tasks:
            return
            
        while True:
            try:
                task_num = int(input(f"\n{Fore.WHITE}Enter task number to delete (0 to cancel): {Style.RESET_ALL}"))
                if task_num == 0:
                    return
                if 1 <= task_num <= len(self.tasks):
                    deleted_task = self.tasks.pop(task_num-1)
                    self.save_tasks()
                    print(f"\n{Fore.GREEN}Task deleted: {deleted_task['task']}{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}Invalid task number!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        
    def run(self):
        while True:
            self.show_menu()
            choice = input(f"\n{Fore.WHITE}Enter your choice (1-5): {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.mark_complete()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                print(f"\n{Fore.GREEN}Thank you for using My Fancy Todo List!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                input("Press Enter to try again...")

if __name__ == "__main__":
    todo_list = TodoList()
    todo_list.run()