class InvalidAgeError(Exception):
    pass


class InvalidEmployeeIDError(Exception):
    pass


class Person:
    company_name = "ADEi Solutions, Inc."

    def __init__(self, name, age):
        if not isinstance(age, int) or age <= 0 or age > 120:
            raise InvalidAgeError("Age must be a whole number between 1 and 120.")
        self.name = name
        self.age = age

    def get_details(self):
        return f"Name: {self.name}, Age: {self.age}, Company: {Person.company_name}"

    def display_info(self):
        return self.get_details()

    def update_info(self, name=None, age=None):
        if name:
            self.name = name
        if age is not None:
            if not isinstance(age, int) or age <= 0 or age > 120:
                raise InvalidAgeError("Age must be a whole number between 1 and 120.")
            self.age = age


class Employee(Person):
    def __init__(self, name, age, employee_id, department, position):
        super().__init__(name, age)
        if not employee_id or not str(employee_id).strip():
            raise InvalidEmployeeIDError("Employee ID cannot be empty.")
        self.employee_id = str(employee_id).strip()
        self.department = department
        self.position = position

    def get_details(self):
        base = super().get_details()
        return f"{base}, ID: {self.employee_id}, Department: {self.department}, Position: {self.position}"

    def display_info(self):
        return self.get_details()

    def to_row(self):
        # used for the tabulate table in the terminal
        return [self.name, self.age, self.employee_id, self.department, self.position]

    def update_info(self, name=None, age=None, department=None, position=None, employee_id=None):
        super().update_info(name=name, age=age)
        if employee_id is not None:
            if not str(employee_id).strip():
                raise InvalidEmployeeIDError("Employee ID cannot be empty.")
            self.employee_id = str(employee_id).strip()
        if department:
            self.department = department
        if position:
            self.position = position
