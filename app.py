from flask import Flask, jsonify, request, Response
import test
from status_codes import *
import json

app = Flask(__name__)

books = [
    {
        'name': 'Green Egg and Ham',
        'price': 7.99,
        'isbn': 980898
    },
    {
        'name': 'The cat in the hat',
        'price': 6.99,
        'isbn': 123123
    }
]

# by default get method
@app.route('/books')
def index():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()

    if test.valid_book_object(request_data):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }

        books.insert(0, new_book)
        response = Response("", status_created, mimetype='application/json')
        response.headers['Location'] = "/book/"+str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':7.99,'ibsn':1354}"
        }

        response = Response(json.dumps(invalidBookObjectErrorMsg), status_bad_request, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()

    if not test.valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':7.99}"
        }

        response = Response(json.dumps(invalidBookObjectErrorMsg), status_bad_request, mimetype='application/json')
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }

    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books[i] = new_book
            response = Response('', status_no_content)
            return response
        i += 1


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()

    update_book = {}
    if "name" in request_data:
        update_book["name"] = request_data["name"]
    for book in books:
        if book["isbn"] == isbn:
            book.update(update_book)
    response = Response("", status_no_content)
    response.headers['Location'] = "/books/"+str(isbn)
    return response


if __name__ == "__main__":
    app.run(debug=True)
