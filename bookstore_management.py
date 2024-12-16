# Bookstore management system.

# Imports
import sqlite3

def create_database():
    """Creates the ebookstore database and populates it with initial data."""
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
    Prompt the user for an integer input based on the book ID.
    Displays error messages for invalid inputs.
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
    Prompts the user for a string input for book title.
    Ensures that invalid or empty inputs are handled.
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
    Prompts the user for a string input for author of the book.
    Ensures that invalid or empty inputs are handled.
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
    Prompt the user for an integer input based on the book quantity.
    Displays error messages for invalid inputs.
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
    """Allows the user to add a new book."""
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
    Prompts the user to enter a string to update book title.
    If there is no input will display a message.
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
    Prompts the user to enter a string without digits to update author name.
    If there is no input will display a message.
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
    Prompts the user to enter a positive integer to update book quantity.
    If there is no input will display a message.
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
    """Allows the user to update book information."""
    try:
        # Enter valid book ID to edit book information.
        id = get_book_id(prompt="Enter book ID to update: ")
        # Connect to database.
        connection = sqlite3.connect("ebookstore.db")
        # Get cursor.
        cursor = connection.cursor()
        # Select the book from row with ID input.
        cursor.execute('''SELECT * FROM book WHERE id = ?''', (id,))
        # Variable 'book' created to store book information.
        book = cursor.fetchone()

        if book:
            print("Current book details:", book)
            # Calls function to get updated title for book from user.
            new_title = get_updated_title()
            # If no input title remains the same or becomes 'new_title'.
            title = new_title or book[1]
            # Calls function to get updated author name for book from user.
            new_author = get_updated_author()
            # If no input author name remains the same or becomes 'new_author'.
            author = new_author or book[2]
            # Calls function to get updated quantity of books from user.
            new_qty = get_updated_qty()
            # If no input quantity remains the same or becomes 'new_qty'.
            qty = new_qty or book[3]

            # Updates specific book details based on the user inputs.
            cursor.execute('''UPDATE book SET title = ?, author = ?, qty = ?
                           WHERE id = ?''', (title, author, qty, id))
            connection.commit()
            print("Book updated successfully!")
        else:
            print("Book not found.")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def delete_book():
    """Allows the user to delete a book."""
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
    """Allows the user to search for a book by ID."""
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
    """Main menu for the bookstore clerk."""
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
