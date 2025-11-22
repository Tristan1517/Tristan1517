from tkinter import *
from tkinter import ttk, messagebox
import datetime

# --------------------------
# CONFIG / THEME
# --------------------------
CATEGORIES = [
    "Food", "Transportation", "Bills", "Shopping", "Entertainment",
    "School", "Health", "Subscriptions", "Groceries", "Others"
]

# Dark Win theme
BG = "#0f1113"
CARD_BG = "#16171a"
FG = "#e7eef6"
ACCENT = "#3fb07f"
BTN_BG = "#1f2225"
BTN_ACTIVE = "#2a2d30"
ENTRY_BG = "#131416"
TABLE_BG = "#0d0e10"
TABLE_FG = "#e7eef6"
TABLE_SEL = "#2b3a3a"

# Window size
WinWidth = 400
WinHeight = 600

# --------------------------
# In-memory storage
# --------------------------
expenses = []  # list of dicts with keys: id, category, amount, date
next_id = 1

# --------------------------
# UI helpers
# --------------------------
def style_window(win, title=None):
    if title:
        win.title(title)
    win.configure(bg=BG)
    win.resizable(False, False)
    win.geometry(f"{WinWidth}x{WinHeight}")
    # center
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (WinWidth // 2)
    y = (win.winfo_screenheight() // 2) - (WinHeight // 2)
    win.geometry(f"+{x}+{y}")

def make_header(parent, text):
    header = Frame(parent, bg=CARD_BG, pady=12)
    header.pack(fill=X, padx=16, pady=(16, 8))
    Label(header, text=text, font=("Helvetica", 18, "bold"),
          fg=FG, bg=CARD_BG).pack()
    return header

def label_entry(parent, label_text, **entry_kwargs):
    frame = Frame(parent, bg=BG)
    Label(frame, text=label_text, fg=FG, bg=BG).pack(anchor="w")
    ent = Entry(frame, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=FLAT, **entry_kwargs)
    ent.pack(fill=X, pady=6)
    return frame, ent

def label_combobox(parent, label_text, values, default="Select Category"):
    frame = Frame(parent, bg=BG)
    Label(frame, text=label_text, fg=FG, bg=BG).pack(anchor="w")
    cb = ttk.Combobox(frame, values=values, state="readonly")
    cb.pack(fill=X, pady=6)
    cb.set(default)
    return frame, cb

def big_button(parent, text, command):
    btn = Button(parent, text=text, command=command, bg=BTN_BG, fg=FG,
                 activebackground=BTN_ACTIVE, relief=FLAT)
    return btn

# --------------------------
# Add Window
# --------------------------
def open_add_window():
    add_win = Toplevel(window)
    add_win.transient(window)
    add_win.grab_set()
    style_window(add_win, "Add Expense")
    make_header(add_win, "Add Expense")

    body = Frame(add_win, bg=BG, padx=16)
    body.pack(fill=BOTH, expand=True)

    cat_frame, category_cb = label_combobox(body, "Category:", CATEGORIES)
    cat_frame.pack(fill=X, pady=6)
    amt_frame, amount_ent = label_entry(body, "Amount:")
    amt_frame.pack(fill=X, pady=6)

    footer = Frame(add_win, bg=BG)
    footer.pack(pady=12)

    def save_expense():
        global next_id  # <-- THIS MUST BE HERE
        c = category_cb.get()
        a = amount_ent.get().strip()
        if c == "Select Category" or a == "":
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            a_val = float(a)
        except:
            messagebox.showerror("Error", "Amount must be numeric.")
            return
        today = datetime.date.today().strftime("%Y-%m-%d")
        expenses.append({"id": next_id, "category": c, "amount": a_val, "date": today})
        next_id += 1
        messagebox.showinfo("Success", "Expense added.")
        add_win.destroy()

    btn_save = big_button(footer, "Save", save_expense)
    btn_cancel = big_button(footer, "Cancel", add_win.destroy)
    btn_save.pack(side=LEFT, padx=8)
    btn_cancel.pack(side=LEFT, padx=8)


# --------------------------
# Update Window
# --------------------------
def open_update_window():
    upd = Toplevel(window)
    upd.transient(window)
    upd.grab_set()
    style_window(upd, "Update Expense")
    make_header(upd, "Update Expense")

    body = Frame(upd, bg=BG, padx=16)
    body.pack(fill=BOTH, expand=True)

    # ID input
    id_frame = Frame(body, bg=BG)
    Label(id_frame, text="Expense ID:", fg=FG, bg=BG).pack(anchor="w")
    id_ent = Entry(id_frame, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=FLAT)
    id_ent.pack(side=LEFT, fill=X, expand=True, pady=6)
    load_btn = big_button(id_frame, "Load", lambda: load_record())
    load_btn.pack(side=LEFT, padx=8)
    id_frame.pack(fill=X, pady=6)

    preview = Frame(body, bg=CARD_BG, padx=10, pady=8)
    preview.pack(fill=X, pady=8)
    preview_lbl = Label(preview, text="No record loaded", fg=FG, bg=CARD_BG, wraplength=360, justify=LEFT)
    preview_lbl.pack(anchor="w")

    cat_frame, category_cb = label_combobox(body, "New Category:", CATEGORIES)
    cat_frame.pack(fill=X, pady=6)
    amt_frame, amount_ent = label_entry(body, "New Amount:")
    amt_frame.pack(fill=X, pady=6)

    footer = Frame(upd, bg=BG)
    footer.pack(pady=12)
    loaded = {"id": None}

    def load_record():
        eid = id_ent.get().strip()
        if not eid.isdigit():
            messagebox.showerror("Error", "ID must be numeric.")
            return
        for e in expenses:
            if e["id"] == int(eid):
                loaded["id"] = e["id"]
                preview_lbl.config(text=f"ID: {e['id']}\nCategory: {e['category']}\nAmount: {e['amount']}\nDate: {e['date']}")
                category_cb.set(e["category"])
                amount_ent.delete(0, END)
                amount_ent.insert(0, str(e["amount"]))
                return
        messagebox.showwarning("Not found", "No expense with that ID.")
        loaded["id"] = None
        preview_lbl.config(text="No record loaded")
        category_cb.set("Select Category")
        amount_ent.delete(0, END)

    def do_update():
        if loaded["id"] is None:
            messagebox.showerror("Error", "Load a record first.")
            return
        cat = category_cb.get()
        amt = amount_ent.get().strip()
        if cat == "Select Category" or amt == "":
            messagebox.showerror("Error", "All fields required.")
            return
        try:
            a_val = float(amt)
        except:
            messagebox.showerror("Error", "Amount must be numeric.")
            return
        for e in expenses:
            if e["id"] == loaded["id"]:
                e["category"] = cat
                e["amount"] = a_val
                messagebox.showinfo("Success", "Expense updated.")
                upd.destroy()
                return

    btn_update = big_button(footer, "Update", do_update)
    btn_cancel = big_button(footer, "Cancel", upd.destroy)
    btn_update.pack(side=LEFT, padx=8)
    btn_cancel.pack(side=LEFT, padx=8)

# --------------------------
# Delete Window
# --------------------------
def open_delete_window():
    dwin = Toplevel(window)
    dwin.transient(window)
    dwin.grab_set()
    style_window(dwin, "Delete Expense")
    make_header(dwin, "Delete Expense")

    body = Frame(dwin, bg=BG, padx=12)
    body.pack(fill=BOTH, expand=True)

    # --- Scrollable table of expenses ---
    table_frame = Frame(body, bg=BG)
    table_frame.pack(fill=BOTH, expand=True, pady=(4,8))

    cols = ("ID", "Category", "Amount", "Date")
    table = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
    for c in cols:
        table.heading(c, text=c)
        table.column(c, anchor="center", width=65)

    vsb = Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
    table.configure(yscrollcommand=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)
    table.pack(side=LEFT, fill=BOTH, expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background=TABLE_BG, foreground=TABLE_FG, fieldbackground=TABLE_BG, rowheight=28)
    style.map("Treeview", background=[("selected", TABLE_SEL)])

    def load_all():
        for r in table.get_children():
            table.delete(r)
        for e in sorted(expenses, key=lambda x: -x["id"]):
            table.insert("", END, values=(e["id"], e["category"], e["amount"], e["date"]))

    load_all()

    # --- Preview selected record ---
    preview = Frame(body, bg=CARD_BG, padx=10, pady=8)
    preview.pack(fill=X, pady=6)
    preview_lbl = Label(preview, text="Select a record from the table", fg=FG, bg=CARD_BG, wraplength=360, justify=LEFT)
    preview_lbl.pack(anchor="w")

    loaded = {"id": None}

    def on_select(event):
        sel = table.focus()
        if sel:
            values = table.item(sel, "values")
            loaded["id"] = int(values[0])
            preview_lbl.config(text=f"ID: {values[0]}\nCategory: {values[1]}\nAmount: {values[2]}\nDate: {values[3]}")

    table.bind("<<TreeviewSelect>>", on_select)

    # --- Footer Buttons ---
    footer = Frame(dwin, bg=BG)
    footer.pack(pady=12)

    def do_delete():
        if loaded["id"] is None:
            messagebox.showerror("Error", "Select a record first.")
            return
        for i, e in enumerate(expenses):
            if e["id"] == loaded["id"]:
                if messagebox.askyesno("Confirm", f"Delete expense ID {e['id']}?"):
                    expenses.pop(i)
                    messagebox.showinfo("Deleted", "Expense deleted.")
                    dwin.destroy()
                return

    btn_delete = big_button(footer, "Delete", do_delete)
    btn_cancel = big_button(footer, "Cancel", dwin.destroy)
    btn_delete.pack(side=LEFT, padx=8)
    btn_cancel.pack(side=LEFT, padx=8)


# --------------------------
# Search Window
# --------------------------
def open_search_window():
    s_win = Toplevel(window)
    s_win.transient(window)
    s_win.grab_set()
    style_window(s_win, "Search Expenses")
    make_header(s_win, "Search Expenses")

    body = Frame(s_win, bg=BG, padx=12)
    body.pack(fill=BOTH, expand=True)

    Label(body, text="Date (YYYY-MM-DD) - optional:", fg=FG, bg=BG).pack(anchor="w")
    date_ent = Entry(body, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=FLAT)
    date_ent.pack(fill=X, pady=6)

    Label(body, text="Category - optional:", fg=FG, bg=BG).pack(anchor="w")
    category_cb = ttk.Combobox(body, values=CATEGORIES, state="readonly")
    category_cb.pack(fill=X, pady=6)
    category_cb.set("Select Category")

    btn_frame = Frame(body, bg=BG)
    btn_frame.pack(fill=X, pady=6)
    btn_search = big_button(btn_frame, "Search", lambda: perform_search())
    btn_search.pack(side=LEFT, padx=6)
    btn_loadall = big_button(btn_frame, "Load All", lambda: load_all())
    btn_loadall.pack(side=LEFT, padx=6)
    btn_cancel = big_button(btn_frame, "Cancel", s_win.destroy)
    btn_cancel.pack(side=LEFT, padx=6)

    table_frame = Frame(body, bg=BG)
    table_frame.pack(fill=BOTH, expand=True, pady=(8,12))

    cols = ("ID", "Category", "Amount", "Date")
    table = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
    for c in cols:
        table.heading(c, text=c)
        table.column(c, anchor="center", width=65)

    vsb = Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
    table.configure(yscrollcommand=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)
    table.pack(side=LEFT, fill=BOTH, expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background=TABLE_BG, foreground=TABLE_FG, fieldbackground=TABLE_BG, rowheight=28)
    style.map("Treeview", background=[("selected", TABLE_SEL)])

    def clear_table():
        for r in table.get_children():
            table.delete(r)

    def load_all():
        clear_table()
        for e in sorted(expenses, key=lambda x: (-int(x["id"]))):
            table.insert("", END, values=(e["id"], e["category"], e["amount"], e["date"]))

    def perform_search():
        date_str = date_ent.get().strip()
        category = category_cb.get()
        results = expenses
        if date_str:
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                results = [e for e in results if e["date"] == date_str]
            except:
                messagebox.showerror("Invalid Date", "Date must be YYYY-MM-DD.")
                return
        if category != "Select Category":
            results = [e for e in results if e["category"] == category]
        clear_table()
        for e in sorted(results, key=lambda x: (-int(x["id"]))):
            table.insert("", END, values=(e["id"], e["category"], e["amount"], e["date"]))
        if not results:
            messagebox.showinfo("No results", "No expenses found.")

    load_all()

# --------------------------
# Main App
# --------------------------
window = Tk()
style_window(window, "Expense Tracker")
make_header(window, "EXPENSE TRACKER")

main_card = Frame(window, bg=CARD_BG, padx=12, pady=12)
main_card.pack(fill=BOTH, padx=16, pady=(8,12))

Label(main_card, text="Manage your expenses", fg=FG, bg=CARD_BG, font=("Helvetica", 12)).pack(pady=(4,12))

btn_add = big_button(main_card, "Add Expense", open_add_window)
btn_update = big_button(main_card, "Update Expense", open_update_window)
btn_delete = big_button(main_card, "Delete Expense", open_delete_window)
btn_search = big_button(main_card, "Search Expenses", open_search_window)

btn_add.pack(fill=X, pady=8)
btn_update.pack(fill=X, pady=8)
btn_delete.pack(fill=X, pady=8)
btn_search.pack(fill=X, pady=8)

window.mainloop()
