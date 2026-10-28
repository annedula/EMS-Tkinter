import tkinter as tk
import requests
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Employee Management System")
root.geometry("800x600")
root.configure(bg="lightblue")

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

title = tk.Label(root, text="Employee Management System", font=("Helvetica", 22, "bold"), bg="lightblue")
title.grid(row=0, column=0, pady=15, sticky="w", padx=20)

main_frame = tk.Frame(root, bg="lightblue")
main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(3, weight=1)

tk.Label(main_frame, text="Employee Name:", font=("Helvetica", 14), bg="lightblue").grid(row=0, column=0, pady=8, sticky="w")
name_entry = tk.Entry(main_frame, font=("Helvetica", 14))
name_entry.grid(row=0, column=1, pady=8, sticky="ew", padx=(10, 0))

tk.Label(main_frame, text="Position:", font=("Helvetica", 14), bg="lightblue").grid(row=1, column=0, pady=8, sticky="w")
position_entry = tk.Entry(main_frame, font=("Helvetica", 14))
position_entry.grid(row=1, column=1, pady=8, sticky="ew", padx=(10, 0))

def clear_fields():
    name_entry.delete(0, tk.END)
    position_entry.delete(0, tk.END)

def add_employee():
    name = name_entry.get().strip()
    position = position_entry.get().strip()

    if not name or not position:
        messagebox.showwarning("Missing Input", "Please fill in all fields.")
        return

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/employees/",
            json={"name": name, "position": position},
            timeout=5
        )

        if response.status_code == 201:
            messagebox.showinfo("Success", "Employee added successfully.")
            clear_fields()
            refresh_list()
        else:
            messagebox.showerror("Error", response.text)

    except requests.RequestException as e:
        messagebox.showerror("Connection Error", str(e))
        

def delete_employee():
    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning("No Selection", "Please select an employee to delete.")
        return

    employee = employee_table.item(selected[0], "values")
    employee_id = employee[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {employee[1]}?"
    )

    if not confirm:
        return

    try:
        response = requests.delete(
            f"http://127.0.0.1:8000/api/employees/{employee_id}/",
            timeout=5
        )

        if response.status_code == 204:
            messagebox.showinfo("Success", "Employee deleted successfully.")
            refresh_list()
        else:
            messagebox.showerror("Error", response.text)

    except requests.RequestException as e:
        messagebox.showerror("Connection Error", str(e))



def refresh_list():
    try:
        response = requests.get(
            "http://127.0.0.1:8000/api/employees/",
            timeout=5
        )
        response.raise_for_status()
        employees = response.json()

        for item in employee_table.get_children():
            employee_table.delete(item)

        for employee in employees:
            employee_table.insert("", tk.END, values=(
                employee.get("id", ""),
                employee.get("name", ""),
                employee.get("position", ""),
                employee.get("date_hired", "")
            ))

    except requests.RequestException as e:
        messagebox.showerror("Connection Error", str(e))
    except ValueError:
        messagebox.showerror("API Error", "Invalid response from the API.")


buttons = tk.Frame(main_frame, bg="lightblue")
buttons.grid(row=2, column=0, columnspan=2, sticky="w", pady=15)

tk.Button(buttons, text="Add Employee", font=("Helvetica", 12, "bold"), padx=15, pady=8, command=add_employee).grid(row=0, column=0, padx=(0, 10))
tk.Button(buttons, text="Refresh List", font=("Helvetica", 12), padx=15, pady=8, command=refresh_list).grid(row=0, column=1, padx=10)
tk.Button(buttons, text="Clear Fields", font=("Helvetica", 12), padx=15, pady=8, command=clear_fields).grid(row=0, column=2, padx=10)
tk.Button(buttons, text="Delete Employee", font=("Helvetica", 12), padx=15, pady=8, command=delete_employee).grid(row=0, column=3, padx=10)

style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), rowheight=28)
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

columns = ("ID", "Name", "Position", "Date Hired")
employee_table = ttk.Treeview(main_frame, columns=columns, show="headings")

for column in columns:
    employee_table.heading(column, text=column)

employee_table.column("ID", width=80, stretch=False)
employee_table.column("Name", width=200, stretch=True)
employee_table.column("Position", width=200, stretch=True)
employee_table.column("Date Hired", width=200, stretch=True)

employee_table.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

root.mainloop()
