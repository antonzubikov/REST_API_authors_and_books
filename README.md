# REST_API_authors_and_books

## Project description:
Это REST API контракт для создания, просмотра, редактирования и удаления записей об авторах и книгах.

## API available methods:
* GET ```"/api/books"``` — просмотр всех доступных книг;
* POST ```"/api/books"``` — добавление новой книги;
* ———
* PUT ```"/api/books/{id}"``` — изменение книги;
* GET ```"/api/books/{id}"``` — получение информации о книге;
* DELETE ```"/api/books/{id}"``` — удаление книги;
* ———
* POST ```"/api/authors/"``` — создание автора;
* GET ```"/api/authors/{id}"``` — просмотр всех книг автора;
* DELETE ```"/api/authors/{id}"``` — удаление автора вместе со всеми его книгами

## Used technologies:
* Flask (Python web framework; 2.3.2);
* Flask–RESTful (Flask RESTful architecture building tool; 0.3.10);
* Marshmallow (simplified object serialization; 3.19.0);
* SQLite3 (relational database; 3.39.5)
