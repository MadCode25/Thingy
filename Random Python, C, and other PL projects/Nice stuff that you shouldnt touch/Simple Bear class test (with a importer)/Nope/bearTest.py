# Bear Class Practice Python
# 1/9/2026

bears = []

class bear:
    def __init__(self, type, age, name):
        self.type = type
        self.age = age
        self.name = name

    def get_type(self):
        """
        Gets the type of the bear
        
        :return: The type of the bear
        """
        return self.type

    def setAge(self, newAge):
        """
        setAge method to set a new age for the bear
        What these variables mean: \n
        :self: Argument used to represent the instance of the class
        :newAge: New age to set for the bear \n
        After this, the bear's age will be updated to newAge, and returned to any caller of the method.
        """
        if self not in bears:  # Check if the bear instance is in the list, not just the name
            raise ValueError("Bear not found in bears list, perhaps you meant to create a new bear using newBear() method?")
        if newAge < 0:
            raise ValueError("Age cannot be negative")
        self.age = newAge
        return newAge
    
    def getInfo(self, name):
        """
        getInfo method to retrieve information about the bear
        What these variables mean: \n
        :self: Argument used to represent the instance of the class \n
        After this, a string containing the bear's name, type, and age will be returned.
        """
        if self.name in bears:  # Fixed: Simplified to check if this bear instance is in the list
            return f"Name: {self.name}, Type: {self.type}, Age: {self.age}"
        else:
            return "Bear not found in the bears list."

    @classmethod
    def newBear(cls, name, age, bear_type):  # Renamed 'type' to 'bear_type' to avoid shadowing built-in
        """
        newBear class method to create a new bear and add it to the bears list
        What these variables mean: \n
        :name: Name of the new bear
        :age: Age of the new bear
        :bear_type: Type of the new bear \n
        After this, a new bear will be created and added to the bears list.
        """
        new_bear = cls(bear_type, age, name)
        bears.append(new_bear)
        print(f"New bear named {name}, type {bear_type} and age of {age} is created and added to bears list.")
        return new_bear
