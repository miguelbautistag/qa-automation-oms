import pytest
import psycopg2
import os
from dotenv import load_dotenv

# Load credentials from .env (Local development)
load_dotenv()

@pytest.fixture(scope="session")
def db_connection():
    """
    Architectural Pillar: DATA INTEGRITY
    Establishes a single connection for the entire test session.
    """
    # Prioritizes Environment Variables (CI/CD) with Local Fallbacks
    host = os.getenv("DB_HOST", "localhost")
    dbname = os.getenv("DB_NAME", "trade_db")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "admin123")
    port = os.getenv("DB_PORT", "5432")

    try:
        # Using a context manager for the connection
        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port
        )
        yield conn
        conn.close()
    except Exception as e:
        # PILLAR: OBSERVABILITY - Detailed failure logging
        print(f"\n[RCA] DB Connection Failed. Check Host: {host}, DB: {dbname}")
        pytest.exit(f"CRITICAL: Database connection failed: {e}")

@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """
    Architectural Pillar: DATA INTEGRITY
    Provides a cursor for individual test transactions.
    Rolls back changes after every test to ensure 'Clean Data' for the next run.
    """
    cursor = db_connection.cursor()
    yield cursor
    # Ensures test isolation: changes in one test won't affect the next
    db_connection.rollback()
    cursor.close()

@pytest.fixture(autouse=True)
def mock_trading_ui(page):
    """
    Architectural Pillar: SHIFT-LEFT
    Intercepts the market URL to simulate the UliteTrade UI without a live frontend.
    """
    def handle_route(route):
        # Professional-grade HTML mock matching POM selectors
        html_content = """
        <html>
            <head><title>UliteTrade Regional OMS</title></head>
            <body>
                <h1>UliteTrade Market</h1>
                <div class="trade-container">
                    <select id="asset-selector" aria-label="Select Asset">
                        <option value="ECOPETROL.CB">Ecopetrol (Colombia)</option>
                    </select>
                    <label for="qty">Quantity</label>
                    <input id="qty" type="number" value="10" />
                    <button id="buy-btn" role="button" onclick="document.getElementById('status').style.display='block'">
                        Place Buy Order
                    </button>
                    <div id="status" style="display:none" role="alert" class="success-toast">
                        Order Placed Successfully!
                    </div>
                </div>
            </body>
        </html>
        """
        route.fulfill(body=html_content, content_type="text/html")

    # Intercepting requests to the market page
    page.route("**/market", handle_route)
