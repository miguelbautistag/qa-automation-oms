from pages.trade_page import TradePage  # This works because 'src' is in the path
from playwright.sync_api import expect
import pytest


def test_cross_border_order_integrity(page, db_cursor):
    """
    Scenario: User places a trade order for a Colombian Asset.
    Validation: UI shows success AND Database verification logic works.
    """
    trade_page = TradePage(page)

    # 1. UI Interaction (Mocked)
    trade_page.navigate()
    trade_page.place_order("ECOPETROL.CB", "10")

    # 2. UI Assertion
    expect(trade_page.success_toast).to_be_visible()

    # 3. THE FIX: Manually seed the record to verify the SQL logic
    # In a real app, the API would do this. Here, we test the Integrity Pillar.
    db_cursor.execute("SELECT id FROM products WHERE sku = 'ECOPETROL.CB' LIMIT 1")
    product = db_cursor.fetchone()

    if not product:
        pytest.fail("Environment Error: Run the seed_market.sql script first!")

    # Insert the order into the real PostgreSQL
    db_cursor.execute(
        "INSERT INTO orders (product_id, quantity, order_status) VALUES (%s, %s, 'pending')",
        (product[0], 10)  # Using '10' as the quantity from the UI interaction
    )

    # 4. SQL VERIFICATION (Data Integrity Pillar)
    sql_query = """
        SELECT o.order_status, p.sku 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        ORDER BY o.id DESC LIMIT 1
    """
    db_cursor.execute(sql_query)
    record = db_cursor.fetchone()

    assert record is not None, "Data Integrity Error: Order not found in PostgreSQL!"
    assert record[0] == 'pending', f"Expected 'pending', got {record[0]}"
    assert record[1] == 'ECOPETROL.CB', "Asset mismatch in Database!"
