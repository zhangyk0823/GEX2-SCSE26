## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
from admin import (
    find_book,
    load_library,
    save_library
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    if category is None:
        return []

    normalized = str(category).strip().lower()

    if not normalized:
        return []

    result = []

    for book_id, book in books.items():
        if (
            str(book.get("category", "")).strip().lower()
            == normalized
        ):
            result.append(book_id)

    return result

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    if search_text is None:
        return []

    normalized = str(search_text).strip().lower()

    if not normalized:
        return []

    result = []

    for book_id, book in books.items():
        title = str(book.get("title", "")).strip().lower()

        if normalized in title:
            result.append(book_id)

    return result
    



## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None or not str(borrower).strip():
        return "EMPTY_NAME"

    if not books[book_id].get("available", False):
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False

    loans.append(
        {
            "book_id": book_id,
            "borrower": str(borrower).strip()
        }
    )

    return "OK"

    



## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None or not str(borrower).strip():
        return "EMPTY_NAME"

    for index, loan in enumerate(loans):
        if (
            str(loan.get("book_id", "")).strip().lower()
            == str(book_id).strip().lower()
        ):
            loans.pop(index)
            books[book_id]["available"] = True
            return "OK"

    return "NOT_ON_LOAN"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")

    books = data["books"]
    loans = data.get("loans", [])

    while True:
        print("LIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by category")
        print("2. Search books by title")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        print("=" * 60)

        choice = input("Select an option: ").strip()

        if choice == "1":
            category = input("Enter category: ")

            result = books_in_category(books, category)

            if result:
                print("Books in category:")
                for book_id in result:
                    print(book_id)
            else:
                print("No books found in that category.")

        elif choice == "2":
            title = input("Enter title: ")

            result = search_by_title(books, title)

            if result:
                print("Books matching title:")
                for book_id in result:
                    print(book_id)
            else:
                print("No books found matching that title.")

        elif choice == "3":
            search_text = input("Enter book ID or title: ")
            borrower = input("Enter borrower name: ")

            print(
                borrow_book(
                    books,
                    loans,
                    search_text,
                    borrower
                )
            )

        elif choice == "4":
            book_title = input("Enter book ID or title: ")
            borrower = input("Enter borrower name: ")

            print(
                return_book(
                    books,
                    loans,
                    book_title,
                    borrower
                )
            )

        elif choice == "5":
            save_library(data, "library.json")
            print("Goodbye!")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
