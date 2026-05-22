import pandas as pd
import numpy as np
import os
import time
import dotenv
import ast
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from typing import Dict, List, Union
from sqlalchemy import create_engine, Engine

# Create an SQLite database
db_engine = create_engine("sqlite:///beavers_choice.db")

# List containing the different kinds of papers 
paper_supplies = [
    # Paper Types (priced per sheet unless specified)
    {"item_name": "A4 paper",                         "category": "paper",        "unit_price": 0.05},
    {"item_name": "Letter-sized paper",              "category": "paper",        "unit_price": 0.06},
    {"item_name": "Cardstock",                        "category": "paper",        "unit_price": 0.15},
    {"item_name": "Colored paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Glossy paper",                     "category": "paper",        "unit_price": 0.20},
    {"item_name": "Matte paper",                      "category": "paper",        "unit_price": 0.18},
    {"item_name": "Recycled paper",                   "category": "paper",        "unit_price": 0.08},
    {"item_name": "Eco-friendly paper",               "category": "paper",        "unit_price": 0.12},
    {"item_name": "Poster paper",                     "category": "paper",        "unit_price": 0.25},
    {"item_name": "Banner paper",                     "category": "paper",        "unit_price": 0.30},
    {"item_name": "Kraft paper",                      "category": "paper",        "unit_price": 0.10},
    {"item_name": "Construction paper",               "category": "paper",        "unit_price": 0.07},
    {"item_name": "Wrapping paper",                   "category": "paper",        "unit_price": 0.15},
    {"item_name": "Glitter paper",                    "category": "paper",        "unit_price": 0.22},
    {"item_name": "Decorative paper",                 "category": "paper",        "unit_price": 0.18},
    {"item_name": "Letterhead paper",                 "category": "paper",        "unit_price": 0.12},
    {"item_name": "Legal-size paper",                 "category": "paper",        "unit_price": 0.08},
    {"item_name": "Crepe paper",                      "category": "paper",        "unit_price": 0.05},
    {"item_name": "Photo paper",                      "category": "paper",        "unit_price": 0.25},
    {"item_name": "Uncoated paper",                   "category": "paper",        "unit_price": 0.06},
    {"item_name": "Butcher paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Heavyweight paper",                "category": "paper",        "unit_price": 0.20},
    {"item_name": "Standard copy paper",              "category": "paper",        "unit_price": 0.04},
    {"item_name": "Bright-colored paper",             "category": "paper",        "unit_price": 0.12},
    {"item_name": "Patterned paper",                  "category": "paper",        "unit_price": 0.15},

    # Product Types (priced per unit)
    {"item_name": "Paper plates",                     "category": "product",      "unit_price": 0.10},  # per plate
    {"item_name": "Paper cups",                       "category": "product",      "unit_price": 0.08},  # per cup
    {"item_name": "Paper napkins",                    "category": "product",      "unit_price": 0.02},  # per napkin
    {"item_name": "Disposable cups",                  "category": "product",      "unit_price": 0.10},  # per cup
    {"item_name": "Table covers",                     "category": "product",      "unit_price": 1.50},  # per cover
    {"item_name": "Envelopes",                        "category": "product",      "unit_price": 0.05},  # per envelope
    {"item_name": "Sticky notes",                     "category": "product",      "unit_price": 0.03},  # per sheet
    {"item_name": "Notepads",                         "category": "product",      "unit_price": 2.00},  # per pad
    {"item_name": "Invitation cards",                 "category": "product",      "unit_price": 0.50},  # per card
    {"item_name": "Flyers",                           "category": "product",      "unit_price": 0.15},  # per flyer
    {"item_name": "Party streamers",                  "category": "product",      "unit_price": 0.05},  # per roll
    {"item_name": "Decorative adhesive tape (washi tape)", "category": "product", "unit_price": 0.20},  # per roll
    {"item_name": "Paper party bags",                 "category": "product",      "unit_price": 0.25},  # per bag
    {"item_name": "Name tags with lanyards",          "category": "product",      "unit_price": 0.75},  # per tag
    {"item_name": "Presentation folders",             "category": "product",      "unit_price": 0.50},  # per folder

    # Large-format items (priced per unit)
    {"item_name": "Large poster paper (24x36 inches)", "category": "large_format", "unit_price": 1.00},
    {"item_name": "Rolls of banner paper (36-inch width)", "category": "large_format", "unit_price": 2.50},

    # Specialty papers
    {"item_name": "100 lb cover stock",               "category": "specialty",    "unit_price": 0.50},
    {"item_name": "80 lb text paper",                 "category": "specialty",    "unit_price": 0.40},
    {"item_name": "250 gsm cardstock",                "category": "specialty",    "unit_price": 0.30},
    {"item_name": "220 gsm poster paper",             "category": "specialty",    "unit_price": 0.35},
]

# Given below are some utility functions you can use to implement your multi-agent system

def generate_sample_inventory(paper_supplies: list, coverage: float = 0.4, seed: int = 137) -> pd.DataFrame:
    """
    Generate inventory for exactly a specified percentage of items from the full paper supply list.

    This function randomly selects exactly `coverage` × N items from the `paper_supplies` list,
    and assigns each selected item:
    - a random stock quantity between 200 and 800,
    - a minimum stock level between 50 and 150.

    The random seed ensures reproducibility of selection and stock levels.

    Args:
        paper_supplies (list): A list of dictionaries, each representing a paper item with
                               keys 'item_name', 'category', and 'unit_price'.
        coverage (float, optional): Fraction of items to include in the inventory (default is 0.4, or 40%).
        seed (int, optional): Random seed for reproducibility (default is 137).

    Returns:
        pd.DataFrame: A DataFrame with the selected items and assigned inventory values, including:
                      - item_name
                      - category
                      - unit_price
                      - current_stock
                      - min_stock_level
    """
    # Ensure reproducible random output
    np.random.seed(seed)

    # Calculate number of items to include based on coverage
    num_items = int(len(paper_supplies) * coverage)

    # Randomly select item indices without replacement
    selected_indices = np.random.choice(
        range(len(paper_supplies)),
        size=num_items,
        replace=False
    )

    # Extract selected items from paper_supplies list
    selected_items = [paper_supplies[i] for i in selected_indices]

    # Construct inventory records
    inventory = []
    for item in selected_items:
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "unit_price": item["unit_price"],
            "current_stock": np.random.randint(200, 800),  # Realistic stock range
            "min_stock_level": np.random.randint(50, 150)  # Reasonable threshold for reordering
        })

    # Return inventory as a pandas DataFrame
    return pd.DataFrame(inventory)

