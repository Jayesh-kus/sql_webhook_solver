import sqlite3
from datetime import datetime

# Sample Data from the Question
DEPARTMENTS = [
    (1, "HR"),
    (2, "Finance"),
    (3, "Engineering"),
    (4, "Sales"),
    (5, "Marketing"),
    (6, "IT")
]

EMPLOYEES = [
    (1, "John", "Williams", "1980-05-15", "Male", 3),
    (2, "Sarah", "Johnson", "1990-07-20", "Female", 2),
    (3, "Michael", "Smith", "1985-02-10", "Male", 3),
    (4, "Emily", "Brown", "1992-11-30", "Female", 4),
    (5, "David", "Jones", "1988-09-05", "Male", 5),
    (6, "Olivia", "Davis", "1995-04-12", "Female", 1),
    (7, "James", "Wilson", "1983-03-25", "Male", 6),
    (8, "Sophia", "Anderson", "1991-08-17", "Female", 4),
    (9, "Liam", "Miller", "1979-12-01", "Male", 1),
    (10, "Emma", "Taylor", "1993-06-28", "Female", 5)
]

PAYMENTS = [
    (1, 2, 65784.00, "2025-01-01 13:44:12.824"),
    (2, 4, 62736.00, "2025-01-06 18:36:37.892"),
    (3, 1, 69437.00, "2025-01-01 10:19:21.563"),
    (4, 3, 67183.00, "2025-01-02 17:21:57.341"),
    (5, 2, 66273.00, "2025-02-01 11:49:15.764"),
    (6, 5, 71475.00, "2025-01-01 07:24:14.453"),
    (7, 1, 70837.00, "2025-02-03 19:11:31.553"),
    (8, 6, 69628.00, "2025-01-02 10:41:15.113"),
    (9, 4, 71876.00, "2025-02-01 12:16:47.807"),
    (10, 3, 70098.00, "2025-02-03 10:11:17.341"),
    (11, 6, 67827.00, "2025-02-02 19:21:27.753"),
    (12, 5, 69871.00, "2025-02-05 17:54:17.453"),
    (13, 2, 72984.00, "2025-03-05 09:37:35.974"),
    (14, 1, 67982.00, "2025-03-01 06:09:51.983"),
    (15, 6, 70198.00, "2025-03-02 10:34:35.753"),
    (16, 4, 74998.00, "2025-03-02 09:27:26.162")
]

def main():
    print("=" * 70)
    print("         HEALTHRX SQL CHALLENGE: STANDALONE PYTHON SOLUTION")
    print("=" * 70)

    # Initialize an in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create Tables
    cursor.execute("""
    CREATE TABLE DEPARTMENT (
        DEPARTMENT_ID INTEGER PRIMARY KEY,
        DEPARTMENT_NAME TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE EMPLOYEE (
        EMP_ID INTEGER PRIMARY KEY,
        FIRST_NAME TEXT NOT NULL,
        LAST_NAME TEXT NOT NULL,
        DOB TEXT NOT NULL,
        GENDER TEXT NOT NULL,
        DEPARTMENT INTEGER,
        FOREIGN KEY(DEPARTMENT) REFERENCES DEPARTMENT(DEPARTMENT_ID)
    );
    """)

    cursor.execute("""
    CREATE TABLE PAYMENTS (
        PAYMENT_ID INTEGER PRIMARY KEY,
        EMP_ID INTEGER,
        AMOUNT REAL,
        PAYMENT_TIME TEXT,
        FOREIGN KEY(EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
    );
    """)

    # Populate Tables with mock data
    cursor.executemany("INSERT INTO DEPARTMENT VALUES (?, ?);", DEPARTMENTS)
    cursor.executemany("INSERT INTO EMPLOYEE VALUES (?, ?, ?, ?, ?, ?);", EMPLOYEES)
    cursor.executemany("INSERT INTO PAYMENTS VALUES (?, ?, ?, ?);", PAYMENTS)
    conn.commit()
    print("[+] Successfully initialized tables and populated mock data.")

    # SQL query solving Question 1:
    # 1. Calculates NAME using string concatenation.
    # 2. Computes precise AGE using DOB and the current date (standard SQLite-compatible DATE algebra).
    # 3. Filters out payments made on the 1st of any month (using strftime to extract the day).
    # 4. Returns the single highest salary.
    sql_query = """
    SELECT 
        p.AMOUNT AS SALARY, 
        e.FIRST_NAME || ' ' || e.LAST_NAME AS NAME,
        (strftime('%Y', 'now') - strftime('%Y', e.DOB)) - (strftime('%m-%d', 'now') < strftime('%m-%d', e.DOB)) AS AGE,
        d.DEPARTMENT_NAME
    FROM PAYMENTS p
    JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    WHERE CAST(strftime('%d', p.PAYMENT_TIME) AS INTEGER) != 1
    ORDER BY p.AMOUNT DESC
    LIMIT 1;
    """

    print("\n[Executing SQL Query...]")
    cursor.execute(sql_query)
    result = cursor.fetchone()

    print("\n" + "=" * 70)
    print("                           OUTPUT RESULT")
    print("=" * 70)
    if result:
        print(f"{"SALARY":<15} | {"NAME":<20} | {"AGE":<5} | {"DEPARTMENT_NAME":<15}")
        print("-" * 70)
        salary, name, age, dept = result
        print(f"{salary:<15.2f} | {name:<20} | {age:<5} | {dept:<15}")
    else:
        print("[-] No records matched the query criteria.")
    print("=" * 70 + "\n")

    conn.close()

if __name__ == "__main__":
    main()
