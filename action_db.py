from models import Product, Company

'''Компанія'''
# додавання
def add_company(name: str, password: str):
    Company.create(name=name, password=password)

def company_exists(name: str) -> bool:
    return Company.select().where(Company.name == name).exists()

def get_company_by_name(name: str):
    return Company.get_or_none(Company.name == name)

'''Товар'''
# отримання
def get_all_products(company_id: int):
    return Product.select().where(Product.company == company_id)

def get_product_by_category(category: str, company_id: int):
    return Product.select().where((Product.category == category) & (Product.company == company_id))

def get_all_categories(company_id: int):
    return Product.select(Product.category).where(Product.company == company_id).distinct().order_by(Product.category)

def product_exist(name, company_id: int) -> bool:
    return Product.select().where((Product.name == name) & (Product.company == company_id)).exists()

# додавання
def add_product(name: str, price: float, category: str, company_id: int):
    Product.create(name=name, price=price, category=category, company_id=company_id)

# видалення
def delete_product(name: str, company_id: int):
    Product.delete().where((Product.company == company_id) & (Product.name == name)).execute()