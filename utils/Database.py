import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_categories(self):
        categories = self.cursor.execute('SELECT id , cat_name FROM categories;')
        return categories.fetchall()

    def add_category(self, new_category):
        try:
            self.cursor.execute(
                "INSERT INTO categories(cat_name) VALUES(?);",
                (new_category,)
            )
            self.conn.commit()
            return True
        except:
            return False

    def rename_category(self, old_name, new_name):
        try:
            self.cursor.execute(
                "UPDATE categories SET cat_name=? WHERE cat_name=?;",
                (new_name, old_name)
            )
            self.conn.commit()
            return True
        except:
            return False

    def delete_category(self, name):
        try:
            self.cursor.execute(
                "DELETE FROM categories WHERE cat_name=?;",
                (name,)
            )
            self.conn.commit()
            return True
        except:
            return False

    def check_category_exists(self, name):
        lst = self.cursor.execute(
            f"SELECT * FROM categories WHERE cat_name=?",
            (name,)
        ).fetchall()
        if not lst:
            return True
        else:
            return False

    def get_products(self):
        products = self.cursor.execute('SELECT p_id, p_name FROM products;')
        return products.fetchall()

    def add_product(self, p_cat_id,p_name,p_text,p_owner,p_phone,p_price,p_image):
        try:
            self.cursor.execute(
                "INSERT INTO products ( p_cat_id,p_name,p_text,p_owner,p_phone,p_price,p_image) VALUES(?,?,?,?,?,?,?)",
                (p_cat_id,p_name,p_text,p_owner,p_phone,p_price,p_image)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f' error {e}')
            return False

    def rename_product(self, old_name, new_name):
        try:
            self.cursor.execute(
                "UPDATE product SET product_name=? WHERE product_name=?;",
                (new_name, old_name)
            )
            self.conn.commit()
            return True
        except:
            return False

    def delete_product(self, n):
        try:
            self.cursor.execute(
                "DELETE FROM products WHERE p_id=?;",
                (n,)
            )
            self.conn.commit()
            return True
        except:
            return False

    def check_product_exists(self, name):
        lst = self.cursor.execute(
            f"SELECT * FROM products WHERE product_name=?",
            (name,)
        ).fetchall()
        if not lst:
            return True
        else:
            return False


    def get_my_last_pr(self,u_id):
        try:
            product = self.cursor.execute(
                f'select p_name,p_text,p_phone,p_price,p_image from products where p_owner = ? order by p_id desc limit 1;',
                (u_id,)
            ).fetchone()
            return product

        except Exception as e:
            print(f'error {e}')



    def get_ad_pr(self,u_id):
        try:
            product = self.cursor.execute(
                f'select p_name,p_text,p_phone,p_price,p_image from products where p_owner = ? order by p_id desc limit 1;',
                (u_id,)
            ).fetchone()
            return product

        except Exception as e:
            print(f'error {e}')



