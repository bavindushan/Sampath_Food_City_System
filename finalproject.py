from DBConnection import DatabaseConnection,AuthenticationService
from BranchManager import BranchService
from ProductManager import ProductService
from BranchProductManger import BranchProductService
from SalesManager import SalesService
from SupplierManager import SupplierService
from StockManager import StockService
from ReportManager import ReportService


def main_menu():
    db_connection = DatabaseConnection()
    db_connection.connect()  

    auth_service = AuthenticationService(db_connection)
    product_service = ProductService(db_connection)
    branch_service = BranchService(db_connection)
    branch_product_service = BranchProductService(db_connection)
    supplier_service = SupplierService(db_connection)
    report_service = ReportService(db_connection)

    username = input("Enter username: ")
    password = input("Enter password: ")
    mybranch_id = 1
    # mybranch_id = input("Enter your Branch Code:")

    user = auth_service.authenticate(username, password)
    sales_service = SalesService(db_connection, mybranch_id, user)
    stock_service = StockService(db_connection, mybranch_id, user)
    
    if user:
        print("Logged in successfully...")
        while True:
            print("===========================================")
            print("               Main Menu                   ")
            print("===========================================")
            print("|  1 - Manage Product Details             |")
            print("|  2 - Manage Sales Details               |")
            print("|  3 - Manage Branch Details              |")
            print("|  4 - Manage Stock Details               |")
            print("|  5 - Manage Branch Product Details      |")
            print("|  6 - Manage Supplier Details            |")
            print("|  7 - Reports                            |")
            print("|  8 - Exit                               |")
            print("===========================================")
            choice = input("Enter your choice: ")

            if choice == "1":             
                manage_products(product_service)
            elif choice == "2":                
                manage_sales(sales_service)
            elif choice == "3":
                manage_branch(branch_service)
            elif choice == "4":
                manage_stock_details(stock_service)
            elif choice == "5":
                manage_branch_product(branch_product_service)
            elif choice == "6":
                manage_supplier_details(supplier_service)
            elif choice == "7":
                manage_reports(report_service)
            elif choice == "8":
                print("Exit...")
                break
            else:
                print("Invalid choice...")
    else:
        print("Invalid username and password...")

    db_connection.close()

def manage_products(product_service):
    print("---------Manage Product Details---------")
    print("|  1 - Add Product Details             |")
    print("|  2 - Search Product Details          |")
    print("|  3 - Delete Product Details          |")
    print("|  4 - Update Product Details          |")
    print("|  5 - Update Product Price Level      |")
    print("|  6 - Search All Products             |")
    print("|  7 - Exit(Back to Mainmenu)          |")
    print("----------------------------------------")
    choice = input("Enter your choice:")

    if choice == "1":
        print("Welcome to Add Product Details..")
        product_service.add_product()
        manage_products(product_service)
    elif choice == "2":
        print("Welcome to Search Product Details..")
        product_service.search_product()
        manage_products(product_service)
    elif choice == "3":
        print("Welcome to Delete Product Details..")
        product_service.delete_product()
        manage_products(product_service)
    elif choice == "4":
        print("Welcome to Update Product Details..")
        product_service.update_product()
        manage_products(product_service)
    elif choice == "5":
        print("Welcome to Update Product Price Level..")
        product_service.update_product_price_level()
        manage_products(product_service)
    elif choice == "6":
        print("Welcome to Show All Products..")
        product_service.show_all_products()
        manage_products(product_service)
    elif choice == "7":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_products(product_service)


def manage_branch(branch_service):
    print("---------Manage Branch Details----------")
    print("|  1 - Add Branch Details              |")
    print("|  2 - Search Branch Details           |")
    print("|  3 - Delete Branch Details           |")
    print("|  4 - Update Branch Details           |")
    print("|  5 - Search All Branch               |")
    print("|  6 - Exit(Back to Mainmenu)          |")
    print("----------------------------------------")
    choice = input("Enter your choice:")

    if choice == "1":
        print("Welcome to Add Branch Details..")
        branch_service.add_branch()
        manage_branch(branch_service)
    elif choice == "2":
        print("Welcome to Search Branch Details..")
        branch_service.search_branch()
        manage_branch(branch_service)
    elif choice == "3":
        print("Welcome to Delete Branch Details..")
        branch_service.delete_branch()
        manage_branch(branch_service)
    elif choice == "4":
        print("Welcome to Update Branch Details..")
        branch_service.update_branch()
        manage_branch(branch_service)
    elif choice == "5":
        print("Welcome to Show All Branches..")
        branch_service.show_all_branches()
        manage_branch(branch_service)
    elif choice == "6":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_branch(branch_service)
            

def print_product(product):
    print("---------------------------------")
    print('| Product Code: ', product[0])
    print('| Product Name: ', product[1])
    print('| Product Unit: ', product[2])
    print('| Product Price: ', product[3])
    print('| Product Discount: ', product[4])
    print('| Product Price After Discount: ', product[5])
    print("---------------------------------")

def print_branch(branch):
    print("---------------------------------")
    print('| Branch ID: ', branch[0])
    print('| Branch Name: ', branch[1])
    print('| Branch Address: ', branch[2])
    print('| Branch Manager: ', branch[3])
    print('| Total Employee Count of the Branch: ', branch[4])
    print("---------------------------------")


