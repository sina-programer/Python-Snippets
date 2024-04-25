from abc import ABC, abstractmethod
import pandas as pd
import operator
import getpass
import hashlib
import random
import string
import os
import re


class DF:
    def __init__(self, path, header=None, load=True):
        self.df = None
        self.path = path
        self.header = header

        if load:
            self.load()

    def load(self):
        if os.path.exists(self.path):
            self.df = pd.read_csv(self.path)
        else:
            self.df = pd.DataFrame(columns=self.header)
            self.save()

    def add_row(self, **params):
        new_row = pd.Series(params)
        self.df = pd.concat([self.df, new_row.to_frame().T], ignore_index=True)
        self.save()

    def save(self):
        self.df.to_csv(self.path, index=False)


Users = DF('users.csv', ['FirstName', 'LastName', 'Username', 'Password', 'Credit', 'Role'])
Products = DF("products.csv", ['ID', 'Name', 'Seller', 'Price', 'Quantity'])
Orders = DF("orders.csv", ['Customer', 'ProductID', 'Quantity'])


class Menu(ABC):

    @property
    @abstractmethod
    def title(self): return str

    @property
    @abstractmethod
    def items(self): return list

    @classmethod
    def choose(cls, text='Choose desired item: '):
        print('\n', cls.title, '\n', sep='')

        for i, item in enumerate(cls.items, start=1):
            print(f"{i}. {item.__name__}")

        idx = input(f"\n{text}")

        while True:
            try:
                idx = int(idx)
                assert 1 <= idx <= len(cls.items)
                return cls.items[idx - 1]

            except Exception:
                print(f'\n"{idx}" is not a valid index!')
                idx = input('\nPlease enter a valid index: ')

    @classmethod
    def loop(cls, splitter='-'*50, **params):
        while True:
            print(splitter)
            cls.choose()(**params)


class MainMenu(Menu):
    title = 'Main Menu'

    @staticmethod
    def sign_in():
        username = input("Username: ")
        if username not in Users.df['Username'].values:
            print('Invalid Username!')
            return

        user = Users.df[Users.df['Username'] == username].iloc[0]

        password = getpass.getpass("Password: ")
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if user.Password != hashed_password:
            print("Invalid Password!")
            return

        if user.Role == "customer":
            menu = CustomerMenu
        else:
            menu = SellerMenu  

        while True:
            print('\n', '-' * 40)
            function = menu.choose(text='Select desired operation: ')
            user = Users.df[Users.df['Username'] == username].iloc[0]

            try:
                function(user)
            except SyntaxError:
                break

    @staticmethod
    def sign_up():
        first_name = input('First Name: ')
        if len(first_name) < 3:
            print('First-Name must be at least 3 characters!')
            return

        last_name = input('Last Name: ')
        if len(last_name) < 3:
            print('Last-Name must be at least 3 characters!')
            return

        password = getpass.getpass('Password: ')
        if not password_checker(password):
            print('Password must be including at least 8 both of upper/lower case characters and numbers!')
            return

        password_confirm = getpass.getpass('Confirm Password: ')
        if password_confirm != password:
            print('<password> & <password-confirm> do not match together!')
            return

        kind = input('What kind of account you want (1=seller, 2=customer)? ')
        if kind == '1':
            role = 'seller'
        elif kind == '2':
            role = 'customer'
        else:
            role = 'unknown'

        username = username_generator(first_name)
        print(f'Your username: {username}')

        Users.add_row(FirstName=first_name, LastName=last_name, Username=username, Role=role, Credit=0, Password=hashlib.md5(password.encode()).hexdigest())

    @staticmethod
    def quit():
        exit()

    items = [sign_in, sign_up, quit]


