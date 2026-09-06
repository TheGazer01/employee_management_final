class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
 
    def calculate_area(self):
        area = self.length * self.width
        return area
 
rectangle1 = Rectangle(10, 5)
result = rectangle1.calculate_area()
 
print("Length:", rectangle1.length)
print("Width:", rectangle1.width)
print("Area:", result)