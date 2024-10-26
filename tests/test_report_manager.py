import pytest
from finalproject import ReportManager, DatabaseConnection

@pytest.fixture
def setup_report_manager():
    # Setup any necessary objects or connections
    db_connection = DatabaseConnection()
    report_manager = ReportManager(db_connection)
    yield report_manager
    # Teardown any resources if needed

def test_generate_sales_report(setup_report_manager):
    report_manager = setup_report_manager
    # Assuming you have a method in ReportManager to generate sales report
    result = report_manager.generate_sales_report()
    assert result is not None
    assert len(result) > 0  # Ensure the report contains valid data

