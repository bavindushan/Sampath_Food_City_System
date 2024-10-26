import pytest
from finalproject import ProductManager, IDatabaseConnection

@pytest.fixture(scope="module")
def product_manager(db_connection):
    # Initialize ProductManager instance for testing
    return ProductManager(db_connection)

def test_search_product_by_id(product_manager):
    # Test Case TC001: Search for a product by ID
    # Assuming pcode exists in the database
    pid = "P001"
    result = product_manager.search_product(pid)
    assert result is not None, "Product details should be returned"

def test_add_new_product(product_manager):
    # Test Case TC002: Add a new product
    pname = "Test Product"
    punit = "Each"
    pprice = 10.0
    pdiscount = 0.0
    pcode = "P999"
    product_manager.add_product(pname, punit, pprice, pdiscount, pcode)
    # Check if the product was added successfully by searching for it
    result = product_manager.search_product(pcode)
    assert result is not None, "Product should have been added"

def test_update_product_information(product_manager):
    # Test Case TC003: Update product information
    pid = "P001"
    new_price = 15.0
    product_manager.update_product(pid, price=new_price)
    # Check if the product information was updated correctly
    updated_product = product_manager.search_product(pid)
    assert updated_product['price'] == new_price, "Product price should be updated"


if __name__ == "__main__":
    pytest.main()
