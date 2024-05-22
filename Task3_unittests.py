import unittest
from datetime import timedelta
from unittest.mock import patch
from Task3_Library import Book, LibraryItem, Magazine, Textbook, User, Transaction, Library


class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        # Установка начальных данных для тестов
        self.library = Library()
        self.book = Book("Test Book", "Test Author", "Test Genre", copies=2)
        self.book.set_due_date()  # Устанавливаем дату возврата
        self.magazine = Magazine("Test Magazine", "Test Author", "Test Genre", "Issue 1", copies=1)
        self.textbook = Textbook("Test Textbook", "Test Author", "Test Genre", "Test Subject", copies=1)
        self.user = User(1, "Test User")

        self.library.add_item(self.book)
        self.library.add_item(self.magazine)
        self.library.add_item(self.textbook)
        self.library.add_user(self.user)

    def test_return_item(self):
        self.user.borrow_item(self.book)
        # Установка желаемого времени возврата с задержкой, чтобы тестировать просроченные возвраты
        with patch('Task3_Library.datetime') as mock_datetime:
            mock_datetime.now.return_value = self.book.due_date + timedelta(days=1)
            self.user.return_item(self.book)
        self.assertEqual(self.user.fines, 1)  # проверка штрафа
        self.assertEqual(self.book.available_copies, 2)
        self.assertEqual(self.book.status, 'available')
        self.assertNotIn(self.book, self.user.borrowed_items)

    def test_borrow_item(self):
        self.user.borrow_item(self.book)
        self.assertEqual(self.book.available_copies, 1)
        self.assertEqual(self.book.status, f'borrowed by {self.user.name}')
        self.assertIn(self.book, self.user.borrowed_items)

    def test_reserve_item(self):
        # Создание еще одного пользователя, чтобы протестировать резервирование
        user2 = User(2, "Another User")
        self.library.add_user(user2)

        self.user.borrow_item(self.book)
        self.user.borrow_item(self.book)  # Все копии книги заняты

        user2.reserve_item(self.book)
        self.assertIn(self.book, user2.reserved_items)
        self.assertEqual(self.book.reserved_by, user2)

        # Проверка, что нельзя зарезервировать, когда есть доступные копии
        user2.cancel_reservation(self.book)
        self.user.return_item(self.book)
        user2.reserve_item(self.book)
        self.assertNotIn(self.book, user2.reserved_items)
        self.assertIsNone(self.book.reserved_by)

    def test_cancel_reservation(self):
        user2 = User(2, "Another User")
        self.library.add_user(user2)

        self.user.borrow_item(self.book)
        self.user.borrow_item(self.book)  # Все копии книги заняты

        user2.reserve_item(self.book)
        user2.cancel_reservation(self.book)
        self.assertNotIn(self.book, user2.reserved_items)
        self.assertIsNone(self.book.reserved_by)

    def test_notify_reservations(self):
        user2 = User(2, "Another User")
        self.library.add_user(user2)

        self.user.borrow_item(self.book)
        self.user.borrow_item(self.book)  # Все копии книги заняты

        user2.reserve_item(self.book)
        with patch('builtins.print') as mocked_print:
            self.library.notify_reservations(self.book)
            mocked_print.assert_called_with(f"Item '{self.book.title}' is now available and reserved by {user2.name}.")

    def test_search_by_title(self):
        result = self.library.search_by_title("Test Book")
        self.assertIn(self.book, result)

    def test_search_by_author(self):
        result = self.library.search_by_author("Test Author")
        self.assertIn(self.book, result)
        self.assertIn(self.magazine, result)
        self.assertIn(self.textbook, result)

    def test_search_by_genre(self):
        result = self.library.search_by_genre("Test Genre")
        self.assertIn(self.book, result)
        self.assertIn(self.magazine, result)
        self.assertIn(self.textbook, result)

    def test_search_by_type(self):
        result_books = self.library.search_by_type("Book")
        result_magazines = self.library.search_by_type("Magazine")
        result_textbooks = self.library.search_by_type("Textbook")

        self.assertIn(self.book, result_books)
        self.assertIn(self.magazine, result_magazines)
        self.assertIn(self.textbook, result_textbooks)


if __name__ == '__main__':
    unittest.main()
