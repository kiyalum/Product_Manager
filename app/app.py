from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

from models import init_db
from action_db import *

app = Flask(__name__)
app.secret_key = "anything"
init_db()

def is_logged():
    return 'company_name' in session

def current_company():
    name_company = session.get('company_name')
    if not name_company:
        return None
    return get_company_by_name(name_company)

@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    current_company()
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

@app.route('/index', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('login'))

    company = current_company()

    if request.method == 'POST':
        product_name = request.form.get('name').lower()
        product_price = float(request.form.get('price'))
        product_category = request.form.get('category').lower()
        if product_exist(product_name, company.id):
            flash('Product already exists!')
        else:
            add_product(product_name, product_price, product_category, company.id)
            flash('Product added!')
        return redirect(url_for('index'))

    categories = get_all_categories(company.id)
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_items = get_all_products(company.id)
    else:
        filter_items = get_product_by_category(choice_category, company.id)

    return render_template('index.html',
                           items=filter_items,
                           categories=categories,
                           choice_category=choice_category)

@app.route('/delete/<name>')
def delete(name):
    if not is_logged():
        return redirect(url_for('login'))

    company = current_company()
    delete_product(name, company.id)
    flash('Item removed from list!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('company_name', None)
    flash('You leave from system!')
    return redirect(url_for('login'))



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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)