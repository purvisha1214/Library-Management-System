
import streamlit as st
from database import get_connection
import pandas as pd

def download_csv(df, button_label, file_name):
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=button_label,
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


# Custom Professional Styling
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f5f7fb;
}

/* Main page text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"] {
    color: #172554;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #172554 !important;
}

/* Sidebar heading */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] p {
    color: white !important;
}

/* Sidebar navigation labels */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label p,
[data-testid="stSidebar"] [role="radiogroup"] label span {
    color: white !important;
}

/* Selected navigation option */
[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
    background-color: #2563eb !important;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    color: #172554 !important;
    background-color: white !important;
}

/* Metrics */
.stMetric {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 18px;
}
/* Success message styling */
div[data-testid="stAlert"][kind="success"] {
    background-color: #d1fae5 !important;
    border: 1px solid #6ee7b7 !important;
}

div[data-testid="stAlert"][kind="success"] p,
div[data-testid="stAlert"][kind="success"] svg {
    color: #065f46 !important;
    fill: #065f46 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# Dashboard title
st.title("📚 Library Management System")
st.write("Manage your library efficiently from one place.")

st.divider()

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Dashboard",
        "Add Book",
        "View Books",
        "Register Member",
        "Issue Book",
        "Return Book",
        "Transaction History"
    ]
)

