from .models import Base, get_engine, get_session, Product, Customer, Sale
from .config import DB_URL
import datetime, random

def seed(engine):
    Base.metadata.create_all(engine)
    session = get_session(engine)
    products = [
        Product(name="Widget A", category="Widgets", price=19.99),
        Product(name="Widget B", category="Widgets", price=29.99),
        Product(name="Gadget X", category="Gadgets", price=49.99),
    ]
    session.add_all(products)
    session.commit()
    customers = [Customer(name=f"Customer {i}", email=f"cust{i}@example.com") for i in range(10)]
    session.add_all(customers)
    session.commit()
    now = datetime.datetime.utcnow()
    sales = []
    for _ in range(50):
        p = random.choice(products)
        c = random.choice(customers)
        qty = random.randint(1, 5)
        sold_at = now - datetime.timedelta(days=random.randint(0, 180))
        sales.append(Sale(product_id=p.id, customer_id=c.id, quantity=qty,
                          unit_price=p.price, total_price=p.price*qty, sold_at=sold_at))
    session.add_all(sales)
    session.commit()
    print("Database seeded.")

if __name__ == "__main__":
    engine = get_engine(DB_URL)
    seed(engine)
