from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "anything"
items = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('name').lower()
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

    filter_items = None
    categories = map(lambda item: item['category'], items)
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_items = items
    elif choice_category == 'category':
        filter_items = filter(lambda item: item['category'] == choice_category, items)

    return render_template('index.html',
                           items=filter_items,
                           categories=categories,
                           choice_category=choice_category)

@app.route('/delete/<item_index>')
def delete(item_index):
        items.pop(int(item_index))
        flash('Item removed from list!')
        return redirect(url_for('index'))

app.run(debug=True)