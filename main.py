from fastapi import FastAPI, Query
from faker.config import AVAILABLE_LOCALES
from faker import Faker


app = FastAPI()


@app.get("/locales")
def get_locales():
    return {"available_locales": AVAILABLE_LOCALES}


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
            "zip_code": fake.postcode(),
            "country": fake.country(),
        },
    }
