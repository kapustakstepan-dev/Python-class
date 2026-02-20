from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Проміжна таблиця для зв’язку багато-до-багатьох (Order <-> MenuItem)
order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
)

# Моделі
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), default=0)
    items = db.relationship('MenuItem', secondary=order_items, backref='orders')

# --- Функції для роботи з БД ---

def add_customer(name, phone):
    """Додавання нового клієнта"""
    new_customer = Customer(name=name, phone_number=phone)
    db.session.add(new_customer)
    db.session.commit()
    print(f"Клієнт {name} доданий.")

def create_order(customer_id, menu_item_ids):
    """Створення замовлення з автоматичним підрахунком вартості"""
    items = MenuItem.query.filter(MenuItem.id.in_(menu_item_ids)).all()
    # Підраховуємо суму через генератор або функцію sum()
    total = sum(item.price for item in items)
    
    new_order = Order(customer_id=customer_id, items=items, total_price=total)
    db.session.add(new_order)
    db.session.commit()
    print(f"Замовлення створено. Загальна вартість: {total}")

def get_customer_orders(customer_id):
    """Запит на отримання всіх замовлень конкретного клієнта"""
    orders = Order.query.filter_by(customer_id=customer_id).all()
    for order in orders:
        print(f"Замовлення №{order.id}, Сума: {order.total_price}")
    return orders

# Ініціалізація бази даних (виконується один раз)
with app.app_context():
    db.create_all()