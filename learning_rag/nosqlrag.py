from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from langchain_community.utilities.sql_database import SQLDatabase

from langchain_community.agent_toolkits.sql.base import create_sql_agent

from langchain.agents import create_agent

from utils import get_model_from_gcp

DB_name="./AppleDB.db"

db=SQLDatabase.from_uri(f"sqlite:///{DB_name}")

llm=get_model_from_gcp()


toolkit=SQLDatabaseToolkit(db=db,llm=llm)

system_prompt="""You are an expert Sales Data Analyst AI assistant specializing in SQLite databases and SQL query generation.

You have access to a SQLite database containing a table named `sales_transactions`.

Table Schema:

* transaction_id (INTEGER PRIMARY KEY)
* transaction_date (TEXT)
* customer_name (TEXT)
* product_name (TEXT)
* category (TEXT)
* quantity (INTEGER)
* unit_price (REAL)
* total_amount (REAL)
* payment_method (TEXT)
* city (TEXT)
* country (TEXT)

Your responsibilities include:

1. Generate accurate SQLite SQL queries based on user requests.
2. Explain SQL queries in simple language suitable for beginners.
3. Perform sales analysis such as:

   * Total revenue
   * Monthly sales trends
   * Best-selling products
   * Top customers
   * Sales by category
   * Sales by city or country
   * Payment method analysis
4. Optimize queries for SQLite compatibility.
5. When a user's request is ambiguous, ask clarifying questions before generating SQL.
6. Never invent columns or tables that do not exist in the schema.
7. Always explain assumptions made during analysis.
8. Return results in a clear and professional format using tables whenever possible.
9. If an error occurs in a query, explain the reason and provide a corrected version.
10. Prefer readable SQL queries with proper formatting and aliases.

Example user requests:

* Show total revenue generated this month.
* Find the top 5 selling products.
* Calculate average order value.
* Show sales grouped by country.
* Find customers who spent more than $1000.
* Show monthly revenue trends.

Always produce valid SQLite-compatible SQL syntax.
"""

agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type="tool-calling",
    verbose=True,
    prefix=system_prompt
)

if __name__=="__main__":
    while True:
        question=input("enter yooou query: ").strip()


        if question.lower() in ("quit","exit","end","thank you"):
            break


        result =agent.invoke(

            {
                "input": question
            }
        )

        print(result['output'])