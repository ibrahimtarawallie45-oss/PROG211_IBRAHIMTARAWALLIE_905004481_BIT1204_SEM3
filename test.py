"""
tests.py - Unit tests for the Mini Library Management System
"""

import operations

def reset_data():
    """Reset global data structures to empty."""
    operations.books.clear()
    operations.members.clear()

def test_add_book_success():
    reset_data()
    result = operations.add_book("123", "Title", "Author", "Fiction", 5)
    assert result == True
    assert "123" in operations.books
    assert operations.books["123"]["title"] == "Title"

def test_add_book_duplicate_isbn():
    reset_data()
    operations.add_book("123", "Title1", "Author1", "Fiction", 5)
    result = operations.add_book("123", "Title2", "Author2", "Fiction", 3)
    assert result == False

def test_add_book_invalid_genre():
    reset_data()
    result = operations.add_book("123", "Title", "Author", "Horror", 5)
    assert result == False

def test_borrow_book_success():
    reset_data()
    operations.add_book("123", "Title", "Author", "Fiction", 2)
    operations.add_member(1, "Alice", "alice@mail.com")
    result = operations.borrow_book(1, "123")
    assert result == True
    assert operations.books["123"]["available_copies"] == 1
    member = operations.find_member_by_id(1)
    assert "123" in member["borrowed_books"]

def test_borrow_book_no_copies():
    reset_data()
    operations.add_book("123", "Title", "Author", "Fiction", 1)
    operations.add_member(1, "Alice", "alice@mail.com")
    operations.borrow_book(1, "123")
    result = operations.borrow_book(1, "123")
    assert result == False
    assert operations.books["123"]["available_copies"] == 0

def test_borrow_book_member_limit():
    reset_data()
    operations.add_book("111", "B1", "A", "Fiction", 1)
    operations.add_book("222", "B2", "A", "Fiction", 1)
    operations.add_book("333", "B3", "A", "Fiction", 1)
    operations.add_book("444", "B4", "A", "Fiction", 1)
    operations.add_member(1, "Alice", "alice@mail.com")
    operations.borrow_book(1, "111")
    operations.borrow_book(1, "222")
    operations.borrow_book(1, "333")
    result = operations.borrow_book(1, "444")
    assert result == False

def test_return_book_success():
    reset_data()
    operations.add_book("123", "Title", "Author", "Fiction", 1)
    operations.add_member(1, "Alice", "alice@mail.com")
    operations.borrow_book(1, "123")
    result = operations.return_book(1, "123")
    assert result == True
    assert operations.books["123"]["available_copies"] == 1
    member = operations.find_member_by_id(1)
    assert "123" not in member["borrowed_books"]

def test_delete_book_with_borrowed():
    reset_data()
    operations.add_book("123", "Title", "Author", "Fiction", 1)
    operations.add_member(1, "Alice", "alice@mail.com")
    operations.borrow_book(1, "123")
    result = operations.delete_book("123")
    assert result == False
    assert "123" in operations.books

def test_delete_member_with_borrowed():
    reset_data()
    operations.add_member(1, "Alice", "alice@mail.com")
    operations.add_book("123", "Title", "Author", "Fiction", 1)
    operations.borrow_book(1, "123")
    result = operations.delete_member(1)
    assert result == False
    assert operations.find_member_by_id(1) is not None

# Run all tests if script executed directly
if __name__ == "__main__":
    test_add_book_success()
    test_add_book_duplicate_isbn()
    test_add_book_invalid_genre()
    test_borrow_book_success()
    test_borrow_book_no_copies()
    test_borrow_book_member_limit()
    test_return_book_success()
    test_delete_book_with_borrowed()
    test_delete_member_with_borrowed()
    print("All tests passed.")