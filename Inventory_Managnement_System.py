import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",      # Replace with your MySQL username
        password="Jeet@1007",  # Replace with your MySQL password
        database="inventory_management"  # Replace with your MySQL database name
    )
    if conn.is_connected():
        print("Connected to MySQL database")
    c = conn.cursor()
except Error as e:
    print("Error while connecting to MySQL:", e)

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS inventory (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              quantity INT NOT NULL,
              price DECIMAL(10, 2) NOT NULL,
              date_added DATE NOT NULL,
              time_added TIME NOT NULL
            )''')

# Function to add item to the inventory
def add_item():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    date_added = date_entry.get()
    time_added = time_entry.get()

    try:
        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            date_obj = datetime.strptime(date_added, "%d-%m-%Y").date()
            time_obj = datetime.strptime(time_added, "%H:%M:%S").time()
            c.execute("INSERT INTO inventory (name, quantity, price, date_added, time_added) VALUES (%s, %s, %s, %s, %s)", 
                      (name, int(quantity), float(price), date_obj, time_obj))
            conn.commit()
            messagebox.showinfo("Success", f"Added {name} to inventory.")
            clear_entries()
            view_inventory()
        else:
            messagebox.showerror("Error", "Please enter valid data.")
    except ValueError:
        messagebox.showerror("Error", "Please enter date in 'DD-MM-YYYY' and time in 'HH:MM:SS' format.")

# Function to update item quantity
def update_item():
    item_id = id_entry.get()
    new_quantity = quantity_entry.get()

    if item_id.isdigit() and new_quantity.isdigit():
        c.execute("UPDATE inventory SET quantity = %s WHERE id = %s", (new_quantity, item_id))
        conn.commit()
        messagebox.showinfo("Success", f"Updated item with ID {item_id}.")
        clear_entries()
        view_inventory()
    else:
        messagebox.showerror("Error", "Please enter valid ID and quantity.")

# Function to delete item from inventory
def delete_item():
    item_id = id_entry.get()

    if item_id.isdigit():
        c.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        conn.commit()
        messagebox.showinfo("Success", f"Deleted item with ID {item_id}.")
        clear_entries()
        view_inventory()
    else:
        messagebox.showerror("Error", "Please enter a valid item ID.")

# Function to delete all items from inventory
def delete_all_items():
    c.execute("DELETE FROM inventory")
    conn.commit()
    messagebox.showinfo("Success", "All items have been deleted from inventory.")
    view_inventory()

# Function to view the inventory
def view_inventory():
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    inventory_list.delete(*inventory_list.get_children())
    for row in rows:
        inventory_list.insert("", "end", values=row)

# Function to search items by name or date
def search_item():
    search_term = search_entry.get()
    date_term = date_search_entry.get()

    if date_term:
        try:
            date_obj = datetime.strptime(date_term, "%d-%m-%Y").date()
            c.execute("SELECT * FROM inventory WHERE date_added = %s", (date_obj,))
        except ValueError:
            messagebox.showerror("Error", "Please enter date in 'DD-MM-YYYY' format.")
            return
    else:
        c.execute("SELECT * FROM inventory WHERE name LIKE %s", ('%' + search_term + '%',))

    rows = c.fetchall()
    inventory_list.delete(*inventory_list.get_children())
    for row in rows:
        inventory_list.insert("", "end", values=row)

# Clear entry fields
def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

# Main window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("750x600")

# Styling and frames
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10))
style.configure("TLabel", font=("Helvetica", 10))

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.pack(fill=tk.BOTH, expand=True)

# Item details frame
details_frame = ttk.LabelFrame(main_frame, text="Item Details", padding=(10, 10))
details_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Labels and Entry widgets for item details
ttk.Label(details_frame, text="ID:").grid(row=0, column=0, padx=10, pady=5)
id_entry = ttk.Entry(details_frame)
id_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(details_frame, text="Name:").grid(row=1, column=0, padx=10, pady=5)
name_entry = ttk.Entry(details_frame)
name_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(details_frame, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
quantity_entry = ttk.Entry(details_frame)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(details_frame, text="Price:").grid(row=3, column=0, padx=10, pady=5)
price_entry = ttk.Entry(details_frame)
price_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(details_frame, text="Date (DD-MM-YYYY):").grid(row=4, column=0, padx=10, pady=5)
date_entry = ttk.Entry(details_frame)
date_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(details_frame, text="Time (HH:MM:SS):").grid(row=5, column=0, padx=10, pady=5)
time_entry = ttk.Entry(details_frame)
time_entry.grid(row=5, column=1, padx=10, pady=5)

# Buttons for actions
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=1, column=0, pady=10)
ttk.Button(button_frame, text="Add Item", command=add_item).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Update Quantity", command=update_item).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Delete Item", command=delete_item).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Delete All", command=delete_all_items).grid(row=0, column=3, padx=5)

# Search frame
search_frame = ttk.Frame(main_frame)
search_frame.grid(row=2, column=0, pady=10)
ttk.Label(search_frame, text="Search by Name:").grid(row=0, column=0, padx=5)
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5)
ttk.Label(search_frame, text="Search by Date (DD-MM-YYYY):").grid(row=1, column=0, padx=5)
date_search_entry = ttk.Entry(search_frame)
date_search_entry.grid(row=1, column=1, padx=5)
ttk.Button(search_frame, text="Search", command=search_item).grid(row=2, column=1, padx=5)

# Treeview (enhanced Listbox) for inventory display
inventory_list = ttk.Treeview(main_frame, columns=("ID", "Name", "Quantity", "Price", "Date Added", "Time Added"), show="headings")
inventory_list.heading("ID", text="ID")
inventory_list.heading("Name", text="Name")
inventory_list.heading("Quantity", text="Quantity")
inventory_list.heading("Price", text="Price")
inventory_list.heading("Date Added", text="Date Added")
inventory_list.heading("Time Added", text="Time Added")
inventory_list.grid(row=3, column=0, pady=10)

# Add a scrollbar to the inventory list
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=inventory_list.yview)
inventory_list.configure(yscroll=scrollbar.set)
scrollbar.grid(row=3, column=1, sticky="ns")

# Button to view inventory
ttk.Button(main_frame, text="View Inventory", command=view_inventory).grid(row=4, column=0, pady=10)

# Run the application
root.mainloop()

