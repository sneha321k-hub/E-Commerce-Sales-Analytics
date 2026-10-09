# E-Commerce Sales Analytics — MVP Plan

## Top-Level Overview

Build a full-stack, locally-runnable **E-Commerce Sales Analytics Dashboard** web application.

- **Backend:** Python 3.11+ with FastAPI, SQLite (pre-seeded with mock data), SQLAlchemy ORM
- **Frontend:** React 18 + TypeScript, Vite dev server, Recharts for visualisations, Tailwind CSS for styling
- **Auth:** Simple JWT-based login (single admin user, no registration flow)
- **Data source:** A seeded SQLite database with realistic mock e-commerce data (orders, products, customers)
- **Run target:** 100% localhost — backend on `http://localhost:8000`, frontend on `http://localhost:5173`
- **No AI/ML features** — all metrics are aggregation/formula-based

### MVP Scope — Three Dashboard Modules
1. **Sales Overview** — Revenue KPIs, order volume trends, period comparison
2. **Product Analytics** — Top products, category breakdown, return rates
3. **Customer Analytics** — New vs returning, top customers by spend, geographic distribution

### Out of Scope for MVP
- File upload / CSV ingestion
- Email / scheduled reports
- Multi-user roles beyond single admin
- Deployment (Docker, cloud)
- Dark mode, drag-and-drop customisation

---

## Project Structure

```
ecommerce-analytics/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # SQLAlchemy engine + session
│   ├── models.py                # ORM models: Order, Product, Customer, OrderItem
│   ├── schemas.py               # Pydantic response schemas
│   ├── seed.py                  # Script to populate SQLite with mock data
│   ├── routers/
│   │   ├── auth.py              # POST /auth/login -> JWT token
│   │   ├── sales.py             # GET /analytics/sales/*
│   │   ├── products.py          # GET /analytics/products/*
│   │   └── customers.py         # GET /analytics/customers/*
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── main.tsx
    │   ├── App.tsx
    │   ├── api/                 # Axios client + typed API hooks
    │   ├── components/          # Reusable chart + UI components
    │   ├── pages/
    │   │   ├── LoginPage.tsx
    │   │   ├── SalesOverviewPage.tsx
    │   │   ├── ProductAnalyticsPage.tsx
    │   │   └── CustomerAnalyticsPage.tsx
    │   ├── store/               # Auth state (Zustand or React Context)
    │   └── types/               # Shared TypeScript interfaces
    ├── index.html
    ├── vite.config.ts
    ├── tailwind.config.ts
    └── package.json
```

---

## Data Model

| Table | Key Columns |
|---|---|
| `customers` | id, name, email, city, state, country, created_at |
| `products` | id, name, category, price, cost, stock_quantity |
| `orders` | id, customer_id, status, created_at, channel, discount_amount |
| `order_items` | id, order_id, product_id, quantity, unit_price |

**Order statuses:** `placed`, `shipped`, `delivered`, `returned`, `cancelled`
**Channels:** `web`, `mobile`, `marketplace`

---

## Sub-Tasks

---

### Sub-Task 1 — Project Scaffolding

**Status:** `[ ] pending`

**Intent:**
Establish the directory structure, install all dependencies, and validate that both the backend and frontend servers start cleanly on localhost with no content yet.

**Expected Outcomes:**
- `backend/` directory with a virtual environment and all pip packages installed
- `frontend/` directory bootstrapped with Vite + React + TypeScript
- Tailwind CSS and Recharts installed in the frontend
- `GET http://localhost:8000/health` returns `{"status": "ok"}`
- `http://localhost:5173` renders a blank React app without errors

**Todo List:**
1. Create `backend/` directory; create `requirements.txt` with: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `python-jose[cryptography]`, `passlib[bcrypt]`, `python-dotenv`
2. Create `backend/main.py` with a minimal FastAPI app including a `/health` route and CORS middleware allowing `http://localhost:5173`
3. Scaffold `frontend/` using `npm create vite@latest` with `react-ts` template
4. Install frontend dependencies: `axios`, `recharts`, `react-router-dom`, `zustand`, `tailwindcss`, `@types/node`
5. Configure `tailwind.config.ts` and add Tailwind directives to global CSS
6. Configure `vite.config.ts` to proxy `/api` requests to `http://localhost:8000`
7. Verify both dev servers start without errors

**Relevant Context:**
- Backend runs via: `uvicorn main:app --reload` from the `backend/` directory
- Frontend runs via: `npm run dev` from the `frontend/` directory
- CORS must explicitly whitelist `http://localhost:5173`

