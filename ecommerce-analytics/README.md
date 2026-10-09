# E-Commerce Sales Analytics Dashboard

A full-stack analytics dashboard with a FastAPI backend and a React + TypeScript frontend.

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, SQLAlchemy, SQLite |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React 18, TypeScript, Vite, Recharts, Tailwind CSS v4 |
| State | Zustand (auth token) |
| HTTP | Axios (proxied via Vite) |

## Quick Start

### Terminal 1 — Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Seed the database (drops + recreates tables, ~200 customers / 50 products / 1 200 orders)
python seed.py

# Start the API server
uvicorn main:app --reload
```

Backend runs on **http://localhost:8000**  
Interactive API docs: **http://localhost:8000/docs**

### Terminal 2 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on **http://localhost:5173**

### Login

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |

## Dashboard Modules

| Page | Route | Description |
|---|---|---|
| Sales Overview | `/sales` | Revenue KPIs, trend line, channel bar chart, order-status donut |
| Product Analytics | `/products` | Top-10 products, category revenue donut, return-rate table |
| Customer Analytics | `/customers` | Customer KPIs, new-vs-returning chart, top customers & country tables |

## API Endpoints

All analytics endpoints require `Authorization: Bearer <token>` (obtain via `POST /auth/login`).

| Method | Path | Description |
|---|---|---|
| POST | `/auth/login` | Returns JWT token |
| GET | `/analytics/sales/kpis` | Total revenue, orders, AOV, customers |
| GET | `/analytics/sales/trend?days=N` | Daily revenue/order trend (default 30 days) |
| GET | `/analytics/sales/by-channel` | Revenue by channel (web / mobile / marketplace) |
| GET | `/analytics/sales/order-status` | Order count per status |
| GET | `/analytics/products/top` | Top 10 products by revenue |
| GET | `/analytics/products/by-category` | Revenue by product category |
| GET | `/analytics/products/return-rate` | Top 10 most-returned products |
| GET | `/analytics/customers/summary` | Total / new this month / returning counts |
| GET | `/analytics/customers/top` | Top 10 customers by spend |
| GET | `/analytics/customers/by-country` | Customer count and revenue by country |
| GET | `/analytics/customers/new-vs-returning` | Monthly new vs returning (last 6 months) |

## Project Structure

```
ecommerce-analytics/
├── backend/
│   ├── main.py          # FastAPI app, CORS, router registration
│   ├── database.py      # SQLAlchemy engine + session factory
│   ├── models.py        # ORM: Customer, Product, Order, OrderItem
│   ├── schemas.py       # Pydantic response models
│   ├── seed.py          # Mock-data seeder
│   └── routers/
│       ├── auth.py      # POST /auth/login + get_current_user dependency
│       ├── sales.py     # /analytics/sales/*
│       ├── products.py  # /analytics/products/*
│       └── customers.py # /analytics/customers/*
└── frontend/
    └── src/
        ├── api/         # Axios client + typed fetch functions
        ├── components/  # KpiCard, AppShell, ProtectedRoute
        ├── pages/       # LoginPage, SalesOverviewPage, ProductAnalyticsPage, CustomerAnalyticsPage
        ├── store/       # Zustand auth store
        └── types/       # Shared TypeScript interfaces
```
