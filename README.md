* The Data Flow Diagram (DFD) of **MILANO PVT LTD** represents the flow of project, employee, and financial data within the company.

* The company management system monitors and manages **five ongoing projects**:

  * Project 1
  * Project 2
  * Project 3
  * Project 4
  * Project 5

* All employee-related information is stored in the **MILANO Employee DB**.

* The Employee DB contains:

  * Employee ID
  * Employee Name
  * Department
  * Position and Level
  * Salary and Bonus
  * Conveyance Charges
  * Monthly Lunch Plan
  * Quarterly Spend Voucher

* Employee data is transferred to the **MILANO Finance Advance DB** for financial processing and analysis.

* The Finance Advance DB stores:

  * Product Revenue
  * Service Revenue
  * Subscription Revenue
  * Salary and Expense Costs
  * Marketing and R&D Costs
  * Gross Profit
  * Operating Profit
  * Tax and Net Profit

* The system helps MILANO PVT LTD efficiently manage projects, employees, expenses, and overall financial performance through centralized data management.



# Updated Data Flow Diagram – MILANO PVT LTD

```text id="milano-final-dfd"
                           +----------------------------------+
                           |         MILANO PVT LTD           |
                           |        Company Management        |
                           +----------------+-----------------+
                                            |
        ----------------------------------------------------------------------------
        |                    |                    |                    |            |
        v                    v                    v                    v            v
 +---------------+   +---------------+   +---------------+   +---------------+   +---------------+
 |   Project 1   |   |   Project 2   |   |   Project 3   |   |   Project 4   |   |   Project 5   |
 +-------+-------+   +-------+-------+   +-------+-------+   +-------+-------+   +-------+-------+
         \_____________________|_____________________|_____________________/ 
                                            |
                                            v
                     +--------------------------------------------+
                     |         MILANO EMPLOYEE DB                 |
                     +--------------------------------------------+
                     | employee_id                                |
                     | first_name                                 |
                     | last_name                                  |
                     | full_name                                  |
                     | age                                        |
                     | nationality                                |
                     | location                                   |
                     | department                                 |
                     | position                                   |
                     | level                                      |
                     | salary                                     |
                     | bonus                                      |
                     | arrears                                    |
                     | conveyance_charge                          |
                     | monthly_lunch_plan                         |
                     | quarterly_spend_voucher                    |
                     +------------------+-------------------------+
                                        |
                                        v
              +-----------------------------------------------------------+
              |            MILANO FINANCE ADVANCE DB                      |
              +-----------------------------------------------------------+
              | month                                                     |
              | year                                                      |
              | department                                                |
              | employee_count                                            |
              | product_revenue                                           |
              | service_revenue                                           |
              | subscription_revenue                                      |
              | total_revenue                                             |
              | salary_cost                                               |
              | bonus_cost                                                |
              | benefits_cost                                             |
              | infrastructure_cost                                       |
              | marketing_cost                                            |
              | rd_cost                                                   |
              | admin_cost                                                |
              | total_expense                                             |
              | gross_profit                                              |
              | operating_profit                                          |
              | tax                                                       |
              | net_profit                                                |
              | revenue_per_employee                                      |
              | cost_per_employee                                         |
              +-----------------------------------------------------------+
```
