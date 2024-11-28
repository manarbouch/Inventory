from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_mail import Message
from models import Product, Supplier, Order, Inventory, Warehouse, db
from flask_mail import Mail


def setup_routes(app):
    @app.route('/')
    def home():
        products = Product.query.all()
        return render_template('index.html', products=products)

    @app.route('/add_product', methods=['GET', 'POST'])
    def add_product():
        suppliers = Supplier.query.all()
        if request.method == 'POST':
            name = request.form['name']
            quantity = request.form['quantity']
            price = request.form['price']
            reorder_level = request.form['reorder_level']
            supplier_id = request.form['supplier_id']

            # Create a new product
            new_product = Product(name=name, quantity=quantity, price=price, reorder_level=reorder_level,
                                  supplier_id=supplier_id)

            # Create a new inventory item (assuming you have a single warehouse)
            warehouse = Warehouse.query.first()  # Assuming a single warehouse
            new_inventory_item = Inventory(quantity=quantity, product=new_product, warehouse=warehouse)

            db.session.add(new_product)
            db.session.add(new_inventory_item)
            db.session.commit()

            flash('Product added successfully!', 'success')
            return redirect(url_for('home'))
        return render_template('add_product.html', suppliers=suppliers)

    @app.route('/add_supplier', methods=['GET', 'POST'])
    def add_supplier():
        if request.method == 'POST':
            name = request.form['name']
            contact_info = request.form['contact_info']
            new_supplier = Supplier(name=name, contact_info=contact_info)
            db.session.add(new_supplier)
            db.session.commit()
            flash('Supplier added successfully!', 'success')
            return redirect(url_for('home'))
        return render_template('add_supplier.html')

    @app.route('/order/<int:product_id>', methods=['POST'])
    def order_product(product_id):
        product = Product.query.get_or_404(product_id)
        quantity = int(request.form['quantity'])

        # Update the inventory when an order is placed
        inventory_item = Inventory.query.filter_by(product_id=product.id, warehouse_id=1).first()  # Single warehouse
        if inventory_item:
            inventory_item.quantity -= quantity
            db.session.commit()

        # Create new order record
        new_order = Order(product_id=product.id, quantity=quantity, date_ordered=datetime.now())
        db.session.add(new_order)
        db.session.commit()

        flash(f'Order placed for {quantity} {product.name}(s)', 'success')

        # Check stock and send low stock alert if necessary
        product.check_stock_level()  # Check if product's stock is below reorder level
        if product.low_stock_alert:
            send_low_stock_alert(product.name)

        return redirect(url_for('home'))

    def send_low_stock_alert(product_name):
        msg = Message("Low Stock Alert", recipients=["admin@example.com"])
        msg.body = f"The stock level of {product_name} is low. Please reorder."
        mail.send(msg)
