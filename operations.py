"""
operations.py - Core functions for the Mini Library Management System
"""

# Data structures
books = {}          # ISBN -> {title, author, genre, total_copies, available_copies}
members = []        # list of dicts: {member_id, name, email, borrowed_books}
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Biography")  # tuple of valid genres


# ---------------------- Book Management (CRUD) ----------------------
def add_book(isbn, title, author, genre, total_copies):
    """
    Add a new book if ISBN is unique and genre is valid.
    Returns True on success, False if ISBN already exists or genre invalid.
    """
    if isbn in books:
        print(f"Error: Book with ISBN {isbn} already exists.")
        return False
    if genre not in GENRES:
        print(f"Error: '{genre}' is not a valid genre. Choose from {GENRES}")
        return False
    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        "available_copies": total_copies
    }
    print(f"Book '{title}' added successfully.")
    return True


def search_books(query):
    """
    Search books by title or author (case-insensitive, partial match).
    Returns a list of matching book details (as dictionaries).
    """
    results = []
    query_lower = query.lower()
    for isbn, details in books.items():
        if query_lower in details["title"].lower() or query_lower in details["author"].lower():
            results.append({"isbn": isbn, **details})
    return results


def update_book(isbn, **kwargs):
    """
    Update book details (title, author, genre, total_copies).
    If total_copies changes, adjust available_copies accordingly.
    Returns True if successful, False if book not found or new total < borrowed.
    """
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    book = books[isbn]
    borrowed = book["total_copies"] - book["available_copies"]

    # Handle total_copies update carefully
    if "total_copies" in kwargs:
        new_total = kwargs["total_copies"]
        if new_total < borrowed:
            print(f"Error: Cannot reduce total copies below borrowed count ({borrowed}).")
            return False
        # Adjust available copies
        book["available_copies"] = new_total - borrowed
        book["total_copies"] = new_total
        del kwargs["total_copies"]

    # Update other fields
    for key, value in kwargs.items():
        if key in ["title", "author", "genre"]:
            if key == "genre" and value not in GENRES:
                print(f"Error: '{value}' is not a valid genre.")
                return False
            book[key] = value

    print(f"Book with ISBN {isbn} updated successfully.")
    return True


def delete_book(isbn):
    """
    Delete a book only if no copies are borrowed (available == total).
    Returns True if deleted, False otherwise.
    """
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False
    book = books[isbn]
    if book["available_copies"] != book["total_copies"]:
        print(f"Error: Cannot delete book with ISBN {isbn} because copies are borrowed.")
        return False
    del books[isbn]
    print(f"Book with ISBN {isbn} deleted successfully.")
    return True


# ---------------------- Member Management (CRUD) ----------------------
def add_member(member_id, name, email):
    """
    Add a new member if ID is unique.
    Returns True on success, False if ID already exists.
    """
    for member in members:
        if member["member_id"] == member_id:
            print(f"Error: Member with ID {member_id} already exists.")
            return False
    members.append({
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []      # list of ISBNs
    })
    print(f"Member '{name}' added successfully.")
    return True


def update_member(member_id, **kwargs):
    """
    Update member details (name, email).
    Returns True if successful, False if member not found.
    """
    member = find_member_by_id(member_id)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    for key, value in kwargs.items():
        if key in ["name", "email"]:
            member[key] = value
    print(f"Member with ID {member_id} updated successfully.")
    return True


def delete_member(member_id):
    """
    Delete a member only if they have no borrowed books.
    Returns True if deleted, False otherwise.
    """
    member = find_member_by_id(member_id)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False
    if member["borrowed_books"]:
        print(f"Error: Cannot delete member with ID {member_id} because they have borrowed books.")
        return False
    members.remove(member)
    print(f"Member with ID {member_id} deleted successfully.")
    return True


# ---------------------- Borrow / Return ----------------------
def borrow_book(member_id, isbn):
    """
    Borrow a book if:
    - Member exists and has less than 3 borrowed books.
    - Book exists and has available copies.
    Returns True on success, False otherwise.
    """
    member = find_member_by_id(member_id)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    book = books[isbn]
    if book["available_copies"] <= 0:
        print(f"Error: No copies available for '{book['title']}'.")
        return False

    if len(member["borrowed_books"]) >= 3:
        print(f"Error: Member {member_id} has already borrowed 3 books.")
        return False

    # Perform borrow
    book["available_copies"] -= 1
    member["borrowed_books"].append(isbn)
    print(f"Member {member_id} borrowed '{book['title']}'.")
    return True


def return_book(member_id, isbn):
    """
    Return a borrowed book.
    Returns True on success, False if member or book not found,
    or the book was not borrowed by this member.
    """
    member = find_member_by_id(member_id)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    if isbn not in member["borrowed_books"]:
        print(f"Error: Member {member_id} did not borrow this book.")
        return False

    # Perform return
    book = books[isbn]
    book["available_copies"] += 1
    member["borrowed_books"].remove(isbn)
    print(f"Member {member_id} returned '{book['title']}'.")
    return True


# ---------------------- Helper Functions ----------------------
def find_member_by_id(member_id):
    """Return member dict if found, else None."""
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None


def display_books():
    """Print all books (for demo purposes)."""
    if not books:
        print("No books in the library.")
        return
    print("\n--- Books in Library ---")
    for isbn, details in books.items():
        print(f"ISBN: {isbn}, Title: {details['title']}, Author: {details['author']}, "
              f"Genre: {details['genre']}, Available: {details['available_copies']}/{details['total_copies']}")


def display_members():
    """Print all members (for demo purposes)."""
    if not members:
        print("No members registered.")
        return
    print("\n--- Members ---")
    for m in members:
        print(f"ID: {m['member_id']}, Name: {m['name']}, Email: {m['email']}, "
              f"Borrowed: {len(m['borrowed_books'])} books")