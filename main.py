from database import get_connection
from datetime import date

def add_book():
    print("\n--- ADD NEW BOOK ---")

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()

    try:
        copies = int(input("Enter number of copies: "))

        if not title or not author or copies <= 0:
            print("Please enter valid details.")
            return

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        query = """
        INSERT INTO books
        (title, author, total_copies, available_copies)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query, (title, author, copies, copies)
        )

        conn.commit()

        print("Book added successfully!")

        cursor.close()
        conn.close()

    except ValueError:
        print("Please enter a valid number.")


def view_books():
    print("\n--- ALL BOOKS ---")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    if not books:
        print("No books available.")
    else:
        for book in books:
            print(book)

    cursor.close()
    conn.close()



def add_member():
    print("\n--- REGISTER NEW MEMBER ---")

    name = input("Enter member name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not email:
        print("Name and email are required.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO members (name, email, phone)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, email, phone))
        conn.commit()

        print("Member registered successfully!")

    except Exception as error:
        conn.rollback()
        print("Registration failed:", error)

    finally:
        cursor.close()
        conn.close()




def issue_book():

    print("\n--- ISSUE BOOK ---")

    try:
        book_id = int(input("Enter book ID: "))
        member_id = int(input("Enter member ID: "))
    except ValueError:
        print("Please enter valid IDs.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        conn.start_transaction()

        cursor.execute(
            "SELECT available_copies FROM books "
            "WHERE book_id = %s FOR UPDATE",
            (book_id,)
        )

        book = cursor.fetchone()

        if book is None or book[0] <= 0:
            raise ValueError("Book is unavailable.")

        cursor.execute(
            "SELECT member_id FROM members WHERE member_id = %s",
            (member_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Member does not exist.")

        query = """
        INSERT INTO transactions
        (book_id, member_id, issue_date, status)
        VALUES (%s, %s, %s, 'Issued')
        """

        cursor.execute(
            query, (book_id, member_id, date.today())
        )

        cursor.execute(
            """
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE book_id = %s
            """,
            (book_id,)
        )

        conn.commit()

        print("Book issued successfully!")

    except Exception as error:
        conn.rollback()
        print("Issue failed:", error)

    finally:
        cursor.close()
        conn.close()

def return_book():
    print("\n--- RETURN BOOK ---")

    try:
        transaction_id = int(input("Enter transaction ID: "))
    except ValueError:
        print("Please enter a valid transaction ID.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        conn.start_transaction()

        cursor.execute(
            """
            SELECT book_id, status
            FROM transactions
            WHERE transaction_id = %s
            FOR UPDATE
            """,
            (transaction_id,)
        )

        transaction = cursor.fetchone()

        if transaction is None:
            raise ValueError("Transaction not found.")

        book_id, status = transaction

        if status == "Returned":
            raise ValueError("This book has already been returned.")

        cursor.execute(
            """
            UPDATE transactions
            SET status = 'Returned', return_date = %s
            WHERE transaction_id = %s
            """,
            (date.today(), transaction_id)
        )

        cursor.execute(
            """
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE book_id = %s
            """,
            (book_id,)
        )

        conn.commit()
        print("Book returned successfully!")

    except Exception as error:
        conn.rollback()
        print("Return failed:", error)

    finally:
        cursor.close()
        conn.close()

def view_transactions():
    print("\n--- TRANSACTION HISTORY ---")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    query = """
    SELECT
        t.transaction_id,
        b.title,
        m.name,
        t.issue_date,
        t.return_date,
        t.status
    FROM transactions t
    JOIN books b ON t.book_id = b.book_id
    JOIN members m ON t.member_id = m.member_id
    ORDER BY t.transaction_id DESC
    """

    cursor.execute(query)
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found.")
    else:
        for transaction in transactions:
            print(transaction)

    cursor.close()
    conn.close()
if __name__ == "__main__":
    view_transactions()

def main():
    while True:
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Add Book")
        print("2. View Books")
        print("3. Register Member")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Transaction History")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            add_member()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            view_transactions()
        elif choice == "7":
            print("Thank you for using Library Management System!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()