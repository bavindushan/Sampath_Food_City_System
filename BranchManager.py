class BranchService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_branch(self):
        bcode = input("Enter Branch Code: ")
        bname = input("Enter Branch Name: ")
        badd = input("Enter Branch Address: ")
        bmanager = input("Enter Branch Manager: ")
        bemp = input("Enter Total Employee Count of the Branch: ")

        self.db_connection.connect()
        sql = "INSERT INTO branch (brid, branchName, address, branchManager, totalEmployees) VALUES (%s, %s, %s, %s, %s)"
        val = (bcode, bname, badd, bmanager, bemp)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        self.db_connection.close()
        print("New Branch record added successfully..")

    def delete_branch(self):
        bcode = input("Enter Branch Code: ")
        self.db_connection.connect()
        sql = "DELETE FROM branch WHERE brid=%s"
        self.db_connection.get_cursor().execute(sql, (bcode,))
        self.db_connection.commit()
        if self.db_connection.get_cursor().rowcount >= 1:
            print(f"{self.db_connection.get_cursor().rowcount} Branch record deleted successfully..")
        else:
            print("Sorry, try again...")
        self.db_connection.close()

    def update_branch(self):
        bcode = input("Enter Branch Code: ")
        bname = input("Enter Branch Name: ")
        badd = input("Enter Branch Address: ")
        bmanager = input("Enter Branch Manager: ")
        bemp = input("Enter Total Employee Count of the Branch: ")

        self.db_connection.connect()
        sql = "UPDATE branch SET branchName=%s, address=%s, branchManager=%s, totalEmployees=%s WHERE brid=%s"
        val = (bname, badd, bmanager, bemp, bcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        self.db_connection.close()
        print("Branch record updated successfully..")

    def search_branch(self):
        bcode = input("Enter Branch Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branch WHERE brid=%s", (bcode,))
        myresult = self.db_connection.get_cursor().fetchall()
        self.db_connection.close()
        for x in myresult:
            print("---------------------------------")
            print('| Branch ID: ', x[0])
            print('| Branch Name: ', x[1])
            print('| Branch Address: ', x[2])
            print('| Branch Manager: ', x[3])
            print('| Total Employee Count of the Branch: ', x[4])
            print("---------------------------------")
        print("--------------End Search Result--------------")

    def show_all_branches(self):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branch")
        myresult = self.db_connection.get_cursor().fetchall()
        self.db_connection.close()

        for x in myresult:
            print("---------------------------------")
            print('Branch Code: ', x[0], '| Branch Name: ', x[1], '| Address: ', x[2], '| Manager: ', x[3], '| Branch Employee Count: ', x[4])
        print("--------------End Search Result--------------")

