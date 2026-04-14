from flask import Flask, render_template, request, redirect, url_for, flash
from models import init_db
from action_db import *

app = Flask(__name__)
app.secret_key = "anything"
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('name').lower()
        product_price = request.form.get('price')
        product_category = request.form.get('category')
        if product_exist(product_name):
            flash('Product already exists!', category='error')
        else:
            add_product(product_name, product_price, product_category)
            flash('Product added!', 'success')
        return redirect(url_for('index'))

    filter_items = None
    categories = get_all_categories()
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_items = get_all_items()
    else:
        filter_items = get_product_by_category(choice_category)

    return render_template('index.html',
                           items=filter_items,
                           categories=categories,
                           choice_category=choice_category)

@app.route('/delete/<name>')
def delete(name):
    delete_product(name)
    flash('Product deleted!', 'error')
    return redirect(url_for('index'))

app.run(debug=True)