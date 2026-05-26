"""
demo.py - Demonstration of the Mini Library Management System
"""

import operations

def main():
    print("=== Library Management System Demo ===\n")

    # Add books
    print("--- Adding Books ---")
    operations.add_book("978-3-16-148410-0", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 5)
    operations.add_book("978-0-14-143951-8", "1984", "George Orwell", "Sci-Fi", 3)
    operations.add_book("978-0-06-112008-4", "To Kill a Mockingbird", "Harper Lee", "Fiction", 4)
    # Invalid genre
    operations.add_book("978-1-234-56789-7", "Invalid Genre Book", "Unknown", "Horror", 2)

    # Add members
    print("\n--- Adding Members ---")
    operations.add_member(101, "Alice Smith", "alice@example.com")
    operations.add_member(102, "Bob Johnson", "bob@example.com")
    # Duplicate ID
    operations.add_member(101, "Charlie", "charlie@example.com")

    # Display initial data
    operations.display_books()
    operations.display_members()

    # Search books
    print("\n--- Search by '1984' ---")
    results = operations.search_books("1984")
    for book in results:
        print(book)

    print("\n--- Search by author 'Fitzgerald' ---")
    results = operations.search_books("Fitzgerald")
    for book in results:
        print(book)

    # Update a book
    print("\n--- Update Book (increase total copies of '1984') ---")
    operations.update_book("978-0-14-143951-8", total_copies=5)

    # Update a member
    print("\n--- Update Member (change email of Alice) ---")
    operations.update_member(101, email="alice.new@example.com")

    # Borrow books
    print("\n--- Borrow Books ---")
    operations.borrow_book(101, "978-3-16-148410-0")  # Great Gatsby
    operations.borrow_book(101, "978-0-14-143951-8")  # 1984
    operations.borrow_book(101, "978-0-06-112008-4")  # Mockingbird
    operations.borrow_book(101, "978-3-16-148410-0")  # Trying to borrow a 4th book (should fail)

    operations.borrow_book(102, "978-3-16-148410-0")  # Bob borrows a copy of Gatsby

    # Return a book
    print("\n--- Return Book (Alice returns 1984) ---")
    operations.return_book(101, "978-0-14-143951-8")

    # Delete a book (should fail because copies borrowed)
    print("\n--- Try to delete book with borrowed copies ---")
    operations.delete_book("978-3-16-148410-0")

    # Delete a member (should fail because Alice still has borrowed books)
    print("\n--- Try to delete member with borrowed books ---")
    operations.delete_member(101)

    # Return all books for Alice, then delete member
    print("\n--- Alice returns remaining books ---")
    operations.return_book(101, "978-3-16-148410-0")
    operations.return_book(101, "978-0-06-112008-4")

    print("\n--- Delete member after returning all books ---")
    operations.delete_member(101)

    # Delete book after all copies returned
    print("\n--- Delete book with no borrowed copies ---")
    operations.delete_book("978-3-16-148410-0")

    # Final display
    operations.display_books()
    operations.display_members()

if __name__ == "__main__":
    main()