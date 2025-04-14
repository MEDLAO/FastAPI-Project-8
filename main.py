import os
from fastapi import FastAPI, Query, Request
from faker.config import AVAILABLE_LOCALES
from fastapi.responses import JSONResponse
from faker import Faker


app = FastAPI()


RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


@app.middleware("http")
async def enforce_rapidapi_usage(request: Request, call_next):
    # Allow "/" and "/health" to work without the header
    if request.url.path in ["/", "/health"]:
        return await call_next(request)

    rapidapi_proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

    if rapidapi_proxy_secret != RAPIDAPI_SECRET:
        return JSONResponse(status_code=403, content={"error": "Access restricted to RapidAPI users only."})

    return await call_next(request)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def read_root():
    welcome_message = (
        "Welcome!"
        "¡Bienvenido!"
        "欢迎!"
        "नमस्ते!"
        "مرحبًا!"
        "Olá!"
        "Здравствуйте!"
        "Bonjour!"
        "বাংলা!"
        "こんにちは!"
    )
    return {"message": welcome_message}


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
