import csv
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_FILE = os.path.join(BASE_DIR, "company_expenses_db.csv")
PROJECTS_FILE = os.path.join(BASE_DIR, "projects_db.csv")
EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees_db.csv")

def run_analysis():
    print("--- COMPANY POINT OF VIEW: PROJECT ANALYSIS ---\n")
    
    # 1. Aggregate Company Expenses by Department
    dept_expenses = defaultdict(int)
    with open(COMPANY_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dept_expenses[row["department"]] += int(row["total_expense"])
            
    # 2. Aggregate Employee Costs by Project
    project_employee_costs = defaultdict(int)
    project_headcount = defaultdict(int)
    with open(EMPLOYEE_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["project_id"]
            # Calculate total compensation cost for the employee
            total_comp = int(row["salary"]) + int(row["bonus"]) + int(row["monthly_lunch_plan"]) * 12
            project_employee_costs[pid] += total_comp
            project_headcount[pid] += 1
            
    # 3. Join and Display the Company View
    with open(PROJECTS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["project_id"]
            pname = row["project_name"]
            dept = row["associated_department"]
            allocated_budget = int(row["budget"])
            
            actual_cost = project_employee_costs[pid]
            headcount = project_headcount[pid]
            dept_total_cost = dept_expenses[dept]
            
            # Determine if the project is under or over its assigned budget
            budget_status = "OVER BUDGET" if actual_cost > allocated_budget else "UNDER BUDGET"
            
            print(f"Project: {pname.upper()} ({pid})")
            print(f"  -> Owning Department    : {dept}")
            print(f"  -> Assigned Headcount   : {headcount} employees")
            print(f"  -> Allocated Budget     : ${allocated_budget:,}")
            print(f"  -> Actual Employee Cost : ${actual_cost:,} ({budget_status})")
            if dept_total_cost > 0:
                percentage_of_dept = (actual_cost / dept_total_cost) * 100
                print(f"  -> Company Impact       : Consumes {percentage_of_dept:.2f}% of the {dept} department's total expenses.\n")

if __name__ == "__main__":
    run_analysis()