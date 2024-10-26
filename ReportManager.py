from datetime import datetime

class ReportService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def show_all_bill_records_today(self):
        today_date = datetime.today()
        bill_date = today_date.strftime("%Y-%m-%d")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesbill WHERE billdate=%s", (bill_date,))
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


    def price_analysis(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT  product.pname, price.productId, price.startDate, price.price, LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate) AS previous_price, (price.price - LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate)) AS price_change FROM price INNER JOIN product ON price.productId=product.pcode")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------|") 
            print('| Product Code: ',x[1])
            print('| Product Name: ',x[0])
            print('| startDate: ',x[2])
            print('| price: ',x[3])
            print('| previous_price: ',x[4])
            print("|--------------------------------|")
            print('| price_change: ',x[5])
            print("|--------------------------------|") 
        print("--------------End Report--------------")


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
        self.db_connection.get_cursor().execute("SELECT salesbill.branchid, branch.branchName, YEAR(salesbill.billdate) AS year, WEEK(salesbill.billdate) AS week, SUM(salesbill.billTotal) AS total_sales FROM salesbill INNER JOIN branch ON salesbill.branchid = branch.brid GROUP BY salesbill.branchid, YEAR(salesbill.billdate), WEEK(salesbill.billdate) ORDER BY salesbill.branchid, year, week")
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
        self.db_connection.get_cursor().execute("SELECT branchid, COUNT(billcode) AS number_of_sales, SUM(total_sales) AS total_sales_amount, AVG(total_sales) AS average_sales_amount, MIN(total_sales) AS minimum_sales_amount, MAX(total_sales) AS maximum_sales_amount FROM (SELECT billcode, branchid, SUM(billTotal) AS total_sales FROM salesbill GROUP BY billcode, branchid) AS sales_per_bill GROUP BY branchid ORDER BY branchid")
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