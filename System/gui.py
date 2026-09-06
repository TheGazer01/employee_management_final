import tkinter as tk
from tkinter import ttk, messagebox

from System.models import Person, Employee, InvalidAgeError, InvalidEmployeeIDError
from System.console_log import (
    show_banner, show_loading_bar, log_success, log_error, log_info, log_employee_table,
)


class SplashScreen(tk.Toplevel):
    def __init__(self, root, on_done):
        super().__init__(root)
        self.on_done = on_done

        self.title("Loading...")
        self.geometry("320x120")
        self.resizable(False, False)
        self.configure(bg="#f4f6f8")

        tk.Label(self, text="Employee Management System", font=("Segoe UI", 12, "bold"),
                 bg="#f4f6f8").pack(pady=(15, 5))
        tk.Label(self, text="Loading, please wait...", bg="#f4f6f8").pack()

        self.progress = ttk.Progressbar(self, orient="horizontal", length=260, mode="determinate")
        self.progress.pack(pady=15)

        self.value = 0
        self.after(30, self.step)

    def step(self):
        self.value += 2
        self.progress["value"] = self.value
        if self.value < 100:
            self.after(30, self.step)
        else:
            self.destroy()
            self.on_done()


class EmployeeManagementApp:
    BG_COLOR = "#f4f6f8"
    PRIMARY = "#2c3e50"
    ACCENT = "#3498db"
    SUCCESS = "#27ae60"
    DANGER = "#e74c3c"
    NEUTRAL = "#95a5a6"
    TEXT_COLOR = "#2c3e50"

    FONT_NORMAL = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_HEADER = ("Segoe UI", 11, "bold")

    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("950x550")
        self.root.configure(bg=self.BG_COLOR)
        self.root.withdraw()

        self.employees = []
        self.selected_id = None

        show_banner()
        show_loading_bar()

        SplashScreen(self.root, on_done=self.start_app)

    def start_app(self):
        self.root.deiconify()

        self.build_header()
        self.build_form()
        self.build_table()
        self.build_search()
        self.load_sample_employees()

    def build_header(self):
        header = tk.Label(self.root, text=f"🏢 {Employee.company_name}",
                           bg=self.PRIMARY, fg="white", font=("Segoe UI", 14, "bold"),
                           anchor="center")
        header.place(x=0, y=0, width=950, height=40)

    def load_sample_employees(self):
        self.employees.append(Employee("Maria Santos", 28, "E001", "IT", "Software Developer"))
        self.employees.append(Employee("Juan Dela Cruz", 34, "E002", "HR", "Recruiter"))
        self.refresh_table()

    def build_form(self):
        form_frame = tk.LabelFrame(self.root, text="Employee Details", padx=10, pady=10,
                                    bg=self.BG_COLOR, fg=self.PRIMARY, font=self.FONT_HEADER)
        form_frame.place(x=10, y=50, width=280, height=300)

        labels = ["Name", "Age", "Employee ID", "Department", "Position"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", bg=self.BG_COLOR, fg=self.TEXT_COLOR,
                     font=self.FONT_NORMAL).grid(row=i, column=0, sticky="w", pady=6)
            entry = tk.Entry(form_frame, width=22, font=self.FONT_NORMAL, relief="solid", bd=1)
            entry.grid(row=i, column=1, pady=6)
            self.entries[label] = entry

        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.place(x=10, y=360, width=280, height=140)

        tk.Button(button_frame, text="➕ Add Employee", width=22, bg=self.SUCCESS, fg="white",
                  font=self.FONT_BOLD, relief="flat", command=self.add_employee).grid(row=0, column=0, pady=4)
        tk.Button(button_frame, text="✏️ Update Employee", width=22, bg=self.ACCENT, fg="white",
                  font=self.FONT_BOLD, relief="flat", command=self.update_employee).grid(row=1, column=0, pady=4)
        tk.Button(button_frame, text="🗑️ Delete Employee", width=22, bg=self.DANGER, fg="white",
                  font=self.FONT_BOLD, relief="flat", command=self.delete_employee).grid(row=2, column=0, pady=4)
        tk.Button(button_frame, text="🧹 Clear Fields", width=22, bg=self.NEUTRAL, fg="white",
                  font=self.FONT_BOLD, relief="flat", command=self.clear_fields).grid(row=3, column=0, pady=4)

    def build_table(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground=self.TEXT_COLOR,
                         rowheight=26, fieldbackground="white", font=self.FONT_NORMAL)
        style.configure("Treeview.Heading", background=self.PRIMARY, foreground="white",
                         font=self.FONT_BOLD)
        style.map("Treeview", background=[("selected", self.ACCENT)])

        table_frame = tk.LabelFrame(self.root, text="Employees", padx=5, pady=5,
                                     bg=self.BG_COLOR, fg=self.PRIMARY, font=self.FONT_HEADER)
        table_frame.place(x=300, y=50, width=630, height=460)

        columns = ("name", "age", "id", "department", "position")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col, text, width in [
            ("name", "Name", 120),
            ("age", "Age", 50),
            ("id", "Employee ID", 100),
            ("department", "Department", 120),
            ("position", "Position", 120),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#eef2f5")

    def build_search(self):
        search_frame = tk.LabelFrame(self.root, text="Search", padx=10, pady=10,
                                      bg=self.BG_COLOR, fg=self.PRIMARY, font=self.FONT_HEADER)
        search_frame.place(x=10, y=460, width=280, height=60)

        self.search_entry = tk.Entry(search_frame, width=20, font=self.FONT_NORMAL, relief="solid", bd=1)
        self.search_entry.grid(row=0, column=0, padx=4)
        tk.Button(search_frame, text="🔍 Search", bg=self.ACCENT, fg="white", relief="flat",
                  font=self.FONT_BOLD, command=self.search_employee).grid(row=0, column=1, padx=4)
        tk.Button(search_frame, text="📋 Show All", bg=self.NEUTRAL, fg="white", relief="flat",
                  font=self.FONT_BOLD, command=self.refresh_table).grid(row=0, column=2, padx=4)

    def get_form_values(self):
        return {
            "name": self.entries["Name"].get().strip(),
            "age": self.entries["Age"].get().strip(),
            "employee_id": self.entries["Employee ID"].get().strip(),
            "department": self.entries["Department"].get().strip(),
            "position": self.entries["Position"].get().strip(),
        }

    def validate_common(self, values):
        if not values["name"] or not values["employee_id"] or not values["department"] or not values["position"]:
            raise ValueError("All fields must be filled in.")
        try:
            age = int(values["age"])
        except ValueError:
            raise ValueError("Age must be a whole number, e.g. 30.")
        return age

    def add_employee(self):
        values = self.get_form_values()
        try:
            age = self.validate_common(values)
            if any(e.employee_id == values["employee_id"] for e in self.employees):
                raise ValueError("An employee with this ID already exists.")
            emp = Employee(values["name"], age, values["employee_id"], values["department"], values["position"])
            self.employees.append(emp)
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", "Employee added successfully.")
            log_success(f"Employee '{emp.name}' added.")
        except InvalidAgeError as e:
            messagebox.showerror("Invalid Age", str(e))
            log_error(str(e))
        except InvalidEmployeeIDError as e:
            messagebox.showerror("Invalid Employee ID", str(e))
            log_error(str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            log_error(str(e))

    def update_employee(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a row in the table first.")
            return
        values = self.get_form_values()
        try:
            age = self.validate_common(values)

            new_id = values["employee_id"]
            if new_id != self.selected_id and any(e.employee_id == new_id for e in self.employees):
                raise ValueError("Another employee already uses that ID.")

            emp = next(e for e in self.employees if e.employee_id == self.selected_id)
            emp.update_info(name=values["name"], age=age, department=values["department"],
                             position=values["position"], employee_id=new_id)
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", "Employee updated successfully.")
            log_success(f"Employee '{emp.name}' updated.")
        except InvalidAgeError as e:
            messagebox.showerror("Invalid Age", str(e))
            log_error(str(e))
        except InvalidEmployeeIDError as e:
            messagebox.showerror("Invalid Employee ID", str(e))
            log_error(str(e))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            log_error(str(e))

    def delete_employee(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a row in the table first.")
            return
        if messagebox.askyesno("Confirm Delete", "Delete the selected employee?"):
            self.employees = [e for e in self.employees if e.employee_id != self.selected_id]
            self.refresh_table()
            self.clear_fields()
            log_success("Employee deleted.")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_id = None

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, emp in enumerate(self.employees):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(emp.name, emp.age, emp.employee_id,
                                                  emp.department, emp.position), tags=(tag,))
        log_info("Employee list (also shown in the GUI table):")
        log_employee_table(self.employees)

    def on_row_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0])["values"]
        name, age, employee_id, department, position = values
        self.selected_id = str(employee_id)
        self.entries["Name"].delete(0, tk.END)
        self.entries["Name"].insert(0, name)
        self.entries["Age"].delete(0, tk.END)
        self.entries["Age"].insert(0, age)
        self.entries["Employee ID"].delete(0, tk.END)
        self.entries["Employee ID"].insert(0, employee_id)
        self.entries["Department"].delete(0, tk.END)
        self.entries["Department"].insert(0, department)
        self.entries["Position"].delete(0, tk.END)
        self.entries["Position"].insert(0, position)

    def search_employee(self):
        term = self.search_entry.get().strip().lower()
        if not term:
            self.refresh_table()
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        matches = []
        for i, emp in enumerate(self.employees):
            if term in emp.name.lower() or term in emp.employee_id.lower():
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values=(emp.name, emp.age, emp.employee_id,
                                                      emp.department, emp.position), tags=(tag,))
                matches.append(emp)
        log_info(f"Search results for '{term}':")
        log_employee_table(matches)