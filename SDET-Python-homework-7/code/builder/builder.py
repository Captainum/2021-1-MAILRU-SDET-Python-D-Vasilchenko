import faker

fake = faker.Faker()

class Builder:
    @staticmethod
    def random_person():
        person = fake.name().split()
        return person[0], person[1]