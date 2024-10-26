from datetime import datetime
class SalesService:
    def __init__(self, db_connection, branch_id, user_id):
        self.db_connection = db_connection
        self.branch_id = branch_id
        self.user_id = user_id[0][0]

    def add_sales_item(self, bill_id)->float:
        pcode = input("Enter Product Code: ")
        pqty = input("Enter Product Qty: ")

        pdata = self.search_product_get_id_and_price(pcode)
        pid = pdata[0]
        pprice = pdata[1]
        ptotal = float(pprice) * float(pqty)
        
        pdata_stock = self.search_branch_product_for_stock(pid, self.branch_id)
        pb_id = pdata_stock[0]
        pb_qty_old = pdata_stock[1]
        pb_qty_new = float(pb_qty_old) - float(pqty)
        
        self.update_branch_product_for_stock(pb_id, pb_qty_new)
        self.db_connection.connect()
        
        sql = "INSERT INTO salesitem (billId, qty, price, total, branchproductid) VALUES (%s, %s, %s, %s, %s)"
        val = (bill_id, pqty, pprice, ptotal, pb_id)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        
        print("New Sales Item record added successfully..")
        return ptotal
    

     
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

    
    def update_branch_product_for_stock(self,bpid,proqty):
        self.db_connection.connect()
        sql = "UPDATE branchproduct SET branchqty=%s where bpid=%s"
        val = (proqty,bpid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Branch Product record updated successfully..")


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


    def add_sales(self):
        bcode = input("Enter Bill Code: ")
        bdis = float(input("Enter Discount: "))
        ptype = input("Enter Payment Type: ")
        pcount = int(input("Enter Product Type Count: "))
        
        bill_total = 0
        for _ in range(pcount):
            bill_total += self.add_sales_item(bcode)

        print("Bill Total: ", bill_total)
        today_date = datetime.today().strftime("%Y-%m-%d")
        print("Bill Date: ", today_date)
        total_after_discount = bill_total - (bdis * bill_total)
        print("Bill Discount: ", total_after_discount)

        self.db_connection.connect()
        sql = "INSERT INTO salesbill (billcode, billdate, billTotal, discount, totalAfterDiscount, paymentType, userId, branchid ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (bcode, today_date, bill_total, bdis, total_after_discount, ptype, self.user_id, self.branch_id)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        
        print("New Bill record added successfully..")


    def search_sales_bill_item(self, billcode):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesitem WHERE billId=%s", (billcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        icount = 0
        for x in myresult:
            icount += 1
            print("--Bill Item(",str(icount),")--------") 
            print('|      Branch Product Id: ', x[5])
            print('|      Qty: ', x[2])
            print('|      Price: ', x[3])
            print('|      Total: ', x[4])
            print("---------------------------------------")

    def search_sales_bill(self):
        billcode = input("Enter Bill Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesbill WHERE billcode=%s", (billcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:
            print("--------------------------------------") 
            print('| Bill Code: ', x[0])
            print('| Date: ', x[1])
            print('| Total: ', x[2])
            print('| Discount: ', x[3])
            print('| Bill Total(After Discount): ', x[4])
            print('| Payment Type: ', x[5])
            print('| Branch ID: ', x[6])
            print('| Staff: ', x[7])
        self.search_sales_bill_item(billcode)
        print("--------------End Search Result--------------")


    def show_all_bill_records_today(self):
        today_date = datetime.today().strftime("%Y-%m-%d")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesbill WHERE billdate=%s", (today_date,))
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("--------------------------------------") 
            print('| Bill Code: ', x[0])
            print('| Date: ', x[1])
            print('| Branch: ', x[6])
            print('| User Id: ', x[7])
            print('| Total:                 ', x[2])
            print('| Discount:              ', x[3])
            print('| ------------------------------------') 
            print('| Total(After Discount): ', x[4])
            print("--------------------------------------")   
        print("-----------End Search Result-------------")


    def monthly_sales_analysis(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT branchid, YEAR(billdate) AS year, MONTH(billdate) AS month, SUM(billTotal) AS total_bill FROM salesbill GROUP BY branchid, YEAR(billdate), MONTH(billdate) ORDER BY branchid, YEAR(billdate), MONTH(billdate)")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------|") 
            print('| Branch Id: ', x[0])
            print('| Year: ', x[1])
            print('| Month: ', x[2])
            print("|--------------------------------|")
            print('| Total Sales: ', x[3])
            print("|--------------------------------|") 
        print("--------------End Report--------------")


    def weekly_sales_analysis(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT salesbill.branchid, branch.branchName, YEAR(salesbill.billdate) AS year,  WEEK(salesbill.billdate) AS week, SUM(salesbill.billTotal) AS total_sales FROM salesbill INNER JOIN branch ON salesbill.branchid = branch.brid GROUP BY salesbill.branchid, YEAR(salesbill.billdate), WEEK(salesbill.billdate) ORDER BY salesbill.branchid, year, week")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------|") 
            print('| Branch Id: ', x[0])
            print('| Branch Name: ', x[1])
            print('| Year: ', x[2])
            print('| Week: ', x[3])
            print("|--------------------------------|")
            print('| Total Sales: ', x[4])
            print("|--------------------------------|") 
        print("--------------End Report--------------")


    def sales_product_preferences(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT si.branchproductid, SUM(si.qty) AS total_quantity_sold, COUNT(DISTINCT si.billId) AS number_of_sales, SUM(si.total) AS total_revenue FROM salesitem si JOIN salesbill yt ON si.billId = yt.billcode GROUP BY si.branchproductid ORDER BY total_quantity_sold DESC")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------|") 
            print('| Branch Product Id: ', x[0])
            print('| Total Sold Qty: ', x[1])
            print('| Bill Count: ', x[2])
            print("|--------------------------------|")
            print('| Product Total Sold Amount: ', x[3])
            print("|--------------------------------|") 
        print("--------------End Report--------------")

    def final_sales_analysis(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT  branchid, COUNT(billcode) AS number_of_sales, SUM(total_sales) AS total_sales_amount, AVG(total_sales) AS average_sales_amount, MIN(total_sales) AS minimum_sales_amount, MAX(total_sales) AS maximum_sales_amount FROM (SELECT billcode, branchid,SUM(billTotal) AS total_sales FROM  salesbill GROUP BY billcode, branchid) AS sales_per_bill GROUP BY branchid ORDER BY branchid")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------|") 
            print('| Branch Id: ', x[0])
            print('| No of Sales: ', x[1])
            print('| Total Sales Amount: ', x[2])  
            print("|--------------------------------|")
            print('| Minimum Sales Amount: ', x[4])
            print('| Average Sales Amount: ', x[3])
            print('| Maximum Sales Amount: ', x[5])
            print("|--------------------------------|") 
        print("--------------End Report--------------")
