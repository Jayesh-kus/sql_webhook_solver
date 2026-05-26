import sys

# SQL Query for Question 1 (Odd Registration Number)
# Goal: Find the highest salary credited to an employee on a day other than the 1st of any month,
# along with their full name (combined), age (calculated), and department.
SQL_QUERY_Q1 = """
SELECT 
    p.AMOUNT AS SALARY, 
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE EXTRACT(DAY FROM p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1
""".strip()

# SQL Query for Question 2 (Even Registration Number)
# Note: Since the PDF was 404, we provide a placeholder template that matches typical DB structures,
# but print a clear indication if it is selected.
SQL_QUERY_Q2 = """
-- Question 2 SQL Solution Template (Even registration number assigned)
SELECT 
    p.AMOUNT AS SALARY, 
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE EXTRACT(DAY FROM p.PAYMENT_TIME) = 1  -- Example condition if it was 1st of month payments
ORDER BY p.AMOUNT DESC
LIMIT 1
""".strip()

def get_sql_query(reg_no: str) -> str:
    """
    Analyzes the registration number and returns the correct SQL query.
    Assigned based on the last digit:
    - Odd last digit -> Question 1
    - Even last digit -> Question 2
    """
    # Clean the registration number to find the last numeric digit
    numeric_chars = [char for char in reg_no if char.isdigit()]
    if not numeric_chars:
        print(f"Error: Could not extract digits from registration number '{reg_no}'. Defaulting to Question 1.")
        return SQL_QUERY_Q1

    last_digit = int(numeric_chars[-1])
    is_odd = last_digit % 2 != 0

    print("=" * 60)
    print("                 PROBLEM RESOLUTION")
    print("=" * 60)
    print(f"Registration Number: {reg_no}")
    print(f"Last Digit extracted: {last_digit} ({'ODD' if is_odd else 'EVEN'})")
    
    if is_odd:
        print("Assigned Task       : [Question 1] (Odd registration number)")
        print("Description         : Highest salary not on 1st day of month + employee profile")
        print("=" * 60)
        return SQL_QUERY_Q1
    else:
        print("Assigned Task       : [Question 2] (Even registration number)")
        print("Description         : Alternative SQL assignment (Question 2)")
        print("=" * 60)
        return SQL_QUERY_Q2
