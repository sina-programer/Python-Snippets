from abc import ABC, abstractmethod
import pandas as pd
import operator
import getpass
import hashlib
import random
import string
import os
import re


class Object(ABC):
    @property
    @abstractmethod
    def path(self): return str

    @property
    @abstractmethod
    def header(self): return list

    @abstractmethod
    def get_str(self): return str

    @classmethod
    def load_df(cls):
        if os.path.exists(cls.path):
            cls.df = pd.read_csv(cls.path)
        else:
            cls.df = pd.DataFrame(columns=cls.header)
            cls.save_df()

    @classmethod
    def add(cls, **parameters):
        new_row = pd.Series(parameters)
        cls.df = pd.concat([cls.df, new_row.to_frame().T], ignore_index=True)
        cls.save_df()

    @classmethod
    def get_info(cls):
        return list(map(cls.get_str, list(map(operator.itemgetter(1), cls.df.iterrows()))))

    @classmethod
    def save_df(cls):
        cls.df.to_csv(cls.path, index=False)



class User(Object):
    path = r"users.csv"
    header = ['FirstName', 'LastName', 'Username', 'Password', 'Role', 'Credit']

    roles = ['seller', 'customer']

    @staticmethod
    def _generate_username(name, length, chars):
        return name + '_' + ''.join(random.choices(chars, k=length))

    @staticmethod
    def generate_username(name, length=4, chars=string.ascii_letters+string.digits):
        username = User._generate_username(name, length, chars)
        while username in User.df['Username'].values:
            username = User._generate_username(name, length, chars)

        return username

    @staticmethod
    def password_verifier(password, regex=r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}"):
        return bool(re.match(regex, password))

    @staticmethod
    def get_str(user):
        return f"{user.Username} ({user.FirstName}, {user.LastName})  Role={user.Role}  Credit={user.Credit}"


class Product(Object):
    path = r"products.csv"
    header = ['ID', 'Name', 'Seller', 'Price', 'Quantity']

    @staticmethod
    def get_str(product):
        return f'{product.Name} ({product.Seller}): {product.Price} (×{product.Quantity})'


class Order(Object):
    path = r"orders.csv"
    header = ['Customer', 'ProductID', 'Quantity']

    @staticmethod
    def get_str(order):
        product = Product.df[Product.df['ID'] == order.ProductID].iloc[0]
        return f"{product.Name} ({product.Seller}): {product.Price} (×{order.Quantity})"




def select_item(items, prompt='Select desired item: ', title=''):
    if title:
        print('\n', title)

    print()
    for idx, item in enumerate(items, 1):
        print(f' {idx}_ {item}')

    selected_item = input(f"\n {prompt}")

    while True:
        try:
            selected_item = int(selected_item)
            assert 1 <= selected_item <= len(items)
            return selected_item - 1

        except:
            print(f'\n "{selected_item}" is not a valid index!')
            selected_item = input('\n Please enter a valid index: ')


def error(kind=RuntimeError, msg=''):
    raise kind(msg)


def signin():
    username = input(" Username: ")
    if username not in User.df['Username'].values:
        print('Invalid Username!')
        return

    user = User.df[User.df['Username'] == username].iloc[0]

    password = getpass.getpass(" Password: ")
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    if user.Password != hashed_password:
        print(" Invalid Password!")
        return

    if user.Role == "customer":
        menu = customer_menu.copy()
    else:
        menu = seller_menu.copy()    

    while True:
        print('-' * 50)
        index = select_item(menu.keys(), prompt='Select desired operation: ', title=f'{user.Role.title()} Menu')
        user = User.df[User.df['Username'] == username].iloc[0]
        function = list(menu.values())[index]

        try:
            function(user)
        except SystemError:
            break


def signup():
    first_name = input(' First Name: ')
    if len(first_name) < 3:
        print(' First-Name must be at least 3 characters!')
        return

    last_name = input(' Last Name: ')
    if len(last_name) < 3:
        print(' Last-Name must be at least 3 characters!')
        return

    password = getpass.getpass(' Password: ')
    if not User.password_verifier(password):
        print(' Password must be including at least 8 both of upper/lower case characters and numbers!')
        return

    password_confirm = getpass.getpass(' Confirm Password: ')
    if password_confirm != password:
        print(' <password> & <password-confirm> do not match together!')
        return

    role_idx = select_item(User.roles, prompt='Select your role: ')
    role = User.roles[role_idx]

    username = User.generate_username(first_name)
    print(f' Your username: {username}')

    User.add(FirstName=first_name, LastName=last_name, Username=username, Role=role, Credit=0, Password=hashlib.md5(password.encode()).hexdigest())


# User Menu Functions ----------------------------

def view_menu():
    for product_info in Product.get_info():
        print('', product_info)


