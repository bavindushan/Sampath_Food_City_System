from datetime import datetime

class ProductService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def search_product(self):
        pcode = input("Enter Product Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        
        for x in myresult:
            print("---------------------------------")
            print('| Product ID: ', x[0])
            print('| Product Name: ', x[1])
            print('| Product Unit: ', x[2])
            print('| Product Price: ', x[3])
            print('| Product Discount: ', x[4])
            print('| Product Price After Discount: ', x[5])
            print('| Product Code: ', x[6])
            print("---------------------------------")
        print("--------------End Search Result--------------")

    def search_product_get_id_and_price(self, pcode) -> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------")
            print('| Product ID: ', x[0])
            print('| Product Name: ', x[1])
            print('| Product Unit: ', x[2])
            print('| Product Price: ', x[3])
            print('| Product Discount: ', x[4])
            print('| Product Price After Discount: ', x[5])
            print('| Product Code: ', x[6])
            print("---------------------------------")
            pid = x[0]
            pprice = x[3]
            pdata = [pid, pprice]
            return pdata

    def show_all_products(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------") 
            print('| Product Code: ', x[6])
            print('| ID: ', x[0])
            print('| Name: ', x[1])
            print('| Unit: ', x[2])
            print('| Price: ', x[3])
            print('| Discount: ', x[4])
            print('| Price After Discount: ', x[5]) 
            print("---------------------------------") 
        print("--------------End Search Result--------------")

    def update_product(self):
        pcode = input("Enter Product Code: ")
        pname = input("Enter Product Name: ")
        unit = input("Enter Product unit: ")
        price = float(input("Enter Product Price: "))
        discount = float(input("Enter Product Discount: "))
        price_after_discount = price - (discount * price)

        self.db_connection.connect()
        sql = "UPDATE product SET pname=%s, unit=%s, price=%s, discount=%s, priceAfterDiscount=%s WHERE pcode=%s"
        val = (pname, unit, price, discount, price_after_discount, pcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Product record updated successfully..")

    def add_product_price_level(self, pcode, price):
        today_date = datetime.today()
        start_date = today_date.strftime("%Y-%m-%d")
        self.db_connection.connect()
        sql = "INSERT INTO price (productId, price, startDate) VALUES (%s, %s, %s)"
        val = (pcode, price, start_date)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Product price level record added successfully..")

    def update_product_price_level(self):
        pcode = input("Enter Product Code: ")
        price = float(input("Enter Product Price: "))

        self.db_connection.connect()
        sql = "UPDATE product SET price=%s WHERE pcode=%s"
        val = (price, pcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Product price level change updated successfully..")
        self.add_product_price_level(pcode, price)

    def price_analysis(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT  product.pname, price.productId, price.startDate, price.price, 
                    LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate) AS previous_price, 
                    (price.price - LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate)) AS price_change 
            FROM price 
            INNER JOIN product ON price.productId=product.pcode
        """)
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------|") 
            print('| Product Code: ', x[1])
            print('| Product Name: ', x[0])
            print('| startDate: ', x[2])
            print('| price: ', x[3])
            print('| previous_price: ', x[4])
            print("|--------------------------------|")
            print('| price_change: ', x[5])
            print("|--------------------------------|") 
        print("--------------End Report--------------")

    def delete_product(self):
        pcode = input("Enter Product Code: ")
        self.db_connection.connect()
        sql = "DELETE FROM product WHERE pcode=%s"
        self.db_connection.get_cursor().execute(sql, (pcode,))
        self.db_connection.commit()
        if self.db_connection.get_cursor().rowcount >= 1:
            print(self.db_connection.get_cursor().rowcount, " Product record deleted successfully..")
        else:
            print("Sorry, try again...")

    def add_branch_product_for_new_product(self, bcode, proid):
        proqty = "0"
        self.db_connection.connect()
        sql = "INSERT INTO branchproduct (branchId, productId, branchqty) VALUES (%s, %s, %s)"
        val = (bcode, proid, proqty)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New Branch Product record added successfully..")

    def all_branch_product_for_new_product(self, pcode):
        pdata = self.search_product_get_id_and_price(pcode)
        proid = pdata[0]
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branch")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------") 
            print('Branch Code: ', x[0], '| Branch Name: ', x[1])
            bcode = x[0]
            self.add_branch_product_for_new_product(bcode, proid)

    def add_product(self):
        pcode = input("Enter Product Code: ")
        pname = input("Enter Product Name: ")
        unit = input("Enter Product unit: ")
        price = float(input("Enter Product Price: "))
        discount = float(input("Enter Product Discount: "))
        price_after_discount = price - (discount * price)

        self.db_connection.connect()
        sql = "INSERT INTO product (pname, unit, price, discount, priceAfterDiscount, pcode) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (pname, unit, price, discount, price_after_discount, pcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New product record added successfully..")
        self.add_product_price_level(pcode, price)
        self.all_branch_product_for_new_product(pcode)


