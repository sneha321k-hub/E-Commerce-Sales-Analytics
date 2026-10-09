# E-Commerce Sales Analytics Dashboard

A full-stack analytics dashboard for e-commerce data — built with **FastAPI** on the backend and **React + TypeScript** on the frontend.

![GitHub repo](https://img.shields.io/badge/repo-E--Commerce--Sales--Analytics-blue?logo=github)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)

---

## Overview

This project provides a secure, locally-runnable analytics dashboard that visualises key e-commerce metrics across three modules:

| Module | What it shows |
|---|---|
| **Sales Overview** | Revenue KPIs, daily trend line, channel breakdown, order-status donut |
| **Product Analytics** | Top-10 products by revenue, category share, return-rate table |
| **Customer Analytics** | New vs returning trend, top customers by spend, revenue by country |

All data is powered by a seeded SQLite database with **200 customers**, **50 products**, and **1,200 orders** spanning 12 months across multiple geographies and sales channels.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy, SQLite |
| **Authentication** | JWT (`python-jose`), bcrypt (`passlib`) |
| **Frontend** | React 18, TypeScript, Vite |
| **Charts** | Recharts |
| **Styling** | Tailwind CSS v4 |
| **State** | Zustand (auth token) |
| **HTTP Client** | Axios (proxied via Vite) |

---

## Project Structure

```
ecommerce-analytics/
├── backend/
│   ├── main.py           # FastAPI app, CORS, router registration
│   ├── database.py       # SQLAlchemy engine + session factory
│   ├── models.py         # ORM: Customer, Product, Order, OrderItem
│   ├── schemas.py        # Pydantic response models
│   ├── seed.py           # Mock-data seeder (run once)
│   ├── env.example       # Environment variable template
│   ├── requirements.txt
│   └── routers/
│       ├── auth.py       # POST /auth/login + JWT dependency
│       ├── sales.py      # /analytics/sales/*
│       ├── products.py   # /analytics/products/*
│       └── customers.py  # /analytics/customers/*
└── frontend/
    └── src/
        ├── api/          # Axios client + typed fetch functions
        ├── components/   # KpiCard, AppShell, ProtectedRoute
        ├── pages/        # LoginPage, SalesOverviewPage, ProductAnalyticsPage, CustomerAnalyticsPage
        ├── store/        # Zustand auth store
        └── types/        # Shared TypeScript interfaces
```

---

## Quick Start

### 1. Backend

```bash
cd ecommerce-analytics/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Copy env template and set your secret key
copy env.example .env          # Windows
# cp env.example .env          # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Seed the database
python seed.py

# Start the API server
uvicorn main:app --reload
```

Backend runs on → **http://localhost:8000**
Interactive API docs → **http://localhost:8000/docs**

### 2. Frontend

```bash
cd ecommerce-analytics/frontend
npm install
npm run dev
```

Frontend runs on → **http://localhost:5173**

### 3. Login

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |

---

## API Endpoints

All analytics endpoints require `Authorization: Bearer <token>` (obtain via `POST /auth/login`).

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/login` | Returns a signed JWT token |
| `GET` | `/analytics/sales/kpis` | Total revenue, orders, AOV, customers |
| `GET` | `/analytics/sales/trend?days=N` | Daily revenue trend (default 30 days) |
| `GET` | `/analytics/sales/by-channel` | Revenue by channel (web / mobile / marketplace) |
| `GET` | `/analytics/sales/order-status` | Order count per status |
| `GET` | `/analytics/products/top` | Top 10 products by revenue |
| `GET` | `/analytics/products/by-category` | Revenue by product category |
| `GET` | `/analytics/products/return-rate` | Top 10 most-returned products |
| `GET` | `/analytics/customers/summary` | Total / new this month / returning counts |
| `GET` | `/analytics/customers/top` | Top 10 customers by spend |
| `GET` | `/analytics/customers/by-country` | Customer count and revenue by country |
| `GET` | `/analytics/customers/new-vs-returning` | Monthly new vs returning (last 6 months) |

---

## Data Model

```
customers      id, name, email, city, state, country, created_at
products       id, name, category, price, cost, stock_quantity
orders         id, customer_id, status, created_at, channel, discount_amount
order_items    id, order_id, product_id, quantity, unit_price
```

**Order statuses:** `placed` · `shipped` · `delivered` · `returned` · `cancelled`
**Channels:** `web` · `mobile` · `marketplace`
**Categories:** Electronics · Clothing · Books · Home · Sports

---

## Environment Variables

Copy `backend/env.example` to `backend/.env` and set:

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
```

> The app will refuse to start if `SECRET_KEY` is not set.

---

## GitHub Repository

[https://github.com/sneha321k-hub/E-Commerce-Sales-Analytics](https://github.com/sneha321k-hub/E-Commerce-Sales-Analytics)
