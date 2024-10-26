from datetime import datetime

class StockService:
    def __init__(self, db_connection, branch_id, user_id):
        self.db_connection = db_connection
        self.branch_id = branch_id
        self.user_id = user_id[0][0]

   
    def search_product_get_id_and_price(self,pcode)-> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product where pcode='"+pcode+"'")
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:
            print("---------------------------------")
            print('| Product ID: ',x[0])
            print('| Product Name: ',x[1])
            print('| Product Unit: ',x[2])
            print('| Product Price: ',x[3])
            print('| Product Discount: ',x[4])
            print('| Product Price After Discount: ',x[5])
            print('| Product Code: ',x[6])
            print("---------------------------------")
            pid = x[0]
            pprice = x[3]
            pdata = [pid, pprice]
            return pdata


    def search_branch_product_for_stock(self,pid, bid)-> list: 
        pid = str(pid)
        bid = str(bid)

        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branchproduct where productId='"+pid+"' and branchId = '"+bid+"' ")
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:
            pid = x[0]
            pqty = x[3]
            pdata = [pid, pqty]
            return pdata


    def update_branch_product_for_stock(self,bpid,proqty):
        self.db_connection.connect()
        sql = "UPDATE branchproduct SET branchqty=%s where bpid=%s"
        val = (proqty,bpid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Branch Product record updated successfully..")

    def add_stock_item(self, grn_id) -> float:
        pcode = input("Enter Product Code: ")
        pqty = input("Enter Stock Qty: ")
        pprice = input("Enter Stock Price: ")
        ex_date = input("Enter Expire Date: ")
        mf_date = input("Enter MF Date: ")

        pdata = self.search_product_get_id_and_price(pcode)
        pid = pdata[0]
        ptotal = float(pprice) * float(pqty)
        pdata = self.search_branch_product_for_stock(pid, self.branch_id)
        pb_id = pdata[0]
        pb_qty_old = pdata[1]
        pb_qty_new = float(pb_qty_old) + float(pqty)
        self.update_branch_product_for_stock(pb_id, pb_qty_new)

        self.db_connection.connect()
        sql = "INSERT INTO stockitem (qty, stockPrice, expDate, mfDate, grnBillNo, branchproductid) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (pqty, pprice, ex_date, mf_date, grn_id, pb_id)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New Stock Item record added successfully..")
        return ptotal

    def search_stock_grn_item_details(self, billcode):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM stockitem where grnBillNo=%s", (billcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        icount = 0
        for x in myresult:
            icount += 1
            mytotal = float(x[2]) * float(x[1])
            print(f"--GRN Item({icount})--------") 
            print('|      Branch Product Id: ', x[6])
            print('|      Qty   : ', x[1])
            print('|      Price : ', x[2])
            print('|      Total : ', mytotal)
            print('|      EXP Date: ', x[3])
            print('|      MF Date: ', x[4])
            print("------------------------------------")

    def search_stock_grn_details(self):
        billcode = input("Enter GRN Bill Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM grn where grnBillNo=%s", (billcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:
            print("--------------------------------------|")
            print('| GRN Bill No: ', x[1])
            print('| Date: ', x[3])
            print('| Status: ', x[7])
            print('| Supplier ID: ', x[8])
            print('| Total                     : ', x[2])
            print('| Discount                  : ', x[4])
            print("|-------------------------------------|")
            print('| Bill Total(After Discount): ', x[5])
            print('| Paid Amount               : ', x[6])
            print("--------------------------------------|")
        self.search_stock_grn_item_details(billcode)
        print("--------------End Search Result--------------")

    def add_stock_details(self):
        grncode = input("Enter GRN Code: ")
        supid = input("Enter Supplier Id: ")
        stock_dis = float(input("Enter Discount: "))
        paid_amount = float(input("Enter Paid Amount: "))
        pcount = int(input("Enter Product Type Count: "))
        grn_total = 0
        for _ in range(pcount):
            grn_total += self.add_stock_item(grncode)

        bill_date = datetime.today().strftime("%Y-%m-%d")
        total_after_discount = grn_total - (stock_dis * grn_total)
        status = "Payment Not Complete"
        if total_after_discount == paid_amount:
            status = "Payment Complete"

        self.db_connection.connect()
        sql = "INSERT INTO grn (grnBillNo, total, date, discount, totalAfterDiscount, paidAmount, status, supplierId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (grncode, grn_total, bill_date, stock_dis, total_after_discount, paid_amount, status, supid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New GRN Bill record added successfully..")

    def show_all_stock_grn_records_today(self):
        bill_date = datetime.today().strftime("%Y-%m-%d")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM grn where date=%s", (bill_date,))
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:
            print("--------------------------------------") 
            print('| GRN Bill No: ', x[1])
            print('| Date: ', x[3])
            print('| Status: ', x[7])
            print('| Supplier Id: ', x[8])
            print('| Total:                 ', x[2])
            print('| Discount:              ', x[4])
            print('| ------------------------------------') 
            print('| Total(After Discount): ', x[5])
            print('| Paid Amount:           ', x[6])
            print("--------------------------------------")   
        print("-----------End Search Result-------------")

    def search_stock_grn_payment_details(self, billcode) -> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM grn where grnBillNo=%s", (billcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:    
            paid_amount = x[6]
            bill_amount = x[5]
            pdata = [paid_amount, bill_amount]
            return pdata

    def update_stock_grn_payment(self):
        grncode = input("Enter GRN Code: ")
        pamount = float(input("Enter Newly Paid Amount: "))
        pdata = self.search_stock_grn_payment_details(grncode)
        pamount_old = pdata[0]
        bill_amount = pdata[1]
        total_paid = float(pamount_old) + pamount
        status = "Payment Not Complete"
        if total_paid == bill_amount:
            status = "Payment Complete"

        self.db_connection.connect()
        sql = "UPDATE grn SET paidAmount=%s, status=%s where grnBillNo=%s"
        val = (total_paid, status, grncode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("GRN Payment record updated successfully..")