def init_database(db_engine: Engine, seed: int = 137) -> Engine:    
    """
    Set up the Beaver's Choice database with all required tables and initial records.

    This function performs the following tasks:
    - Creates the 'transactions' table for logging stock orders and sales
    - Loads customer inquiries from 'quote_requests.csv' into a 'quote_requests' table
    - Loads previous quotes from 'quotes.csv' into a 'quotes' table, extracting useful metadata
    - Generates a random subset of paper inventory using `generate_sample_inventory`
    - Inserts initial financial records including available cash and starting stock levels

    Args:
        db_engine (Engine): A SQLAlchemy engine connected to the SQLite database.
        seed (int, optional): A random seed used to control reproducibility of inventory stock levels.
                              Default is 137.

    Returns:
        Engine: The same SQLAlchemy engine, after initializing all necessary tables and records.

    Raises:
        Exception: If an error occurs during setup, the exception is printed and raised.
    """
    try:
        # ----------------------------
        # 1. Create an empty 'transactions' table schema
        # ----------------------------
        transactions_schema = pd.DataFrame({
            "id": [],
            "item_name": [],
            "transaction_type": [],  # 'stock_orders' or 'sales'
            "units": [],             # Quantity involved
            "price": [],             # Total price for the transaction
            "transaction_date": [],  # ISO-formatted date
        })
        transactions_schema.to_sql("transactions", db_engine, if_exists="replace", index=False)

        # Set a consistent starting date
        initial_date = datetime(2025, 1, 1).isoformat()

        # ----------------------------
        # 2. Load and initialize 'quote_requests' table
        # ----------------------------
        quote_requests_df = pd.read_csv("quote_requests.csv")
        quote_requests_df["id"] = range(1, len(quote_requests_df) + 1)
        quote_requests_df.to_sql("quote_requests", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 3. Load and transform 'quotes' table
        # ----------------------------
        quotes_df = pd.read_csv("quotes.csv")
        quotes_df["request_id"] = range(1, len(quotes_df) + 1)
        quotes_df["order_date"] = initial_date

        # Unpack metadata fields (job_type, order_size, event_type) if present
        if "request_metadata" in quotes_df.columns:
            quotes_df["request_metadata"] = quotes_df["request_metadata"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            quotes_df["job_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("job_type", ""))
            quotes_df["order_size"] = quotes_df["request_metadata"].apply(lambda x: x.get("order_size", ""))
            quotes_df["event_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("event_type", ""))

        # Retain only relevant columns
        quotes_df = quotes_df[[
            "request_id",
            "total_amount",
            "quote_explanation",
            "order_date",
            "job_type",
            "order_size",
            "event_type"
        ]]
        quotes_df.to_sql("quotes", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 4. Generate inventory and seed stock
        # ----------------------------
        inventory_df = generate_sample_inventory(paper_supplies, seed=seed)

        # Seed initial transactions
        initial_transactions = []

        # Add a starting cash balance via a dummy sales transaction
        initial_transactions.append({
            "item_name": None,
            "transaction_type": "sales",
            "units": None,
            "price": 50000.0,
            "transaction_date": initial_date,
        })

        # Add one stock order transaction per inventory item
        for _, item in inventory_df.iterrows():
            initial_transactions.append({
                "item_name": item["item_name"],
                "transaction_type": "stock_orders",
                "units": item["current_stock"],
                "price": item["current_stock"] * item["unit_price"],
                "transaction_date": initial_date,
            })

        # Commit transactions to database
        pd.DataFrame(initial_transactions).to_sql("transactions", db_engine, if_exists="append", index=False)

        # Save the inventory reference table
        inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

        return db_engine

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    """
    This function records a transaction of type 'stock_orders' or 'sales' with a specified
    item name, quantity, total price, and transaction date into the 'transactions' table of the database.

    Args:
        item_name (str): The name of the item involved in the transaction.
        transaction_type (str): Either 'stock_orders' or 'sales'.
        quantity (int): Number of units involved in the transaction.
        price (float): Total price of the transaction.
        date (str or datetime): Date of the transaction in ISO 8601 format.

    Returns:
        int: The ID of the newly inserted transaction.

    Raises:
        ValueError: If `transaction_type` is not 'stock_orders' or 'sales'.
        Exception: For other database or execution errors.
    """
    try:
        # Convert datetime to ISO string if necessary
        date_str = date.isoformat() if isinstance(date, datetime) else date

        # Validate transaction type
        if transaction_type not in {"stock_orders", "sales"}:
            raise ValueError("Transaction type must be 'stock_orders' or 'sales'")

        # Prepare transaction record as a single-row DataFrame
        transaction = pd.DataFrame([{
            "item_name": item_name,
            "transaction_type": transaction_type,
            "units": quantity,
            "price": price,
            "transaction_date": date_str,
        }])

        # Insert the record into the database
        transaction.to_sql("transactions", db_engine, if_exists="append", index=False)

        # Fetch and return the ID of the inserted row
        result = pd.read_sql("SELECT last_insert_rowid() as id", db_engine)
        return int(result.iloc[0]["id"])

    except Exception as e:
        print(f"Error creating transaction: {e}")
        raise

def get_all_inventory(as_of_date: str) -> Dict[str, int]:
    """
    Retrieve a snapshot of available inventory as of a specific date.

    This function calculates the net quantity of each item by summing 
    all stock orders and subtracting all sales up to and including the given date.

    Only items with positive stock are included in the result.

    Args:
        as_of_date (str): ISO-formatted date string (YYYY-MM-DD) representing the inventory cutoff.

    Returns:
        Dict[str, int]: A dictionary mapping item names to their current stock levels.
    """
    # SQL query to compute stock levels per item as of the given date
    query = """
        SELECT
            item_name,
            SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END) as stock
        FROM transactions
        WHERE item_name IS NOT NULL
        AND transaction_date <= :as_of_date
        GROUP BY item_name
        HAVING stock > 0
    """

    # Execute the query with the date parameter
    result = pd.read_sql(query, db_engine, params={"as_of_date": as_of_date})

    # Convert the result into a dictionary {item_name: stock}
    return dict(zip(result["item_name"], result["stock"]))

def get_stock_level(item_name: str, as_of_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Retrieve the stock level of a specific item as of a given date.

    This function calculates the net stock by summing all 'stock_orders' and 
    subtracting all 'sales' transactions for the specified item up to the given date.

    Args:
        item_name (str): The name of the item to look up.
        as_of_date (str or datetime): The cutoff date (inclusive) for calculating stock.

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'current_stock'.
    """
    # Convert date to ISO string format if it's a datetime object
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # SQL query to compute net stock level for the item
    stock_query = """
        SELECT
            item_name,
            COALESCE(SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name
        AND transaction_date <= :as_of_date
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        stock_query,
        db_engine,
        params={"item_name": item_name, "as_of_date": as_of_date},
    )

def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date based on the requested order quantity and a starting date.

    Delivery lead time increases with order size:
        - ≤10 units: same day
        - 11–100 units: 1 day
        - 101–1000 units: 4 days
        - >1000 units: 7 days

    Args:
        input_date_str (str): The starting date in ISO format (YYYY-MM-DD).
        quantity (int): The number of units in the order.

    Returns:
        str: Estimated delivery date in ISO format (YYYY-MM-DD).
    """
    # Debug log (comment out in production if needed)
    print(f"FUNC (get_supplier_delivery_date): Calculating for qty {quantity} from date string '{input_date_str}'")

    # Attempt to parse the input date
    try:
        input_date_dt = datetime.fromisoformat(input_date_str.split("T")[0])
    except (ValueError, TypeError):
        # Fallback to current date on format error
        print(f"WARN (get_supplier_delivery_date): Invalid date format '{input_date_str}', using today as base.")
        input_date_dt = datetime.now()

    # Determine delivery delay based on quantity
    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7

    # Add delivery days to the starting date
    delivery_date_dt = input_date_dt + timedelta(days=days)

    # Return formatted delivery date
    return delivery_date_dt.strftime("%Y-%m-%d")

def get_cash_balance(as_of_date: Union[str, datetime]) -> float:
    """
    Calculate the current cash balance as of a specified date.

    The balance is computed by subtracting total stock purchase costs ('stock_orders')
    from total revenue ('sales') recorded in the transactions table up to the given date.

    Args:
        as_of_date (str or datetime): The cutoff date (inclusive) in ISO format or as a datetime object.

    Returns:
        float: Net cash balance as of the given date. Returns 0.0 if no transactions exist or an error occurs.
    """
    try:
        # Convert date to ISO format if it's a datetime object
        if isinstance(as_of_date, datetime):
            as_of_date = as_of_date.isoformat()

        # Query all transactions on or before the specified date
        transactions = pd.read_sql(
            "SELECT * FROM transactions WHERE transaction_date <= :as_of_date",
            db_engine,
            params={"as_of_date": as_of_date},
        )

        # Compute the difference between sales and stock purchases
        if not transactions.empty:
            total_sales = transactions.loc[transactions["transaction_type"] == "sales", "price"].sum()
            total_purchases = transactions.loc[transactions["transaction_type"] == "stock_orders", "price"].sum()
            return float(total_sales - total_purchases)

        return 0.0

    except Exception as e:
        print(f"Error getting cash balance: {e}")
        return 0.0


def generate_financial_report(as_of_date: Union[str, datetime]) -> Dict:
    """
    Generate a complete financial report for the company as of a specific date.

    This includes:
    - Cash balance
    - Inventory valuation
    - Combined asset total
    - Itemized inventory breakdown
    - Top 5 best-selling products

    Args:
        as_of_date (str or datetime): The date (inclusive) for which to generate the report.

    Returns:
        Dict: A dictionary containing the financial report fields:
            - 'as_of_date': The date of the report
            - 'cash_balance': Total cash available
            - 'inventory_value': Total value of inventory
            - 'total_assets': Combined cash and inventory value
            - 'inventory_summary': List of items with stock and valuation details
            - 'top_selling_products': List of top 5 products by revenue
    """
    # Normalize date input
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # Get current cash balance
    cash = get_cash_balance(as_of_date)

    # Get current inventory snapshot
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0.0
    inventory_summary = []

    # Compute total inventory value and summary by item
    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = stock_info["current_stock"].iloc[0]
        item_value = stock * item["unit_price"]
        inventory_value += item_value

        inventory_summary.append({
            "item_name": item["item_name"],
            "stock": stock,
            "unit_price": item["unit_price"],
            "value": item_value,
        })

    # Identify top-selling products by revenue
    top_sales_query = """
        SELECT item_name, SUM(units) as total_units, SUM(price) as total_revenue
        FROM transactions
        WHERE transaction_type = 'sales' AND transaction_date <= :date
        GROUP BY item_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    top_sales = pd.read_sql(top_sales_query, db_engine, params={"date": as_of_date})
    top_selling_products = top_sales.to_dict(orient="records")

    return {
        "as_of_date": as_of_date,
        "cash_balance": cash,
        "inventory_value": inventory_value,
        "total_assets": cash + inventory_value,
        "inventory_summary": inventory_summary,
        "top_selling_products": top_selling_products,
    }


def search_quote_history(search_terms: List[str], limit: int = 5) -> List[Dict]:
    """
    Retrieve a list of historical quotes that match any of the provided search terms.

    The function searches both the original customer request (from `quote_requests`) and
    the explanation for the quote (from `quotes`) for each keyword. Results are sorted by
    most recent order date and limited by the `limit` parameter.

    Args:
        search_terms (List[str]): List of terms to match against customer requests and explanations.
        limit (int, optional): Maximum number of quote records to return. Default is 5.

    Returns:
        List[Dict]: A list of matching quotes, each represented as a dictionary with fields:
            - original_request
            - total_amount
            - quote_explanation
            - job_type
            - order_size
            - event_type
            - order_date
    """
    conditions = []
    params = {}

    # Build SQL WHERE clause using LIKE filters for each search term
    for i, term in enumerate(search_terms):
        param_name = f"term_{i}"
        conditions.append(
            f"(LOWER(qr.response) LIKE :{param_name} OR "
            f"LOWER(q.quote_explanation) LIKE :{param_name})"
        )
        params[param_name] = f"%{term.lower()}%"

    # Combine conditions; fallback to always-true if no terms provided
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Final SQL query to join quotes with quote_requests
    query = f"""
        SELECT
            qr.response AS original_request,
            q.total_amount,
            q.quote_explanation,
            q.job_type,
            q.order_size,
            q.event_type,
            q.order_date
        FROM quotes q
        JOIN quote_requests qr ON q.request_id = qr.id
        WHERE {where_clause}
        ORDER BY q.order_date DESC
        LIMIT {limit}
    """

    # Execute parameterized query
    with db_engine.connect() as conn:
        result = conn.execute(text(query), params)
        return [dict(row._mapping) for row in result]


########################
########################
########################
# MULTI AGENT IMPLEMENTATION STARTS HERE
########################
########################
########################

import contextlib
import io
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean

try:
    from smolagents import OpenAIServerModel, ToolCallingAgent, tool
except Exception:  # Allows deterministic evaluation when smolagents is not installed.
    OpenAIServerModel = None
    ToolCallingAgent = None

    class _FallbackTool:
        """Small fallback wrapper with the same .forward shape used below."""

        def __init__(self, fn):
            self.forward = fn
            self.name = fn.__name__
            self.description = fn.__doc__ or ""

    def tool(fn):
        return _FallbackTool(fn)


VOC_BASE_URL = "https://openai.vocareum.com/v1"
DEFAULT_MODEL_ID = os.getenv("UDACITY_OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


def build_openai_compatible_model():
    """Create the OpenAI-compatible model object used by the smolagents shells when a key is available."""
    if OpenAIServerModel is None:
        return None
    dotenv.load_dotenv()
    api_key = os.getenv("UDACITY_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAIServerModel(
        model_id=DEFAULT_MODEL_ID,
        api_base=VOC_BASE_URL,
        api_key=api_key,
    )


def _json_dumps(value) -> str:
    return json.dumps(value, default=str, ensure_ascii=False)


@tool
def inventory_snapshot_tool(as_of_date: str) -> str:
    """
    Return the current inventory snapshot for a date.

    Args:
        as_of_date: ISO date used as the inventory cutoff.
    """
    return _json_dumps(get_all_inventory(as_of_date))


@tool
def stock_status_tool(item_name: str, as_of_date: str) -> str:
    """
    Return the current stock level for one catalog item.

    Args:
        item_name: Exact catalog item name.
        as_of_date: ISO date used as the inventory cutoff.
    """
    stock_df = get_stock_level(item_name, as_of_date)
    current_stock = int(stock_df["current_stock"].iloc[0]) if not stock_df.empty else 0
    return _json_dumps({"item_name": item_name, "current_stock": current_stock})


@tool
def supplier_timeline_tool(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier arrival date for a replenishment quantity.

    Args:
        input_date_str: ISO date when the supplier order is placed.
        quantity: Number of units requested from the supplier.
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        return get_supplier_delivery_date(input_date_str, int(quantity))


@tool
def cash_status_tool(as_of_date: str) -> str:
    """
    Return the available cash balance for a date.

    Args:
        as_of_date: ISO date used as the cash balance cutoff.
    """
    return _json_dumps({"cash_balance": get_cash_balance(as_of_date)})


@tool
def financial_report_tool(as_of_date: str) -> str:
    """
    Return the financial report for a date.

    Args:
        as_of_date: ISO date used as the report cutoff.
    """
    return _json_dumps(generate_financial_report(as_of_date))


@tool
def quote_history_tool(search_terms_csv: str, limit: int = 5) -> str:
    """
    Search prior quotes for comparable orders.

    Args:
        search_terms_csv: Comma-separated search terms, such as event type or product family.
        limit: Maximum number of historical quote records to return.
    """
    terms = [term.strip() for term in search_terms_csv.split(",") if term.strip()]
    return _json_dumps(search_quote_history(terms, limit=int(limit)))


@tool
def record_transaction_tool(item_name: str, transaction_type: str, quantity: int, price: float, transaction_date: str) -> str:
    """
    Record a stock order or sale in the transactions table.

    Args:
        item_name: Exact catalog item name for the transaction.
        transaction_type: Either stock_orders or sales.
        quantity: Number of units in the transaction.
        price: Total dollar value for the transaction.
        transaction_date: ISO date for the transaction.
    """
    transaction_id = create_transaction(item_name, transaction_type, int(quantity), float(price), transaction_date)
    return _json_dumps({"transaction_id": transaction_id})


CATALOG_BY_NAME: Dict[str, Dict[str, Union[str, float]]] = {item["item_name"]: item for item in paper_supplies}

# Natural request patterns mapped to exact catalog names. Order matters: specific patterns come first.
ITEM_RULES = [
    (r"balloons?", None),
    (r"tickets?", None),
    (r"flyers?", "Flyers"),
    (r"paper\s+napkins?|table\s+napkins?|napkins?", "Paper napkins"),
    (r"paper\s+plates?|plates?", "Paper plates"),
    (r"paper\s+cups?|disposable\s+cups?|cups?", "Paper cups"),
    (r"table\s+covers?", "Table covers"),
    (r"washi\s+tape|decorative\s+adhesive\s+tape", "Decorative adhesive tape (washi tape)"),
    (r"streamers?", "Party streamers"),
    (r"envelopes?", "Envelopes"),
    (r"poster\s+boards?|posters?", "Large poster paper (24x36 inches)"),
    (r"poster\s+paper", "Poster paper"),
    (r"a4\s+glossy|glossy\s+a4|a3\s+glossy|glossy\s+paper", "Glossy paper"),
    (r"a4\s+matte|a3\s+matte|matte\s+a3|matte\s+paper|matte.*a3", "Matte paper"),
    (r"recycled\s+cardstock", "Cardstock"),
    (r"heavy\s+cardstock|heavyweight\s+cardstock|white\s+cardstock|sturdy\s+cardstock", "Cardstock"),
    (r"cardstock|card\s*stock", "Cardstock"),
    (r"cardboard", "100 lb cover stock"),
    (r"construction\s+paper", "Construction paper"),
    (r"colored\s+paper|colorful\s+paper|a3\s+colored|a5\s+colored|assorted\s+colors", "Colored paper"),
    (r"kraft\s+paper", "Kraft paper"),
    (r"standard\s+(copy|printer|printing)\s+paper|printer\s+paper|printing\s+paper", "Standard copy paper"),
    (r"a4\s+(white\s+)?(paper|printer|printing)|a4\s+size\s+printer", "A4 paper"),
    (r"a3\s+paper", None),
]

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


@dataclass
class RequestedItem:
    item_name: str
    quantity: int
    source_text: str
    supported: bool = True
    unit_price: float = 0.0


@dataclass
class InventoryLineDecision:
    item_name: str
    quantity: int
    available_before: int
    reorder_quantity: int
    supplier_arrival_date: str
    can_fulfill: bool
    reason: str
    unit_price: float
    min_stock_level: int


@dataclass
class InventoryDecision:
    can_fulfill: bool
    request_date: str
    delivery_deadline: str
    line_decisions: List[InventoryLineDecision] = field(default_factory=list)
    unsupported_items: List[str] = field(default_factory=list)
    total_reorder_cost: float = 0.0
    cash_before: float = 0.0
    reasons: List[str] = field(default_factory=list)


@dataclass
class QuoteLine:
    item_name: str
    quantity: int
    line_total: float


@dataclass
class QuoteDecision:
    total_amount: float
    base_amount: float
    discount_rate: float
    discount_label: str
    quote_lines: List[QuoteLine]
    history_count: int


@dataclass
class AgentResult:
    status: str
    response: str
    quote_amount: float = 0.0
    items_requested: int = 0
    items_fulfilled: int = 0
    cash_delta: float = 0.0
    inventory_delta: float = 0.0


class RequestParser:
    """Extract dates and order lines from customer text."""

    @staticmethod
    def request_date(text: str, fallback: str = "2025-04-01") -> str:
        match = re.search(r"Date of request:\s*(\d{4}-\d{2}-\d{2})", text, flags=re.IGNORECASE)
        return match.group(1) if match else fallback

    @staticmethod
    def delivery_deadline(text: str, request_date: str) -> str:
        matches = re.findall(
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
            r"(\d{1,2}),\s*(\d{4})",
            text,
            flags=re.IGNORECASE,
        )
        if matches:
            month_name, day, year = matches[-1]
            return datetime(int(year), MONTHS[month_name.lower()], int(day)).strftime("%Y-%m-%d")
        return (datetime.fromisoformat(request_date) + timedelta(days=14)).strftime("%Y-%m-%d")

    @staticmethod
    def _clean_for_quantity_scan(text: str) -> str:
        cleaned = re.sub(r"Date of request:\s*\d{4}-\d{2}-\d{2}", " ", text, flags=re.IGNORECASE)
        cleaned = re.sub(
            r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}",
            " ",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"\d+(?:\.\d+)?\s*[\"”]?\s*[xX]\s*\d+(?:\.\d+)?\s*[\"”]?", " ", cleaned)
        cleaned = re.sub(r"\d+\s*%", " ", cleaned)
        return cleaned

    @staticmethod
    def _match_item(description: str) -> Union[str, None]:
        desc = description.lower()
        for pattern, item_name in ITEM_RULES:
            if re.search(pattern, desc, flags=re.IGNORECASE):
                return item_name
        return None

    @staticmethod
    def parse_items(text: str) -> List[RequestedItem]:
        cleaned = RequestParser._clean_for_quantity_scan(text)
        quantity_matches = list(re.finditer(r"(?<![\d.])\b(\d[\d,]*)\b(?!\s*%)", cleaned))
        items: List[RequestedItem] = []
        unsupported: List[RequestedItem] = []

        for idx, match in enumerate(quantity_matches):
            quantity_text = match.group(1)
            quantity = int(quantity_text.replace(",", ""))
            next_start = quantity_matches[idx + 1].start() if idx + 1 < len(quantity_matches) else min(len(cleaned), match.end() + 180)
            description = cleaned[match.end():next_start].strip(" :-–—,.;\n\t")
            if not description:
                continue
            if re.search(r"\breams?\b", description, flags=re.IGNORECASE):
                quantity *= 500
            item_name = RequestParser._match_item(description)
            if item_name is None:
                unsupported_label = None
                if re.search(r"balloons?", description, flags=re.IGNORECASE):
                    unsupported_label = "balloons"
                elif re.search(r"tickets?", description, flags=re.IGNORECASE):
                    unsupported_label = "tickets"
                elif re.search(r"a3\s+paper", description, flags=re.IGNORECASE):
                    unsupported_label = "A3 paper"
                if unsupported_label:
                    unsupported.append(RequestedItem(unsupported_label, quantity, unsupported_label, supported=False))
                continue
            if item_name not in CATALOG_BY_NAME:
                unsupported.append(RequestedItem(item_name, quantity, description, supported=False))
                continue
            items.append(
                RequestedItem(
                    item_name=item_name,
                    quantity=quantity,
                    source_text=description,
                    unit_price=float(CATALOG_BY_NAME[item_name]["unit_price"]),
                )
            )

        combined: Dict[str, RequestedItem] = {}
        for item in items:
            if item.item_name not in combined:
                combined[item.item_name] = item
            else:
                combined[item.item_name].quantity += item.quantity
                combined[item.item_name].source_text += "; " + item.source_text
        return list(combined.values()) + unsupported


class InventoryAgent:
    """Checks stock, replenishment timing, and cash availability."""

    def __init__(self):
        self.inventory_snapshot_tool = inventory_snapshot_tool
        self.stock_status_tool = stock_status_tool
        self.supplier_timeline_tool = supplier_timeline_tool
        self.cash_status_tool = cash_status_tool

    @staticmethod
    def _ensure_inventory_reference(item_name: str) -> None:
        existing = pd.read_sql(
            "SELECT item_name FROM inventory WHERE item_name = :item_name",
            db_engine,
            params={"item_name": item_name},
        )
        if not existing.empty or item_name not in CATALOG_BY_NAME:
            return
        catalog_item = CATALOG_BY_NAME[item_name]
        pd.DataFrame([{
            "item_name": item_name,
            "category": catalog_item["category"],
            "unit_price": catalog_item["unit_price"],
            "current_stock": 0,
            "min_stock_level": 100,
        }]).to_sql("inventory", db_engine, if_exists="append", index=False)

    @staticmethod
    def _min_stock_level(item_name: str) -> int:
        row = pd.read_sql(
            "SELECT min_stock_level FROM inventory WHERE item_name = :item_name",
            db_engine,
            params={"item_name": item_name},
        )
        if row.empty:
            return 100
        return int(row["min_stock_level"].iloc[0])

    def assess(self, parsed_items: List[RequestedItem], request_date: str, delivery_deadline: str) -> InventoryDecision:
        snapshot_json = self.inventory_snapshot_tool.forward(request_date)
        _ = json.loads(snapshot_json)  # The snapshot is used to force a dated inventory read for the workflow.
        cash_info = json.loads(self.cash_status_tool.forward(request_date))
        cash_before = float(cash_info["cash_balance"])
        decision = InventoryDecision(
            can_fulfill=True,
            request_date=request_date,
            delivery_deadline=delivery_deadline,
            cash_before=cash_before,
        )

        for requested in parsed_items:
            if not requested.supported or requested.item_name not in CATALOG_BY_NAME:
                decision.can_fulfill = False
                label = requested.source_text if requested.source_text else requested.item_name
                decision.unsupported_items.append(label)
                decision.reasons.append(f"{label} is not in the current sellable catalog.")
                continue

            self._ensure_inventory_reference(requested.item_name)
            stock_info = json.loads(self.stock_status_tool.forward(requested.item_name, request_date))
            available_before = int(stock_info["current_stock"])
            min_stock = self._min_stock_level(requested.item_name)
            customer_shortage = max(0, requested.quantity - available_before)
            remaining_after_customer = available_before + customer_shortage - requested.quantity
            buffer_shortage = max(0, min_stock - remaining_after_customer)
            reorder_quantity = customer_shortage + buffer_shortage
            arrival_date = request_date
            can_line_fulfill = True
            reason = "available stock covers the requested quantity"

            if reorder_quantity > 0:
                arrival_date = self.supplier_timeline_tool.forward(request_date, reorder_quantity)
                if arrival_date > delivery_deadline:
                    can_line_fulfill = False
                    reason = f"supplier replenishment would arrive {arrival_date}, after the requested delivery date {delivery_deadline}"
                else:
                    reason = f"supplier replenishment can arrive by {arrival_date}"

            line_cost = reorder_quantity * float(CATALOG_BY_NAME[requested.item_name]["unit_price"])
            decision.total_reorder_cost += line_cost
            line_decision = InventoryLineDecision(
                item_name=requested.item_name,
                quantity=requested.quantity,
                available_before=available_before,
                reorder_quantity=reorder_quantity,
                supplier_arrival_date=arrival_date,
                can_fulfill=can_line_fulfill,
                reason=reason,
                unit_price=float(CATALOG_BY_NAME[requested.item_name]["unit_price"]),
                min_stock_level=min_stock,
            )
            decision.line_decisions.append(line_decision)
            if not can_line_fulfill:
                decision.can_fulfill = False
                decision.reasons.append(f"{requested.item_name}: {reason}.")

        if decision.total_reorder_cost > cash_before:
            decision.can_fulfill = False
            decision.reasons.append("supplier purchases would exceed available operating cash.")

        if not decision.line_decisions:
            decision.can_fulfill = False
            decision.reasons.append("no supported catalog items were found in the request.")

        return decision


class QuoteAgent:
    """Builds customer quotes using catalog pricing, quantity tiers, and prior quote history."""

    def __init__(self):
        self.quote_history_tool = quote_history_tool

    @staticmethod
    def _discount_for_units(total_units: int) -> tuple[float, str]:
        if total_units >= 10000:
            return 0.15, "15% large-volume discount"
        if total_units >= 5000:
            return 0.12, "12% large-volume discount"
        if total_units >= 1000:
            return 0.10, "10% bulk discount"
        if total_units >= 500:
            return 0.07, "7% bulk discount"
        if total_units >= 200:
            return 0.05, "5% quantity discount"
        return 0.0, "standard catalog pricing"

    def generate(self, parsed_items: List[RequestedItem], job: str, event: str, need_size: str) -> QuoteDecision:
        supported_items = [item for item in parsed_items if item.supported and item.item_name in CATALOG_BY_NAME]
        total_units = sum(item.quantity for item in supported_items)
        discount_rate, discount_label = self._discount_for_units(total_units)
        search_terms = ",".join(term for term in [event, need_size] if term)
        history = json.loads(self.quote_history_tool.forward(search_terms, 5)) if search_terms else []

        quote_lines: List[QuoteLine] = []
        base_amount = 0.0
        for item in supported_items:
            # Customer price is based on catalog value with a modest service factor for sourcing and handling.
            line_base = item.quantity * float(CATALOG_BY_NAME[item.item_name]["unit_price"]) * 1.35
            base_amount += line_base
            line_total = round(line_base * (1 - discount_rate), 2)
            quote_lines.append(QuoteLine(item_name=item.item_name, quantity=item.quantity, line_total=line_total))

        total_amount = round(sum(line.line_total for line in quote_lines), 2)
        if history and total_units <= 1000:
            positive_history = [float(row["total_amount"]) for row in history if float(row.get("total_amount", 0)) > 0]
            if positive_history:
                historical_average = mean(positive_history)
                # For small and medium orders, avoid drifting far above nearby historical quotes.
                if 0 < historical_average < total_amount:
                    cap = historical_average * 1.25
                    if total_amount > cap:
                        adjustment = cap / total_amount
                        quote_lines = [
                            QuoteLine(line.item_name, line.quantity, round(line.line_total * adjustment, 2))
                            for line in quote_lines
                        ]
                        total_amount = round(sum(line.line_total for line in quote_lines), 2)
                        discount_label += "; adjusted against comparable quote history"

        return QuoteDecision(
            total_amount=total_amount,
            base_amount=round(base_amount, 2),
            discount_rate=discount_rate,
            discount_label=discount_label,
            quote_lines=quote_lines,
            history_count=len(history),
        )


class SalesAgent:
    """Finalizes approved orders and writes stock and sales transactions."""

    def __init__(self):
        self.record_transaction_tool = record_transaction_tool
        self.financial_report_tool = financial_report_tool

    def finalize(self, inventory_decision: InventoryDecision, quote_decision: QuoteDecision, request_date: str) -> Dict[str, Union[int, float, List[int]]]:
        transaction_ids: List[int] = []
        reorder_total = 0.0
        for line in inventory_decision.line_decisions:
            if line.reorder_quantity > 0:
                reorder_price = round(line.reorder_quantity * line.unit_price, 2)
                reorder_total += reorder_price
                payload = json.loads(self.record_transaction_tool.forward(
                    line.item_name,
                    "stock_orders",
                    line.reorder_quantity,
                    reorder_price,
                    request_date,
                ))
                transaction_ids.append(int(payload["transaction_id"]))

        for quote_line in quote_decision.quote_lines:
            payload = json.loads(self.record_transaction_tool.forward(
                quote_line.item_name,
                "sales",
                quote_line.quantity,
                quote_line.line_total,
                request_date,
            ))
            transaction_ids.append(int(payload["transaction_id"]))

        report = json.loads(self.financial_report_tool.forward(request_date))
        return {
            "transaction_count": len(transaction_ids),
            "transaction_ids": transaction_ids,
            "reorder_total": round(reorder_total, 2),
            "cash_after": float(report["cash_balance"]),
            "inventory_value_after": float(report["inventory_value"]),
        }


class BusinessAdvisorAgent:
    """Summarizes end-of-run business indicators without changing transactions."""

    def __init__(self):
        self.financial_report_tool = financial_report_tool

    def summarize(self, as_of_date: str) -> str:
        report = json.loads(self.financial_report_tool.forward(as_of_date))
        top_items = report.get("top_selling_products", [])
        visible_top_items = [item for item in top_items if item.get("item_name")]
        if visible_top_items:
            top_text = ", ".join(f"{item['item_name']} (${float(item['total_revenue']):.2f})" for item in visible_top_items[:3])
        else:
            top_text = "no completed sales yet"
        low_stock = [
            item for item in report.get("inventory_summary", [])
            if int(item.get("stock", 0)) <= 100
        ][:3]
        low_text = ", ".join(item["item_name"] for item in low_stock) if low_stock else "no urgent low-stock item"
        return (
            f"Business review for {as_of_date}: top revenue items are {top_text}. "
            f"Restock watch list: {low_text}."
        )


class OrchestratorAgent:
    """Coordinates parser, inventory, quoting, and sales decisions."""

    def __init__(self, framework_agents: Dict[str, object] | None = None):
        self.inventory_agent = InventoryAgent()
        self.quote_agent = QuoteAgent()
        self.sales_agent = SalesAgent()
        self.advisor_agent = BusinessAdvisorAgent()
        self.framework_agents = framework_agents or {}

    @staticmethod
    def _line_items_text(quote_decision: QuoteDecision) -> str:
        return "; ".join(
            f"{line.quantity} units of {line.item_name} (${line.line_total:.2f})"
            for line in quote_decision.quote_lines
        )

    @staticmethod
    def _inventory_reason_text(inventory_decision: InventoryDecision) -> str:
        reasons = []
        for line in inventory_decision.line_decisions:
            reasons.append(f"{line.item_name}: {line.reason}")
        if inventory_decision.unsupported_items:
            reasons.append("Unsupported items: " + "; ".join(inventory_decision.unsupported_items))
        return " | ".join(reasons)

    def handle(self, request_text: str, job: str = "", event: str = "", need_size: str = "") -> AgentResult:
        request_date = RequestParser.request_date(request_text)
        delivery_deadline = RequestParser.delivery_deadline(request_text, request_date)
        parsed_items = RequestParser.parse_items(request_text)
        inventory_before = float(generate_financial_report(request_date)["inventory_value"])
        cash_before = float(get_cash_balance(request_date))
        inventory_decision = self.inventory_agent.assess(parsed_items, request_date, delivery_deadline)
        quote_decision = self.quote_agent.generate(parsed_items, job=job, event=event, need_size=need_size)
        supported_count = len([item for item in parsed_items if item.supported and item.item_name in CATALOG_BY_NAME])

        if inventory_decision.can_fulfill:
            transaction_summary = self.sales_agent.finalize(inventory_decision, quote_decision, request_date)
            cash_after = float(transaction_summary["cash_after"])
            inventory_after = float(transaction_summary["inventory_value_after"])
            latest_arrival = max((line.supplier_arrival_date for line in inventory_decision.line_decisions), default=request_date)
            response = (
                f"Status: fulfilled. Quote total: ${quote_decision.total_amount:.2f}. "
                f"Items: {self._line_items_text(quote_decision)}. "
                f"Delivery commitment: ready by {max(latest_arrival, request_date)} and no later than {delivery_deadline}. "
                f"Pricing rationale: {quote_decision.discount_label}; comparable prior requests checked: {quote_decision.history_count}. "
                f"Fulfillment rationale: {self._inventory_reason_text(inventory_decision)}. "
                f"Order confirmation: posted on {request_date}."
            )
            return AgentResult(
                status="fulfilled",
                response=response,
                quote_amount=quote_decision.total_amount,
                items_requested=len(parsed_items),
                items_fulfilled=supported_count,
                cash_delta=round(cash_after - cash_before, 2),
                inventory_delta=round(inventory_after - inventory_before, 2),
            )

        reason_text = "; ".join(inventory_decision.reasons) if inventory_decision.reasons else "requested delivery cannot be met"
        supported_quote = ""
        if quote_decision.quote_lines:
            supported_quote = (
                f" Supported catalog portion would price at ${quote_decision.total_amount:.2f} "
                f"using {quote_decision.discount_label}."
            )
        response = (
            f"Status: not fulfilled. Reason: {reason_text}. "
            f"Requested delivery date: {delivery_deadline}.{supported_quote} "
            f"No order was posted because the full request cannot be completed as written."
        )
        return AgentResult(
            status="not_fulfilled",
            response=response,
            quote_amount=quote_decision.total_amount,
            items_requested=len(parsed_items),
            items_fulfilled=0,
            cash_delta=0.0,
            inventory_delta=0.0,
        )


def build_smolagents_team() -> Dict[str, object]:
    """Create smolagents worker shells and bind each shell to its tool set."""
    if ToolCallingAgent is None:
        return {}
    model = build_openai_compatible_model()
    if model is None:
        return {}
    try:
        return {
            "inventory": ToolCallingAgent(
                tools=[inventory_snapshot_tool, stock_status_tool, supplier_timeline_tool, cash_status_tool],
                model=model,
                name="inventory_agent",
                description="Checks stock levels, replenishment timing, and cash availability.",
                max_steps=4,
            ),
            "quote": ToolCallingAgent(
                tools=[quote_history_tool],
                model=model,
                name="quote_agent",
                description="Builds quotes from product quantities, discounts, and prior quote history.",
                max_steps=4,
            ),
            "sales": ToolCallingAgent(
                tools=[record_transaction_tool, financial_report_tool],
                model=model,
                name="sales_agent",
                description="Posts approved stock and sales transactions and verifies the financial report.",
                max_steps=4,
            ),
        }
    except Exception:
        return {}


_MULTI_AGENT_SYSTEM: OrchestratorAgent | None = None


def get_multi_agent_system() -> OrchestratorAgent:
    global _MULTI_AGENT_SYSTEM
    if _MULTI_AGENT_SYSTEM is None:
        _MULTI_AGENT_SYSTEM = OrchestratorAgent(framework_agents=build_smolagents_team())
    return _MULTI_AGENT_SYSTEM


def call_multi_agent_system(request_text: str, job: str = "", event: str = "", need_size: str = "") -> AgentResult:
    return get_multi_agent_system().handle(request_text, job=job, event=event, need_size=need_size)


# Run the provided sample scenarios and write test_results.csv.
def run_test_scenarios():
    global _MULTI_AGENT_SYSTEM
    _MULTI_AGENT_SYSTEM = None
    print("Initializing Database...")
    init_database(db_engine)
    try:
        quote_requests_sample = pd.read_csv("quote_requests_sample.csv")
        quote_requests_sample["request_date"] = pd.to_datetime(
            quote_requests_sample["request_date"], format="%m/%d/%y", errors="coerce"
        )
        quote_requests_sample.dropna(subset=["request_date"], inplace=True)
        quote_requests_sample = quote_requests_sample.sort_values("request_date", kind="mergesort")
    except Exception as e:
        print(f"FATAL: Error loading test data: {e}")
        return []

    initial_date = quote_requests_sample["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)
    current_cash = report["cash_balance"]
    current_inventory = report["inventory_value"]

    results = []
    for idx, row in quote_requests_sample.iterrows():
        request_date = row["request_date"].strftime("%Y-%m-%d")
        print(f"\n=== Request {idx + 1} ===")
        print(f"Context: {row['job']} organizing {row['event']}")
        print(f"Request Date: {request_date}")
        print(f"Cash Balance: ${current_cash:.2f}")
        print(f"Inventory Value: ${current_inventory:.2f}")

        request_with_date = f"{row['request']} (Date of request: {request_date})"
        cash_before = float(get_cash_balance(request_date))
        inventory_before = float(generate_financial_report(request_date)["inventory_value"])
        agent_result = call_multi_agent_system(
            request_with_date,
            job=str(row.get("job", "")),
            event=str(row.get("event", "")),
            need_size=str(row.get("need_size", "")),
        )

        report = generate_financial_report(request_date)
        current_cash = report["cash_balance"]
        current_inventory = report["inventory_value"]

        print(f"Response: {agent_result.response}")
        print(f"Updated Cash: ${current_cash:.2f}")
        print(f"Updated Inventory: ${current_inventory:.2f}")

        results.append({
            "request_id": idx + 1,
            "request_date": request_date,
            "job": row.get("job", ""),
            "event": row.get("event", ""),
            "need_size": row.get("need_size", ""),
            "status": agent_result.status,
            "quote_amount": agent_result.quote_amount,
            "cash_before": cash_before,
            "cash_balance": current_cash,
            "cash_delta": round(current_cash - cash_before, 2),
            "inventory_before": inventory_before,
            "inventory_value": current_inventory,
            "inventory_delta": round(current_inventory - inventory_before, 2),
            "items_requested": agent_result.items_requested,
            "items_fulfilled": agent_result.items_fulfilled,
            "response": agent_result.response,
        })

    final_date = quote_requests_sample["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)
    print("\n===== FINAL FINANCIAL REPORT =====")
    print(f"Final Cash: ${final_report['cash_balance']:.2f}")
    print(f"Final Inventory: ${final_report['inventory_value']:.2f}")
    print(get_multi_agent_system().advisor_agent.summarize(final_date))

    pd.DataFrame(results).to_csv("test_results.csv", index=False)
    return results


if __name__ == "__main__":
    run_test_scenarios()
