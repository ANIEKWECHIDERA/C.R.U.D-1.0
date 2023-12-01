import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Database connection details
server = ''
database = '' 
driver = 'ODBC Driver 17 for SQL Server'

# Establishing the database connection
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def create_customer(customer_name, gender, city, Country, telephone, address):
    try:
        # Check if all fields are filled
        if not all((customer_name, gender, city, Country, telephone, address)):
            raise ValueError("Please fill in all fields.")

        # Confirmation dialog
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to add the contact?")
        if not confirm:
            return

        # Create a new customer record
        cursor.execute(
            "INSERT INTO Customers (ContactName, Gender, City, Country, Telephone, Address) VALUES (?, ?, ?, ?, ?, ?)",
            customer_name, gender, city, Country, telephone, address)
        conn.commit()
        messagebox.showinfo("Success", "Customer created successfully.")
        read_last_five_customers()

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except pyodbc.DataError as de:
        field = str(de).split("[")[1].split("]")[0]  # Extracting the field name from the error message
        messagebox.showerror("Data Error", f"Invalid data in the {field} field.")
    except pyodbc.IntegrityError as ie:
        messagebox.showerror("Integrity Error", str(ie))
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred.")

def update_customer(customer_name, gender, address, city, Country, telephone, customer_id):
    try:
        # Check if at least one field is filled
        if not any((customer_name, gender, address, city, Country, telephone, customer_id)):
            raise ValueError("Please provide at least one field to update.")

        # Confirmation dialog
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to update the contact?")
        if not confirm:
            return

        # Update customer record
        cursor.execute(
            "UPDATE Customers SET ContactName=?, Gender=?, Address=?, City=?, Country=?, Telephone=?  WHERE CustomerID=?",
            customer_name, gender, address, city, Country, telephone, customer_id)
        conn.commit()
        messagebox.showinfo("Success", "Customer updated successfully.")
        read_last_five_customers()

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except pyodbc.Error as e:
        # Print the details of the SQL Server error
        print("SQL Server Error:", e)
        messagebox.showerror("Database Error", "An error occurred while interacting with the database. Check the console for details.")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred.")

def delete_customer(customer_id, customer_name):
    try:
        # Check if either Customer ID or Contact Name is provided
        if not (customer_id or customer_name):
            raise ValueError("Please provide Customer ID or Contact Name.")

        # Confirmation dialog
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the contact?")
        if not confirm:
            return

        # Delete customer record
        if customer_id:
            cursor.execute("DELETE FROM Customers WHERE CustomerID=?", customer_id)
        elif customer_name:
            cursor.execute("DELETE FROM Customers WHERE ContactName=?", customer_name)
        conn.commit()
        messagebox.showinfo("Success", "Customer deleted successfully.")
        read_last_five_customers()

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except pyodbc.DataError as de:
        field = str(de).split("[")[1].split("]")[0] 
        messagebox.showerror("Data Error", f"Invalid data in the {field} field.")
    except pyodbc.IntegrityError as ie:
        messagebox.showerror("Integrity Error", str(ie))
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred.")

def read_last_five_customers():
    try:
        # Read the last five customers
        cursor.execute("SELECT TOP 20 * FROM Customers ORDER BY CustomerID DESC")
        rows = cursor.fetchall()
        populate_table(rows)

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred.")

def populate_table(rows):
    # Clear existing data in the treeview
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data into the treeview
    for row in rows:
        # Modify each value to handle commas
        modified_row = ['"' + str(val) + '"' if isinstance(val, str) and ',' in val else val for val in row]
        tree.insert("", "end", values=modified_row)

