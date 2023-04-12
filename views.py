from sqlite3 import OperationalError
from cloudipsp import Api, Checkout
from app import app, db
from flask import (
    render_template,
    request, redirect,
    flash, abort,
    Blueprint, url_for,
    get_flashed_messages
)
from models import Category, Product


@app.route('/')
def index():
    product = Product.query.all()
    category = Category.query.group_by(Category.cat_name).all()
    el = {
        'product': product,
        'category': category
    }
    return render_template('index.html', el=el)


@app.route('/buy/<int:id>/')
def buy(id):
    item = Product.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "BYN",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/add_prod', methods=['POST', 'GET'])
def add_prod():
    categories = Category.query.group_by(Category.cat_name).all()

    if request.method == 'POST':
        try:
            p = Product(name=request.form['name'], description=request.form['description'],
                        price=request.form['price'])
            db.session.add(p)
            db.session.flush()

            c = Category(cat_name=request.form['cat_name'], prod_id=p.id)
            db.session.add(c)

            db.session.commit()
            return redirect('/')
        except Exception as ex:
            db.session.rollback()
            print('error add_product', ex)

    return render_template('add_prod.html', categories=categories)


@app.route('/add_cat', methods=['POST', 'GET'])
def add_cat():
    if request.method == 'POST':
        try:
            c = Category(cat_name=request.form['cat_name'])
            db.session.add(c)

            db.session.commit()
            return redirect('/')
        except Exception as ex:
            db.session.rollback()
            print('error add_category', ex)
    return render_template('add_cat.html')


@app.route("/details/<cat_name>", methods=['POST', 'GET'])
def details(cat_name: str):
    detail = []
    products = Product.query.all()
    for product in products:
        if product.pr.cat_name == cat_name:
            detail.append(product)
    # detail = products.filter_by(cat_name='cat_name')

    return render_template('details.html', detail=detail)


