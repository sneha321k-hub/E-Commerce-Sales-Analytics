import random
import string
from datetime import datetime, timedelta
from database import engine, SessionLocal
from models import Base, Customer, Product, Order, OrderItem

random.seed(42)

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Dorothy", "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna",
    "Kenneth", "Michelle", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Timothy", "Deborah"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts"
]

GEO = [
    ("New York", "NY", "USA"),
    ("Los Angeles", "CA", "USA"),
    ("Chicago", "IL", "USA"),
    ("Houston", "TX", "USA"),
    ("Phoenix", "AZ", "USA"),
    ("Philadelphia", "PA", "USA"),
    ("San Antonio", "TX", "USA"),
    ("San Diego", "CA", "USA"),
    ("Dallas", "TX", "USA"),
    ("San Jose", "CA", "USA"),
    ("London", "England", "UK"),
    ("Manchester", "England", "UK"),
    ("Birmingham", "England", "UK"),
    ("Toronto", "ON", "Canada"),
    ("Vancouver", "BC", "Canada"),
    ("Montreal", "QC", "Canada"),
    ("Sydney", "NSW", "Australia"),
    ("Melbourne", "VIC", "Australia"),
    ("Berlin", "Berlin", "Germany"),
    ("Munich", "Bavaria", "Germany"),
    ("Paris", "Ile-de-France", "France"),
    ("Lyon", "Auvergne", "France"),
    ("Amsterdam", "NH", "Netherlands"),
    ("Madrid", "Madrid", "Spain"),
    ("Barcelona", "Catalonia", "Spain"),
]

PRODUCTS = [
    # Electronics
    ("Wireless Bluetooth Headphones", "Electronics", 89.99, 35.00),
    ("Smart Watch Pro", "Electronics", 249.99, 98.00),
    ("USB-C Hub 7-in-1", "Electronics", 49.99, 18.00),
    ("Mechanical Keyboard", "Electronics", 129.99, 52.00),
    ("Gaming Mouse", "Electronics", 69.99, 25.00),
    ("Portable Charger 20000mAh", "Electronics", 39.99, 14.00),
    ("Webcam 1080p", "Electronics", 79.99, 30.00),
    ("Noise Cancelling Earbuds", "Electronics", 149.99, 58.00),
    ("LED Desk Lamp", "Electronics", 34.99, 12.00),
    ("Smart Home Speaker", "Electronics", 99.99, 40.00),
    # Clothing
    ("Men's Running Shoes", "Clothing", 79.99, 28.00),
    ("Women's Yoga Pants", "Clothing", 49.99, 16.00),
    ("Classic Denim Jacket", "Clothing", 89.99, 32.00),
    ("Merino Wool Sweater", "Clothing", 119.99, 45.00),
    ("Waterproof Hiking Boots", "Clothing", 149.99, 60.00),
    ("Cotton T-Shirt Pack (3)", "Clothing", 34.99, 10.00),
    ("Slim Fit Chinos", "Clothing", 59.99, 20.00),
    ("Sports Hoodie", "Clothing", 69.99, 24.00),
    ("Summer Dress", "Clothing", 54.99, 18.00),
    ("Leather Belt", "Clothing", 29.99, 9.00),
    # Books
    ("The Art of Clean Code", "Books", 29.99, 6.00),
    ("Data Science Fundamentals", "Books", 39.99, 8.00),
    ("Financial Freedom Guide", "Books", 24.99, 5.00),
    ("Modern Web Development", "Books", 44.99, 10.00),
    ("Psychology of Habits", "Books", 19.99, 4.00),
    ("Machine Learning Cookbook", "Books", 49.99, 12.00),
    ("History of the Internet", "Books", 22.99, 5.00),
    ("Leadership Essentials", "Books", 27.99, 6.00),
    ("Creative Writing Mastery", "Books", 21.99, 4.50),
    ("Mindful Productivity", "Books", 18.99, 3.50),
    # Home
    ("Stainless Steel Water Bottle", "Home", 24.99, 7.00),
    ("Bamboo Cutting Board Set", "Home", 34.99, 11.00),
    ("Memory Foam Pillow", "Home", 44.99, 16.00),
    ("Smart Thermostat", "Home", 129.99, 52.00),
    ("Air Purifier Compact", "Home", 89.99, 35.00),
    ("Cast Iron Skillet", "Home", 59.99, 22.00),
    ("French Press Coffee Maker", "Home", 39.99, 13.00),
    ("Robot Vacuum Mini", "Home", 199.99, 85.00),
    ("Scented Candle Set", "Home", 29.99, 8.00),
    ("Electric Kettle", "Home", 49.99, 18.00),
    # Sports
    ("Yoga Mat Premium", "Sports", 54.99, 18.00),
    ("Resistance Bands Set", "Sports", 24.99, 7.00),
    ("Adjustable Dumbbells", "Sports", 189.99, 78.00),
    ("Jump Rope Speed", "Sports", 19.99, 5.00),
    ("Foam Roller Deep Tissue", "Sports", 34.99, 11.00),
    ("Pull-Up Bar Doorway", "Sports", 44.99, 16.00),
    ("Cycling Gloves", "Sports", 29.99, 9.00),
    ("Tennis Racket Pro", "Sports", 119.99, 48.00),
    ("Soccer Ball Size 5", "Sports", 39.99, 13.00),
    ("Swim Goggles Anti-Fog", "Sports", 22.99, 6.50),
]

