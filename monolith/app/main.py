from fastapi import FastAPI

from app.database import Base, engine
from app.routes.products import router as products_router
from app.routes.customers import router as customers_router
from app.routes.orders import router as orders_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TCC - Sistema Monolítico de Pedidos",
    version="1.0.0"
)


app.include_router(products_router)
app.include_router(customers_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "architecture": "monolith",
        "message": "API monolítica em execução"
    }