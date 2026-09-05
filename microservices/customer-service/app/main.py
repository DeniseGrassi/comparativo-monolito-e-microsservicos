from fastapi import FastAPI

from app.database import Base, engine
from app.routes.customers import router as customers_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Customer Service",
    version="1.0.0"
)


app.include_router(customers_router)


@app.get("/")
def root():
    return {
        "service": "customer-service",
        "status": "ok"
    }