class SupplierService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def search_supplier(self):
        sid = input("Enter Supplier Id: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM supplier where supid=%s", (sid,))
        myresult = self.db_connection.get_cursor().fetchall()
        for x in myresult:
            print("---------------------------------") 
            print('| Supplier ID: ', x[0])
            print('| Supplier Name: ', x[1])
            print('| Supplier Address: ', x[2])
            print('| Supplier NIC: ', x[3])
            print('| Supplier Tel: ', x[4])
            print('| Supplier Email: ', x[5])
        print("--------------End Search Result--------------")

    def show_all_supplier_details(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM supplier")
        myresult = self.db_connection.get_cursor().fetchall()

        for x in myresult:
            print("---------------------------------") 
            print('| Supplier Id: ', x[0])
            print('| Name: ', x[1])
            print('| Address: ', x[2])
            print('| NIC: ', x[3],'| Tel: ', x[4])
            print('| Email: ', x[5])  
        print("--------------End Search Result--------------")

    def update_supplier(self):
        sid = input("Enter Supplier Id: ")
        supname = input("Enter Supplier Name: ")
        sup_address = input("Enter Supplier Address: ")
        sup_nic = input("Enter Supplier NIC: ")
        sup_tel = input("Enter Supplier Tel: ")
        sup_email = input("Enter Supplier Email: ")

        self.db_connection.connect()
        sql = "UPDATE supplier SET supName=%s, supAddress=%s, supNic=%s, supTel=%s, supEmail=%s where supid=%s"
        val = (supname, sup_address, sup_nic, sup_tel, sup_email, sid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Supplier record updated successfully..")

    def delete_supplier(self):
        sid = input("Enter Supplier Id: ")
        self.db_connection.connect()
        sql = "DELETE FROM supplier where supid=%s"
        self.db_connection.get_cursor().execute(sql, (sid,))
        self.db_connection.commit()
        if self.db_connection.get_cursor().rowcount >= 1:
            print(self.db_connection.get_cursor().rowcount, " Supplier record deleted successfully..")
        else: 
            print("Sorry, no records found for deletion.")

    def add_supplier(self):
        supname = input("Enter Supplier Name: ")
        sup_address = input("Enter Supplier Address: ")
        sup_nic = input("Enter Supplier NIC: ")
        sup_tel = input("Enter Supplier Tel: ")
        sup_email = input("Enter Supplier Email: ")

        self.db_connection.connect()
        sql = "INSERT INTO supplier (supName, supAddress, supNic, supTel, supEmail) VALUES (%s, %s, %s, %s, %s)"
        val = (supname, sup_address, sup_nic, sup_tel, sup_email)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New supplier record added successfully..")

