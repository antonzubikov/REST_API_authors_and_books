from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from werkzeug.serving import WSGIRequestHandler

from models import (
    BOOKS_DATA,
    AUTHORS_DATA,
    get_all_books,
    init_db_books,
    init_db_authors,
    add_book,
    update_book_by_id,
    get_book_by_id,
    delete_book_by_id,
    add_author,
    get_author_books_by_id,
    delete_author_and_books_by_author_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)

spec = APISpec(
    title='BookList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        """
        This is an endpoint for obtaining the books list.
        ---
        tags:
          - books
        responses:
          200:
            description: Books data
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        """
        This is an endpoint for book creation.
        ---
        tags:
         - books
        parameters:
         - in: body
           name: new book params
           schema:
             $ref: '#/definitions/Book'
        responses:
         201:
           description: The book has been created
           schema:
             $ref: '#/definitions/Book'
        """
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class Book_by_ID(Resource):
    def put(self, id: int) -> tuple[list[dict], int]:
        """
        This is an endpoint for book update.
        ---
        tags:
         - books
        parameters:
         - in: body
           name: update book params
           schema:
             $ref: '#/definitions/Book'
        responses:
         200:
           description: The book has been update
           schema:
             $ref: '#/definitions/Book'
        """
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        update_book_by_id(book)
        return schema.dump(get_all_books(), many=True), 200

    def get(self, id: int) -> tuple[dict, int]:
        """
        This is an endpoint for obtaining the book by ID.
        ---
        tags:
          - books
        responses:
          200:
            description: Book by ID
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        schema = BookSchema()
        return schema.dump(get_book_by_id(id)), 200

    def delete(self, id: int) -> tuple[list[dict], int]:
        """
        This is an endpoint for delete the book by ID.
        ---
        tags:
          - books
        responses:
          200:
            description: Delete book by ID
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        schema = BookSchema()
        delete_book_by_id(id)
        return schema.dump(get_all_books(), many=True), 200


class AuthorCreate(Resource):
    def post(self) -> tuple[dict, int]:
        """
        This is an endpoint for author creation.
        ---
        tags:
         - authors
        parameters:
         - in: body
           name: new author creation
           schema:
             $ref: '#/definitions/Author'
        responses:
         201:
           description: The author has been created
           schema:
             $ref: '#/definitions/Author'
        """
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        result = add_author(author)
        return schema.dump(result), 201


class AuthorManipulate(Resource):
    def get(self, id: int) -> tuple[list[dict], int]:
        """
        This is an endpoint for obtaining the author by ID.
        ---
        tags:
          - authors
        responses:
          200:
            description: Authors data
            schema:
              type: array
              items:
                $ref: '#/definitions/Author'
        """
        schema = AuthorSchema()
        return schema.dump(get_author_books_by_id(id), many=True), 200

    def delete(self, id: int) -> tuple[list[dict], int]:
        """
        This is an endpoint for delete the author by ID.
        ---
        tags:
          - authors
        responses:
          200:
            description: Delete author by ID
            schema:
              type: array
              items:
                $ref: '#/definitions/Author'
        """
        schema = BookSchema()
        delete_author_and_books_by_author_id(id)
        return schema.dump(get_all_books(), many=True), 200


template = spec.to_flasgger(
    app,
    definitions=[BookSchema],
)
swagger = Swagger(app, template=template)

api.add_resource(BookList, '/api/books')
api.add_resource(Book_by_ID, '/api/books/<int:id>')
api.add_resource(AuthorCreate, '/api/authors')
api.add_resource(AuthorManipulate, '/api/authors/<int:id>')


if __name__ == '__main__':
    init_db_books(initial_records=BOOKS_DATA)
    init_db_authors(initial_records=AUTHORS_DATA)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