STATUSES = ["placed", "shipped", "delivered", "returned", "cancelled"]
STATUS_WEIGHTS = [0.05, 0.15, 0.65, 0.10, 0.05]
CHANNELS = ["web", "mobile", "marketplace"]
CHANNEL_WEIGHTS = [0.50, 0.30, 0.20]


def random_date(days_back: int) -> datetime:
    offset = random.randint(0, days_back)
    return datetime.utcnow() - timedelta(days=offset)


def random_email(first: str, last: str, existing: set) -> str:
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]
    base = f"{first.lower()}.{last.lower()}"
    candidate = f"{base}@{random.choice(domains)}"
    if candidate in existing:
        candidate = f"{base}{random.randint(1, 999)}@{random.choice(domains)}"
    existing.add(candidate)
    return candidate


def main():
    print("Dropping and recreating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ── Customers ──────────────────────────────────────────────────────────
    print("Seeding 200 customers...")
    used_emails: set = set()
    customers = []
    for i in range(200):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        city, state, country = random.choice(GEO)
        email = random_email(first, last, used_emails)
        c = Customer(
            name=f"{first} {last}",
            email=email,
            city=city,
            state=state,
            country=country,
            created_at=random_date(540),
        )
        customers.append(c)

    db.add_all(customers)
    db.commit()
    for c in customers:
        db.refresh(c)

    # ── Products ───────────────────────────────────────────────────────────
    print("Seeding 50 products...")
    products = []
    for name, category, price, cost in PRODUCTS:
        p = Product(
            name=name,
            category=category,
            price=price,
            cost=cost,
            stock_quantity=random.randint(20, 500),
        )
        products.append(p)

    db.add_all(products)
    db.commit()
    for p in products:
        db.refresh(p)

    # ── Orders + OrderItems ────────────────────────────────────────────────
    print("Seeding 1200 orders with items...")
    orders = []
    for _ in range(1200):
        customer = random.choice(customers)
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        channel = random.choices(CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]
        discount = round(random.choice([0, 0, 0, 5, 10, 15, 20, 25]), 2)
        o = Order(
            customer_id=customer.id,
            status=status,
            created_at=random_date(365),
            channel=channel,
            discount_amount=discount,
        )
        orders.append(o)

    db.add_all(orders)
    db.commit()
    for o in orders:
        db.refresh(o)

    order_items = []
    for order in orders:
        num_items = random.randint(1, 4)
        chosen_products = random.sample(products, k=min(num_items, len(products)))
        for product in chosen_products:
            qty = random.randint(1, 3)
            oi = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
            )
            order_items.append(oi)

    db.add_all(order_items)
    db.commit()

    # ── Verify ─────────────────────────────────────────────────────────────
    print(f"  Customers : {db.query(Customer).count()}")
    print(f"  Products  : {db.query(Product).count()}")
    print(f"  Orders    : {db.query(Order).count()}")
    print(f"  OrderItems: {db.query(OrderItem).count()}")
    db.close()
    print("Done — ecommerce.db is ready.")


if __name__ == "__main__":
    main()
