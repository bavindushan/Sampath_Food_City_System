class BranchProductService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_branch_product(self):
        bcode = input("Enter Branch Code: ")
        proid = input("Enter Product Id: ")
        proqty = input("Enter Product Qty: ")

        cursor = self.db_connection.get_cursor()
        sql = "INSERT INTO branchproduct (branchId, productId, branchqty) VALUES (%s, %s, %s)"
        val = (bcode, proid, proqty)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("New Branch Product record added successfully.")

    def search_branch_product(self):
        bcode = input("Enter Branch Code: ")
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct where branchId='" + bcode + "'")
        myresult = cursor.fetchall()
        for x in myresult:
            print("----------------------------")
            print('| BranchProduct ID: ', x[0])
            print('| Branch ID: ', x[1])
            print('| Product ID: ', x[2])
            print('| Product Qty: ', x[3])
            print("----------------------------")
        print("--------------End Search Result--------------")

    def search_branch_product_by_product_id(self, pid, bid):
        pid = str(pid)
        bid = str(bid)
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct where productId='" + pid + "' and branchId = '" + bid + "' ")
        myresult = cursor.fetchall()
        for x in myresult:
            pbId = int(x[0])
            return pbId

    def search_branch_product_for_stock(self, pid, bid):
        pid = str(pid)
        bid = str(bid)
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct where productId='" + pid + "' and branchId = '" + bid + "' ")
        myresult = cursor.fetchall()
        for x in myresult:
            pid = x[0]
            pqty = x[3]
            pdata = [pid, pqty]
            return pdata

    def delete_branch_product(self):
        bcode = input("Enter Branch Code: ")
        prid = input("Enter Product Id: ")
        cursor = self.db_connection.get_cursor()
        sql = "DELETE FROM branchproduct where branchId='" + bcode + "' and productId = '" + prid + "'"
        cursor.execute(sql)
        self.db_connection.commit()
        if cursor.rowcount >= 1:
            print(cursor.rowcount, " Branch Product record deleted successfully.")
        else:
            print("Sorry, try again.")

    def update_branch_product(self):
        bcode = input("Enter Branch Code: ")
        proid = input("Enter Product ID: ")
        proqty = input("Enter Correct Product Qty: ")

        cursor = self.db_connection.get_cursor()
        sql = "UPDATE branchproduct SET branchqty=%s where branchId=%s and productId=%s"
        val = (proqty, bcode, proid)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("Branch Product record updated successfully.")

    def update_branch_product_for_stock(self, bpid, proqty):
        cursor = self.db_connection.get_cursor()
        sql = "UPDATE branchproduct SET branchqty=%s where bpid=%s"
        val = (proqty, bpid)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("Branch Product record updated successfully.")

    def show_all_branch_products(self):
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct")
        myresult = cursor.fetchall()

        for x in myresult:
            print("---------------------------------")
            print('Branch Product Code: ', x[0], '| Branch Code: ', x[1], '| Product Id: ', x[2], '| Product Qty: ',x[3])
        print("--------------End Search Result--------------")



