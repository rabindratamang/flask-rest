def valid_book_object(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


valid_object = {
    'name': 'F',
    'price': 6.99,
    'isbn': 1233456
}


name_missing = {
    'price': 6.99,
    'isbn': 1233456
}


price_missing = {
    'name': 'F',
    'isbn': 1233456
}


isbn_missing = {
    'name': 'F',
    'price': 6.99,
}