# Dashboard
if page == "Dashboard":

    st.subheader("Dashboard Overview")

    connection = get_connection()
    

    if connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COALESCE(SUM(total_copies), 0) FROM books"
        )
        total_books = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COALESCE(SUM(available_copies), 0) FROM books"
        )
        available_books = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM members")
        total_members = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM transactions WHERE status = 'Issued'"
        )
        issued_books = cursor.fetchone()[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Book Copies", total_books)
        col2.metric("Available Copies", available_books)
        col3.metric("Total Members", total_members)
        col4.metric("Currently Issued", issued_books)
        st.divider()

        st.subheader("⚠️ Low Stock Books")

        cursor.execute("""
            SELECT title, author, available_copies
            FROM books
            WHERE available_copies <= 2
            ORDER BY available_copies ASC
        """)

        low_stock = cursor.fetchall()

        if low_stock:
            low_stock_df = pd.DataFrame(
                low_stock,
                columns=["Book Title", "Author", "Available Copies"]
            )

            st.dataframe(
                low_stock_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("All books have sufficient stock!")

        st.divider()

        st.subheader("📋 Recent Transactions")

        cursor.execute("""
            SELECT
                b.title AS book_title,
                m.name AS member_name,
                t.issue_date,
                t.status
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN members m ON t.member_id = m.member_id
            ORDER BY t.transaction_id DESC
            LIMIT 5
        """)

        recent_transactions = cursor.fetchall()

        if recent_transactions:
            recent_df = pd.DataFrame(
                recent_transactions,
                columns=["Book Title", "Member Name", "Issue Date", "Status"]
            )

            st.dataframe(
                recent_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions available yet.")
        cursor.close()
        connection.close()

    else:
        st.error("Unable to connect to MySQL database.")
    

# Add Book Page
elif page == "Add Book":

    st.subheader("➕ Add New Book")

    with st.form("add_book_form"):

        title = st.text_input("Book Title")
        author = st.text_input("Author Name")

        quantity = st.number_input(
            "Total Copies",
            min_value=1,
            step=1
        )

        submit = st.form_submit_button("Add Book")

        if submit:

            if not title.strip() or not author.strip():
                st.error("Please fill in all fields.")

            else:
                connection = get_connection()

                if connection:
                    cursor = connection.cursor()

                    try:
                        cursor.execute(
                            """
                            INSERT INTO books
                            (title, author, total_copies, available_copies)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                title.strip(),
                                author.strip(),
                                quantity,
                                quantity
                            )
                        )

                        connection.commit()

                        st.success("Book added successfully!")

                    except Exception as error:
                        connection.rollback()
                        st.error(f"Error: {error}")

                    finally:
                        cursor.close()
                        connection.close()
        
# View Books Page
elif page == "View Books":

    st.subheader("📚 Book Inventory")

    connection = get_connection()

    if connection:

        try:
            query = """
                SELECT
                    book_id,
                    title,
                    author,
                    total_copies,
                    available_copies
                FROM books
            """

            df = pd.read_sql(query, connection)

            st.metric("Total Book Records", len(df))

            search = st.text_input("🔍 Search by title or author")

            if search:
                df = df[
                    df["title"].str.contains(search, case=False, na=False) |
                    df["author"].str.contains(search, case=False, na=False)
                ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            download_csv(df, "📥 Download Books as CSV", "library_books.csv")
            
            st.caption(f"Showing {len(df)} book records")

        except Exception as error:
            st.error(f"Unable to load books: {error}")

        finally:
            connection.close()

    else:
        st.error("Unable to connect to MySQL.")



# Register Member Page
elif page == "Register Member":

    st.subheader("👤 Register New Member")

    # Registration Form
    with st.form("register_member_form"):

        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number (Optional)")

        submit = st.form_submit_button("Register Member")

        if submit:

            if not name.strip() or not email.strip():
                st.error("Name and email are required.")

            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")

            elif phone.strip() and (
                not phone.isdigit() or len(phone) != 10
            ):
                st.error("Phone number must contain exactly 10 digits.")

            else:
                connection = get_connection()

                if connection:
                    cursor = connection.cursor()

                    try:
                        cursor.execute(
                            """
                            INSERT INTO members (name, email, phone)
                            VALUES (%s, %s, %s)
                            """,
                            (
                                name.strip(),
                                email.strip().lower(),
                                phone.strip() or None
                            )
                        )

                        connection.commit()
                        st.success("Member registered successfully!")

                    except Exception as error:
                        connection.rollback()

                        if getattr(error, "errno", None) == 1062:
                            st.error("This email is already registered.")
                        else:
                            st.error(f"Registration failed: {error}")

                    finally:
                        cursor.close()
                        connection.close()

                else:
                    st.error("Unable to connect to MySQL.")

    # Display Registered Members and CSV Download
    st.divider()
    st.subheader("📋 Registered Members")

    connection = get_connection()

    if connection:
        try:
            query = """
                SELECT member_id, name, email, phone
                FROM members
                ORDER BY member_id DESC
            """

            members_df = pd.read_sql(query, connection)

            st.dataframe(
                members_df,
                use_container_width=True,
                hide_index=True
            )

            download_csv(
                members_df,
                "📥 Download Members as CSV",
                "library_members.csv"
            )

        except Exception as error:
            st.error(f"Unable to load members: {error}")

        finally:
            connection.close()

    else:
        st.error("Unable to connect to MySQL.")


# Issue Book Page
elif page == "Issue Book":

    st.subheader("📖 Issue a Book")

    connection = get_connection()

    if connection:

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                "SELECT member_id, name FROM members ORDER BY name"
            )
            members = cursor.fetchall()

            cursor.execute(
                """
                SELECT book_id, title, available_copies
                FROM books
                WHERE available_copies > 0
                ORDER BY title
                """
            )
            books = cursor.fetchall()

        except Exception as error:
            st.error(f"Unable to load records: {error}")
            members = []
            books = []

        finally:
            cursor.close()
            connection.close()

        if not members:
            st.warning("Please register a member first.")

        elif not books:
            st.warning("No books are currently available.")

        else:

            member_options = {
                f"{m['name']} (ID: {m['member_id']})": m['member_id']
                for m in members
            }

            book_options = {
                f"{b['title']} (Available: {b['available_copies']})": b['book_id']
                for b in books
            }

            with st.form("issue_book_form"):

                selected_member = st.selectbox(
                    "Select Member",
                    list(member_options.keys())
                )

                selected_book = st.selectbox(
                    "Select Book",
                    list(book_options.keys())
                )

                submit = st.form_submit_button("Issue Book")

                if submit:

                    connection = get_connection()

                    if connection:

                        cursor = connection.cursor()

                        try:
                            connection.start_transaction()

                            book_id = book_options[selected_book]
                            member_id = member_options[selected_member]

                            cursor.execute(
                                """
                                SELECT available_copies
                                FROM books
                                WHERE book_id = %s
                                FOR UPDATE
                                """,
                                (book_id,)
                            )

                            book = cursor.fetchone()

                            if not book or book[0] <= 0:
                                connection.rollback()
                                st.error("This book is no longer available.")

                            else:
                                cursor.execute(
                                    """
                                    INSERT INTO transactions
                                    (book_id, member_id, issue_date, status)
                                    VALUES (%s, %s, CURDATE(), 'Issued')
                                    """,
                                    (book_id, member_id)
                                )

                                cursor.execute(
                                    """
                                    UPDATE books
                                    SET available_copies = available_copies - 1
                                    WHERE book_id = %s
                                    """,
                                    (book_id,)
                                )

                                connection.commit()

                                st.success("Book issued successfully!")

                        except Exception as error:
                            connection.rollback()
                            st.error(f"Unable to issue book: {error}")

                        finally:
                            cursor.close()
                            connection.close()

                    else:
                        st.error("Unable to connect to MySQL.")

    else:
        st.error("Unable to connect to MySQL.")


# Return Book Page
elif page == "Return Book":

    st.subheader("↩️ Return a Book")

    connection = get_connection()

    if connection:

        try:
            query = """
                SELECT
                    t.transaction_id,
                    b.title,
                    m.name,
                    t.issue_date,
                    t.status
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                JOIN members m ON t.member_id = m.member_id
                WHERE t.status = 'Issued'
                ORDER BY t.issue_date
            """

            df = pd.read_sql(query, connection)

        except Exception as error:
            st.error(f"Unable to load transactions: {error}")
            df = pd.DataFrame()

        finally:
            connection.close()

        if df.empty:
            st.info("There are no books currently issued.")

        else:

            st.write("### Currently Issued Books")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            transaction_options = {
                f"Transaction {row['transaction_id']} - {row['title']} ({row['name']})":
                row['transaction_id']
                for _, row in df.iterrows()
            }

            with st.form("return_book_form"):

                selected_transaction = st.selectbox(
                    "Select Transaction to Return",
                    list(transaction_options.keys())
                )

                submit = st.form_submit_button("Return Book")

                if submit:

                    connection = get_connection()

                    if connection:

                        cursor = connection.cursor()

                        try:
                            connection.start_transaction()

                            transaction_id = transaction_options[
                                selected_transaction
                            ]

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

                            if not transaction or transaction[1] != "Issued":

                                connection.rollback()
                                st.error("This transaction cannot be returned.")

                            else:

                                book_id = transaction[0]

                                cursor.execute(
                                    """
                                    UPDATE transactions
                                    SET status = 'Returned',
                                        return_date = CURDATE()
                                    WHERE transaction_id = %s
                                    """,
                                    (transaction_id,)
                                )

                                cursor.execute(
                                    """
                                    UPDATE books
                                    SET available_copies = available_copies + 1
                                    WHERE book_id = %s
                                    """,
                                    (book_id,)
                                )

                                connection.commit()

                                st.success("Book returned successfully!")

                        except Exception as error:
                            connection.rollback()
                            st.error(f"Unable to return book: {error}")

                        finally:
                            cursor.close()
                            connection.close()

                    else:
                        st.error("Unable to connect to MySQL.")

    else:
        st.error("Unable to connect to MySQL.")


# Transaction History Page
elif page == "Transaction History":

    st.subheader("📋 Transaction History")

    connection = get_connection()

    if connection:

        try:
            query = """
                SELECT
                    t.transaction_id,
                    b.title AS book_title,
                    m.name AS member_name,
                    t.issue_date,
                    t.return_date,
                    t.status
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                JOIN members m ON t.member_id = m.member_id
                ORDER BY t.transaction_id DESC
            """

            df = pd.read_sql(query, connection)

            col1, col2 = st.columns(2)

            col1.metric("Total Transactions", len(df))
            col2.metric(
                "Currently Issued",
                len(df[df["status"] == "Issued"])
            )

            st.divider()

            search = st.text_input(
                "🔍 Search by book title or member name"
            )

            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Issued", "Returned"]
            )

            if search:
                df = df[
                    df["book_title"].str.contains(
                        search, case=False, na=False
                    ) |
                    df["member_name"].str.contains(
                        search, case=False, na=False
                    )
                ]

            if status_filter != "All":
                df = df[df["status"] == status_filter]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            download_csv(df, "📥 Download Transactions as CSV", "transaction_history.csv")

            st.caption(f"Showing {len(df)} transactions")

        except Exception as error:
            st.error(f"Unable to load history: {error}")

        finally:
            connection.close()

    else:
        st.error("Unable to connect to MySQL.")