# Function to handle double-click on a treeview item
def on_item_double_click(event):
    item = tree.selection()[0]
    values = tree.item(item, 'values')

    # Clean up the values by stripping leading and trailing whitespace
    cleaned_values = [str(val).strip('(),\'"') for val in values]

    current_tab = notebook.index(notebook.select())

    # Populate entry widgets based on the current tab
    if current_tab == 1:  # Update tab
        # Populate entry widgets in the Update tab with the cleaned data
        customer_id_entry_update.delete(0, tk.END)
        customer_id_entry_update.insert(0, cleaned_values[0])
        customer_name_entry_update.delete(0, tk.END)
        customer_name_entry_update.insert(0, cleaned_values[1])
        gender_entry_update.delete(0, tk.END)
        gender_entry_update.insert(0, cleaned_values[2])
        Address_entry_update.delete(0, tk.END)
        Address_entry_update.insert(0, cleaned_values[3])
        city_entry_update.delete(0, tk.END)
        city_entry_update.insert(0, cleaned_values[4])
        Country_entry_update.delete(0, tk.END)
        Country_entry_update.insert(0, cleaned_values[5])
        telephone_entry_update.delete(0, tk.END)
        telephone_entry_update.insert(0, cleaned_values[6])

    elif current_tab == 2:  # Delete tab
        # Populate entry widgets in the Delete tab with the cleaned data
        customer_id_entry_delete.delete(0, tk.END)
        customer_id_entry_delete.insert(0, cleaned_values[0])
        customer_name_entry_delete.delete(0, tk.END)
        customer_name_entry_delete.insert(0, cleaned_values[1])
    
def on_create():
    create_customer(customer_name_entry.get(), gender_entry.get(), city_entry.get(), Country_entry.get(),
                    telephone_entry.get(), Address_entry.get())
    
def load_first_fifty_records():
    try:
        # Read the first 50 records
        cursor.execute("SELECT TOP 50 * FROM Customers ORDER BY CustomerID")
        rows = cursor.fetchall()
        populate_table(rows)

    except pyodbc.Error as e:
        messagebox

def on_update():
    try:
        # Get selected item
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        customer_id = values[0]  # Assuming CustomerID is at index 0
        
        # Call update_customer with all required arguments
        update_customer(customer_name_entry_update.get(), gender_entry_update.get(), Address_entry_update.get(), city_entry_update.get(), Country_entry_update.get(), 
                        telephone_entry_update.get(),customer_id_entry_update.get())

    except IndexError:
        messagebox.showerror("Error", "Please select a contact to update.")
        
def on_delete():
    try:
        # Get selected items
        selected_items = tree.selection()

        # Check if any item is selected or manual input is provided
        if not selected_items and not (customer_id_entry_delete.get() or customer_name_entry_delete.get()):
            raise ValueError("Please select at least one contact or provide ID/Contact Name/Manual Input to delete.")

        # Confirmation dialog
        Warning = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected contact(s)??\nThis cannot be Undone!")
        if not Warning:
            return

        # Delete selected customer records or by ID/Contact Name/Manual Input
        for item in selected_items:
            values = tree.item(item, 'values')
            customer_id = values[0] 
            if customer_id:
                cursor.execute("DELETE FROM Customers WHERE CustomerID=?", customer_id)

        if customer_id_entry_delete.get():
            cursor.execute("DELETE FROM Customers WHERE CustomerID=?", customer_id_entry_delete.get())
        if customer_name_entry_delete.get():
            cursor.execute("DELETE FROM Customers WHERE ContactName=?", customer_name_entry_delete.get())

        conn.commit()
        messagebox.showinfo("Success", "Selected contact(s) deleted successfully.")
        read_last_five_customers()

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except pyodbc.DataError as de:
        field = str(de).split("[")[1].split("]")[0]
        messagebox.showerror("Data Error", f"Invalid data in the {field} field.")
    except pyodbc.IntegrityError as ie:
        messagebox.showerror("Integrity Error", str(ie))
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred.")
    

# GUI setup
root = tk.Tk()
root.title("C.R.U.D 1.0")
root.geometry("1500x760")

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, columnspan=2, padx=50, pady=50, sticky="w")

# Style to add more space between tabs
style = ttk.Style()
style.configure("TNotebook", padding=(10, 5))

# Create a Text widget for SQL queries
sql_query_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
sql_query_text.grid(row=0, column=1, rowspan=2, padx=50, pady=5, sticky="w")

# Create a button to execute the SQL query
def execute_sql_query():
    query = sql_query_text.get("1.0", tk.END)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        populate_table(rows)
        result_text.set("Query executed successfully.")
    except Exception as e:
        result_text.set(f"Error executing query: {str(e)}")

execute_button = tk.Button(root, text="Execute Query", command=execute_sql_query)
execute_button.grid(row=1, column=1, padx=220, pady=10, sticky="w")

# Tab for Add Contact
tab_add_contact = ttk.Frame(notebook)
notebook.add(tab_add_contact, text="Add Contact")

