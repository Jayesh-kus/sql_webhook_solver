# HealthRx (Bajaj Finserv Health) SQL Webhook Solver Challenge

A premium, production-grade Python application that automates the generation of a hiring webhook, dynamically parses registration numbers to determine assigned SQL tasks (Odd/Even logic), and submits a fully optimized SQL query solution back to the validated webhook endpoint.

---

## 🛠️ Tech Stack & Design

- **Language**: Python 3.13+
- **API Communication**: `requests` (robust network operations with timeout safeguards)
- **Configuration**: `python-dotenv` (environment-based isolation)
- **Architecture**: Modular, clean, and highly configurable design separation:
  - `app.py`: Entry orchestrator executing step-by-step handshake and submission.
  - `config.py`: Loads environment configurations with safe, validated defaults.
  - `query_builder.py`: Resolves the appropriate SQL solution dynamically based on registration number parity.

---

## 📁 Repository Structure

```
sql_webhook_solver/
│
├── .env                  # Environment file (Candidate Name, RegNo, Email)
├── .gitignore            # Git exclusion rules
├── README.md             # Developer documentation
├── requirements.txt      # Project requirements
│
├── app.py                # Main executable script
├── config.py             # Configuration loader
└── query_builder.py      # Parity-based SQL resolver
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Install Dependencies
Navigate to the project directory and install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Configuration
The application is pre-configured with default values. To configure the script with your own credentials, edit the `.env` file:
```ini
CANDIDATE_NAME="John Doe"
CANDIDATE_REG_NO="REG12347"
CANDIDATE_EMAIL="john@example.com"
```

### 4. Running the Application
To run the solver application:
```bash
python app.py
```

Upon execution, the terminal will display a beautifully formatted report:
```
============================================================
      HEALTHRX SQL WEBHOOK SOLVER CHALLENGE (PYTHON)
============================================================
============================================================
                ACTIVE CONFIGURATION
============================================================
Candidate Name   : John Doe
Registration No. : REG12347
Email Address    : john@example.com
API Target URL   : https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON
============================================================

[Step 1] Initiating API handshake...
POSTing candidate details to: https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON...
[+] Handshake successful!
    Webhook URL Received : https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON
    Access Token Length  : 191 chars
============================================================
                 PROBLEM RESOLUTION
============================================================
Registration Number: REG12347
Last Digit extracted: 7 (ODD)
Assigned Task       : [Question 1] (Odd registration number)
Description         : Highest salary not on 1st day of month + employee profile
============================================================

[Step 2] Sending SQL query solution to the webhook...
POSTing solution to: https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON...

============================================================
                 SUBMISSION RESULT
============================================================
HTTP Status Code : 200
Response Payload :
{
  "success": true,
  "message": "Webhook processed successfully"
}

[SUCCESS] Assignment has been verified and submitted successfully!
============================================================
```

---

## 📝 SQL Query Design (Question 1)

### The Challenge:
Find the highest salary credited to an employee on any day *except the 1st day of any month*. Extract the highest salary amount, the combined employee full name (`<FIRST_NAME> <LAST_NAME>`), current age in years, and department name.

### Solution Design:
```sql
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
```

### Key Techniques:
- **Concatenation**: Uses SQL standard `CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME)` to output a unified `NAME` column.
- **Parity / Day Isolation**: Employs ANSI SQL `EXTRACT(DAY FROM p.PAYMENT_TIME) != 1` to reliably filter out 1st-of-the-month salary credits across MySQL/PostgreSQL databases.
- **Relational Joins**: Intersects `PAYMENTS`, `EMPLOYEE`, and `DEPARTMENT` using relational foreign keys.
- **Precision Age Calculation**: Employs `TIMESTAMPDIFF(YEAR, e.DOB, CURDATE())` (or `EXTRACT(YEAR FROM AGE(e.DOB))` under PostgreSQL) to calculate the precise age in years dynamically.
- **Optimal Selection**: Employs `ORDER BY p.AMOUNT DESC LIMIT 1` to isolate the single highest salary without heavy aggregation over the payment space.
