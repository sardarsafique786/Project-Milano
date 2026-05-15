import os
import snowflake.connector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_FILE = os.path.join(BASE_DIR, "company_expenses_db.csv")
PROJECTS_FILE = os.path.join(BASE_DIR, "projects_db.csv")
EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees_db.csv")

SF_ACCOUNT = 'jl94581.ap-southeast-7.aws'
SF_USER = 'Milano'
SF_PASSWORD = 'Milano@1234567890'
SF_WAREHOUSE = 'COMPUTE_WH'
SF_DATABASE = 'MILANO_TECH_DB'
SF_SCHEMA = 'PUBLIC'

def upload_to_snowflake():
    print("Establishing secure connection to Snowflake...")
    try:
        conn = snowflake.connector.connect(
            user=SF_USER,
            password=SF_PASSWORD,
            account=SF_ACCOUNT,
            warehouse=SF_WAREHOUSE
        )
        cursor = conn.cursor()
        
        print(f"Creating database {SF_DATABASE} if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {SF_DATABASE}")
        cursor.execute(f"USE DATABASE {SF_DATABASE}")
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SF_SCHEMA}")
        cursor.execute(f"USE SCHEMA {SF_SCHEMA}")

        # 1. Projects Table DDL
        print("Configuring Projects Table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_db (
            project_id STRING PRIMARY KEY, project_name STRING,
            associated_department STRING, budget NUMBER
        )""")

        # 2. Company Expenses Table DDL
        print("Configuring Company Expenses Table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_expenses_db (
            month NUMBER, year NUMBER, department STRING, employee_count NUMBER,
            product_revenue NUMBER, service_revenue NUMBER, subscription_revenue NUMBER, total_revenue NUMBER,
            salary_cost NUMBER, bonus_cost NUMBER, benefits_cost NUMBER, infrastructure_cost NUMBER,
            marketing_cost NUMBER, rd_cost NUMBER, admin_cost NUMBER,
            total_expense NUMBER, gross_profit NUMBER, operating_profit NUMBER, tax NUMBER, net_profit NUMBER,
            revenue_per_employee NUMBER, cost_per_employee NUMBER
        )""")

        # 3. Employees Table DDL
        print("Configuring Employees Table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees_db (
            employee_id STRING PRIMARY KEY, first_name STRING, last_name STRING, full_name STRING,
            age NUMBER, nationality STRING, location STRING, department STRING, position STRING, level STRING,
            salary NUMBER, bonus NUMBER, arrears NUMBER, conveyance_charge NUMBER, monthly_lunch_plan NUMBER,
            quarterly_spend_voucher NUMBER, project_id STRING
        )""")

        # Perform optimized Bulk Load using PUT & COPY INTO
        files_to_load = [
            (PROJECTS_FILE, "projects_db"),
            (COMPANY_FILE, "company_expenses_db"),
            (EMPLOYEE_FILE, "employees_db")
        ]

        for file_path, table in files_to_load:
            if os.path.exists(file_path):
                print(f"Uploading {os.path.basename(file_path)} to Snowflake internal stage...")
                cursor.execute(f"PUT file://{file_path} @%{table} AUTO_COMPRESS=TRUE OVERWRITE=TRUE")
                print(f"Copying staged data into {table}...")
                cursor.execute(f"COPY INTO {table} FILE_FORMAT=(TYPE='CSV' SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='\"')")
                print(f"✅ Successfully synced {table}!\n")
            else:
                print(f"⚠️ File not found, skipping: {file_path}")

        cursor.close()
        conn.close()
        print("--- Snowflake Data Warehouse Sync Complete! ---")

    except Exception as e:
        print(f"❌ Snowflake Error: {e}")

if __name__ == "__main__":
    upload_to_snowflake()