# Entry widgets for Add Contact
tk.Label(tab_add_contact, text="Contact Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
customer_name_entry = tk.Entry(tab_add_contact)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_add_contact, text="Gender:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
gender_values = ["M", "F"]
gender_entry = ttk.Combobox(tab_add_contact, values=gender_values)
gender_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_add_contact, text="Address:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
Address_entry = tk.Entry(tab_add_contact)
Address_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab_add_contact, text="City:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
city_entry = tk.Entry(tab_add_contact)
city_entry.grid(row=3, column=1, padx=5, pady=5)
3
tk.Label(tab_add_contact, text="Country:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
Country_entry = tk.Entry(tab_add_contact)
Country_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(tab_add_contact, text="Telephone:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
telephone_entry = tk.Entry(tab_add_contact)
telephone_entry.grid(row=5, column=1, padx=5, pady=5)

# Buttons for Add Contact
tk.Button(tab_add_contact, text="Create Contact", command=on_create).grid(row=6, column=0, columnspan=2, pady=10)

# Button for Preview
tk.Button(tab_add_contact, text="Preview First 50 Records", command=load_first_fifty_records).grid(row=7, column=0, columnspan=2, pady=10)

# Tab for Update Contact
tab_update_contact = ttk.Frame(notebook)
notebook.add(tab_update_contact, text="Update Contact")

# Entry widgets for Update Contact
tk.Label(tab_update_contact, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
customer_id_entry_update = tk.Entry(tab_update_contact)
customer_id_entry_update.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_update_contact, text="Contact Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
customer_name_entry_update = tk.Entry(tab_update_contact)
customer_name_entry_update.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_update_contact, text="Gender:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
gender_entry_update = tk.Entry(tab_update_contact)
gender_entry_update.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab_update_contact, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
Address_entry_update = tk.Entry(tab_update_contact)
Address_entry_update.grid(row=3, column=1, padx=5, pady=5)

tk.Label(tab_update_contact, text="City:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
city_entry_update = tk.Entry(tab_update_contact)
city_entry_update.grid(row=4, column=1, padx=5, pady=5)

tk.Label(tab_update_contact, text="Country:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
Country_entry_update = tk.Entry(tab_update_contact)
Country_entry_update.grid(row=5, column=1, padx=5, pady=5)

tk.Label(tab_update_contact, text="Telephone:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
telephone_entry_update = tk.Entry(tab_update_contact)
telephone_entry_update.grid(row=6, column=1, padx=5, pady=5)

# Buttons for Update Contact
tk.Button(tab_update_contact, text="Update Contact", command=on_update).grid(row=7, column=0, columnspan=2, pady=10)

# Button for Preview
tk.Button(tab_update_contact, text="Preview First 50 Records", command=load_first_fifty_records).grid(row=8, column=0, columnspan=2, pady=10)

tab_delete_contact = ttk.Frame(notebook)
notebook.add(tab_delete_contact, text="Delete Contact")

# Entry widgets for Delete Contact
tk.Label(tab_delete_contact, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
customer_id_entry_delete = tk.Entry(tab_delete_contact)
customer_id_entry_delete.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_delete_contact, text="Contact Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
customer_name_entry_delete = tk.Entry(tab_delete_contact)
customer_name_entry_delete.grid(row=1, column=1, padx=5, pady=5)

# Buttons for Delete Contact
tk.Button(tab_delete_contact, text="Delete Contact", command=on_delete).grid(row=3, column=0, columnspan=2, pady=10)

# Button for Preview
tk.Button(tab_delete_contact, text="Preview First 50 Records", command=load_first_fifty_records).grid(row=4, column=0, columnspan=2, pady=10)

# Treeview for displaying results in a table
columns = ("ID", "Contact Name", "Gender", "Address", "City","Country", "Telephone")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=8, column=0, columnspan=2, padx=50, pady=5, sticky="w")

# Set column headings
for col in columns:
    tree.heading(col, text=col)

# Result display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="w")

# Treeview for displaying results in a table
columns = ("ID", "Contact Name", "Gender", "Address", "City","Country", "Telephone")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=8, column=0, columnspan=2, padx=50, pady=5, sticky="w")

# Set column headings
for col in columns:
    tree.heading(col, text=col)

# Populate table with the first 100 contacts
cursor.execute("SELECT TOP 100 * FROM Customers ORDER BY CustomerID DESC")
rows = cursor.fetchall()
populate_table(rows)

# Bind double-click event to the treeview
tree.bind("<Double-1>", on_item_double_click)

# Run the GUI
root.mainloop()

# Close the connection
conn.close()