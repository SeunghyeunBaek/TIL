class Person:
    population = 0

    def __init__(self,name):
        self.name = name
        Person.population = Person.population+1


p1 = Person('a')
print(p1.population)
