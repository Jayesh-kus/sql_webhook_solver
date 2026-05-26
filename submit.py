import requests
import json

# First, get the accessToken
gen_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
gen_data = {
    "name": "John Doe",
    "regNo": "REG12347",
    "email": "john@example.com"
}
gen_resp = requests.post(gen_url, json=gen_data)
token = gen_resp.json()["accessToken"]
print("Token acquired successfully!")

# Define the query to test
# Let's try MySQL TIMESTAMPDIFF with CURDATE()
query = """
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

submit_url = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"
headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}
payload = {
    "finalQuery": query
}

print(f"Submitting query to {submit_url}...")
print("Query:")
print(query)

resp = requests.post(submit_url, headers=headers, json=payload)
print("Status Code:", resp.status_code)
print("Response JSON:")
try:
    print(json.dumps(resp.json(), indent=2))
except Exception:
    print(resp.text)
