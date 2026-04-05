from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "anything"
items = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('name')
        product_price = request.form.get('price')
        product_category = request.form.get('category')
        for item in items:
            if item.get('name') == product_name:
                flash('Product already exists!')
                break
        else:
            items.append({'name': product_name,
                          'price': product_price,
                          'category': product_category})
        return redirect(url_for('index'))
    return render_template('index.html', items=items)

@app.route('/delete/<item_index>')
def delete(item_index):
        items.pop(int(item_index))
        flash('Item removed from list!')
        return redirect(url_for('index'))

app.run(debug=True)