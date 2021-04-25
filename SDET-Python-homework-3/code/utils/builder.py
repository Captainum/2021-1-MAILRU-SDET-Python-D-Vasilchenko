import faker

fake = faker.Faker()

class Builder:
    @staticmethod
    def random_title(length=5):
        title = fake.lexify(text='?'*length)
        return title