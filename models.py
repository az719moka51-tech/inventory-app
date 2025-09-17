from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    supplier = db.Column(db.String(100))
    category = db.Column(db.String(50))
    note = db.Column(db.Text)
