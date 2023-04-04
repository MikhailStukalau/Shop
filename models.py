from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<product {self.id}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), nullable=False)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return self.cat_name
