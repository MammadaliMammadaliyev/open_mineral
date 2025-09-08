#!/usr/bin/env python3
"""
Test script to demonstrate the submit flow functionality.
This script shows how to use the new submit and task status endpoints.
"""

import requests
import time
import json
from uuid import uuid4

# Configuration
BASE_URL = "http://localhost:8000/api/deals"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"  # Replace with actual token
}

def test_submit_flow():
    """
    Test the complete submit flow:
    1. Create a business confirmation deal
    2. Submit it for processing
    3. Poll task status until completion
    """
    
    print("=== Testing Business Confirmation Submit Flow ===\n")
    
    # Step 1: Create a business confirmation deal
    print("1. Creating a business confirmation deal...")
    deal_data = {
        "status": "draft",
        "user": 1  # Assuming user ID 1 exists
    }
    
    try:
        response = requests.post(f"{BASE_URL}/business-confirmation-deals/", 
                               json=deal_data, headers=HEADERS)
        if response.status_code == 201:
            deal = response.json()
            deal_id = deal['id']
            print(f"   ✓ Deal created with ID: {deal_id}")
        else:
            print(f"   ✗ Failed to create deal: {response.status_code} - {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error creating deal: {e}")
        return
    
    # Step 2: Submit the deal for processing
    print("\n2. Submitting deal for processing...")
    try:
        response = requests.post(f"{BASE_URL}/deals/{deal_id}/submit/", headers=HEADERS)
        if response.status_code == 200:
            submit_result = response.json()
            task_status_id = submit_result['task_status_id']
            task_id = submit_result['task_id']
            print(f"   ✓ Deal submitted successfully")
            print(f"   ✓ Task ID: {task_id}")
            print(f"   ✓ Task Status ID: {task_status_id}")
        else:
            print(f"   ✗ Failed to submit deal: {response.status_code} - {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error submitting deal: {e}")
        return
    
    # Step 3: Poll task status until completion
    print("\n3. Polling task status...")
    max_polls = 30  # Poll for up to 30 times (30 seconds)
    poll_count = 0
    
    while poll_count < max_polls:
        try:
            response = requests.get(f"{BASE_URL}/task-status/{task_status_id}/", headers=HEADERS)
            if response.status_code == 200:
                status_data = response.json()
                status = status_data['status']
                message = status_data['message']
                
                print(f"   Poll {poll_count + 1}: Status = {status}, Message = {message}")
                
                if status in ['completed', 'failed']:
                    print(f"\n   ✓ Task finished with status: {status}")
                    if status == 'completed':
                        print(f"   ✓ Message: {message}")
                        print(f"   ✓ Completed at: {status_data.get('completed_at', 'N/A')}")
                    else:
                        print(f"   ✗ Task failed: {message}")
                    break
                else:
                    time.sleep(1)  # Wait 1 second before next poll
                    poll_count += 1
            else:
                print(f"   ✗ Failed to get task status: {response.status_code} - {response.text}")
                break
        except requests.exceptions.RequestException as e:
            print(f"   ✗ Error polling task status: {e}")
            break
    
    if poll_count >= max_polls:
        print(f"\n   ⚠ Timeout: Task did not complete within {max_polls} seconds")
    
    print("\n=== Test Complete ===")

def print_api_endpoints():
    """
    Print the available API endpoints for reference.
    """
    print("=== Available API Endpoints ===\n")
    
    endpoints = [
        ("POST", "/api/deals/business-confirmation-deals/", "Create a business confirmation deal"),
        ("POST", "/api/deals/deals/{deal_id}/submit/", "Submit a deal for processing"),
        ("GET", "/api/deals/task-status/{task_status_id}/", "Get task status"),
        ("GET", "/api/deals/business-confirmation-deals/", "List all deals"),
    ]
    
    for method, endpoint, description in endpoints:
        print(f"{method:6} {endpoint:50} - {description}")
    
    print("\n=== Usage Instructions ===")
    print("1. Start the Django server: python manage.py runserver")
    print("2. Start Redis: redis-server")
    print("3. Start Celery worker: celery -A bc worker --loglevel=info")
    print("4. Update the HEADERS in this script with a valid authentication token")
    print("5. Run this script: python test_submit_flow.py")

if __name__ == "__main__":
    print_api_endpoints()
    print("\n" + "="*60 + "\n")
    
    # Uncomment the line below to run the actual test
    # test_submit_flow()
    
    print("To run the test, uncomment the 'test_submit_flow()' call in the script.")
    print("Make sure to update the authentication token in the HEADERS variable.")
