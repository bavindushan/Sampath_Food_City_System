import pytest
from finalproject import SalesManager, IDatabaseConnection

@pytest.fixture(scope="module")
def sales_manager(db_connection):
    # Initialize SalesManager instance for testing
    return SalesManager(db_connection)

def test_generate_sales_report(sales_manager):
    # Test Case TC007: Generate a sales report
    # Assuming some sales data exists in the database
    sales_report = sales_manager.generate_sales_report()
    assert sales_report is not None, "Sales report should be generated"


if __name__ == "__main__":
    pytest.main()