---

### Sub-Task 2 — Database Models, Seed Data, and Database Setup

**Status:** `[ ] pending`

**Intent:**
Define the SQLAlchemy ORM models, create the SQLite database schema, and populate it with realistic mock data so all analytics endpoints have data to query against.

**Expected Outcomes:**
- `backend/database.py` establishes a SQLite connection at `./ecommerce.db`
- `backend/models.py` defines `Customer`, `Product`, `Order`, `OrderItem` ORM tables
- Running `python seed.py` populates the database with at minimum:
  - 200 customers across multiple cities/countries
  - 50 products across 5 categories
  - 1,000+ orders spanning the last 12 months with varied statuses and channels
  - Order items linking orders to products
- All foreign key relationships are valid (no orphaned records)

**Todo List:**
1. Create `backend/database.py` with SQLAlchemy engine pointing to `ecommerce.db` and a `SessionLocal` factory
2. Create `backend/models.py` with all four ORM models and correct relationships
3. Create `backend/seed.py` that:
   - Drops and recreates all tables via `Base.metadata.create_all`
   - Generates customers with realistic names, emails, and geographic spread
   - Generates products across categories (Electronics, Clothing, Books, Home, Sports)
   - Generates orders with randomised dates across the past 12 months, statuses, channels, and discounts
   - Generates order items for each order linking to products with quantities and prices
4. Run `python seed.py` and confirm `ecommerce.db` is created with populated tables

**Relevant Context:**
- Use Python's `random` and `datetime` modules for data generation — no external faker library needed
- SQLite file will live at `backend/ecommerce.db` (add to `.gitignore`)

---

### Sub-Task 3 — Authentication Endpoint

**Status:** `[ ] pending`

**Intent:**
Implement a simple JWT-based login so the dashboard is protected behind a username/password form. A single hardcoded admin credential is sufficient for the MVP.

**Expected Outcomes:**
- `POST /auth/login` with `{"username": "admin", "password": "admin123"}` returns a signed JWT token
- Any request with a missing or invalid token to a protected route returns `401 Unauthorized`
- A `get_current_user` dependency can be reused across all analytics routers

**Todo List:**
1. Add a `SECRET_KEY` value to a `.env` file and load it via `python-dotenv` in `main.py`
2. Create `backend/routers/auth.py` with:
   - Hardcoded admin credentials (username: `admin`, password: `admin123`) validated with `passlib`
   - `POST /auth/login` returning `{"access_token": "...", "token_type": "bearer"}`
3. Create a `get_current_user` dependency that decodes the JWT from the `Authorization: Bearer` header
4. Register the auth router in `main.py` under the `/auth` prefix
5. Test the endpoint manually with curl or a browser HTTP client

**Relevant Context:**
- Use `python-jose` for JWT encoding/decoding with `HS256` algorithm
- Token expiry can be set to 24 hours for MVP convenience
- Hardcoded credentials are acceptable for MVP — no user table needed

---

### Sub-Task 4 — Sales Overview API Endpoints

**Status:** `[ ] pending`

**Intent:**
Expose the aggregated sales data that the Sales Overview dashboard page will consume. All metrics are pure SQL aggregations — no ML logic.

**Expected Outcomes:**
All routes are protected by the JWT dependency and return correctly shaped JSON.

| Endpoint | Returns |
|---|---|
| `GET /analytics/sales/kpis` | Total revenue, total orders, AOV, total customers |
| `GET /analytics/sales/trend` | Daily/weekly revenue and order count for the last N days (query param) |
| `GET /analytics/sales/by-channel` | Revenue and order count grouped by channel |
| `GET /analytics/sales/order-status` | Count of orders per status |

**Todo List:**
1. Create `backend/schemas.py` with Pydantic models for all four response shapes
2. Create `backend/routers/sales.py` with the four routes using SQLAlchemy aggregate queries (`func.sum`, `func.count`, `func.avg`, `group_by`)
3. Register the sales router in `main.py` under `/analytics/sales`
4. Validate all four endpoints return correct data by calling them via the FastAPI auto-generated docs at `http://localhost:8000/docs`

**Relevant Context:**
- `trend` endpoint should accept a `?days=30` query parameter defaulting to 30
- Revenue = `sum(order_items.quantity * order_items.unit_price)` minus `orders.discount_amount`
- Only count orders with status not in `['cancelled']` for revenue metrics

---

### Sub-Task 5 — Product Analytics API Endpoints

**Status:** `[ ] pending`

**Intent:**
Expose product-level aggregations for the Product Analytics dashboard page.