def place_order(user):
    products = Product.get_info()
    product_id = select_item(products)
    product = Product.df.iloc[product_id]
    quantity = int(input('Enter the quantity: '))
    total_price = product.Price * quantity

    if user.Credit >= total_price:
        if product.Quantity >= quantity:
            Order.add(Customer=user.Username, ProductID=product.ID, Quantity=quantity)

            Product.df.loc[Product.df['ID'] == product.ID, 'Quantity'] -= quantity
            Product.save_df()

            User.df.loc[User.df['Username'] == user.Username, 'Credit'] -= total_price
            User.df.loc[User.df['Username'] == product.Seller, 'Credit'] += (total_price * .8)
            User.save_df()

            print("Your order has been placed. Your total price is", str(total_price))

        else:
            print(f"The product doesn't have enough quantity! (product quantity={product.Quantity})")
    else:
        print(f"You don't have enough credit to pay the order! (your credit={user.Credit})")


def order_history(user):
    for idx, order in Order.df.iterrows():
        if order.Customer == user.Username:
            print(Order.get_str(order))


def charge_wallet(user):
    amount = float(input(' Enter the amount: '))
    if amount > 200_000:
        print(' The maximum amount is 200_000!')
        return

    User.df.loc[User.df['Username'] == user.Username, 'Credit'] += amount
    User.save_df()
    print(' Your wallet has been charged successfully')


def view_profile(user):
    print(' Full Name: ', user.FirstName, user.LastName)
    print(' Username: ', user.Username)
    print(' Role: ', user.Role)
    print(' Credit: ', user.Credit)


def edit_profile(user):
    new_first_name = input(" Enter new first name (or leave blank to ignore): ")
    if new_first_name:
        if len(new_first_name) >= 3:
            User.df.loc[User.df['Username'] == user.Username, 'FirstName'] = new_first_name
        else:
            print(' First name must contains at least 3 characters')

    new_last_name = input(" Enter new last name (or leave blank to ignore): ")
    if new_last_name:
        if len(new_last_name) >= 3:
            User.df.loc[User.df['Username'] == user.Username, 'LastName'] = new_last_name
        else:
            print(' Last name must contains at least 3 characters')

    new_password = input(" Enter new password (or leave blank to ignore): ")
    if new_password:
        if User.password_verifier(new_password):
            User.df.loc[User.df['Username'] == user.Username, 'Password'] = hashlib.md5(new_password.encode()).hexdigest()
        else:
            print(' Password must be including at least 8 both of upper/lower case characters and numbers!')

    User.save_df()
    print(' Your profile updated successfully')


def edit_product(user):
    user_products = Product.df.loc[Product.df['Seller'] == user.Username]
    user_products_info = list(map(Product.get_str, list(map(operator.itemgetter(1), user_products.iterrows()))))
    product_idx = select_item(user_products_info, "Select desired product: ", 'Your Products')
    product = user_products.iloc[product_idx]
    
    new_name = input(' Enter new name: ')
    if new_name:
        Product.df.loc[Product.df['ID'] == product.ID, 'Name'] = new_name

    new_price = input(' Enter new price: ')
    if new_price:
        Product.df.loc[Product.df['ID'] == product.ID, 'Price'] = float(new_price)

    new_quantity = input(' Enter new quantity: ')
    if new_quantity:
        Product.df.loc[Product.df['ID'] == product.ID, 'Quantity'] = int(new_quantity)


def view_credit(user):
    print(f" Your Credit: {user.Credit}")


def add_product(user):
    name = input(' Enter the name: ')
    price = float(input(' Enter the price: '))
    quantity = int(input(' Enter the quantity: '))

    Product.add(ID=hash(user.Username + name), Name=name, Seller=user.Username, Price=price, Quantity=quantity)


def view_sold_products(user):
    product_ids = Product.df.loc[Product.df['Seller'] == user.Username, 'ID'].values.tolist()
    for idx, order in Order.df[Order.df['ProductID'].isin(product_ids)].iterrows():
        product = Product.df[Product.df['ID'] == order.ProductID].iloc[0]
        print(Product.get_str(product))



customer_menu = {
    'View Menu': lambda _: view_menu(),
    'Place Order': place_order,
    'Order History': order_history,
    'Charge Wallet': charge_wallet,
    'View Profile': view_profile,
    'Edit Profile': edit_profile,
    'Logout': lambda _: error(SystemError)
}

seller_menu = {
    'Add Product': add_product,
    'View Sold Products': view_sold_products,
    'View Credit': view_credit,
    'View Profile': view_profile,
    'Edit Profile': edit_profile,
    'Edit Product': edit_product,
    'Logout': lambda _: error(SystemError)
}

main_menu = {
    'Sign In': signin,
    'Sign Up': signup,
    'Exit': exit
}

User.load_df()
Product.load_df()
Order.load_df()


if __name__ == "__main__":
    while True:
        print('-' * 50)
        index = select_item(main_menu.keys(), prompt='Select desired operation: ', title='Main Menu')
        function = list(main_menu.values())[index]
        function()