def manage_branch_product(branch_product_service):   
    print("---------Manage Branchwise Product Details-------")
    print("|  1 - Add Branch Product Details               |")
    print("|  2 - Search Branch Product Details            |")
    print("|  3 - Delete Branch Product Details            |")
    print("|  4 - Update Branch Product Details            |")
    print("|  5 - Search All Branch Product                |")
    print("|  6 - Exit(Back to Mainmenu)                   |")
    print("-------------------------------------------------")
    choice = input("Enter your choice:")

    if choice == "1":
        print("Welcome to Add Branch Product Details..")
        branch_product_service.add_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "2":
        print("Welcome to Search Branch Product Details..")
        branch_product_service.search_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "3":
        print("Welcome to Delete Branch Product Details..")
        branch_product_service.delete_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "4":
        print("Welcome to Update Branch Product Details..")
        branch_product_service.update_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "5":
        print("Welcome to Show All Branch Products..")
        branch_product_service.show_all_branch_products()
        manage_branch_product(branch_product_service)
    elif choice == "6":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_branch_product(branch_product_service)

def manage_sales(sales_service):
    print("-----------Manage Sales Details------------")
    print("|  1 - Add Sales Details                  |")
    print("|  2 - Show Sales Bill Details            |")
    print("|  3 - Show All Sales Bill Details(Today) |")
    print("|  4 - Exit(Back to Mainmenu)             |")
    print("-------------------------------------------")
    choice = input("Enter your choice:")

    if choice == "1":
        print("Welcome to Add Sales Details..")
        sales_service.add_sales()
        manage_sales(sales_service)
    elif choice == "2":
        print("Welcome to Search Sales Bill Details..")
        sales_service.search_sales_bill()
        manage_sales(sales_service)
    elif choice == "3":
        print("Welcome to Show All Sales Bill Details..")
        sales_service.show_all_bill_records_today()
        manage_sales(sales_service)
    elif choice == "4":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_sales(sales_service)


def manage_supplier_details(supplier_service):
    print("---------Manage Supplier Details---------")
    print("|  1 - Add Supplier Details             |")
    print("|  2 - Search Supplier Details          |")
    print("|  3 - Delete Supplier Details          |")
    print("|  4 - Update Supplier Details          |")
    print("|  5 - Search All Supplier              |")
    print("|  6 - Exit(Back to Mainmenu)           |")
    print("----------------------------------------")
    choice = input("Enter your choice:")

    if choice == "1":
        print("Welcome to Add Supplier Details..")
        supplier_service.add_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "2":
        print("Welcome to Search Supplier Details..")
        supplier_service.search_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "3":
        print("Welcome to Delete Supplier Details..")
        supplier_service.delete_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "4":
        print("Welcome to Update Supplier Details..")
        supplier_service.update_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "5":
        print("Welcome to Show All Suppliers..")
        supplier_service.show_all_supplier_details()
        manage_supplier_details(supplier_service)
    elif choice == "6":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_supplier_details(supplier_service)



def manage_stock_details(stock_service):
    print("-----------Manage Stock Details------------")
    print("|  1 - Add Stock Details                  |")
    print("|  2 - Show Stock GRN Details             |")
    print("|  3 - Show All Stock GRN Details(Today)  |")
    print("|  4 - Update GRN Payment Details         |")
    print("|  5 - Exit(Back to Mainmenu)             |")
    print("-------------------------------------------")
    choice = input("Enter your choice:")

    if choice == "1":
        print("Welcome to Add Stock Details..")
        stock_service.add_stock_details()
        manage_stock_details(stock_service)
    elif choice == "2":
        print("Welcome to Search Stock GRN Details..")
        stock_service.search_stock_grn_details()
        manage_stock_details(stock_service)
    elif choice == "3":
        print("Welcome to Show All Stock GRN Details..")
        stock_service.show_all_stock_grn_records_today()
        manage_stock_details(stock_service)
    elif choice == "4":
        print("Welcome to Update GRN Payment Details..")
        stock_service.update_stock_grn_payment()
        manage_stock_details(stock_service)
    elif choice == "5":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_stock_details(stock_service)


def manage_reports(report_service):
    print("---------------Generate Reports----------------")
    print("|  1 - Monthly sales analysis of each branch  |")
    print("|  2 - Price analysis of each product         |")
    print("|  3 - Weekly sales analysis of all branches  |")
    print("|  4 - Product preference analysis            |")
    print("|  5 - Analysis of the distribution           |")
    print("|      of total sales amount of purchases     |")
    print("|  6 - Exit(Back to Mainmenu)                 |")
    print("-----------------------------------------------")
    choice = input("Enter your choice:")

    if choice=="1":
        print("Welcome to Monthly Sales Analysis..")
        report_service.monthly_sales_analysis()
        manage_reports(report_service)
    elif choice=="2":
        print("Welcome to Price Analysis of Product..")
        report_service.price_analysis()
        manage_reports(report_service)
    elif choice=="3":
        print("Welcome to Weekly Sales Analysis..")
        report_service.weekly_sales_analysis()
        manage_reports(report_service)
    elif choice=="4":
        print("Welcome to Product Preferences..")
        report_service.sales_product_preferences()
        manage_reports(report_service)
    elif choice=="5":
        print("Welcome to Overall Product and Sales Analysis..")
        report_service.final_sales_analysis()
        manage_reports(report_service)
    elif choice=="6":
        print("Exit...")
    else:
        print("Invalid choice...")
        manage_reports(report_service)




if __name__ == "__main__":
    main_menu()
