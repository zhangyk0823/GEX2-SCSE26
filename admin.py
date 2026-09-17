##Import the necessary module
import json


## This function should load the library data from a JSON file and return it as a suitable Python data structure.
def load_library(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)



## This function should save the library data to a JSON file.
## This function does not need to return anything, but it should ensure that the data is saved correctly to the specified file.
def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    



## This function should find a book by its title, author, or ID.
## If the book is found, it should return the book ID.
## If the book is not found, it should return None.
def find_book(books, search_text):
    if search_text is None:
        return None

    normalized = str(search_text).strip().lower()

    if not normalized:
        return None

    for book_id, book in books.items():
        if (
            str(book_id).strip().lower() == normalized
            or str(book.get("title", "")).strip().lower() == normalized
            or str(book.get("author", "")).strip().lower() == normalized
        ):
            return book_id

    return None



## This function should display the list of books in a user-friendly format.
## It should show the book ID, title, category, and availability status (available or on loan).
## If the book is available, it should display "AVAILABLE", and if it is on loan, it should display "ON LOAN".
## The function should not return anything, but it should print the information to the console.
## The heading for this display should be "BOOK CATALOGUE".
def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)

    for book_id, book in books.items():
        status = (
            "AVAILABLE"
            if book.get("available", False)
            else "ON LOAN"
        )

        print(
            f"{book_id} | {book.get('title', 'Unknown')} "
            f"| {book.get('category', 'Unknown')} | {status}"
        )


## This function should display the list of current loans in a user-friendly format.
## It should show the book ID, title, and the name of the borrower.
## The heading for this display should be "CURRENT LOANS".
## The function should not return anything, but it should print the information to the console.
def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)

    for loan in loans:
        book_id = loan.get("book_id", "Unknown")

        title = books.get(book_id, {}).get("title", "Unknown")

        print(
            f"{book_id} | {title} | "
            f"Borrower: {loan.get('borrower', 'Unknown')}"
        )


## This function should calculate and return the library statistics
## The statsitics should include the total number of books, the number of available books, and the number of borrowed books.
## The function should return these three values in the order: total, available, borrowed. Use a suitable data structure to return these values, such as a tuple or a dictionary.

def library_statistics(books):
    total = len(books)

    available = sum(
        1
        for book in books.values()
        if book.get("available", False)
    )

    borrowed = total - available

    return (total, available, borrowed)


## This function should display the library statistics in a user-friendly format.
## It should first load the library data from a JSON file, 
## Then calculate the statistics, and finally print the information to the console.
## The heading for this display should be "LIBRARY STATISTICS".
## It should print the total number of books, the number of available books, and the number of borrowed books.
## The function should not return anything, but it should print the information to the console.
def main():
    data = load_library("library.json")

    library = data["library"]
    categories = data["categories"]
    books = data["books"]
    loans = data.get("loans", [])

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library['name']}")
    print(f"Branch: {library['branch']}")
    print(f"Year: {library['year']}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()

    display_loans(loans, books)
    print()

    print("LIBRARY STATISTICS")
    print("-" * 60)

    total, available, borrowed = library_statistics(books)

    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()
