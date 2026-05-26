import requests
import json
import sys
import config
from query_builder import get_sql_query

def main():
    print("\n" + "=" * 60)
    print("      HEALTHRX SQL WEBHOOK SOLVER CHALLENGE (PYTHON)")
    print("=" * 60)
    
    # 1. Display active configurations
    config.print_config()
    
    # 2. Build startup POST payload
    payload = {
        "name": config.CANDIDATE_NAME,
        "regNo": config.CANDIDATE_REG_NO,
        "email": config.CANDIDATE_EMAIL
    }
    
    print("\n[Step 1] Initiating API handshake...")
    print(f"POSTing candidate details to: {config.GENERATE_WEBHOOK_URL}...")
    
    try:
        response = requests.post(config.GENERATE_WEBHOOK_URL, json=payload, timeout=15)
        
        if response.status_code != 200:
            print(f"[-] Handshake failed! HTTP Status Code: {response.status_code}")
            print(f"[-] Response: {response.text}")
            sys.exit(1)
            
        res_data = response.json()
        webhook_url = res_data.get("webhook")
        access_token = res_data.get("accessToken")
        
        if not webhook_url or not access_token:
            print("[-] Error: Missing 'webhook' or 'accessToken' in the response payload.")
            print(f"[-] Response payload: {json.dumps(res_data, indent=2)}")
            sys.exit(1)
            
        print("[+] Handshake successful!")
        print(f"    Webhook URL Received : {webhook_url}")
        print(f"    Access Token Length  : {len(access_token)} chars")
        
        # 3. Determine the correct SQL Query based on Registration No.
        sql_query = get_sql_query(config.CANDIDATE_REG_NO)
        
        # 4. Submit the solution to the webhook URL
        print("\n[Step 2] Sending SQL query solution to the webhook...")
        submit_headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        submit_payload = {
            "finalQuery": sql_query,
            "githubUrl": "https://github.com/Jayesh-kus/sql_webhook_solver"
        }
        
        print(f"POSTing solution to: {webhook_url}...")
        submit_response = requests.post(webhook_url, headers=submit_headers, json=submit_payload, timeout=15)
        
        print("\n" + "=" * 60)
        print("                 SUBMISSION RESULT")
        print("=" * 60)
        print(f"HTTP Status Code : {submit_response.status_code}")
        
        try:
            submit_data = submit_response.json()
            print("Response Payload :")
            print(json.dumps(submit_data, indent=2))
            
            if submit_data.get("success") is True:
                print("\n[SUCCESS] Assignment has been verified and submitted successfully!")
            else:
                print("\n[FAILURE] Submission was received but validation failed.")
        except Exception:
            print("Response Text    :")
            print(submit_response.text)
            print("\n[WARNING] Could not parse response as JSON. Check logs above.")
            
        print("=" * 60 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"[-] Networking Error: Could not connect to API server. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
