import unittest
from datetime import datetime, timedelta
from Task2_Task_Manager import User, Task, Subtask, TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.task_manager.register_user('testuser', 'testpassword')
        self.task_manager.login_user('testuser', 'testpassword')

    def tearDown(self):
        self.task_manager.logout_user()

    def test_user_registration(self):
        self.assertTrue(self.task_manager.register_user('newuser', 'newpassword'))
        self.assertFalse(self.task_manager.register_user('testuser', 'testpassword'))  # Duplicate username

    def test_user_login(self):
        self.assertTrue(self.task_manager.login_user('testuser', 'testpassword'))
        self.assertFalse(self.task_manager.login_user('wronguser', 'testpassword'))
        self.assertFalse(self.task_manager.login_user('testuser', 'wrongpassword'))

    def test_task_creation(self):
        task_id = len(self.task_manager.logged_in_user.tasks) + 1
        task = Task(task_id, 'Test Task', 'Test Description', 'in progress', '2024-12-31', 'high')
        self.task_manager.add_task(task)
        self.assertEqual(len(self.task_manager.logged_in_user.tasks), 1)
        self.assertEqual(self.task_manager.logged_in_user.tasks[0].title, 'Test Task')

    def test_subtask_creation(self):
        task_id = len(self.task_manager.logged_in_user.tasks) + 1
        task = Task(task_id, 'Parent Task', 'Parent Description', 'in progress', '2024-12-31', 'high')
        self.task_manager.add_task(task)
        subtask_id = len(self.task_manager.logged_in_user.tasks) + 1
        subtask = Subtask(subtask_id, 'Subtask', 'Subtask Description', 'in progress', '2024-12-31', 'medium', task_id)
        self.task_manager.add_task(subtask)
        self.assertEqual(len(self.task_manager.logged_in_user.tasks), 2)
        self.assertEqual(self.task_manager.logged_in_user.tasks[1].title, 'Subtask')

    def test_task_update(self):
        task_id = len(self.task_manager.logged_in_user.tasks) + 1
        task = Task(task_id, 'Old Title', 'Old Description', 'in progress', '2024-12-31', 'high')
        self.task_manager.add_task(task)
        self.task_manager.update_task_title(task_id, 'New Title')
        self.task_manager.update_task_description(task_id, 'New Description')
        self.task_manager.update_task_status(task_id, 'completed')
        self.task_manager.update_task_deadline(task_id, '2025-01-01')
        self.task_manager.update_task_priority(task_id, 'low')
        updated_task = self.task_manager.get_task_by_id(task_id)
        self.assertEqual(updated_task.title, 'New Title')
        self.assertEqual(updated_task.description, 'New Description')
        self.assertEqual(updated_task.status, 'completed')
        self.assertEqual(updated_task.deadline, '2025-01-01')
        self.assertEqual(updated_task.priority, 'low')

    def test_task_removal(self):
        task_id = len(self.task_manager.logged_in_user.tasks) + 1
        task = Task(task_id, 'Task to Remove', 'Description', 'in progress', '2024-12-31', 'high')
        self.task_manager.add_task(task)
        self.assertTrue(self.task_manager.remove_task(task_id))
        self.assertIsNone(self.task_manager.get_task_by_id(task_id))
        self.assertEqual(len(self.task_manager.logged_in_user.tasks), 0)

    def test_overdue_tasks(self):
        task_id = len(self.task_manager.logged_in_user.tasks) + 1
        overdue_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        task = Task(task_id, 'Overdue Task', 'Description', 'in progress', overdue_date, 'high')
        self.task_manager.add_task(task)
        overdue_tasks = self.task_manager.check_overdue_tasks()
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0].title, 'Overdue Task')

    def test_generate_report(self):
        self.task_manager.logged_in_user.tasks = []
        task_id1 = len(self.task_manager.logged_in_user.tasks) + 1
        task1 = Task(task_id1, 'Completed Task', 'Description', 'completed', '2024-12-31', 'high')
        self.task_manager.add_task(task1)
        task_id2 = len(self.task_manager.logged_in_user.tasks) + 1
        overdue_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        task2 = Task(task_id2, 'Overdue Task', 'Description', 'in progress', overdue_date, 'high')
        self.task_manager.add_task(task2)
        task_id3 = len(self.task_manager.logged_in_user.tasks) + 1
        task3 = Task(task_id3, 'High Priority Task', 'Description', 'in progress', '2024-12-31', 'high')
        self.task_manager.add_task(task3)
        self.assertEqual(len(self.task_manager.logged_in_user.tasks), 3)
        report = self.task_manager.generate_report()
        self.assertEqual(report['total_tasks'], 3)
        self.assertEqual(report['completed_tasks'], 1)
        self.assertEqual(report['overdue_tasks'], 1)
        self.assertEqual(report['high_priority_tasks'], 3)


if __name__ == '__main__':
    unittest.main()
