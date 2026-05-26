import sqlite3
import datetime

# Sample Data from the Assignment PDF
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

# Custom SQLite Functions to match MySQL compatibility
def sql_concat(*args):
    return "".join(str(x) for x in args)

def sql_timestampdiff(unit, dob_str, base_str):
    try:
        # standard ISO parsing
        d1 = datetime.datetime.strptime(dob_str.split()[0], '%Y-%m-%d')
        d2 = datetime.datetime.strptime(base_str.split()[0], '%Y-%m-%d')
        return d2.year - d1.year - ((d2.month, d2.day) < (d1.month, d1.day))
    except Exception:
        return 0

def sql_extract(field, timestamp_str):
    if field.upper() == 'DAY':
        try:
            d = datetime.datetime.strptime(timestamp_str.split()[0], '%Y-%m-%d')
            return d.day
        except Exception:
            return 0
    return 0

def run_local_test():
    print("=" * 60)
    print("        HEALTHRX SQL CHALLENGE - LOCAL DB SIMULATION")
    print("=" * 60)

    # Initialize In-memory SQLite Database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Register custom MySQL functions
    conn.create_function("CONCAT", -1, sql_concat)
    conn.create_function("TIMESTAMPDIFF", 3, sql_timestampdiff)
    conn.create_function("EXTRACT_DAY", 1, lambda ts: sql_extract('DAY', ts))

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

    # Populate Data
    cursor.executemany("INSERT INTO DEPARTMENT VALUES (?, ?);", DEPARTMENTS)
    cursor.executemany("INSERT INTO EMPLOYEE VALUES (?, ?, ?, ?, ?, ?);", EMPLOYEES)
    cursor.executemany("INSERT INTO PAYMENTS VALUES (?, ?, ?, ?);", PAYMENTS)
    conn.commit()
    print("[+] Mock database successfully initialized with PDF sample data!")

    # 1. Test Query 1 (Odd: Highest salary NOT on 1st day of month)
    # We replace 'EXTRACT(DAY FROM p.PAYMENT_TIME)' with our registered function 'EXTRACT_DAY(p.PAYMENT_TIME)' for SQLite
    query_q1 = """
    SELECT 
        p.AMOUNT AS SALARY, 
        CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
        TIMESTAMPDIFF('YEAR', e.DOB, '2026-05-26') AS AGE,
        d.DEPARTMENT_NAME
    FROM PAYMENTS p
    JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    WHERE EXTRACT_DAY(p.PAYMENT_TIME) != 1
    ORDER BY p.AMOUNT DESC
    LIMIT 1
    """
    
    print("\n--- RUNNING QUESTION 1 (ODD REG NO) LOCAL SIMULATION ---")
    cursor.execute(query_q1)
    row_q1 = cursor.fetchone()
    if row_q1:
        print(f"SALARY          : {row_q1[0]:.2f}")
        print(f"NAME            : {row_q1[1]}")
        print(f"AGE (As of 2026): {row_q1[2]} years")
        print(f"DEPARTMENT      : {row_q1[3]}")
    else:
        print("No result found.")

    # 2. Test Query 2 (Even: Highest salary ON 1st day of month)
    query_q2 = """
    SELECT 
        p.AMOUNT AS SALARY, 
        CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
        TIMESTAMPDIFF('YEAR', e.DOB, '2026-05-26') AS AGE,
        d.DEPARTMENT_NAME
    FROM PAYMENTS p
    JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    WHERE EXTRACT_DAY(p.PAYMENT_TIME) = 1
    ORDER BY p.AMOUNT DESC
    LIMIT 1
    """

    print("\n--- RUNNING QUESTION 2 (EVEN REG NO) LOCAL SIMULATION ---")
    cursor.execute(query_q2)
    row_q2 = cursor.fetchone()
    if row_q2:
        print(f"SALARY          : {row_q2[0]:.2f}")
        print(f"NAME            : {row_q2[1]}")
        print(f"AGE (As of 2026): {row_q2[2]} years")
        print(f"DEPARTMENT      : {row_q2[3]}")
    else:
        print("No result found.")
        
    print("=" * 60 + "\n")
    conn.close()

if __name__ == "__main__":
    run_local_test()
