import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
import datetime


CATEGORIES = [
    "Food",
    "Transportation",
    "Bills",
    "Shopping",
    "Entertainment",
    "School",
    "Health",
    "Subscriptions",
    "Groceries",
    "Others"
]


# --------------------------
# Database Connection
# --------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="expense_tracker"
    )

# --------------------------
# DARK MODE THEME SETTINGS
# --------------------------
BG = "#1e1e1e"        # Main background
FG = "#ffffff"        # Main text
BTN_BG = "#2c2c2c"    # Button background
BTN_ACTIVE = "#3a3a3a"
ENTRY_BG = "#2b2b2b"
TABLE_BG = "#2a2a2a"
TABLE_FG = "#f0f0f0"
TABLE_SEL = "#444444"

def style_window(win):
    win.configure(bg=BG)

# ===========================================================
# POPUP WINDOWS
# ===========================================================

# --------------------------
# ADD WINDOW
# --------------------------
def open_add_window():
    add_win = Toplevel(window)
    add_win.title("Add Expense")
    add_win.geometry("300x250")

    Label(add_win, text="Category:").pack(pady=5)

    category = ttk.Combobox(add_win, values=CATEGORIES, state="readonly")
    category.pack(pady=5)
    category.set("Select Category")

    Label(add_win, text="Amount:").pack(pady=5)
    amount = Entry(add_win)
    amount.pack(pady=5)

    def save_expense():
        c = category.get()
        a = amount.get()

        if c == "Select Category" or a == "":
            messagebox.showerror("Error", "All fields required!")
            return

        try:
            a = float(a)
        except:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        db = connect_db()
        cursor = db.cursor()
        query = "INSERT INTO expenses (category, amount, date_added) VALUES (%s, %s, %s)"
        cursor.execute(query, (c, a, datetime.date.today()))
        db.commit()

        messagebox.showinfo("Success", "Expense added!")
        add_win.destroy()

    Button(add_win, text="Save", width=15, command=save_expense).pack(pady=15)



# --------------------------
# DELETE WINDOW
# --------------------------
def open_delete_window():
    del_win = Toplevel(window)
    del_win.title("Delete Expense")
    del_win.geometry("300x200")
    style_window(del_win)

    Label(del_win, text="Expense ID:", fg=FG, bg=BG).pack(pady=5)
    exp_id = Entry(del_win, bg=ENTRY_BG, fg=FG, insertbackground=FG)
    exp_id.pack(pady=5)

    def delete_expense():
        id_val = exp_id.get()

        if id_val == "":
            messagebox.showerror("Error", "ID required!")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = %s", (id_val,))
        db.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Warning", "ID not found.")
        else:
            messagebox.showinfo("Success", "Deleted successfully.")
            del_win.destroy()

    Button(del_win, text="Delete", bg=BTN_BG, fg=FG, activebackground=BTN_ACTIVE,
           width=15, command=delete_expense).pack(pady=15)


# --------------------------
# UPDATE WINDOW
# --------------------------
def open_update_window():
    upd_win = Toplevel(window)
    upd_win.title("Update Expense")
    upd_win.geometry("350x300")

    Label(upd_win, text="Expense ID:").pack(pady=5)
    id_entry = Entry(upd_win)
    id_entry.pack(pady=5)

    Label(upd_win, text="New Category:").pack(pady=5)

    new_cat = ttk.Combobox(upd_win, values=CATEGORIES, state="readonly")
    new_cat.pack(pady=5)
    new_cat.set("Select Category")

    Label(upd_win, text="New Amount:").pack(pady=5)
    new_amount = Entry(upd_win)
    new_amount.pack(pady=5)

    def update_expense():
        eid = id_entry.get()
        cat = new_cat.get()
        amt = new_amount.get()

        if eid == "" or cat == "Select Category" or amt == "":
            messagebox.showerror("Error", "All fields required!")
            return

        try:
            amt = float(amt)
        except:
            messagebox.showerror("Error", "Amount must be numeric.")
            return

        db = connect_db()
        cursor = db.cursor()
        q = "UPDATE expenses SET category=%s, amount=%s WHERE id=%s"
        cursor.execute(q, (cat, amt, eid))
        db.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Warning", "No record found.")
        else:
            messagebox.showinfo("Success", "Expense updated.")
            upd_win.destroy()

    Button(upd_win, text="Update", width=15, command=update_expense).pack(pady=15)



# --------------------------
# SEARCH WINDOW
# --------------------------
def open_search_window():
    search_win = Toplevel(window)
    search_win.title("Search / View Expenses")
    search_win.geometry("650x450")
    style_window(search_win)

    Label(search_win, text="Search by Category:", fg=FG, bg=BG).pack(pady=5)
    search_entry = Entry(search_win, bg=ENTRY_BG, fg=FG, insertbackground=FG)
    search_entry.pack(pady=5)

    cols = ("ID", "Category", "Amount", "Date")
    table = ttk.Treeview(search_win, columns=cols, show="headings")
    table.pack(fill=BOTH, expand=True, pady=10)

    # Style table
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background=TABLE_BG, foreground=TABLE_FG, 
                    fieldbackground=TABLE_BG, rowheight=25)
    style.map("Treeview", background=[("selected", TABLE_SEL)])

    for col in cols:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=130)

    def load_all():
        for row in table.get_children():
            table.delete(row)

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        for r in rows:
            table.insert("", END, values=r)

    def search():
        keyword = search_entry.get()

        for row in table.get_children():
            table.delete(row)

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM expenses WHERE category LIKE %s", (f"%{keyword}%",))
        rows = cursor.fetchall()

        for r in rows:
            table.insert("", END, values=r)

    Button(search_win, text="Load All", bg=BTN_BG, fg=FG,
           activebackground=BTN_ACTIVE, width=12, command=load_all).pack(pady=5)
    Button(search_win, text="Search", bg=BTN_BG, fg=FG,
           activebackground=BTN_ACTIVE, width=12, command=search).pack(pady=5)

    load_all()


# ===========================================================
# MAIN WINDOW
# ===========================================================
window = Tk()
window.title("Expense Tracker - Dark Mode")
window.geometry("320x380")
style_window(window)

Label(window, text="EXPENSE TRACKER", font=("Arial", 18, "bold"),
      fg=FG, bg=BG).pack(pady=20)

Button(window, text="Add Expense", width=20, bg=BTN_BG, fg=FG,
       activebackground=BTN_ACTIVE, command=open_add_window).pack(pady=10)

Button(window, text="Update Expense", width=20, bg=BTN_BG, fg=FG,
       activebackground=BTN_ACTIVE, command=open_update_window).pack(pady=10)

Button(window, text="Delete Expense", width=20, bg=BTN_BG, fg=FG,
       activebackground=BTN_ACTIVE, command=open_delete_window).pack(pady=10)

Button(window, text="Search / Show Expenses", width=20, bg=BTN_BG, fg=FG,
       activebackground=BTN_ACTIVE, command=open_search_window).pack(pady=10)

window.mainloop()
