import os
import psycopg2
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

# We load the .env here so every child page has access to credentials
load_dotenv()

class BasePage:
    """
    TUTOR NOTE: The BasePage is the 'blueprint' for all other pages.
    Instead of writing the Database connection code in 50 different files,
    we write it once here. Every other page will 'inherit' these skills.
    """

    def __init__(self, page: Page):
        # This gives the page object its 'eyes' (the browser page)
        self.page = page

    # --- UI COMMON ACTIONS ---
    
    def navigate(self, path: str):
        """Navigates to a URL. The path is appended to the BASE_URL from .env."""
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        self.page.goto(f"{base_url}{path}")

    # --- DATABASE PILLAR (The 'Senior' Secret) ---

    def query_db(self, query: str, params: tuple = None):
        """
        TUTOR NOTE: This method handles the 'Data Integrity' pillar.
        It uses a 'Context Manager' (the 'with' statement) which is the 
        Senior way to ensure the connection closes even if the test fails.
        """
        try:
            # We connect using the 127.0.0.1 host to avoid socket errors
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    # If it's a SELECT, we return the data
                    if cur.description:
                        return cur.fetchall()
                    # If it's an INSERT/DELETE, we commit the change
                    conn.commit()
        except Exception as e:
            print(f"❌ Database Error in BasePage: {e}")
            return None

    # --- JAVA BRIDGE NOTE ---
    # In Java, this 'BasePage' would use a JDBC 'Connection' object 
    # inside a try-with-resources block. The concept of 'Inheritance' 
    # (class LoginPage extends BasePage) works exactly the same way.
