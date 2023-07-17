# REST_API_authors_and_books

## Project description:
Это REST API контракт для создания, просмотра, редактирования и удаления записей об авторах и книгах.

## Swagger UI specifications with Open API:
* ```"/apidocs"```

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
* SQLite3 (relational database; 3.39.5);
* apispec (API specifications tools; 6.0.2);
* apispec–webframeworks (API specifications tools; 0.5.2);
* flasgger (Swagger UI tool; 0.9.7.1)

## Installation:
* Необходимо скопировать всё содержимое репозитория в отдельный каталог;
* Установить все связи из `requirements.txt`:

```
python pip install -r requirements.txt
```
* Запустить файл `routes.py`
