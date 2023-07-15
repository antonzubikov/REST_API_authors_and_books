import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

BOOKS_DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]

AUTHORS_DATA = [
    {'id': 0, 'first_name': 'Herman', 'last_name': 'Melville'},
    {'id': 1, 'first_name': 'Leo', 'last_name': 'Tolstoy'}
]

BOOKS_DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_DATABASE_NAME = 'table_authors.db'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author: str
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item) -> Union[int, str]:
        return getattr(self, item)


def init_db_books(initial_records: List[Dict]) -> None:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' 
            AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author TEXT
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])


def get_all_books() -> list[Book]:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` 
            WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` 
            WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def init_db_authors(initial_records: List[Dict]) -> None:
    with sqlite3.connect(AUTHORS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name TEXT,
                    last_name TEXT,
                    middle_name TEXT
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, last_name) VALUES (?, ?)
                """,
                [
                    (item['first_name'], item['last_name'])
                    for item in initial_records
                ]
            )


def add_author(author: Author) -> Author:
    with sqlite3.connect(AUTHORS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` 
            (first_name, last_name) VALUES (?, ?)
            """,
            (author.first_name, author.last_name)
        )
        author.id = cursor.lastrowid
        return author


def get_author_books_by_id(author_id: int) -> list[Book]:
    with sqlite3.connect(AUTHORS_DATABASE_NAME) as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT `first_name`, `last_name` '
                       f'FROM {AUTHORS_TABLE_NAME} '
                       f'WHERE `id` = ?',
                       (author_id,))
        result = cursor.fetchall()
        first_name, last_name = result[0][0], result[0][1]

    with sqlite3.connect(BOOKS_DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` 
            WHERE `author` = ?
            """,
            (first_name + ' ' + last_name,)
        )
        books = cursor.fetchall()
        if books:
            return [_get_book_obj_from_row(row) for row in books]


def delete_author_and_books_by_author_id(author_id: int):
    with sqlite3.connect(AUTHORS_DATABASE_NAME) as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT `first_name`, `last_name` '
                       f'FROM {AUTHORS_TABLE_NAME} '
                       f'WHERE `id` = ?',
                       (author_id,))
        result = cursor.fetchall()
        first_name, last_name = result[0][0], result[0][1]

        cursor.execute(f'DELETE FROM {AUTHORS_TABLE_NAME} '
                       f'WHERE `id` = ?',
                       (author_id,))

    with sqlite3.connect(BOOKS_DATABASE_NAME) as db:
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM {BOOKS_TABLE_NAME} '
                       f'WHERE `author` = ?',
                       (first_name + ' ' + last_name,))
