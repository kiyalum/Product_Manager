from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import init_db
from action_db import *

app = Flask(__name__)
app.secret_key = "anything"
init_db()

def is_logged():
    return 'company_name' in session

@app.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_name = request.form.get('name').lower()
        product_price = float(request.form.get('price'))
        product_category = request.form.get('category').lower()
        if product_exist(product_name):
            flash('Product already exists!')
        else:
            add_product(product_name, product_price, product_category)
            flash('Product added!')
        return redirect(url_for('index'))

    categories = get_all_categories()
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_items = get_all_products()
    else:
        filter_items = get_product_by_category(choice_category)

    return render_template('index.html',
                           items=filter_items,
                           categories=categories,
                           choice_category=choice_category)

@app.route('/delete/<name>')
def delete(name):
        delete_product(name)
        flash('Item removed from list!')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name_company')
        password = request.form.get('password')

        if company_exists(name):
            flash('Company already exists!')
            return redirect(url_for('register'))
        else:    
            password_hash = generate_password_hash(password)

            flash(f'Company {name} is registered!')
            add_company(name, password_hash)
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name_company')
        password = request.form.get('password')

        if not company_exists(name):
            flash(f'Company {name} does not exist!')
            return redirect(url_for('login'))

        company = get_company_by_name(name)
        if not check_password_hash(company.password, password):
            flash('Password incorrect!')
            return redirect(url_for('login'))

        session['company_name'] = company.name
        flash(f'Welcome, {company.name}!')
        return redirect(url_for('index'))

    return render_template('login.html')

app.run(debug=True)