import csv
from datetime import datetime, timedelta


class LibraryItem:
    def __init__(self, title, author, genre, item_type, copies=1):
        self._title = title
        self._author = author
        self._genre = genre
        self._item_type = item_type
        self._total_copies = copies
        self._available_copies = copies
        self._status = 'available'
        self._borrow_date = None
        self._due_date = None
        self._reserved_by = None

    def __repr__(self):
        return (f"LibraryItem(title='{self._title}', author='{self._author}', genre='{self._genre}', "
                f"item_type='{self._item_type}', total_copies={self._total_copies}, available_copies={self._available_copies}, "
                f"status='{self._status}', borrow_date={self._borrow_date}, due_date={self._due_date}, "
                f"reserved_by={self._reserved_by})")

    @classmethod
    def from_csv(cls, file_path):
        items = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                item_type = row[3]
                if item_type == 'Book':
                    items.append(Book(*row[:3], int(row[4])))
                elif item_type == 'Magazine':
                    items.append(Magazine(*row[:3], row[3], int(row[4])))
                elif item_type == 'Textbook':
                    items.append(Textbook(*row[:3], row[3], int(row[4])))
        return items

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def genre(self):
        return self._genre

    @property
    def item_type(self):
        return self._item_type

    @property
    def total_copies(self):
        return self._total_copies

    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        if 0 <= value <= self._total_copies:
            self._available_copies = value
        else:
            raise ValueError("Available copies cannot exceed total copies or be negative.")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def borrow_date(self):
        return self._borrow_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def reserved_by(self):
        return self._reserved_by

    @reserved_by.setter
    def reserved_by(self, user):
        self._reserved_by = user

    def set_due_date(self, days=14):
        self._borrow_date = datetime.now()
        self._due_date = self._borrow_date + timedelta(days=days)

    def check_overdue(self):
        if self._due_date and datetime.now() > self._due_date:
            return True
        return False

    def reserve(self, user):
        if self._available_copies > 0:
            print(f"Item '{self._title}' is available and cannot be reserved.")
        else:
            self.reserved_by = user

    def cancel_reservation(self):
        self._reserved_by = None

    def __str__(self):
        return f"{self._item_type}: {self._title} by {self._author} ({self._genre}) - {self._status}, Copies: {self._available_copies}/{self._total_copies}"


class Book(LibraryItem):
    def __init__(self, title, author, genre, copies=1):
        super().__init__(title, author, genre, "Book", copies)

    def __repr__(self):
        return (f"Book(title='{self._title}', author='{self._author}', genre='{self._genre}', "
                f"total_copies={self._total_copies}, available_copies={self._available_copies}, "
                f"status='{self._status}', borrow_date={self._borrow_date}, due_date={self._due_date}, "
                f"reserved_by={self._reserved_by})")


class Magazine(LibraryItem):
    def __init__(self, title, author, genre, issue_number, copies=1):
        super().__init__(title, author, genre, "Magazine", copies)
        self._issue_number = issue_number

    @property
    def issue_number(self):
        return self._issue_number

    def __repr__(self):
        return (f"Magazine(title='{self._title}', author='{self._author}', genre='{self._genre}', "
                f"issue_number={self._issue_number}, total_copies={self._total_copies}, available_copies={self._available_copies}, "
                f"status='{self._status}', borrow_date={self._borrow_date}, due_date={self._due_date}, "
                f"reserved_by={self._reserved_by})")

    def __str__(self):
        return f"Magazine: {self._title} by {self._author} ({self._genre}), Issue: {self._issue_number} - {self._status}, Copies: {self._available_copies}/{self._total_copies}"


class Textbook(LibraryItem):
    def __init__(self, title, author, genre, subject, copies=1):
        super().__init__(title, author, genre, "Textbook", copies)
        self._subject = subject

    @property
    def subject(self):
        return self._subject

    def __str__(self):
        return f"Textbook: {self._title} by {self._author} ({self._genre}), Subject: {self._subject} - {self._status}, Copies: {self._available_copies}/{self._total_copies}"

    def __repr__(self):
        return (f"Textbook(title='{self._title}', author='{self._author}', genre='{self._genre}', "
                f"subject='{self._subject}', total_copies={self._total_copies}, available_copies={self._available_copies}, "
                f"status='{self._status}', borrow_date={self._borrow_date}, due_date={self._due_date}, "
                f"reserved_by={self._reserved_by})")


