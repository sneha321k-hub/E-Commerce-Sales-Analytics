import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base
from routers import auth, sales, products, customers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(sales.router, prefix="/analytics/sales", tags=["sales"])
app.include_router(products.router, prefix="/analytics/products", tags=["products"])
app.include_router(customers.router, prefix="/analytics/customers", tags=["customers"])


@app.get("/health")
def health():
    return {"status": "ok"}
