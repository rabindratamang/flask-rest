from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer)

    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn':self.isbn}

    @staticmethod
    def add_book(name, price, isbn):
        new_book = Book(name=name, price=price, isbn=isbn)
        db.session.add(new_book)
        db.session.commit()

    @staticmethod
    def get_book(isbn):
        book = Book.query.filter_by(isbn=isbn).first()
        if book:
            return Book.json(book)
        else:
            return {}

    @staticmethod
    def update_book_price(isbn, price):
        book_to_update = Book.query.filter_by(isbn=isbn).first()
        book_to_update.price = price
        db.session.commit()

    @staticmethod
    def update_book_name(isbn, name):
        book_to_update = Book.query.filter_by(isbn=isbn).first()
        book_to_update.name = name
        db.session.commit()

    @staticmethod
    def replace_book(isbn, name, price):
        book_to_update = Book.query.filter_by(isbn=isbn).first()
        book_to_update.name = name
        book_to_update.price = price
        db.session.commit()

    def delete_book(self, isbn):
        is_successful =Book.query.filter_by(isbn=isbn).delete()
        db.session.commit()
        return bool(is_successful)

    @staticmethod
    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)