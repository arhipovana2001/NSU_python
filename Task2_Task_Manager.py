import json
import os
from datetime import datetime


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def __str__(self):
        return f'User {self.username}'


class Task:
    def __init__(self, task_id, title, description, status, deadline, priority):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.priority = priority

    def __str__(self):
        return (f'Task {self.task_id}: {self.title} - Status: {self.status}, '
                f'Deadline: {self.deadline}, Priority: {self.priority}')

    def update_status(self, new_status):
        self.status = new_status

    def update_priority(self, new_priority):
        self.priority = new_priority

    def update_description(self, new_description):
        self.description = new_description

    def update_title(self, new_title):
        self.title = new_title

    def update_deadline(self, new_deadline):
        self.deadline = new_deadline

    def check_overdue(self):
        if self.deadline:
            deadline_date = datetime.strptime(self.deadline, '%Y-%m-%d')
            return deadline_date < datetime.today()
        return False


class Subtask(Task):
    def __init__(self, task_id, title, description, status, deadline, priority, parent_task_id):
        super().__init__(task_id, title, description, status, deadline, priority)
        self.parent_task_id = parent_task_id

    def __str__(self):
        return (f'Subtask {self.task_id}: {self.title} - Status: {self.status}, '
                f'Deadline: {self.deadline}, Priority: {self.priority}, Parent Task ID: {self.parent_task_id}')


