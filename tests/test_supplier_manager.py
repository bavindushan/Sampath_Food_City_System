import pytest
from finalproject import SupplierManager, IDatabaseConnection

@pytest.fixture(scope="module")
def supplier_manager(db_connection):
    # Initialize SupplierManager instance for testing
    return SupplierManager(db_connection)

def test_search_supplier_by_id(supplier_manager):
    # Test Case TC009: Search for a supplier by ID
    # Assuming supplier_id exists in the database
    supplier_id = "S001"
    result = supplier_manager.search_supplier(supplier_id)
    assert result is not None, "Supplier details should be returned"

def test_update_supplier_information(supplier_manager):
    # Test Case TC010: Update supplier information
    supplier_id = "S001"
    new_address = "New Address"
    supplier_manager.update_supplier(supplier_id, address=new_address)
    # Check if the supplier information was updated correctly
    updated_supplier = supplier_manager.search_supplier(supplier_id)
    assert updated_supplier['address'] == new_address, "Supplier address should be updated"


if __name__ == "__main__":
    pytest.main()
