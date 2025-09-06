from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .config import GROQ_API_KEY
import pandas as pd

schema_description = """
Tables:
products(id, name, category, price)
customers(id, name, email, created_at)
sales(id, product_id, customer_id, quantity, unit_price, total_price, sold_at)
Relationships:
- sales.product_id → products.id
- sales.customer_id → customers.id
"""


sql_prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""
You are a senior business analyst. Given the following SQLite database schema:

{schema_description}

User Question: {{question}}

Generate a valid SQLite SQL query. 
Use SQLite date functions (strftime, date) instead of EXTRACT. 
Output only the SQL, no explanations.
"""
)


def generate_sql(question: str):
    if not GROQ_API_KEY:
        return None, "Groq API key not found in .env."

    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0)
    chain = LLMChain(llm=llm, prompt=sql_prompt)

    try:
        sql = chain.run(question)
        return sql.strip(), f"Generated SQL for: {question}"
    except Exception as e:
        return None, f"SQL generation failed: {e}"

import pandas as pd

def summarize_results(question: str, df: pd.DataFrame) -> str:
    """
    Convert SQL query results (DataFrame) into human-readable natural language.
    Adds context, trends, and recommendations automatically.
    """
    if df.empty:
        return "No data found for your query."

    # ----------------------
    # Top-N Products / Sales
    # ----------------------
    if "name" in df.columns and ("total_sales" in df.columns or "total_revenue" in df.columns):
        lines = []
        metric = "total_sales" if "total_sales" in df.columns else "total_revenue"
        unit = "units sold" if metric == "total_sales" else "in revenue"
        top_product = df.iloc[0]
        value = top_product[metric]
        if metric == "total_revenue":
            value = f"${value:.2f}"
        lines.append(f"The top product for your query is {top_product['name']}, {value} {unit}.")
        for row in df.iloc[1:].itertuples():
            val = getattr(row, metric)
            if metric == "total_revenue":
                val = f"${val:.2f}"
            lines.append(f"{row.name} followed with {val} {unit}.")
        lines.append("This shows which products are currently performing well and may need attention.")
        return " ".join(lines)

    # ----------------------
    # Revenue Trends
    # ----------------------
    if "month" in df.columns and "revenue" in df.columns:
        lines = [f"In {row['month']}, the revenue was ${row['revenue']:.2f}." for _, row in df.iterrows()]
        trend = "increasing" if df['revenue'].iloc[-1] >= df['revenue'].iloc[0] else "decreasing"
        lines.append(f"Overall, revenue is {trend} over the selected period.")
        return " ".join(lines)

    # ----------------------
    # Customer Statistics
    # ----------------------
    if "customer_name" in df.columns and "total_orders" in df.columns:
        lines = []
        top_customer = df.iloc[0]
        lines.append(
            f"{top_customer['customer_name']} is your most active customer with {top_customer['total_orders']} orders."
        )
        for row in df.iloc[1:].itertuples():
            lines.append(f"{row.customer_name} placed {row.total_orders} orders.")
        lines.append("These insights help you understand customer behavior and loyalty.")
        return " ".join(lines)

    if "customer_name" in df.columns and "total_spent" in df.columns:
        lines = []
        top_customer = df.iloc[0]
        lines.append(
            f"{top_customer['customer_name']} spent the most, totaling ${top_customer['total_spent']:.2f}."
        )
        for row in df.iloc[1:].itertuples():
            lines.append(f"{row.customer_name} spent ${row.total_spent:.2f}.")
        lines.append("Monitoring customer spending helps identify high-value clients.")
        return " ".join(lines)

    # ----------------------
    # Generic fallback
    # ----------------------
    # Convert all rows to readable sentences
    lines = []
    for row in df.itertuples():
        row_text = ", ".join([f"{col}: {getattr(row, col)}" for col in df.columns])
        lines.append(row_text)
    return "Here are the results:\n" + "\n".join(lines)


def generate_insight(question: str, df: pd.DataFrame) -> str:
    if "top products" in question.lower():
        if not df.empty and df['total_qty'].max() < 5:
            return "\nInsight: Sales are low. Consider promotions for best-selling products."
    return ""