class TaskManager:
    def __init__(self):
        self.users = []
        self.logged_in_user = None

    def register_user(self, username, password):
        if self.get_user_by_username(username):
            print("Username already exists!")
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        print(f"User {username} registered successfully.")
        return True

    def login_user(self, username, password):
        user = self.get_user_by_username(username)
        if user and user.password == password:
            self.logged_in_user = user
            print(f"User {username} logged in successfully.")
            return True
        print("Invalid username or password!")
        return False

    def logout_user(self):
        if self.logged_in_user:
            print(f"User {self.logged_in_user.username} logged out.")
            self.logged_in_user = None

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def add_task(self, task):
        if self.logged_in_user:
            self.logged_in_user.tasks.append(task)
        else:
            print("No user is logged in!")

    def remove_task(self, task_id):
        if self.logged_in_user:
            for task in self.logged_in_user.tasks:
                if task.task_id == task_id:
                    self.logged_in_user.tasks.remove(task)
                    return True
        return False

    def get_task_by_id(self, task_id):
        if self.logged_in_user:
            for task in self.logged_in_user.tasks:
                if task.task_id == task_id:
                    return task
        return None

    def display_all_tasks(self):
        if self.logged_in_user:
            for task in self.logged_in_user.tasks:
                print(task)
        else:
            print("No user is logged in!")

    def save_tasks_to_file(self, file_name):
        data = {
            'users': [
                {
                    'username': user.username,
                    'password': user.password,
                    'tasks': [
                        {
                            'task_id': task.task_id,
                            'title': task.title,
                            'description': task.description,
                            'status': task.status,
                            'deadline': task.deadline,
                            'priority': task.priority,
                            'type': type(task).__name__,
                            'parent_task_id': task.parent_task_id if isinstance(task, Subtask) else None
                        } for task in user.tasks
                    ]
                } for user in self.users
            ]
        }
        with open(file_name, 'w') as file:
            json.dump(data, file)
        print("Tasks saved to file.")

    def load_tasks_from_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict) and 'users' in data:
                    for user_data in data['users']:
                        user = User(user_data['username'], user_data['password'])
                        for task_data in user_data['tasks']:
                            if task_data['type'] == 'Subtask':
                                task = Subtask(task_data['task_id'], task_data['title'], task_data['description'],
                                               task_data['status'], task_data['deadline'], task_data['priority'],
                                               task_data['parent_task_id'])
                            else:
                                task = Task(task_data['task_id'], task_data['title'], task_data['description'],
                                            task_data['status'], task_data['deadline'], task_data['priority'])
                            user.tasks.append(task)
                        self.users.append(user)
            print("Tasks loaded from file.")

    def update_task_status(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        if task:
            task.update_status(new_status)
            return True
        return False

    def update_task_priority(self, task_id, new_priority):
        task = self.get_task_by_id(task_id)
        if task:
            task.update_priority(new_priority)
            return True
        return False

    def update_task_title(self, task_id, new_title):
        task = self.get_task_by_id(task_id)
        if task:
            task.update_title(new_title)
            return True
        return False

    def update_task_description(self, task_id, new_description):
        task = self.get_task_by_id(task_id)
        if task:
            task.update_description(new_description)
            return True
        return False

    def update_task_deadline(self, task_id, new_deadline):
        task = self.get_task_by_id(task_id)
        if task:
            task.update_deadline(new_deadline)
            return True
        return False

    def check_overdue_tasks(self):
        overdue_tasks = []
        if self.logged_in_user:
            for task in self.logged_in_user.tasks:
                if task.check_overdue():
                    overdue_tasks.append(task)
        return overdue_tasks

    def generate_report(self):
        if self.logged_in_user:
            completed_tasks = [task for task in self.logged_in_user.tasks if task.status == 'completed']
            overdue_tasks = self.check_overdue_tasks()
            high_priority_tasks = [task for task in self.logged_in_user.tasks if task.priority == 'high']

            report = {
                'total_tasks': len(self.logged_in_user.tasks),
                'completed_tasks': len(completed_tasks),
                'overdue_tasks': len(overdue_tasks),
                'high_priority_tasks': len(high_priority_tasks),
            }
            return report
        return {}


# Пример использования
def main():
    task_manager = TaskManager()
    task_manager.load_tasks_from_file('tasks.json')

    while True:
        print(
            "\n1. Register\n2. Login\n3. Logout\n4. Add Task\n5. Display All Tasks\n6. Generate Report\n7. Update Task\n8. Get Task by ID\n9. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            task_manager.register_user(username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            task_manager.login_user(username, password)

        elif choice == '3':
            task_manager.logout_user()

        elif choice == '4':
            if task_manager.logged_in_user:
                task_id = len(task_manager.logged_in_user.tasks) + 1
                title = input("Enter title: ")
                description = input("Enter description: ")
                status = input("Enter status: ")
                deadline = input("Enter deadline (YYYY-MM-DD): ")
                priority = input("Enter priority: ")
                is_subtask = input("Is this a subtask? (yes/no): ").lower() == 'yes'
                if is_subtask:
                    parent_task_id = int(input("Enter parent task ID: "))
                    task = Subtask(task_id, title, description, status, deadline, priority, parent_task_id)
                else:
                    task = Task(task_id, title, description, status, deadline, priority)
                task_manager.add_task(task)
            else:
                print("No user is logged in! Please log in to add tasks.")

        elif choice == '5':
            if task_manager.logged_in_user:
                task_manager.display_all_tasks()
            else:
                print("No user is logged in! Please log in to display tasks.")

        elif choice == '6':
            if task_manager.logged_in_user:
                report = task_manager.generate_report()
                print("\nReport:")
                for key, value in report.items():
                    print(f"{key}: {value}")
            else:
                print("No user is logged in! Please log in to generate report.")

        elif choice == '7':
            if task_manager.logged_in_user:
                task_id = int(input("Enter task ID: "))
                task = task_manager.get_task_by_id(task_id)
                if task:
                    print(
                        "1. Update Title\n2. Update Description\n3. Update Status\n4. Update Deadline\n5. Update Priority")
                    update_choice = input("Enter your choice: ")
                    if update_choice == '1':
                        new_title = input("Enter new title: ")
                        task_manager.update_task_title(task_id, new_title)
                    elif update_choice == '2':
                        new_description = input("Enter new description: ")
                        task_manager.update_task_description(task_id, new_description)
                    elif update_choice == '3':
                        new_status = input("Enter new status: ")
                        task_manager.update_task_status(task_id, new_status)
                    elif update_choice == '4':
                        new_deadline = input("Enter new deadline (YYYY-MM-DD): ")
                        task_manager.update_task_deadline(task_id, new_deadline)
                    elif update_choice == '5':
                        new_priority = input("Enter new priority: ")
                        task_manager.update_task_priority(task_id, new_priority)
                    else:
                        print("Invalid choice!")
                else:
                    print("Task not found!")
            else:
                print("No user is logged in! Please log in to update tasks.")

        elif choice == '8':
            if task_manager.logged_in_user:
                task_id = int(input("Enter task ID: "))
                task = task_manager.get_task_by_id(task_id)
                if task:
                    print(task)
                else:
                    print("Task not found!")
            else:
                print("No user is logged in! Please log in to get task information.")

        elif choice == '9':
            task_manager.save_tasks_to_file('tasks.json')
            break

        else:
            print("Invalid choice!")


if __name__ == '__main__':
    main()