**Expected Outcomes:**
All routes protected and returning correctly shaped JSON.

| Endpoint | Returns |
|---|---|
| `GET /analytics/products/top` | Top 10 products by revenue with units sold |
| `GET /analytics/products/by-category` | Revenue and order count grouped by category |
| `GET /analytics/products/return-rate` | Return rate per product (top 10 most returned) |

**Todo List:**
1. Add Pydantic schemas for product analytics responses to `schemas.py`
2. Create `backend/routers/products.py` with the three routes
3. For `return-rate`: calculate as `count(orders with status='returned') / count(all orders)` per product, joined through `order_items`
4. Register the products router in `main.py` under `/analytics/products`
5. Validate all three endpoints via `/docs`

**Relevant Context:**
- Join path for product metrics: `order_items` → `orders` → `products`
- Category values come from `products.category` — no separate category table needed

---

### Sub-Task 6 — Customer Analytics API Endpoints

**Status:** `[ ] pending`

**Intent:**
Expose customer-level aggregations for the Customer Analytics dashboard page.

**Expected Outcomes:**
All routes protected and returning correctly shaped JSON.

| Endpoint | Returns |
|---|---|
| `GET /analytics/customers/summary` | Total customers, new this month, returning customers count |
| `GET /analytics/customers/top` | Top 10 customers by total spend |
| `GET /analytics/customers/by-country` | Customer count and revenue grouped by country |
| `GET /analytics/customers/new-vs-returning` | Monthly breakdown of new vs returning customers for the last 6 months |

**Todo List:**
1. Add Pydantic schemas for customer analytics responses to `schemas.py`
2. Create `backend/routers/customers.py` with the four routes
3. For `new-vs-returning`: a customer is "new" in month M if their first-ever order was in month M; otherwise "returning"
4. Register the customers router in `main.py` under `/analytics/customers`
5. Validate all four endpoints via `/docs`

**Relevant Context:**
- "New this month" = customers whose `min(orders.created_at)` falls in the current calendar month
- `by-country` data will power the geographic distribution table/chart on the frontend

---

### Sub-Task 7 — Frontend: Auth Flow and App Shell

**Status:** `[ ] pending`

**Intent:**
Build the login page, JWT token storage, protected route guard, and the persistent app shell (sidebar navigation + top bar) that wraps all dashboard pages.

**Expected Outcomes:**
- Navigating to any route while unauthenticated redirects to `/login`
- Submitting correct credentials on `/login` stores the JWT in `localStorage` and redirects to `/sales`
- A sidebar shows navigation links to Sales Overview, Product Analytics, Customer Analytics
- The app shell renders consistently on all three dashboard routes

**Todo List:**
1. Create `frontend/src/store/authStore.ts` using Zustand to hold the JWT token and a `logout` action
2. Create `frontend/src/api/client.ts` — an Axios instance that reads the token from the store and attaches `Authorization: Bearer` header to every request
3. Create `frontend/src/pages/LoginPage.tsx` — a centred form with username/password fields; calls `POST /auth/login` via Axios; stores token on success; shows error on failure
4. Create `frontend/src/components/ProtectedRoute.tsx` — redirects to `/login` if token is absent
5. Create `frontend/src/components/AppShell.tsx` — sidebar with nav links and a top bar showing "E-Commerce Analytics" title and a logout button
6. Wire up `react-router-dom` routes in `App.tsx`:
   - `/login` → `LoginPage`
   - `/sales`, `/products`, `/customers` → protected, render inside `AppShell`
7. Verify login flow and redirect behaviour end-to-end

**Relevant Context:**
- Vite proxy config (Sub-Task 1) routes `/api/*` to `http://localhost:8000/*` — all Axios calls should use `/api/` prefix
- Logout clears the Zustand store and `localStorage`, then redirects to `/login`

---

### Sub-Task 8 — Frontend: Sales Overview Page

**Status:** `[ ] pending`

**Intent:**
Build the Sales Overview dashboard page consuming the four sales API endpoints and rendering KPI cards and charts.

**Expected Outcomes:**
- Four KPI cards: Total Revenue, Total Orders, AOV, Total Customers
- A line chart showing daily revenue trend for the last 30 days
- A bar chart showing revenue by channel
- A donut chart showing order status distribution
- A date-range selector (Last 7 / 30 / 90 days) that re-fetches the trend data

