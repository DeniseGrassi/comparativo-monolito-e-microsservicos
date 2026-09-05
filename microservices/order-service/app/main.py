from fastapi import FastAPI

from app.database import Base, engine
from app.routes.orders import router as orders_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Order Service",
    version="1.0.0"
)


app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "service": "order-service",
        "status": "ok"
    }