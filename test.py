class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def sleep(self):
        print(f"{self.name} is sleeping. zzzzz.......")  


class GuardDog(Dog):
    def __init__(self, name, breed):
        super().__init__(name, breed, age=5)

    def rrrrr(self):
        print("Grrrrr!")

class Puppy(Dog):
    def __init__(self, name, breed):
        super().__init__(name, breed, age=0.1)

    def woof_woof(self):
        print("Woof! Woof!")


ruffus = Puppy(name="Ruffus", breed="Golden Retriever")
bibi = GuardDog(name="Bibi", breed="Poodle")

ruffus.woof_woof()
bibi.rrrrr()

ruffus.sleep()
bibi.sleep()