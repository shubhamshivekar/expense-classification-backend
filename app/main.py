from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import transactions, categories, users


app = FastAPI(
    title="Expense Classification API",
    description="Fintech Expense Classification & Reporting Tool",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ================= ROUTERS =================

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["Transactions"]
)

app.include_router(
    categories.router,
    prefix="/categories",
    tags=["Categories"]
)

# ================= HEALTH CHECK =================

@app.get("/")
def health_check():
    return {"status": "Expense Classification API is running"}