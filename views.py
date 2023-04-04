from sqlite3 import OperationalError

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
    db.create_all()
    return render_template('index.html')


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
            print('Error DB!', ex)
        # finally:
        #     db.create_all()
    print('3', categories) #проверка
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
    return render_template('add_cat.html')

#выполнено добавление записи в обе бд
#не повторяющиеся категории в выпадающем списке
