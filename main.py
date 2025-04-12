from fastapi import FastAPI, Query
from faker import Faker


app = FastAPI()


@app.get("/generate")
def generate_identity(locale: str = Query(default="en_US")):
    Faker.seed(0)
    fake = Faker(locale)

    return {
        "name": fake.name(),
        "gender": fake.random_element(elements=["Male", "Female", "Non-binary"]),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat(),
        "job": fake.job(),
        "company": fake.company(),
        "ssn": fake.ssn(),
        "address": {
            "street_address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country(),
            "country_code": fake.country_code(),
            "latitude": fake.latitude(),
            "longitude": fake.longitude()
        },
    }