class User:
    def __init__(self, user_id, name):
        self._user_id = user_id
        self._name = name
        self._borrowed_items = []
        self._fines = 0
        self._reserved_items = []
        self._transaction_history = []

    def __repr__(self):
        return (f"User(user_id={self._user_id}, name='{self._name}', fines={self._fines}, "
                f"borrowed_items={[item.title for item in self._borrowed_items]}, reserved_items={[item.title for item in self._reserved_items]}, "
                f"transaction_history={[str(transaction) for transaction in self._transaction_history]})")

    @classmethod
    def from_csv(cls, file_path):
        users = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                user_id, name = row
                users.append(cls(int(user_id), name))
        return users

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def borrowed_items(self):
        return self._borrowed_items

    @property
    def fines(self):
        return self._fines

    @fines.setter
    def fines(self, amount):
        if amount >= 0:
            self._fines = amount
        else:
            raise ValueError("Fines cannot be negative.")

    @property
    def reserved_items(self):
        return self._reserved_items

    @property
    def transaction_history(self):
        return self._transaction_history

    def current_time(self):
        return datetime.now()  # Новый метод, который можно замокать

    def borrow_item(self, library_item):
        if library_item.available_copies > 0:
            library_item.available_copies -= 1
            library_item.status = f'borrowed by {self._name}'
            library_item.set_due_date()
            self._borrowed_items.append(library_item)
            self._transaction_history.append(Transaction(self, library_item, 'borrowed'))
            if library_item in self._reserved_items:
                self._reserved_items.remove(library_item)
        else:
            print(f"Item '{library_item.title}' is not available.")

    def return_item(self, library_item):
        if library_item in self._borrowed_items:
            if library_item.check_overdue():
                overdue_days = (self.current_time() - library_item.due_date).days
                fine = overdue_days * 1  # 1 unit of currency per overdue day
                self._fines += fine
                print(f"Item '{library_item.title}' is overdue. Fine: {fine}")
            library_item.available_copies += 1
            library_item.status = 'available' if library_item.available_copies > 0 else 'unavailable'
            library_item._borrow_date = None
            library_item._due_date = None
            self._borrowed_items.remove(library_item)
            self._transaction_history.append(Transaction(self, library_item, 'returned'))
        else:
            print(f"Item '{library_item.title}' not found in user's borrowed items.")

    def reserve_item(self, library_item):
        if library_item.available_copies == 0 and library_item.reserved_by is None:
            library_item.reserve(self)
            self._reserved_items.append(library_item)
        else:
            print(f"Item '{library_item.title}' cannot be reserved.")

    def cancel_reservation(self, library_item):
        if library_item in self._reserved_items:
            library_item.cancel_reservation()
            self._reserved_items.remove(library_item)
        else:
            print(f"Item '{library_item.title}' not found in user's reserved items.")

    def __str__(self):
        return f"User: {self._name}, Borrowed items: {[item.title for item in self._borrowed_items]}, Reserved items: {[item.title for item in self._reserved_items]}"


class Transaction:
    def __init__(self, user, item, action):
        self.user = user
        self.item = item
        self.action = action
        self.date = datetime.now()

    def __str__(self):
        return f"{self.date}: {self.user.name} {self.action} '{self.item.title}'"

    def __repr__(self):
        return (f"Transaction(user={self.user.name}, item={self.item.title}, action='{self.action}', date={self.date})")


class Library:
    def __init__(self):
        self._items = []
        self._users = []
        self._transactions = []

    def __repr__(self):
        return (f"Library(items={len(self._items)}, users={len(self._users)}, transactions={len(self._transactions)})")

    def add_item(self, item):
        self._items.append(item)

    def add_user(self, user):
        self._users.append(user)

    @classmethod
    def from_csv(cls, item_file_path, user_file_path):
        library = cls()
        library._items.extend(LibraryItem.from_csv(item_file_path))
        library._users.extend(User.from_csv(user_file_path))
        return library

    def search_by_title(self, title):
        return [item for item in self._items if title.lower() in item.title.lower()]

    def search_by_author(self, author):
        return [item for item in self._items if author.lower() in item.author.lower()]

    def search_by_genre(self, genre):
        return [item for item in self._items if genre.lower() in item.genre.lower()]

    def search_by_type(self, item_type):
        return [item for item in self._items if item_type.lower() == item.item_type.lower()]

    def record_transaction(self, transaction):
        self._transactions.append(transaction)

    def notify_reservations(self, item):
        if item.reserved_by:
            print(f"Item '{item.title}' is now available and reserved by {item.reserved_by.name}.")

    def __str__(self):
        return f"Library: {len(self._items)} items, {len(self._users)} users"


# Примеры CSV файлов:

# items.csv
# Title,Author,Genre,ItemType,Copies
# BookTitle1,Author1,Genre1,Book,3
# MagazineTitle1,Author2,Genre2,Magazine,2
# TextbookTitle1,Author3,Genre3,Textbook,1

# users.csv
# UserID,Name
# 1,Alice
# 2,Bob

# Создание библиотеки из файла
library = Library.from_csv('items.csv', 'users.csv')

print(library)

# Поиск юзера по имени
try:
    user1 = next(user for user in library._users if user.name == 'Alice')
except StopIteration:
    print("User 'Alice' not found")
    user1 = None

if user1:
    # Взятие юзером книги и журнала из библиотеки
    book1 = next(item for item in library._items if item.title == 'BookTitle1')
    magazine1 = next(item for item in library._items if item.title == 'MagazineTitle1')

    user1.borrow_item(book1)
    user1.borrow_item(magazine1)

    # Резервирование книги пользователем
    user2 = next(user for user in library._users if user.name == 'Bob')
    user2.reserve_item(book1)

    # Проверка статуса книг и юзеров
    print(library)
    print(user1)
    print(user2)

    # Симуляция задержки
    import time

    time.sleep(1)

    # Возврат книги и журнала пользователем
    user1.return_item(book1)
    user1.return_item(magazine1)

    # Запись о транзакции в библиотеку
    for transaction in user1.transaction_history:
        library.record_transaction(transaction)

    # Проверка статусов после возвращения книги
    library.notify_reservations(book1)

    print(library)
    print(user1)
    print(user2)

    # Поиск по типу
    print("Books:", library.search_by_type("Book"))
    print("Magazines:", library.search_by_type("Magazine"))
    print("Textbooks:", library.search_by_type("Textbook"))
