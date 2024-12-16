# Bookstore management system.

# Imports
import sqlite3


def create_database():
    """
    Creates the ebookstore database and populates it with initial data.

    - If the database or the "book" table does not exist, it will be created.
    - Prepopulates the "book" table with a predefined set of books.
    """
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()

    # Create the table called book if it doesn't exist.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        qty INTEGER NOT NULL
    )
    ''')

    # Insert into book table the given values from task.
    books_in_stock = [
        (3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
        (3005, "Alice in Wonderland", "Lewis Carroll", 12)
    ]

    cursor.executemany('''INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)''',
                       books_in_stock)

    # Commit changes and close the connection to "ebookstore.db"
    connection.commit()
    connection.close()


def get_book_id(prompt="Enter book ID: "):
    """
    Prompts the user to input a valid book ID.

    - Ensures that the input is a positive integer.
    - Re-prompts the user in case of invalid input.

    Args:
        prompt (str): Custom message to display when asking for input.

    Returns:
        int: A valid book ID entered by the user.
    """
    while True:  # Loop to keep asking for valid user input.
        try:
            # User input removing leading/trailing spaces.
            user_input = int(input(prompt).strip())
            if user_input < 0:  # Check for positive number.
                print("Error: Book ID must be a positive integer.")
                continue
            return user_input  # Exit the loop and return the valid input.
        except ValueError:
            print("Error: Invalid input. Please enter a valid book ID.")


def get_book_title():
    """
    Prompts the user to input a valid book title.

    - Ensures that the title is not empty.
    - Re-prompts the user in case of invalid input.

    Returns:
        str: A valid book title entered by the user.
    """
    while True:
        try:
            # Request user input.
            user_input = input("Enter a book title: ").strip()
            if not user_input:  # Check if input is empty.
                raise ValueError("Book title cannot be empty!")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid book title.")


def get_author_name():
    """
    Prompts the user to input a valid author name.

    - Ensures that the author name is not empty and does not contain numbers.
    - Re-prompts the user in case of invalid input.

    Returns:
        str: A valid author name entered by the user.
    """
    while True:
        try:
            user_input = input("Enter an author name: ").strip()
            if not user_input:  # Check if input is empty.
                raise ValueError("Author name cannot be empty!")
            # Check if input contains numbers.
            if any(char.isdigit() for char in user_input):
                raise ValueError("Author name cannot contain numbers!")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid author name.")


def get_book_qty():
    """
    Prompts the user to input a valid book quantity.

    - Ensures that the quantity is a positive integer.
    - Re-prompts the user in case of invalid input.

    Returns:
        int: A valid book quantity entered by the user.
    """
    while True:
        try:
            user_input = int(input("Enter book quantity: ").strip())
            if user_input < 0:
                print("Error: Book quantity must be a positive integer.")
                continue
            return user_input
        except ValueError:
            print("Error: Invalid input. Please enter a valid book quantity.")


def enter_book():
    """
    Adds a new book to the database.

    - Prompts the user for book details (ID, title, author, quantity).
    - Ensures that the book ID is unique.
    - Inserts the new book into the database.
    """
    try:
        id = get_book_id()  # Gets book id to insert into table.
        # Establishes connection to database 'ebookstore.db'
        connection = sqlite3.connect("ebookstore.db")
        # Establishes a cursor.
        cursor = connection.cursor()
        # Check if the book ID already exists.
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        if cursor.fetchone():
            print("A book with this ID already exists."
                  " Please use a unique ID.")
            connection.close()
            return

        title = get_book_title()  # Gets book title to insert into table.
        author = get_author_name()  # Gets author name to insert into table.
        qty = get_book_qty()  # Gets book quantity to insert into table.

        # Inserts the new values to the book table.
        cursor.execute('''INSERT INTO book VALUES (?, ?, ?, ?)''', (id, title,
                                                                author, qty))
        # Commits the changes.
        connection.commit()
        # Closes connection to database.
        connection.close()
        print("Book added successfully!")
        # Catches any exceptions and displays them as e.
    except Exception as e:
        print(f"Error: {e}")


def get_updated_title():
    """
    Prompts the user to input a new title for a book or leave it unchanged.

    - Displays a message if the user chooses to make no changes.

    Returns:
        str: The new title or an empty string if unchanged.
    """
    # Get user input and strip leading/trailing whitespace.
    user_input = input("Type in new title or press 'Enter' to make no"
                       " changes to book title): ").strip()
    # Check if input is empty.
    if user_input == "":
        print("You have pressed 'Enter' to make no changes to title.")
    return user_input  # Return the entered string.


def get_updated_author():
    """
    Prompts the user to input a new author name for a book or leave it unchanged.

    - Ensures that the new author name does not contain digits.
    - Displays a message if the user chooses to make no changes.

    Returns:
        str: The new author name or an empty string if unchanged.
    """
    while True:
        user_input = input("Type in new author or press 'Enter' to make no"
                           " changes to author name): ").strip()
        # Check if input is empty
        if user_input == "":
            print("You have pressed 'Enter' to make no changes to author.")
            return user_input

        # Check if the input contains digits
        if any(char.isdigit() for char in user_input):
            print("Invalid input. The author name must not contain digits."
                  " Please try again.")
        else:
            # Return valid input.
            return user_input


def get_updated_qty():
    """
    Prompts the user to input a new quantity for a book or leave it unchanged.

    - Ensures that the quantity is a positive integer.
    - Displays a message if the user chooses to make no changes.

    Returns:
        int or str: The new quantity as an integer, or an empty string if unchanged.
    """
    while True:
        user_input = input("Type in new quantity or press 'Enter' to make no"
                           " changes to book quantity): ").strip()

        # Check if the input is empty.
        if user_input == "":
            print("You have pressed 'Enter' to make no changes to quantity.")
            return user_input

    # Check if the input is a positive integer and characters are all digits.
        if user_input.isdigit():
            # Convert the valid input to an integer and return it.
            return int(user_input)

        # If the input is invalid, display error message.
        print("Invalid input. The book quantity must be a positive number."
              " Please try again.")


def update_book():
    """
    Updates the details of an existing book in the database.

    - Prompts the user for a book ID to identify the book.
    - Displays the current details of the book.
    - Allows the user to modify the title, author, and/or quantity.
    - Updates the database with the new details.
    """
    try:
        id = get_book_id(prompt="Enter book ID to update: ")
        
        # Connect to database
        with sqlite3.connect("ebookstore.db") as connection:
            cursor = connection.cursor()
            
            # Fetch the current book details
            cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
            book = cursor.fetchone()
            
            if book:
                print("Current book details:", book)
                
                # Gather updates from the user
                updates = {}
                new_title = get_updated_title()
                if new_title:
                    updates["title"] = new_title
                new_author = get_updated_author()
                if new_author:
                    updates["author"] = new_author
                new_qty = get_updated_qty()
                if new_qty:
                    updates["qty"] = new_qty
                
                # If there are updates, construct and execute the update query
                if updates:
                    query = "UPDATE book SET " + ", ".join(f"{key} = ?" for key in updates) + " WHERE id = ?"
                    params = list(updates.values()) + [id]
                    cursor.execute(query, params)
                    connection.commit()
                    print("Book updated successfully!")
                else:
                    print("No changes were made.")
            else:
                print("Book not found.")
    except Exception as e:
        print(f"Error: {e}")


def delete_book():
    """
    Deletes a book from the database.

    - Prompts the user for a book ID.
    - Removes the corresponding book record from the database.
    """
    try:
        id = get_book_id(prompt="Enter book ID to delete: ")
        connection = sqlite3.connect("ebookstore.db")
        cursor = connection.cursor()
        # Deletes book from row with the entered ID.
        cursor.execute('''DELETE FROM book WHERE id = ?''', (id,))
        connection.commit()
        connection.close()
        print("Book deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")


def search_books():
    """
    Searches for a book in the database by its ID.

    - Prompts the user for a book ID.
    - Displays the details of the book if found.
    """
    try:
        id = get_book_id(prompt="Enter book ID to search: ")
        connection = sqlite3.connect("ebookstore.db")
        cursor = connection.cursor()
        # Displays book from table with the entered ID.
        cursor.execute('''SELECT * FROM book WHERE id = ?''', (id,))
        book = cursor.fetchone()
        connection.close()

        # Check if book exists and displays information.
        if book:
            print("Book found:", book)
        # Displays message if book not found.
        else:
            print("Book not found.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """
    Main menu for the bookstore management system.

    - Provides options to add, update, delete, and search for books.
    - Allows the user to exit the program.
    """
    create_database()

    while True:
        print("\nBookstore Management System")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            enter_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_books()
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
