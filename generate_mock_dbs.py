import csv
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_FILE = os.path.join(BASE_DIR, "company_expenses_db.csv")
PROJECTS_FILE = os.path.join(BASE_DIR, "projects_db.csv")
EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees_db.csv")

DEPARTMENTS = ["Engineering", "Sales & Marketing", "Finance", "HR", "Product", "Operations", "Customer Support", "Data & AI"]

# 1. Generate Projects DB (5 Projects)
def generate_projects_db():
    projects = [
        {"project_id": "PRJ-101", "project_name": "apex", "associated_department": "Engineering", "budget": 1500000},
        {"project_id": "PRJ-102", "project_name": "betex", "associated_department": "Sales & Marketing", "budget": 850000},
        {"project_id": "PRJ-103", "project_name": "conol", "associated_department": "Data & AI", "budget": 2100000},
        {"project_id": "PRJ-104", "project_name": "drivenX", "associated_department": "Operations", "budget": 500000},
        {"project_id": "PRJ-105", "project_name": "Balenciaga-RED", "associated_department": "Product", "budget": 3400000}
    ]
    
    with open(PROJECTS_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["project_id", "project_name", "associated_department", "budget"])
        writer.writeheader()
        writer.writerows(projects)
    
    print(f"Generated {len(projects)} records in {PROJECTS_FILE}")
    return projects

# 2. Generate Company Expenses DB (100 records)
def generate_company_db():
    records = []
    year = 2024
    month = 1
    
    for _ in range(100):
        emp_count = random.randint(50, 300)
        prod_rev = random.randint(500000, 2000000)
        serv_rev = random.randint(200000, 1000000)
        sub_rev = random.randint(100000, 500000)
        total_rev = prod_rev + serv_rev + sub_rev
        
        sal_cost = emp_count * random.randint(5000, 12000)
        bonus_cost = int(sal_cost * random.uniform(0.05, 0.15))
        ben_cost = int(sal_cost * random.uniform(0.05, 0.10))
        infra_cost = random.randint(50000, 300000)
        mkt_cost = random.randint(20000, 150000)
        rd_cost = random.randint(100000, 400000)
        admin_cost = random.randint(30000, 100000)
        
        total_exp = sal_cost + bonus_cost + ben_cost + infra_cost + mkt_cost + rd_cost + admin_cost
        gross_profit = total_rev - (sal_cost + infra_cost + rd_cost)
        operating_profit = total_rev - total_exp
        tax = int(operating_profit * 0.2) if operating_profit > 0 else 0
        net_profit = operating_profit - tax
        
        records.append({
            "month": month, "year": year, "department": random.choice(DEPARTMENTS),
            "employee_count": emp_count, "product_revenue": prod_rev, "service_revenue": serv_rev,
            "subscription_revenue": sub_rev, "total_revenue": total_rev, "salary_cost": sal_cost,
            "bonus_cost": bonus_cost, "benefits_cost": ben_cost, "infrastructure_cost": infra_cost,
            "marketing_cost": mkt_cost, "rd_cost": rd_cost, "admin_cost": admin_cost,
            "total_expense": total_exp, "gross_profit": gross_profit, "operating_profit": operating_profit,
            "tax": tax, "net_profit": net_profit, "revenue_per_employee": int(total_rev / emp_count),
            "cost_per_employee": int(total_exp / emp_count)
        })
        
        month += 1
        if month > 12:
            month = 1
            year += 1
            
    with open(COMPANY_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Generated 100 records in {COMPANY_FILE}")

# 3. Generate Employees DB (10,000 records)
def generate_employees_db(projects):
    first_names = ["Adam", "Janet", "Jeremy", "James", "Joshua", "Briana", "John", "Stephen", "Victoria", "Sally", "David", "Michael", "Sarah"]
    last_names = ["Vasquez", "Bruce", "Taylor", "Oneal", "Graves", "Flores", "Dixon", "Hanson", "Davis", "Lucas", "Smith", "Johnson", "Williams"]
    nationalities = ["British", "Indian", "Australian", "American", "Canadian", "German"]
    locations = ["Manchester", "Pune", "Delhi", "Sydney", "Chennai", "New York", "London", "Toronto", "Berlin", "Munich"]
    positions = ["Executive", "Manager", "Director", "Analyst", "Lead", "Associate", "Engineer", "Scientist"]
    
    project_ids = [p["project_id"] for p in projects]
    
    records = []
    for i in range(1, 10001):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        dept = random.choice(DEPARTMENTS)
        level = f"L{random.randint(1, 10)}"
        salary = random.randint(40000, 150000)
        
        records.append({
            "employee_id": f"EMP-{str(i).zfill(5)}",
            "first_name": fname,
            "last_name": lname,
            "full_name": f"{fname} {lname}",
            "age": random.randint(21, 60),
            "nationality": random.choice(nationalities),
            "location": random.choice(locations),
            "department": dept,
            "position": f"{dept} {random.choice(positions)}",
            "level": level,
            "salary": salary,
            "bonus": int(salary * random.uniform(0.05, 0.2)),
            "arrears": random.choice([0, 0, 0, random.randint(1000, 5000)]), # 75% chance of 0
            "conveyance_charge": random.randint(1000, 5000),
            "monthly_lunch_plan": random.randint(1000, 4000),
            "quarterly_spend_voucher": random.randint(2000, 15000),
            "project_id": random.choice(project_ids) # FOREIGN KEY LINK!
        })
        
    with open(EMPLOYEE_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Generated 10000 records in {EMPLOYEE_FILE}")

if __name__ == "__main__":
    print("Starting mock data generation...")
    projs = generate_projects_db()
    generate_company_db()
    generate_employees_db(projs)
    print("All databases successfully created!")