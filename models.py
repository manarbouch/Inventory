from app import db
from datetime import datetime


# Warehouse Model (if you decide to expand to more warehouses later)
class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    # Relationship with the Inventory model
    inventory_items = db.relationship('Inventory', back_populates='warehouse')


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    reorder_level = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

    # Relationship to Supplier
    supplier = db.relationship('Supplier', back_populates='products')

    # One-to-many relationship with Inventory
    inventory_items = db.relationship('Inventory', back_populates='product')

    # One-to-many relationship with Order
    orders = db.relationship('Order', backref='ordered_product', lazy=True)

    # Low stock alert
    low_stock_alert = db.Column(db.Boolean, default=False)

    def check_stock_level(self):
        # Check if stock is below reorder level
        if self.inventory_items and self.inventory_items[0].quantity < self.reorder_level:
            self.low_stock_alert = True
            db.session.commit()
        else:
            self.low_stock_alert = False
            db.session.commit()


# Supplier Model
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=True)

    # Relationship to Product
    products = db.relationship('Product', back_populates='supplier')


# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')

    product = db.relationship('Product', backref=db.backref('orders', lazy=True))


# Inventory Model
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Relationships
    warehouse = db.relationship('Warehouse', back_populates='inventory_items')
    product = db.relationship('Product', back_populates='inventory_items')

    def update_quantity(self, quantity_change):
        """ Method to update quantity of the product in inventory """
        self.quantity += quantity_change
        db.session.commit()

    def get_current_quantity(self):
        """ Method to get current inventory quantity """
        return self.quantity

