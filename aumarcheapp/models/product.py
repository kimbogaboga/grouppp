from aumarcheapp.config.mysqlconnection import connectToMySQL
from flask import flash
from aumarcheapp.models import user

class Product:
    db_name = 'aumarche'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.product_title = db_data['product_title']
        self.description = db_data['description']
        self.materials = db_data['materials']
        self.price = db_data['price']
        self.images = db_data['images']
        self.video = db_data['video']
        self.quantity = (db_data['quantity'])
        self.notes = db_data['notes']
        self.date = db_data['date']
        self.duration = (db_data['duration'])
        self.user_id = None

    @classmethod
    def save1(cls,data):
        query = "INSERT INTO products (product_title, description, materials, price, images, video, quantity, notes, user_id) VALUES (%(product_title)s,%(description)s,%(materials)s,%(price)s,%(images)s, %(video)s,%(quantity)s, %(notes)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def save2(cls,data):
        query = "UPDATE products SET date = %(date)s, duration = %(duration)s WHERE user_id =  %(user_id)s AND products.date IS NULL AND products.duration IS NULL"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM products;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_products = []
        for row in results:
            all_products.append( cls(row) )
        return all_products

    @classmethod
    def get_all_complete(cls, data):
        query = "SELECT * FROM products JOIN users ON products.user_id = users.id WHERE users.id = %(id)s AND products.date IS NULL AND products.duration IS NULL"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        new_products = []
        if len(results) ==0:
            return new_products
        else:
            for product in results:
                user_data ={
                    'id' : product['id'],
                    'first_name' : product['first_name'],
                    'last_name' : product['last_name'],
                    'company' : product['company'],
                    'jobtitle' : product['jobtitle'],
                    'email' : product['email'],
                    'phonenumber' : product['phonenumber'],
                    'website' : product['website'],
                    'password' : product['password'],
                    'created_at' : product['created_at'],
                    'updated_at' : product['updated_at'],
                }
                userhere = user.User(user_data)
                new_product = cls(product)
                new_product.user_id = userhere
                new_products.append(new_product)
            return new_products

    @classmethod
    def get_all_products(cls, data):
        query = "SELECT * FROM products JOIN users ON products.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        new_products = []
        if len(results) ==0:
            return new_products
        else:
            for product in results:
                user_data ={
                    'id' : product['id'],
                    'first_name' : product['first_name'],
                    'last_name' : product['last_name'],
                    'company' : product['company'],
                    'jobtitle' : product['jobtitle'],
                    'email' : product['email'],
                    'phonenumber' : product['phonenumber'],
                    'website' : product['website'],
                    'password' : product['password'],
                    'created_at' : product['created_at'],
                    'updated_at' : product['updated_at'],
                }
                userhere = user.User(user_data)
                new_product = cls(product)
                new_product.user_id = userhere
                new_products.append(new_product)
            return new_products

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_one_complete(cls,data):
        query = "SELECT * FROM products JOIN users ON products.user_id = users.id WHERE products.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        product = cls(results[0])
        user_data ={
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'company' : results[0]['company'],
            'jobtitle' : results[0]['jobtitle'],
            'email' : results[0]['email'],
            'phonenumber' : results[0]['phonenumber'],
            'website' : results[0]['website'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        }
        userhere = user.User(user_data)
        product.user_id = userhere
        return product

    @classmethod
    def update(cls, data):
        query = "UPDATE products SET product_title=%(product_title)s, description=%(description)s, materials = %(materials)s,price = %(price)s, images = %(images)s, video = %(video)s, quantity = %(quantity)s, notes = %(notes)s, user_id = %(user_id)s WHERE products.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_product(data):
        is_valid = True
        if len(data['product_title']) < 2:
            is_valid = False
            flash("Product title must be at least 2 characters", "product")
        if len(data['description']) > 100:
            is_valid = False
            flash("Location must be at most 100 characters", "product")
        if len(data['materials'])<2:
            is_valid = False
            flash("Materials must be at least 2 characters", "product")
        if len(data['images'])<1:
            is_valid = False
            flash("You need to upload at least one image", "product")
        if int(data['quantity'])<0:
            is_valid = False
            flash("Minimum quantity must be more than 0", "product")
        if int(data['price'])<0:
            is_valid = False
            flash("Price must be more than 0", "product")
        return is_valid

    @staticmethod
    def validate_project(data):
        is_valid = True
        if int(data['duration'])>60:
            is_valid = False
            flash("Duration must be shorter than 60 days", "project")
        return is_valid