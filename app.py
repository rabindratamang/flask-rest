from flask import Flask, jsonify, request, Response
import test
from status_codes import *
from BookModel import *
from UserModel import *
from settings import *
import json
import jwt, datetime
from functools import wraps

app.config['SECRET_KEY'] = "testsecret"


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid token please login'}), status_unauthorized
    return wrapper


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    if User.username_password_match(username, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        invalid_login = {
            'error': 'Invalid credentials'
        }
        return Response(json.dumps(invalid_login), 401, mimetype='application/json')

# by default get method
@app.route('/books')
@token_required
def index():
    return jsonify({'books': Book.get_all_books()})


@app.route('/books/<int:isbn>')
@token_required
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    print(return_value)
    return jsonify(return_value)


@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()

    if test.valid_book_object(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", status_created, mimetype='application/json')
        response.headers['Location'] = "/book/"+str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':7.99,'ibsn':1354}"
        }

        response = Response(json.dumps(invalidBookObjectErrorMsg), status_bad_request, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()

    if not test.valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':7.99}"
        }

        response = Response(json.dumps(invalidBookObjectErrorMsg), status_bad_request, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response('', status_no_content)
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if "name" in request_data:
        Book.update_book_name(request_data["name"])
    if "price" in request_data:
        Book.update_book_name(request_data["price"])

    response = Response("", status_no_content)
    response.headers['Location'] = "/books/"+str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status_no_content)
        return response
    message = {
        'error': 'Book with the ISBM number that was provided was not found'
    }
    response = Response(json.dumps(message), status_not_found, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(debug=True)