class SellerMenu(Menu):
    title = 'Seller Menu'

    @staticmethod
    def add_product(user):
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        quantity = int(input('Enter the quantity: '))

        Products.add_row(ID=hash(user.Username + name), Name=name, Seller=user.Username, Price=price, Quantity=quantity)

    @staticmethod
    def view_sold_products(user):
        product_ids = Products.df.loc[Products.df['Seller'] == user.Username, 'ID'].values.tolist()
        for idx, order in Orders.df[Orders.df['ProductID'].isin(product_ids)].iterrows():
            print(get_order_info(order))

    @staticmethod
    def view_credit(user):
        print(f"Your Credit: {user.Credit}")

    @staticmethod
    def view_profile(user):
        print('Full Name: ', user.FirstName, user.LastName)
        print('Username: ', user.Username)
        print('Role: ', user.Role)
        print('Credit: ', user.Credit)

    @staticmethod
    def edit_profile(user):
        new_first_name = input("Enter new first name (or leave blank to ignore): ")
        if new_first_name:
            if len(new_first_name) >= 3:
                Users.df.loc[Users.df['Username'] == user.Username, 'FirstName'] = new_first_name
            else:
                print('First name must contains at least 3 characters')

        new_last_name = input("Enter new last name (or leave blank to ignore): ")
        if new_last_name:
            if len(new_last_name) >= 3:
                Users.df.loc[Users.df['Username'] == user.Username, 'LastName'] = new_last_name
            else:
                print('Last name must contains at least 3 characters')

        new_password = input("Enter new password (or leave blank to ignore): ")
        if new_password:
            if password_checker(new_password):
                Users.df.loc[Users.df['Username'] == user.Username, 'Password'] = hashlib.md5(new_password.encode()).hexdigest()
            else:
                print('Password must be including at least 8 both of upper/lower case characters and numbers!')

        Users.save()
        print('Your profile updated successfully')

    @staticmethod
    def edit_product(user):
        user_products = Products.df.loc[Products.df['Seller'] == user.Username]
        user_products_info = list(map(get_product_info, list(map(operator.itemgetter(1), user_products.iterrows()))))
        for i, product_info in enumerate(user_products_info):
            print(f"{i+1}. {product_info}")
        product_idx = int(input('Choose desired product: ')) - 1
        product = user_products.iloc[product_idx]

        new_name = input('Enter new name (or leave blank to ignore): ')
        if new_name:
            Products.df.loc[Products.df['ID'] == product.ID, 'Name'] = new_name

        new_price = input('Enter new price (or leave blank to ignore): ')
        if new_price:
            Products.df.loc[Products.df['ID'] == product.ID, 'Price'] = float(new_price)

        new_quantity = input('Enter new quantity (or leave blank to ignore): ')
        if new_quantity:
            Products.df.loc[Products.df['ID'] == product.ID, 'Quantity'] = int(new_quantity)

        Products.save()
        print('The product updated successfully!')

    def logout(_):
        raise SyntaxError

    items = [add_product, view_sold_products, view_credit, view_profile, edit_profile, edit_product, logout]


class CustomerMenu(Menu):
    title = 'Customer Menu'

    @staticmethod
    def view_menu(_):
        for product_info in get_all_products_info():
            print(product_info)

    @staticmethod
    def place_order(user):
        products_info = get_all_products_info()
        for i, info in enumerate(products_info):
            print(f"{i+1}. {info}")

        product_id = int(input('Enter the index of product: ')) - 1
        product = Products.df.iloc[product_id]
        quantity = int(input('Enter the quantity: '))
        total_price = product.Price * quantity

        if user.Credit >= total_price:
            if product.Quantity >= quantity:
                Orders.add_row(Customer=user.Username, ProductID=product.ID, Quantity=quantity)

                Products.df.loc[Products.df['ID'] == product.ID, 'Quantity'] -= quantity
                Products.save()

                Users.df.loc[Users.df['Username'] == user.Username, 'Credit'] -= total_price
                Users.df.loc[Users.df['Username'] == product.Seller, 'Credit'] += (total_price * .8)
                Users.save()

                print("Your order has been placed. Your total price is", str(total_price))

            else:
                print(f"The product doesn't have enough quantity! (product quantity={product.Quantity})")
        else:
            print(f"You don't have enough credit to pay the order! (your credit={user.Credit})")

    @staticmethod
    def order_history(user):
        for idx, order in Orders.df.iterrows():
            if order.Customer == user.Username:
                print(get_order_info(order))

    @staticmethod
    def charge_wallet(user):
        amount = float(input('Enter the amount: '))
        if amount > 200_000:
            print('The maximum amount is 200_000!')
            return

        Users.df.loc[Users.df['Username'] == user.Username, 'Credit'] += amount
        Users.save()
        print('Your wallet has been charged successfully')

    items = [view_menu, place_order, order_history, charge_wallet, SellerMenu.view_profile, SellerMenu.edit_profile, SellerMenu.logout]



def password_checker(password, regex=r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}"):
    return bool(re.match(regex, password))


def username_generator(name, length=4, chars=string.ascii_letters):
    username = name + '_' + ''.join(random.choices(chars, k=length))
    while username in Users.df['Username'].values:
        username = name + '_' + ''.join(random.choices(chars, k=length))

    return username


def get_order_info(order):
    product = Products.df[Products.df['ID'] == order.ProductID].iloc[0]
    return f"{product.Name} ({product.Seller}): {product.Price} (×{order.Quantity})"


def get_product_info(product):
    return f'{product.Name} ({product.Seller}): {product.Price} (×{product.Quantity})'


def get_all_products_info():
    return list(map(get_product_info, list(map(operator.itemgetter(1), Products.df.iterrows()))))



if __name__ == "__main__":
    MainMenu.loop(splitter='='*50)
