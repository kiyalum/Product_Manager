from models import Product

# отримання
def get_all_items():
    return Product.select()

def get_product_by_category(category):
    return Product.select().where(Product.category == category)

def get_all_categories():
    return Product.select(Product.category).distinct().order_by(Product.category)

def product_exist(name):
    return Product.select().where(Product.name == name).exists()

# додавання
def add_product(name, price, category):
    Product.create(name=name, price=price, category=category)

# видалення
def delete_product(name):
    Product.delete().where(Product.name == name).execute()