**Todo List:**
1. Create `frontend/src/types/sales.ts` with TypeScript interfaces matching the sales API response schemas
2. Create `frontend/src/api/salesApi.ts` with typed functions for all four sales endpoints
3. Create reusable `frontend/src/components/KpiCard.tsx` component
4. Create `frontend/src/pages/SalesOverviewPage.tsx`:
   - Use `useEffect` + `useState` to fetch and hold data from all four endpoints
   - Render `KpiCard` components for the four top-line metrics
   - Render a `<LineChart>` (Recharts) for the revenue trend
   - Render a `<BarChart>` (Recharts) for revenue by channel
   - Render a `<PieChart>` (Recharts) for order status breakdown
   - Add a segmented button group for the days selector that refetches trend data
5. Add loading spinners while data is in-flight and a simple error message on failure

**Relevant Context:**
- Recharts components needed: `LineChart`, `BarChart`, `PieChart`, `Tooltip`, `Legend`, `ResponsiveContainer`
- All currency values should be formatted as USD with `Intl.NumberFormat`

---

### Sub-Task 9 — Frontend: Product Analytics Page

**Status:** `[ ] pending`

**Intent:**
Build the Product Analytics dashboard page consuming the three product API endpoints.

**Expected Outcomes:**
- A horizontal bar chart of top 10 products by revenue
- A donut chart of revenue share by category
- A table of top 10 most-returned products with return rate percentage

**Todo List:**
1. Create `frontend/src/types/products.ts` with TypeScript interfaces
2. Create `frontend/src/api/productsApi.ts` with typed fetch functions
3. Create `frontend/src/pages/ProductAnalyticsPage.tsx`:
   - Horizontal `<BarChart>` for top products (Recharts `layout="vertical"`)
   - `<PieChart>` for category revenue share
   - A styled HTML table for return rate data, sorted by return rate descending
4. Add loading and error states

**Relevant Context:**
- Return rate should be displayed as a percentage with one decimal place
- Category colours should be consistent across the donut chart and any category labels

---

### Sub-Task 10 — Frontend: Customer Analytics Page

**Status:** `[ ] pending`

**Intent:**
Build the Customer Analytics dashboard page consuming the four customer API endpoints.

**Expected Outcomes:**
- Three KPI cards: Total Customers, New This Month, Returning Customers
- A grouped bar chart showing new vs returning customers per month (last 6 months)
- A table of top 10 customers by spend
- A table of revenue and customer count by country

**Todo List:**
1. Create `frontend/src/types/customers.ts` with TypeScript interfaces
2. Create `frontend/src/api/customersApi.ts` with typed fetch functions
3. Create `frontend/src/pages/CustomerAnalyticsPage.tsx`:
   - Reuse `KpiCard` for the three customer summary metrics
   - A grouped `<BarChart>` for new vs returning trend (Recharts)
   - A styled table for top customers with spend formatted as USD
   - A styled table for country breakdown with a customer count and revenue column
4. Add loading and error states

**Relevant Context:**
- Reuse the `KpiCard` component created in Sub-Task 8
- Tables should be sorted by the primary metric column descending by default

---

### Sub-Task 11 — Integration Testing and Localhost Validation

**Status:** `[ ] pending`

**Intent:**
Do a full end-to-end walkthrough of the running application on localhost to confirm every page, chart, and API integration works correctly before declaring the MVP complete.

**Expected Outcomes:**
- `python seed.py` runs cleanly and populates the database
- `uvicorn main:app --reload` starts without errors on port 8000
- `npm run dev` starts without errors on port 5173
- All 11 API endpoints return HTTP 200 with valid data via `/docs`
- Login flow works with correct credentials; rejects incorrect ones with an error message
- All three dashboard pages render charts and tables with real data
- Navigating directly to a protected URL while logged out redirects to `/login`
- Logout clears the session and redirects to `/login`

**Todo List:**
1. Run `python seed.py` and verify record counts in `ecommerce.db`
2. Start the backend and open `http://localhost:8000/docs` — test each endpoint manually using the "Authorize" button with a valid token
3. Start the frontend and walk through the full login → Sales → Products → Customers flow
4. Verify all charts render with data (no empty states)
5. Verify the days selector on the Sales page refetches data
6. Test logout and protected route redirect
7. Fix any CORS, proxy, or data-shape mismatches discovered during the walkthrough
8. Write a concise `README.md` at the project root with setup and run instructions

**Relevant Context:**
- If CORS errors appear, verify the `allow_origins` list in `main.py` matches the Vite dev server URL exactly
- If charts show empty, check the Axios base URL and proxy config in `vite.config.ts`

---

## Run Instructions (final state)

```
# Terminal 1 — Backend
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

- Backend API docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:5173`
- Login: `admin` / `admin123`
