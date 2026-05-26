import os
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

# Fallback defaults from the assignment instructions
CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "John Doe")
CANDIDATE_REG_NO = os.getenv("CANDIDATE_REG_NO", "REG12347")
CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL", "john@example.com")

# Target URLs for API endpoints
GENERATE_WEBHOOK_URL = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

def print_config():
    """Prints the currently active configuration for visual clarity."""
    print("=" * 60)
    print("                ACTIVE CONFIGURATION")
    print("=" * 60)
    print(f"Candidate Name   : {CANDIDATE_NAME}")
    print(f"Registration No. : {CANDIDATE_REG_NO}")
    print(f"Email Address    : {CANDIDATE_EMAIL}")
    print(f"API Target URL   : {GENERATE_WEBHOOK_URL}")
    print("=" * 60)
